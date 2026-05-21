import maboss
from pathlib import Path
from typing import Dict, Union

class MaBossManager:
    """
    Handles the loading, parsing, and modification of MaBoSS Boolean models.
    """
    def __init__(self):
        self.model = None
        self.nodes = []

    def load_pretrained(self, bnd_path: Union[str, Path], cfg_path: Union[str, Path]):
        """
        Loads an existing MaBoSS model from .bnd and .cfg files.
        
        Args:
            bnd_path: Path to the .bnd file (Boolean network definition).
            cfg_path: Path to the .cfg file (Configuration and parameters).
        """
        # Ensure paths are strings as expected by maboss API
        self.model = maboss.load(str(bnd_path), str(cfg_path))
        self.nodes = list(self.model.network.keys())
        return self.model

    def set_receptor_activation(self, receptor_name: str, activation_score: float, mode: str = "istate"):
        """
        Modifies the model to reflect receptor activation based on external signals.
        
        Args:
            receptor_name: The name of the node representing the receptor.
            activation_score: Normalized score (0.0 to 1.0) representing signal strength.
            mode: 'istate' modifies initial probabilities, 'rate' modifies transition rates.
        """
        if receptor_name not in self.nodes:
            raise ValueError(f"Receptor {receptor_name} not found in the Boolean network.")

        if mode == "istate":
            # Set the initial probability [Prob(0), Prob(1)]
            self.model.network.set_istate(receptor_name, [1 - activation_score, activation_score])
        elif mode == "rate":
            # Modify the transition rate parameter directly for spatial/continuous updates
            param_name = f"${receptor_name}_up"
            self.model.param[param_name] = activation_score
        else:
            raise ValueError("Mode must be either 'istate' or 'rate'.")