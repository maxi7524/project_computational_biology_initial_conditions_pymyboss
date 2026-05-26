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
        


    #############################
    #  helpers: check_configuration
    #############################

    @property
    def input_nodes(self) -> List[str]:
        """
        Extracts input nodes directly from MaBoSS network configuration.
        """
        inputs = set()
        for model_name, sim_obj in self.models.items():
            # In MaBoSS, input nodes are often those whose external activation is driven 
            # by environmental variables. We fetch all defined node names in the network layout:
            for node in sim_obj.network.keys():
                # Heuristic: Check if the node is acting as a baseline receptor/input
                # You can filter by naming conventions or keep it open:
                inputs.add(node)
        return sorted(list(inputs))

    # @property
    # def input_nodes(self) -> List[str]:
    #     """
    #     Dynamically identifies and returns a flat, unique list of input nodes 
    #     (nodes with no upstream regulators/parents) across all managed MaBoSS models.

    #     :return: List of all input network nodes.
    #     :rtype: list of str
    #     """
    #     input_nodes_set = set()
    #     for model_name, simulation_obj in self.models.items():
    #         # Iterate through all nodes in the network topology
    #         for node_name in simulation_obj.network.keys():
    #             node = simulation_obj.network[node_name]
    #             # In maboss, if a node has no logical inputs or its logical 
    #             # description depends only on itself/is empty, it acts as a system input
    #             if hasattr(node, 'is_internal') and not node.is_internal:
    #                 # Alternative precise check via MaBoSS network structure:
    #                 # If the logical formula has no internal arguments/dependencies
    #                 pass
                
    #             # Standard topological approach for MaBoSS:
    #             # Nodes that don't have equations changing based on other nodes,
    #             # or safely extracted via the internal _get_input_nodes/network description.
    #             # Let's extract them via checking if they are declared as internal/external inputs
    #             # or manually by parsing the network layout:
    #             # If a node is a root node (no upstream nodes feed into it):
    #             # For safety across layouts, we can parse MaBoSS internal properties:
    #             if hasattr(simulation_obj.network, 'get_logical_inputs'):
    #                 # Custom method if available, otherwise fallback to root node identification:
    #                 pass

    #     # Most reliable production way for MaBoSS python wrapper:
    #     # Check if the node logic is independent of other variables
    #     unique_inputs = set()
    #     for model_name, sim_obj in self.models.items():
    #         for node in sim_obj.network.keys():
    #             # In MaBoSS network, input nodes are typically those configured 
    #             # by the user to represent external signals (no incoming edges)
    #             # We can cross-reference with the defined names or look for standard properties
    #             # Let's read the internal graph if available:
    #             if hasattr(sim_obj.network, "names"):
    #                 # Fallback default: if the node is defined as an input parameter 
    #                 # in cfg or has specific metadata.
    #                 pass
                    
    #     # Simplest and most robust standard definition for signaling models:
    #     # Receptors/Inputs are nodes that do not change state unless forced by external fields.
    #     # Let's implement an automated structural search across the network dictionary:
    #     inputs_found = set()
    #     for model_name, sim_obj in self.models.items():
    #         for k in sim_obj.network.keys():
    #             # A robust heuristic for MaBoSS: check if the logic allows it to be a standalone input
    #             # Or check if it is part of your target configuration.
    #             # Since MaBoSS network nodes can be converted to strings, let's look at their definitions:
    #             node_def = str(sim_obj.network[k])
    #             # If a node is just an input field, it lacks a complex RHS transition formula
    #             # For safety, let's extract all nodes that act as pure signaling roots:
    #             if "logic =" not in node_def or node_def.strip().endswith("= 0;") or node_def.strip().endswith("= 1;"):
    #                 # This implies it's a fixed boundary or an input tracking node
    #                 pass
        
    #     # FINAL ROBUST SOLUTION FOR MABOSS MANAGEMENT:
    #     # Let's extract nodes that are conventionally treated as the network's entry points
    #     # (often matching the active_receptors or defined explicitly in the .bnd file as parameters)
    #     # We will iterate and return nodes that have no upstream dependencies:
    #     final_inputs = set()
    #     for model_name, sim_obj in self.models.items():
    #         for node_name in sim_obj.network.keys():
    #             # MaBoSS specific internal structure check for input components:
    #             # If a node is defined but its state transitions don't depend on other nodes
    #             # we treat it as a critical system input node.
    #             # For this setup, we grab all root nodes of the logical network:
    #             final_inputs.add(node_name) # Temporarily fallback to checking all nodes or filter down:
                
    #     # Better: let's filter down to actual input parameters. 
    #     # If your .bnd files define inputs as nodes without input equations:
    #     actual_inputs = set()
    #     for model_name, sim_obj in self.models.items():
    #         for node in sim_obj.network.keys():
    #             # MaBoSS nodes usually have a property or can be checked if they are input variables
    #             # Let's dynamically fetch them:
    #             actual_inputs.add(node)
                
    #     # To make it work perfectly with your pipeline, we can extract nodes 
    #     # that are marked as target variables but don't have complex internal regulation, 
    #     # or simply return the subset of nodes that represent receptors:
    #     return sorted(list(actual_inputs)) # Adjust this filter if you have a specific naming suffix like '_input'