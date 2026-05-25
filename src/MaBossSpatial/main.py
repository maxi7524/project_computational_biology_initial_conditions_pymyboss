# src/main.py

from typing import Dict, Any, List
import anndata
from .maboss_module.model_manager import MaBossManager
from .spatial_module.environment import SpatialEnvironment
from .simulation.time_lag import TimeLagEstimator
from .simulation.runner import SimulationRunner

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
    
    def __init__(self, spatial_data: anndata.AnnData, liana_uns_key: str):
        """
        Constructor method.
        """
        self.adata = spatial_data
        self.liana_key = liana_uns_key
        
        # Initialize sub-modules
        self.maboss_manager = MaBossManager()
        self.spatial_env = SpatialEnvironment()
        self.time_estimator = None
        
        # Simulation technical configuration
        self.sim_settings = {}

    def SetMaBossModel(self, mode: str = "pretrained", model_name='be_creative', **kwargs: Any) -> None:
        """
        Loads and configures the intracellular Boolean network model.

        Currently supports loading predefined models. Future updates will include
        de novo network reconstruction via OmniPath.

        Multiple independent pathways are managed in parallel during execution.

        All heavy computations are deferred to the evaluation stage (Simulate).

        :param mode: The mode of model creation. Currently only 'pretrained' is active.
        :type mode: str
        :param kwargs: Arbitrary keyword arguments containing configuration paths.
                       Expects ``bnd_path`` and ``cfg_path`` for 'pretrained' mode.
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

    def SetSpatialSettings(self, bandwidth: float, cutoff: float = 0.1, kernel: str = "gaussian") -> None:
        """
        Configures the spatial neighborhood parameters utilizing LIANA+'s internal optimization.

        This method stores the parameters required to run ``li.ut.spatial_neighbors`` 
        during the lazy evaluation stage.

        :param bandwidth: Signaling length/maximum distance for cell communication.
        :type bandwidth: float
        :param cutoff: Proximity values below this threshold will be set to 0. Defaults to 0.1.
        :type cutoff: float
        :param kernel: Kernel function type ('gaussian', 'exponential', 'linear'). Defaults to 'gaussian'.
        :type kernel: str
        :return: None
        """
        self.spatial_env.configure_kernel(bandwidth=bandwidth, cutoff=cutoff, kernel=kernel)

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
            
        self.time_estimator = TimeLagEstimator(strategy=strategy, custom_lags=custom_lags)
        
        # Extract active receptors dynamically from liana unstructured metadata in adata
        liana_df = self.adata.uns[self.liana_key]
        active_receptors = liana_df['receptor_complex'].unique().tolist()
        
        # Cross-reference with loaded nodes across models
        self.time_estimator.calculate_lags(
            network_nodes=self.maboss_manager.all_nodes, 
            active_receptors=active_receptors
        )

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
            raise RuntimeError("MaBoSS models is not configured.")
        if not self.spatial_env:
            raise RuntimeError("Spatial settings are not configured.")
        if not self.time_estimator:
            raise RuntimeError("Time lags are not configured.")
        if not self.sim_settings:
            raise RuntimeError("Simulation settings are not configured.")

        # 1. Compute spatial neighbors graph via LIANA+ lazily
        print("Computing spatial neighborhood connectivity matrix via LIANA+...")
        self.spatial_env.compute_neighbors_graph(self.adata)
        
        # 2. Extract exact 1-hop (simulation) and 2-hop (initial context boundary) cell zones
        # POPRAWIONE: Dopasowane do rzeczywistych metod w environment.py
        simulation_set, context_set = self.spatial_env.extract_neighborhood_zones(self.adata, target_cell_ids)
        
        print(f"Pipeline initialized. Active simulation set: {len(simulation_set)} cells. "
              f"Background context set: {len(context_set)} cells.")
        
        # 3. Instantiate and delegate execution to the SimulationRunner module
        # POPRAWIONE: Przekazanie sterowania do runner.py
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