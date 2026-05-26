# src/MaBossSpatial/spatial_module/base.py

from abc import ABC, abstractmethod
import anndata
from typing import List, Tuple

class BaseSpatialEnvironment(ABC):
    """
    Abstract Base Class for managing and extracting spatial tissue environments.

    This class defines the interface for constructing spatial connectivity 
    graphs and extracting precise localized subgraphs (Simulation Set ($V_\mathrm{sim}$) and Context Set ($V_\mathrm{context}$)) 
    necessary for continuous piecewise Boolean simulations.
    """

    @abstractmethod
    def build_spatial_context(self, adata: anndata.AnnData, **kwargs) -> anndata.AnnData:
        """
        Ensures the AnnData object contains spatial graphs and cell-cell communication metrics.

        :param adata: The annotated data matrix of shape n_obs x n_vars.
        :type adata: anndata.AnnData
        :param kwargs: Arbitrary keyword arguments for spatial algorithm tuning.
        :return: The updated AnnData object containing spatial connectivity and communication data.
        :rtype: anndata.AnnData
        """
        pass

    @abstractmethod
    def extract_simulation_and_context_sets(
        self, adata: anndata.AnnData, target_cell_ids: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Extracts localized subgraphs representing the execution boundary and boundary conditions.

        Defines the (Simulation Set ($V_\mathrm{sim}$) and Context Set ($V_\mathrm{context}$) based on the
        underlying spatial connectivity matrix.

        :param adata: The annotated data matrix containing computed spatial connectivities.
        :type adata: anndata.AnnData
        :param target_cell_ids: Barcodes of focal cells chosen for detailed spatial tracking.
        :type target_cell_ids: list of str
        :return: A tuple containing (simulation_set_barcodes, context_set_barcodes).
        :rtype: tuple of (list of str, list of str)
        """
        pass