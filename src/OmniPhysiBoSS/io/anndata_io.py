"""
io/anndata_io.py
----------------------------
Class for loading anndata objects, to ensure compatibility. 
"""


import os
import anndata as ad
import pandas as pd
import numpy as np

class AnnDataParser:
    """
    Class responsible for parsing and extracting data from AnnData objects
    containing spatial transcriptomics data.

    :param file_path: Path to the .h5ad format file.
    :type file_path: str
    """

    def __init__(self, file_path: str) -> None:
        # io initialization
        ## path validation
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        self.file_path = file_path
        self.adata: ad.AnnData = None

    def load_data(self) -> ad.AnnData:
        """
        Loads the .h5ad file into memory as an AnnData object.

        :return: Loaded omics data object.
        :rtype: anndata.AnnData
        """
        # io operations
        ## loading anndata
        ### read h5ad file from disk
        self.adata = ad.read_h5ad(self.file_path)
        return self.adata

    def extract_spatial_coordinates(self, key: str = "spatial") -> np.ndarray:
        """
        Extracts two-dimensional spatial coordinates of cells.

        :param key: Key in obsm containing coordinates, defaults to "spatial".
        :type key: str
        :return: Coordinate matrix with dimensions (n_cells, 2).
        :rtype: numpy.ndarray
        :raises KeyError: If the key does not exist in the object's obsm.
        """
        # data extraction
        ## spatial extraction
        ### check obsm matrix validity
        if self.adata is None:
            raise ValueError("Data has not been loaded. Call load_data() first.")
        
        if key in self.adata.obsm:
            # dimensional pruning
            ## force 2d coordinates
            coords = self.adata.obsm[key]
            return coords[:, :2]
        else:
            raise KeyError(f"Key '{key}' was not found in the .obsm section of the loaded AnnData object.")

    def extract_metadata(self, cell_type_column: str) -> pd.DataFrame:
        """
        Extracts cell metadata, specifically cell type annotations.

        :param cell_type_column: Name of the column in obs containing cell types.
        :type cell_type_column: str
        :return: DataFrame containing identifiers and assigned cell types.
        :rtype: pandas.DataFrame
        :raises KeyError: If the column does not exist in the obs section.
        """
        # data extraction
        ## metadata extraction
        ### check obs columns validity
        if self.adata is None:
            raise ValueError("Data has not been loaded. Call load_data() first.")
        
        if cell_type_column not in self.adata.obs.columns:
            raise KeyError(f"Column '{cell_type_column}' does not exist in the .obs section.")
            
        return self.adata.obs[[cell_type_column]]