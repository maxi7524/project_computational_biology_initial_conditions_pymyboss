from .maboss_module.model_manager import MaBossManager
from .spatial_module.environment import SpatialEnvironment
from .simulation.time_lag_estimator import TimeLagEstimator

class SpatialBooleanPipeline:
    """
    The main orchestrator for integrating spatial scRNA-seq data (LIANA+) 
    with Boolean network simulations (MaBoSS).
    """
    def __init__(self, spatial_data, liana_results):
        """
        Args:
            spatial_data: AnnData or MuData object containing spatial coordinates.
            liana_results: DataFrame containing LR interaction scores.
        """
        self.spatial_data = spatial_data
        # TODO - rework 
        self.liana_results = liana_results
        
        # Modules
        self.maboss_manager = MaBossManager()
        self.spatial_env = None
        self.time_estimator = None
        self.sim_settings = {}

    def SetMaBossModel(self, mode: str = "pretrained", **kwargs):
        """
        Configures the intracellular Boolean model.
        
        Args:
            mode: 'pretrained' (loads .bnd/.cfg) or 'denovo' (builds via OmniPath).
            **kwargs: Paths or parameters required for the chosen mode.
        """
        if mode == "pretrained":
            bnd_path = kwargs.get("bnd_path")
            cfg_path = kwargs.get("cfg_path")
            self.maboss_manager.load_pretrained(bnd_path, cfg_path)
        elif mode == "denovo":
            # Logic for building dynamic graphs using OmniPath and decoupler
            pass
        else:
            raise ValueError(f"Unknown MaBoSS model mode: {mode}")

    def SetSpatialSettings(self, settings: dict):
        """
        Configures spatial distance thresholds and kernel decay functions.
        """
        self.spatial_env = SpatialEnvironment(settings)

    def SetTimeLags(self, strategy: str = "topological", custom_lags: dict = None):
        """
        Configures the estimation of biological time delays for intracellular pathways.
        """
        self.time_estimator = TimeLagEstimator(strategy=strategy, custom_lags=custom_lags)
        # Compute lags immediately if the model is already loaded
        if self.maboss_manager.model:
             # Just a placeholder call, actual logic requires defining target nodes
             self.time_estimator.calculate_lags(self.maboss_manager.nodes, ["Apoptosis", "Survival"])

    def SetSimulationSettings(self, max_time: float, sample_count: int, type: str = "stochastic"):
        """
        Sets execution parameters for the MaBoSS engine.
        """
        self.sim_settings = {
            "max_time": max_time,
            "sample_count": sample_count,
            "type": type
        }

    def RunPipeline(self, target_cell_type: str):
        """
        Executes the integration and runs the simulation.
        
        Returns:
            MaBoSS simulation result object.
        """
        if not self.maboss_manager.model:
            raise RuntimeError("MaBoSS model not set. Call SetMaBossModel first.")
            
        print(f"Starting pipeline for target: {target_cell_type}")
        
        # 1. Filter LIANA results for target cell type
        # 2. Extract spatial coordinates and calculate environment weights via spatial_env
        # 3. Apply time lags to determine the effective signal window
        # 4. Map final integrated scores to the MaBoSS model (istate or rate)
        
        # Apply technical simulation settings directly to the model configuration
        self.maboss_manager.model.update_parameters(
            sample_count=self.sim_settings["sample_count"],
            max_time=self.sim_settings["max_time"]
        )
        
        # 5. Run simulation
        print("Running MaBoSS simulation...")
        result = self.maboss_manager.model.run()
        
        return result