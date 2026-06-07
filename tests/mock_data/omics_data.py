import anndata as ad
import pandas as pd
import numpy as np

# Transcriptomics mock data generator
## Function to construct high-fidelity space profiles
def create_mock_anndata() -> ad.AnnData:
    """
    Generates a standardized mock AnnData object for spatial transcriptomics unit tests.

    The object contains a small expression matrix (5 cells, 4 genes),
    2D spatial coordinates, 3D spatial coordinates for dimension pruning tests,
    and cell type metadata annotations.

    :return: A populated AnnData instance for testing.
    :rtype: anndata.AnnData
    """
    # Matrix setup
    X = np.array([
        [0.1, 0.8, 0.0, 0.4],
        [0.9, 0.2, 0.1, 0.0],
        [0.0, 0.0, 0.7, 0.9],
        [0.4, 0.5, 0.3, 0.2],
        [0.1, 0.1, 0.9, 0.8]
    ], dtype=np.float32)

    # Metadata annotations
    obs = pd.DataFrame(
        {"cell_type": ["Tumor", "T-Cell", "B-Cell", "Tumor", "Macrophage"]},
        index=[f"cell_{i}" for i in range(5)]
    )
    var = pd.DataFrame(index=["Gene_A", "Gene_B", "Gene_C", "Gene_D"])

    # Spatial coordinates matrices
    spatial_2d = np.array([
        [10.0, 20.0],
        [15.0, 25.0],
        [20.0, 30.0],
        [25.0, 35.0],
        [30.0, 40.0]
    ], dtype=np.float32)

    spatial_3d = np.array([
        [10.0, 20.0, 5.0],
        [15.0, 25.0, 6.0],
        [20.0, 30.0, 7.0],
        [25.0, 35.0, 8.0],
        [30.0, 40.0, 9.0]
    ], dtype=np.float32)

    # Encapsulate matrices into the AnnData container
    adata = ad.AnnData(X=X, obs=obs, var=var)
    adata.obsm["spatial"] = spatial_2d
    adata.obsm["spatial_3d"] = spatial_3d

    return adata