# src/MaBossSpatial/spatial_module/environment.py

import numpy as np
import anndata
import scanpy as sc
import liana as li
from scipy.sparse import issparse
from typing import List, Tuple, Dict, Any
from .base import BaseSpatialEnvironment

class LianaSpatialEnvironment(BaseSpatialEnvironment):
    r"""
    Spatial environment manager utilizing LIANA+'s coordinate-based graph backends.

    Methodology:
        The framework models the spatial tissue slice as a topological graph structure 
        :math:`G = (V, E, W)`. To execute localized, time-delayed Boolean simulations 
        without global computational overhead, the manager dynamically isolates two 
        distinct spatial subgraphs flanking user-defined focal nodes (:math:`V_{\mathrm{target}}`):
        
        1. **Simulation Set** (:math:`V_{\mathrm{sim}}`): Contains the focal target nodes 
           and their immediate spatial neighbors. Every node within this boundary undergoes 
           active stochastic piecewise Boolean transitions via MaBoSS, meaning their state 
           vectors evolve continuously over time.
        
        2. **Context Set** (:math:`V_{\mathrm{context}}`): Comprises the immediate boundary 
           layer surrounding :math:`V_{\mathrm{sim}}` (neighbors of neighbors that do not 
           overlap with :math:`V_{\mathrm{sim}}`). These nodes act as spatial boundary 
           conditions; their profiles are frozen at :math:`t = 0` to provide static external 
           signaling inputs (ligand pools) to the outer rim of the active simulation set.

    :param connectivity_key: Key under ``adata.obsp`` where the adjacency matrix is stored. Defaults to 'spatial_connectivities'.
    :type connectivity_key: str
    :param liana_key: Key under ``adata.uns`` where ligand-receptor associations are cached. Defaults to 'liana_res'.
    :type liana_key: str
    """

    def __init__(self, connectivity_key: str = "spatial", liana_key: str = "liana_res"):
        """
        Constructor method.
        """
        self.connectivity_key = connectivity_key
        self.liana_key = liana_key



    def build_spatial_context(
        self, 
        adata: anndata.AnnData, 
        config_spatial_neighbors: Dict[str, Any], 
        config_liana_bivariate: Dict[str, Any], 
        **kwargs
    ) -> anndata.AnnData:
        r"""
        Executes spatial graph generation and formal cell-cell communication bivariate scoring.

        Derives baseline parameters, merges user-defined overrides, prints a comprehensive 
        auditing report detailing the final execution parameters, and lazily triggers 
        the underlying coordinate graph assembly and ligand-receptor colocalization pipelines.

        :param adata: The annotated single-cell/spatial data matrix to supplement.
        :type adata: anndata.AnnData
        :param config_spatial_neighbors: Parameter configuration dictionary for LIANA+'s neighbor graph generator.
        :type config_spatial_neighbors: dict
        :param config_liana_bivariate: Parameter configuration dictionary for LIANA+'s local bivariate association metrics.
        :type config_liana_bivariate: dict
        :param kwargs: Optional runtime adjustments and catch-all overrides.
        :return: Augmented AnnData object with completed spatial parameters.
        :rtype: anndata.AnnData
        """
        print("=" * 80)
        print("                 LIANA+ SPATIAL CONTEXT ESTIMATION & AUDIT")
        print("=" * 80)

        # --- STEP 1: Parameter Estimation and Merging ---

        # Obtain optimal parameters
        ## preprocessing (if it is not provided) 
        ### Check log1p condition
        if "log1p" in adata.uns:
            is_raw_counts = False
            print("[-] Verified via adata.uns: 'log1p' transformation flag detected.")
        else:
            ### we take not zero values 
            if issparse(adata.X):
                #### we take sample of 5000 not zero values 
                sample_vals = adata.X.data[:5000]
            else:
                sample_vals = adata.X[adata.X > 0][:5000]

            if len(sample_vals) > 0:
                ### WE check if all values are ints (raw data)
                is_raw_counts = np.all(np.equal(np.mod(sample_vals, 1), 0))
                ### scale check - should not be higher than 20
                if not is_raw_counts and np.max(sample_vals) > 100:
                    print("[!] Warning: High continuous values detected without log1p flag.")
            else:
                is_raw_counts = False

        ### Execution of dynamic normalization if raw counts are proven
        if is_raw_counts:
            print("[!] Critical: Raw integer counts detected in adata.X! Triggering automated log-normalization...")
            if adata.raw is None:
                print("    - Freezing raw integer counts inside backup register: adata.raw")
                adata.raw = adata
            print("    - Executing total library size normalization (target_sum=1e4)...")
            sc.pp.normalize_total(adata, target_sum=1e4)
            print("    - Appending natural log transformation: log1p...")
            sc.pp.log1p(adata)
            print("[✓] Preprocessing sequence completed successfully.")
        else:
            print("[-] Verified via numerical sampling: adata.X contains preprocessed/continuous coordinates.")


        ## bandwidth
        ### Obtain optimal spatial bandwidth heuristically via neighbor scanning density curves
        print("\n[-] Evaluating optimal spatial propagation constraints via query_bandwidth...")
        _, df_bandwidth_vs_neighbors = li.ut.query_bandwidth(
            coordinates=adata.obsm['spatial'], 
            start=0, 
            end=500, 
            interval_n=20
        )
        ### calculate valid bandwidths (n_neighbors >= 6)
        valid_bandwidths = df_bandwidth_vs_neighbors[df_bandwidth_vs_neighbors['neighbours'] >= 6]['bandwith']
        #### case: take minimum bandwidth which met condition
        if not valid_bandwidths.empty:
            min_bandwidth = float(valid_bandwidths.min())
        #### case: not reached - take highest bandwidth
        else:
            min_bandwidth = float(df_bandwidth_vs_neighbors['bandwith'].max())
            print("[!] Warning: Safe bandwidth bound (k >= 6) not reached. Utilizing max fallback.")
            
        print(f"    - Resolved minimum mathematical bandwidth for unified connectivity (k>=6): {min_bandwidth}")
        # Define configs
        ## Idempotent connectivity key synchronization
        base_conn_key = self.connectivity_key.replace("_connectivities", "")
        bivariate_conn_key = f"{base_conn_key}_connectivities"

        ## Define internal empirical baselines for spatial neighbor configuration
        estimated_neighbors = {
            'adata': adata,
            "kernel": "gaussian",
            "bandwidth": min_bandwidth,
            "cutoff": 0.1,
            "set_diag": False,
            ### Synchronized dynamic assignment
            ### > it automatically 
            "key_added": base_conn_key
        }
        
        ## Define internal empirical baselines for local bivariate configuration
        estimated_bivariate = {
            'mdata': adata,
            'local_name': 'cosine',
            'global_name': None,
            ### REMARK - this depends on speciee
            'resource_name': 'consensus',
            ### graph key for `SpatialEnvironment`
            'n_perms': None,
            'mask_negatives': True, # we remove noise 
            'use_raw': False,
            'seed': 1337,
            ### Synchronized dynamic assignment
            "connectivity_key": bivariate_conn_key,
            "key_added": self.liana_key
        }


        ## Print estimated baselines
        print("[-] Initial Empirical Estimates:")
        print(f"    Spatial Neighbors : {estimated_neighbors}")
        print(f"    Local Bivariate   : {estimated_bivariate}")

        # Merge user configurations as overrides to the estimates
        ## spatial_neighbors config
        final_neighbors_config = estimated_neighbors.copy()
        overridden_neighbors = []
        for key, val in config_spatial_neighbors.items():
            if key in final_neighbors_config and final_neighbors_config[key] != val:
                overridden_neighbors.append(f"{key} ({final_neighbors_config[key]} -> {val})")
            final_neighbors_config[key] = val
        
        ## bivariate config
        final_bivariate_config = estimated_bivariate.copy()
        overridden_bivariate = []
        for key, val in config_liana_bivariate.items():
            if key in final_bivariate_config and final_bivariate_config[key] != val:
                overridden_bivariate.append(f"{key} ({final_bivariate_config[key]} -> {val})")
            final_bivariate_config[key] = val

        # Print override audit trail
        print("\n[!] Configuration Overrides Detected:")
        if overridden_neighbors:
            print(f"    Spatial Neighbors overrides : {', '.join(overridden_neighbors)}")
        else:
            print("    Spatial Neighbors overrides : None. Using pure empirical estimates.")
            
        if overridden_bivariate:
            print(f"    Local Bivariate overrides   : {', '.join(overridden_bivariate)}")
        else:
            print("    Local Bivariate overrides   : None. Using pure empirical estimates.")

        # Print final runtime configurations
        print("\n[✓] Final Consolidated Runtime Configuration:")
        print(f"    Final Spatial Neighbors parameters : {final_neighbors_config}")
        print(f"    Final Local Bivariate parameters   : {final_bivariate_config}")
        print("=" * 80)

        # --- STEP 2: Graph Construction Execution ---
        print(f"Executing neighbor adjacency calculation into adata.obsp['{self.connectivity_key}']...")
        li.ut.spatial_neighbors(
            **final_neighbors_config
        )

        # --- STEP 3: Bivariate Signaling Execution ---
        print(f"Executing bivariate ligand-receptor association scoring into adata.uns['{self.liana_key}']...")
        ## important dynamic path fix 
        target_uns_key = final_bivariate_config.pop('key_added', self.liana_key)
        bivariate_res = li.mt.bivariate(
            **final_bivariate_config
        )

        if bivariate_res is not None:
            adata.uns[target_uns_key] = bivariate_res
            print(f"[✓] Bivariate results successfully mapped into adata.uns['{self.liana_key}']")

        return adata

    def extract_simulation_and_context_sets(
        self, adata: anndata.AnnData, target_cell_ids: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Extracts structural indices to isolate the active Simulation Set ($V_{\mathrm{sim}}$) 
        and the boundary Condition Frame Context Set ($V_{\mathrm{context}}$).

        Parses the CSR sparse connectivity array to extract adjacent physical indices. 
        Ensures lazy evaluation limits simulation loads to relevant spatial neighborhoods.

        :param adata: The processed annotated data object containing the adjacency matrix.
        :type adata: anndata.AnnData
        :param target_cell_ids: List of source barcodes starting the spatial search.
        :type target_cell_ids: list of str
        :return: A structured tuple of (simulation_set_ids, context_set_ids).
        :rtype: tuple of (list of str, list of str)
        :raises KeyError: If the requested connectivity key cannot be resolved inside adata.obsp.
        """
        actual_conn_key = self.connectivity_key if self.connectivity_key.endswith("_connectivities") else f"{self.connectivity_key}_connectivities"

        if actual_conn_key not in adata.obsp:
            raise KeyError(f"Target adjacency matrix '{actual_conn_key}' not located in adata.obsp.")

        connectivities = adata.obsp[actual_conn_key]
        cell_names = adata.obs_names.tolist()
        cell_to_idx = {cell: i for i, cell in enumerate(cell_names)}
        
        simulation_set_idx = set()
        context_set_idx = set()
        
        # --- Step 1: Resolve Active Simulation Domain (Simulation Set - $V_{\mathrm{sim}}$) ---
        for cell_id in target_cell_ids:
            if cell_id not in cell_to_idx:
                continue
            idx = cell_to_idx[cell_id]
            simulation_set_idx.add(idx)
            
            if issparse(connectivities):
                row = connectivities[idx].toarray().flatten()
            else:
                row = connectivities[idx]
                
            neighbors = np.where(row > 0)[0]
            simulation_set_idx.update(neighbors)
            
        # --- Step 2: Resolve Boundary Condition Frame (Context Set - $V_{\mathrm{context}}$) ---
        for idx in simulation_set_idx:
            if issparse(connectivities):
                row = connectivities[idx].toarray().flatten()
            else:
                row = connectivities[idx]
                
            neighbors = np.where(row > 0)[0]
            for n in neighbors:
                if n not in simulation_set_idx:
                    context_set_idx.add(n)
                    
        # Map unique index pointers back to cell barcode entities
        simulation_set_ids = [cell_names[i] for i in simulation_set_idx]
        context_set_ids = [cell_names[i] for i in context_set_idx]
        
        return simulation_set_ids, context_set_ids