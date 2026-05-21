# src/simulation/time_estimator.py

from typing import Dict, List, Optional, Any

class TimeLagEstimator:
    """
    Estimates biological time delays for both intracellular and extracellular signaling pathways.

    Time lags represent the delay between ligand secretion by a sender cell and the 
    corresponding downstream functional activation inside a receiver cell. It accounts for:
    1. Extracellular delay: The time required for a signal to traverse the physical distance between cells.
    2. Intracellular delay: The time required for a signal to propagate down the Boolean network topology.
    
    :param strategy: Strategy to estimate intracellular delays ('topological' or 'experimental'). Defaults to 'topological'.
    :type strategy: str
    :param custom_lags: A dictionary mapping receptor/pathway names to specific intracellular time lags (in minutes).
    :type custom_lags: dict, optional
    :param signal_velocity: The propagation speed of the extracellular signal through the tissue matrix (distance units per minute). Defaults to 5.0.
    :type signal_velocity: float
    """

    def __init__(self, strategy: str = "topological", custom_lags: Optional[Dict[str, float]] = None, signal_velocity: float = 5.0):
        """
        Constructor method.
        """
        self.strategy = strategy
        self.custom_lags = custom_lags or {}
        self.signal_velocity = signal_velocity
        
        # Internal storage for computed intracellular delays per receptor/pathway
        self.intracellular_lags: Dict[str, float] = {}

    def calculate_intracellular_lags(self, network_nodes: List[str], active_receptors: List[str]) -> None:
        """
        Computes the intracellular signal propagation delay for each active receptor.

        If the strategy is 'topological', it estimates the delay based on a heuristic 
        proportional to the complexity of the sub-network or path length (placeholder for full graph parsing).
        If 'experimental', it applies literature-based standard values for common signaling families.

        :param network_nodes: All nodes present in the loaded MaBoSS models.
        :type network_nodes: list of str
        :param active_receptors: List of receptor complexes identified as active by LIANA+.
        :type active_receptors: list of str
        :return: None
        """
        for receptor in active_receptors:
            # If a custom lag is provided by the user, it takes highest priority
            if receptor in self.custom_lags:
                self.intracellular_lags[receptor] = self.custom_lags[receptor]
                continue

            if self.strategy == "topological":
                # Heuristic: Placeholder simulating path-length analysis in the Boolean network.
                # In full implementation, this parses the dependency tree of the .bnd definitions.
                # Default baseline of 10 minutes for typical kinase cascades.
                self.intracellular_lags[receptor] = 10.0
                
            elif self.strategy == "experimental":
                # Literature baseline heuristics based on receptor family name matches
                rec_upper = receptor.upper()
                if "TNF" in rec_upper or "FAS" in rec_upper: # Death receptors / apoptosis pathways
                    self.intracellular_lags[receptor] = 15.0
                elif "EGFR" in rec_upper or "FGFR" in rec_upper or "MAPK" in rec_upper: # RTKs (fast cascades)
                    self.intracellular_lags[receptor] = 5.0
                elif "JAK" in rec_upper or "STAT" in rec_upper or "IL" in rec_upper: # Cytokine receptors
                    self.intracellular_lags[receptor] = 20.0
                else:
                    self.intracellular_lags[receptor] = 10.0 # Standard fallback
            else:
                self.intracellular_lags[receptor] = 0.0

    def compute_extracellular_lag(self, distance: float) -> float:
        """
        Calculates the physical time delay for a ligand to diffuse or travel across a given distance.

        :param distance: The Euclidean distance between the sender and receiver cell.
        :type distance: float
        :return: Extracellular time delay in minutes.
        :rtype: float
        """
        if self.signal_velocity <= 0:
            return 0.0
        return distance / self.signal_velocity

    def get_total_lag(self, receptor_name: str, distance: float) -> float:
        """
        Computes the combined total lag (extracellular + intracellular) for a communication event.

        This total lag defines how far back into the historical state buffer the simulation
        must look to find the effective signal strength influencing the receiver cell at time t.

        :param receptor_name: Name of the receptor/pathway node being evaluated.
        :type receptor_name: str
        :param distance: Physical distance between the sending cell and receiving cell.
        :type distance: float
        :return: Total time lag in minutes.
        :rtype: float
        """
        intra_lag = self.intracellular_lags.get(receptor_name, 10.0)
        extra_lag = self.compute_extracellular_lag(distance)
        
        return intra_lag + extra_lag