# src/wrapper.py

from typing import Dict, Any, List
import anndata
from .maboss_module.model_manager import MaBossManager
from .spatial_module.environment import LianaSpatialEnvironment
from .simulation.time_lag import TimeLagEstimator
from .simulation.runner import SimulationRunner
from .utils.utils_check_configuration import generate_config_report

class SpatialBooleanPipeline:
    """
    Main orchestrator integrating spatial scRNA-seq data with Boolean networks.

    This class coordinates spatial cell-cell communication outputs (from LIANA+)
    with stochastic/deterministic intracellular Boolean simulations (via MaBoSS),
    taking into account biological time lags and cell spatial microenvironments.

    :param spatial_data: AnnData object containing spatial coordinates and gene expression.
    :type spatial_data: anndata.AnnData
    :param liana_uns_key: The key under ``spatial_data.uns`` where LIANA+ results are stored.
    :type liana_uns_key: str
    """
    
    def __init__(self, 
                 spatial_data: anndata.AnnData, 
                 liana_uns_key: str, 
                 connectivity_key: str = "spatial", 
                 liana_key: str = "liana_res"
        ):
        """
        Constructor method.
        """
        self.adata = spatial_data
        self.liana_key = liana_uns_key
        
        # Initialize sub-modules
        self.maboss_manager = MaBossManager()
        self.spatial_env = LianaSpatialEnvironment(connectivity_key=connectivity_key, liana_key=liana_key)
        self.time_estimator = None
        
        # Simulation technical configuration
        self.sim_settings = {}

    #############################
    # Configuration Setters
    #############################


    def SetMaBossModel(self, mode: str = "pretrained", model_name='be_creative', **kwargs: Any) -> None:
        """
        Loads and configures the intracellular Boolean network model.

        Currently supports loading predefined models. 
        
        Future updates will include de novo network reconstruction via OmniPath.

        Multiple independent pathways are managed in parallel during execution.

        All heavy computations are deferred to the evaluation stage (Simulate).

        :param mode: The mode of model creation. Currently only 'pretrained' is active.
        :type mode: str
        :param kwargs: Configuration paths containing ``bnd_path`` and ``cfg_path``.
        :type kwargs: dict
        :raises ValueError: If an unsupported mode is provided.
        :return: None
        """
        if mode == "pretrained":
            bnd_path = kwargs.get("bnd_path")
            cfg_path = kwargs.get("cfg_path")
            if not bnd_path or not cfg_path:
                raise ValueError("Both 'bnd_path' and 'cfg_path' must be provided for pretrained mode.")
            self.maboss_manager.load_pretrained(bnd_path, cfg_path, model_name)
        elif mode == "denovo":
            # Placeholder for dynamic creation using OmniPath and decoupler
            pass
        else:
            raise ValueError(f"Unknown MaBoSS model mode: {mode}")

    def BuildSpatialContext(self, config_spatial_neighbors: Dict[str, Any] = {}, config_liana_bivariate: Dict[str, Any] = {}) -> None:
        """
        Triggers the automated preprocessing, structural graph generation, and signaling matrix derivation.

        Delegates heavy configuration auditing and graph extraction to the LianaSpatialEnvironment module.

        :param config_spatial_neighbors: Parameter configuration dictionary for neighbor graph building.
        :type config_spatial_neighbors: dict
        :param config_liana_bivariate: Parameter configuration dictionary for bivariate association computations.
        :type config_liana_bivariate: dict
        :return: None
        """
        # Execute context pipeline directly modifying self.adata in-place
        self.adata = self.spatial_env.build_spatial_context(
            adata=self.adata,
            config_spatial_neighbors=config_spatial_neighbors,
            config_liana_bivariate=config_liana_bivariate
        )

    def SetTimeLags(self, strategy: str = "topological", custom_lags: Dict[str, float] = None) -> None:
        """
        Configures biological time delays for intracellular and extracellular signaling pathways.

        :param strategy: Strategy to estimate lags ('topological' or 'experimental').
        :type strategy: str
        :param custom_lags: Optional dictionary to manually override lags for specific receptors.
        :type custom_lags: dict, optional
        :return: None
        """
        if not self.maboss_manager.models:
            raise RuntimeError("MaBoSS model must be set via SetMaBossModel before configuring time lags.")
            
        # Store estimator instance without immediate calculation
        self.time_estimator = TimeLagEstimator(strategy=strategy, custom_lags=custom_lags)

    #############################
    # Pipeline functionality
    #############################

    def SetSimulationSettings(self, max_time: float, delta_t: float, sample_count: int, sim_type: str = "stochastic") -> None:
        """
        Sets the technical parameters for execution.

        Defines the total simulation window, the discrete step interval for updates,
        and MaBoSS engine specific arguments.

        :param max_time: Total biological simulation time (e.g., in minutes).
        :type max_time: float
        :param delta_t: Size of the time increment for piecewise updates.
        :type delta_t: float
        :param sample_count: Number of Monte Carlo trajectories for stochastic simulations.
        :type sample_count: int
        :param sim_type: Simulation engine type, 'stochastic' or 'deterministic'.
        :type sim_type: str
        :return: None
        """
        self.sim_settings = {
            "max_time": max_time,
            "delta_t": delta_t,
            "sample_count": sample_count,
            "type": sim_type
        }

    

    def RunPipeline(self, target_cell_ids: List[str], output_csv_path: str) -> None:
        #TODO change implementations - include gemini part for repair 
        """
        Executes the piecewise simulation loop for the selected cells.

        Integrates spatial coordinates, expression profiles, and time-delayed inputs.
        Outputs are streamed directly to a CSV file at each step interval.

        :param target_cell_ids: List of specific cell barcodes/IDs to focus the study on.
        :type target_cell_ids: list of str
        :param output_csv_path: Path to the output CSV file where results are appended dynamically.
        :type output_csv_path: str
        :raises RuntimeError: If required modules or configurations are missing.
        :return: None
        """
        if not self.maboss_manager.models:
            raise RuntimeError("MaBoSS models are not configured.")
        if not self.spatial_env:
            raise RuntimeError("Spatial settings are not configured.")
        if not self.time_estimator:
            raise RuntimeError("Time lags are not configured.")
        if not self.sim_settings:
            raise RuntimeError("Simulation settings are not configured.")

        # --- Step 1: Isolate Spatial Subgraph Domains ---
        print("Extracting active simulation and context boundary subgraphs...")
        simulation_set, context_set = self.spatial_env.extract_simulation_and_context_sets(
            self.adata, target_cell_ids
        )

        # --- Step 2: Lazy Time-Lag Estimation via Active Receptors ---
        print("Evaluating biological time lags for active pathways...")
        liana_anndata = self.adata.uns[self.liana_key]
        
        # Robust extraction from AnnData .var dataframe or fallback to var_names parsing
        if 'receptor_complex' in liana_anndata.var.columns:
            active_receptors = liana_anndata.var['receptor_complex'].unique().tolist()
        elif 'receptor' in liana_anndata.var.columns:
            active_receptors = liana_anndata.var['receptor'].unique().tolist()
        else:
            # Fallback parse if columns are missing but var_names follow the 'Ligand^Receptor' convention
            active_receptors = list(set([
                pair.split('^')[1] for pair in liana_anndata.var_names if '^' in pair
            ]))
        
        # Map intracellular path rules right before running the simulation blocks
        self.time_estimator.calculate_intracellular_lags(
            network_nodes=self.maboss_manager.all_nodes, 
            active_receptors=active_receptors
        )

        # --- Step 3: Pre-Flight Configuration Check ---
        # Automatically outputs the structured report right before entering the simulation loop
        self.CheckConfiguration()
        
        print(f"Pipeline initialized. Active simulation set: {len(simulation_set)} cells. "
              f"Background context set: {len(context_set)} cells.")
        
        # --- Step 4: Instantiation and Simulation Loop ---
        runner = SimulationRunner(
            adata=self.adata,
            spatial_env=self.spatial_env,
            time_estimator=self.time_estimator,
            manager=self.maboss_manager
        )
        
        print("Triggering continuous hybrid piecewise simulation loop. Streaming rows to CSV...")
        runner.RunPiecewiseSimulation(
            simulation_set=simulation_set,
            context_set=context_set,
            sim_settings=self.sim_settings,
            output_csv_path=output_csv_path
        )

    #############################
    # Internal helpers
    #############################

    ## ----- Sanity check: configuration -----

    def CheckConfiguration(self, show_all_examples: bool = False) -> None:
        """
        Runs a pre-execution audit on the loaded data and model specifications.

        Evaluates gene nomenclature matches, checks spatial graphs, and details
        time delay matrices before starting the stochastic simulations.
        
        :return: None
        """
        generate_config_report(
            adata=self.adata,
            liana_key=self.liana_key,
            manager=self.maboss_manager,
            spatial_env=self.spatial_env,
            time_estimator=self.time_estimator,
            show_all_examples=show_all_examples
        )