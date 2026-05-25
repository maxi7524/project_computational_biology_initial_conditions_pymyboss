# src/maboss_module/model_manager.py

import copy
import anndata
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional

# maboSS is imported inside methods or safely handled to avoid installation blocks during setup
try:
    import maboss
except ImportError:
    maboss = None


class MaBossManager:
    """
    Manages the lifecycle, configuration, and initialization of MaBoSS Boolean models.

    This module maintains a collection of Boolean network models used for simulation.
    It provides capabilities to load pretrained models, structure placeholders for 
    de novo network generation based on cell expression profiles, and compute baseline
    initial states (istate) using global 99th percentile normalization.
    """

    def __init__(self):
        """
        Constructor method.
        """
        # Stores models by a unique identifier string (e.g., pathway name or cell type)
        self.models: Dict[str, Any] = {}
        # Cached list of nodes present across the loaded models
        self.network_nodes: Dict[str, List[str]] = {}
        # Internal cache to store structural file paths for safe lazy duplication
        self.model_paths: Dict[str, Dict[str, str]] = {}

    def load_pretrained(self, bnd_path: str, cfg_path: str, model_name: str) -> None:
        """
        Loads an existing MaBoSS model definition from structural and configuration files.

        :param bnd_path: Path to the .bnd file containing network topology and logic gates.
        :type bnd_path: str
        :param cfg_path: Path to the .cfg file containing parameters and simulation settings.
        :type cfg_path: str
        :param model_name: A unique identifier key to store this specific model in the manager.
        :type model_name: str
        :raises ImportError: If the maboss library is not installed in the environment.
        :return: None
        """
        if maboss is None:
            raise ImportError("The 'maboss' library is required but not installed in this environment.")

        # maboss.load returns a maboss.Simulation object
        simulation_obj = maboss.load(bnd_path, cfg_path)

        # Save file references to bypass deepcopy restrictions with compiled C++ wrappers
        self.model_paths[model_name] = {"bnd": bnd_path, "cfg": cfg_path}
        
        self.models[model_name] = simulation_obj
        self.network_nodes[model_name] = list(simulation_obj.network.keys())
        print(f"Successfully loaded pretrained MaBoSS model '{model_name}' with {len(self.network_nodes[model_name])} nodes.")

    def build_pathways_denovo(self, adata: anndata.AnnData, cell_ids: List[str], model_name: str = "denovo_model") -> None:
        """
        Constructs a Boolean network model de novo based on transcriptomic data.

        This method acts as a placeholder for downstream integration with OmniPath and decoupler.
        It will classify cells based on expression footprints, identify active downstream
        targets for specific receptors, and assemble independent Boolean rule graphs.

        :param adata: The main AnnData object containing expression data.
        :type adata: anndata.AnnData
        :param cell_ids: Subset of cell barcodes to utilize for pathway footprinting.
        :type cell_ids: list of str
        :param model_name: A unique identifier key to save the generated model.
        :type model_name: str
        :return: None
        """
        # TODO: Implement OmniPath graph querying
        # TODO: Use decoupler to score transcription factor / pathway activity
        # TODO: Translate scored interactions into boolean logic rules (.bnd structure)
        pass

    @property
    def all_nodes(self) -> List[str]:
        """
        Returns a flat, unique list of all node names present across all managed models.

        :return: List of all network nodes.
        :rtype: list of str
        """
        unique_nodes = set()
        for nodes_list in self.network_nodes.values():
            unique_nodes.update(nodes_list)
        return sorted(list(unique_nodes))

    def compute_global_quantiles(self, adata: anndata.AnnData, nodes: List[str]) -> Dict[str, float]:
        """
        Calculates the 99th percentile expression threshold for network nodes across the entire dataset.

        This serves as a normalization baseline to eliminate outliers and map continuous expression
        values into a [0, 1] probability range for initial states.

        :param adata: The main AnnData object.
        :type adata: anndata.AnnData
        :param nodes: List of node/gene names to evaluate.
        :type nodes: list of str
        :return: A dictionary mapping gene/node names to their calculated 99th percentile value.
        :rtype: dict
        """
        #TODO - we can modify this values a little adding some arcsin normalized or something so it is more curvy (increase is lower)
        quantiles = {}
        # Ensure we only check genes that are actually present in the expression matrix (adata.var_names)
        available_genes = [node for node in nodes if node in adata.var_names]
        
        for gene in available_genes:
            # Extract expression vector across all cells in the dataset
            # Handles sparse or dense matrices safely
            if hasattr(adata[:, gene].X, "toarray"):
                expression_vector = adata[:, gene].X.toarray().flatten()
            else:
                expression_vector = adata[:, gene].X.flatten()
                
            q99 = np.percentile(expression_vector, 99)
            # Prevent division by zero if the gene expression is entirely zero
            quantiles[gene] = q99 if q99 > 0 else 1.0
            
        return quantiles

    def initialize_evaluation_models(self, adata: anndata.AnnData, simulation_set: List[str], 
                                     context_set: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Generates cell-specific initialized MaBoSS models for the evaluation phase.

        Applies the 99th percentile normalization to map gene expression to initial node activation
        probabilities (istate) for all cells in the simulation subgraph.

        :param adata: The main AnnData object.
        :type adata: anndata.AnnData
        :param simulation_set: Barcodes of cells to be actively simulated over time (1-hop zone).
        :type simulation_set: list of str
        :param context_set: Barcodes of background context cells (2-hop zone, used for initial outer conditions).
        :type context_set: list of str
        :return: A nested dictionary structure mapping cell IDs to their personalized cloned models.
                 Format: {cell_id: {model_name: maboss.Simulation}}
        :rtype: dict
        """
        initialized_cell_systems = {}
        all_active_nodes = self.all_nodes
        
        # Calculate the 99th percentile threshold globally across the whole tissue image
        global_q99 = self.compute_global_quantiles(adata, all_active_nodes)
        
        # Combine both sets to ensure we know the initial state of everything in our spatial boundaries
        all_tracked_cells = list(set(simulation_set).union(set(context_set)))
        
        for cell_id in all_tracked_cells:
            initialized_cell_systems[cell_id] = {}
            
            # For every cell, clone the template models and calibrate them using the cell's expression profile
            for model_name, template_sim in self.models.items():
                # FIX: Reload via file paths instead of copy.deepcopy to bypass SWIG-compiled memory constraints
                bnd_p = self.model_paths[model_name]["bnd"]
                cfg_p = self.model_paths[model_name]["cfg"]
                cell_sim_instance = maboss.load(bnd_p, cfg_p)
                
                # Fetch cell index in the anndata object
                cell_idx = adata.obs_names.get_loc(cell_id)
                
                # Set node initial states based on normalized single-cell expression values
                for node in self.network_nodes[model_name]:
                    if node in adata.var_names:
                        if hasattr(adata.X, "toarray"):
                            raw_val = adata[cell_idx, node].X.toarray()[0, 0]
                        else:
                            raw_val = adata[cell_idx, node].X[0, node] if hasattr(adata.X, "ndim") and adata.X.ndim > 1 else adata[cell_idx, node].X
                            
                        # Apply 99% quantile saturation logic
                        normalized_activity = min(1.0, float(raw_val / global_q99[node]))
                    else:
                        # Fallback default if the node is not a gene in the adata (e.g., abstract phenotypes)
                        normalized_activity = 0.0
                    
                    # Map to MaBoSS initial state: [Prob(Node=0), Prob(Node=1)]
                    cell_sim_instance.network.set_istate(node, [1.0 - normalized_activity, normalized_activity])
                
                initialized_cell_systems[cell_id][model_name] = cell_sim_instance
                
        return initialized_cell_systems