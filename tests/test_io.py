import os
import pytest
import numpy as np
from OmniPhysiBoSS.io.anndata_io import AnnDataParser
from tests.mock_data import create_mock_anndata

def test_load_data_file_not_found() -> None:
    """
    Verifies that AnnDataParser raises FileNotFoundError for non-existent paths.
    """
    # Execution validation
    ## Missing file scenario
    ### Assert exception handling for wrong path
    with pytest.raises(FileNotFoundError):
        AnnDataParser("non_existent_file_path.h5ad")

def test_extract_spatial_coordinates_2d(tmp_path) -> None:
    """
    Validates correct 2D matrix extraction and 3D-to-2D dimension pruning.
    """
    # Test fixture setup
    ## Temporary disk write
    ### Save mock object to temporary location
    adata = create_mock_anndata()
    file_path = os.path.join(tmp_path, "test_data.h5ad")
    adata.write_h5ad(file_path)

    # Parser execution
    ## Coordinate parsing
    ### Load and verify structural properties
    parser = AnnDataParser(file_path)
    parser.load_data()

    coords_2d = parser.extract_spatial_coordinates(key="spatial")
    coords_3d_pruned = parser.extract_spatial_coordinates(key="spatial_3d")

    # Assertions block
    ## Shape and integrity checks
    ### Validate dimensional boundaries
    assert coords_2d.shape == (5, 2)
    assert coords_3d_pruned.shape == (5, 2)
    np.testing.assert_array_equal(coords_2d, coords_3d_pruned)


def test_extract_spatial_coordinates_key_error(tmp_path) -> None:
    """
    Ensures KeyError is raised when the requested spatial key is missing from obsm.
    """
    # Test fixture setup
    ## Data persistence
    ### Commit structural template to disk
    adata = create_mock_anndata()
    file_path = os.path.join(tmp_path, "test_data.h5ad")
    adata.write_h5ad(file_path)

    # Validation flow
    ## Boundary check
    ### Query undefined dictionary key
    parser = AnnDataParser(file_path)
    parser.load_data()

    with pytest.raises(KeyError):
        parser.extract_spatial_coordinates(key="missing_key")

def test_extract_metadata_success(tmp_path) -> None:
    """
    Confirms correct parsing of annotated metadata and cellular phenotypes.
    """
    # Setup step
    ## Object isolation
    ### Write and read test database
    adata = create_mock_anndata()
    file_path = os.path.join(tmp_path, "test_data.h5ad")
    adata.write_h5ad(file_path)

    # Metadata extraction execution
    ## Execution pipeline
    ### Run query against sample attributes
    parser = AnnDataParser(file_path)
    parser.load_data()

    metadata = parser.extract_metadata(cell_type_column="cell_type")

    # Structural assertion
    ## Verifying content correctness
    ### Match explicit classification groups
    assert metadata.shape == (5, 1)
    assert list(metadata["cell_type"]) == ["Tumor", "T-Cell", "B-Cell", "Tumor", "Macrophage"]