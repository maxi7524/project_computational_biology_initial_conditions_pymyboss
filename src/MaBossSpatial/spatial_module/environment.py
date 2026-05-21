# src/spatial_module/environment.py

import anndata
import liana as li
import numpy as np
from scipy.sparse import issparse
from typing import Dict, List, Any, Set, Tuple

class SpatialEnvironment:
    """
    Manages spatial neighborhood graphs leveraging LIANA+'s optimized backend.

    This module delegates spatial weight calculations to LIANA+ and handles the extraction
    of 1-hop simulation subgraphs and 2-hop neighborhood-of-neighborhood context boundaries
    required for lazy evaluation.
    """

    def __init__(self):
        """
        Constructor method.
        """
        self.kernel_params: Dict[str, Any] = {}
        self.connectivity_key: str = "spatial_connectivities"

    def configure_kernel(self, bandwidth: float, cutoff: float, kernel: str) -> None:
        """
        Stores parameters for LIANA+'s spatial neighbor calculation.

        :param bandwidth: Bandwidth parameter controlling signaling distance.
        :type bandwidth: float
        :param cutoff: Minimum weight threshold below which connectivity is zero.
        :type cutoff: float
        :param kernel: Kernel type, e.g., 'gaussian', 'exponential', 'linear'.
        :type kernel: str
        :return: None
        """
        self.kernel_params = {
            "bandwidth": bandwidth,
            "cutoff": cutoff,
            "kernel": kernel,
            "set_diag": True,
            "inplace": True,
            "key_added": "spatial"
        }

    def compute_neighbors_graph(self, adata: anndata.AnnData) -> None:
        """
        Executes LIANA+'s optimized neighbor computation in place on the AnnData object.

        Populates ``adata.obsp['spatial_connectivities']``.

        :param adata: The main AnnData object containing spatial coordinates.
        :type adata: anndata.AnnData
        :return: None
        """
        if not self.kernel_params:
            raise RuntimeError("Spatial kernel settings have not been configured. Call configure_kernel first.")
        
        # Invoke LIANA+ native optimized spatial grid builder
        li.ut.spatial_neighbors(adata, **self.kernel_params)

    def extract_neighborhood_zones(self, adata: anndata.AnnData, target_cell_ids: List[str]) -> Tuple[List[str], List[str]]:
        """
        Extracts the 1-hop simulation set and 2-hop context set for a list of target cells.

        Uses the computed connectivity matrix to look up neighbors efficiently.

        :param adata: The main AnnData object containing the calculated connectivities.
        :type adata: anndata.AnnData
        :param target_cell_ids: Barcodes of the starting core cells.
        :type target_cell_ids: list of str
        :return: A tuple containing (simulation_set_ids, context_set_ids).
                 simulation_set contains targets + 1-hop neighbors.
                 context_set contains 2-hop neighbors (neighborhood of neighborhood).
        :rtype: tuple of lists
        """
        if self.connectivity_key not in adata.obsp:
            raise KeyError(f"Neighborhood graph '{self.connectivity_key}' not found in adata.obsp. Run compute_neighbors_graph first.")
            
        connectivities = adata.obsp[self.connectivity_key]
        cell_names = adata.obs_names.tolist()
        cell_to_idx = {cell: i for i, cell in enumerate(cell_names)}
        
        simulation_set_idx: Set[int] = set()
        context_set_idx: Set[int] = set()
        
        # 1-Hop: Find target cells and their immediate spatial neighbors
        for cell_id in target_cell_ids:
            if cell_id not in cell_to_idx:
                continue
            idx = cell_to_idx[cell_id]
            simulation_set_idx.add(idx)
            
            # Get row from adjacency matrix (handles sparse CSR matrix format from LIANA+)
            row = connectivities[idx].toarray().flatten() if issparse(connectivities) else connectivities[idx]
            neighbors = np.where(row > 0)[0]
            simulation_set_idx.update(neighbors)
            
        # 2-Hop: Find neighbors of the immediate neighbors (Context Set for t=0 initial state)
        for idx in simulation_set_idx:
            row = connectivities[idx].toarray().flatten() if issparse(connectivities) else connectivities[idx]
            neighbors = np.where(row > 0)[0]
            for n in neighbors:
                if n not in simulation_set_idx:
                    context_set_idx.add(n)
                    
        # Map indices back to cell barcode strings
        simulation_set_ids = [cell_names[i] for i in simulation_set_idx]
        context_set_ids = [cell_names[i] for i in context_set_idx]
        
        return sorted(simulation_set_ids), sorted(context_set_ids)