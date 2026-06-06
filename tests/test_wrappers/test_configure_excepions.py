import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from OmniPhysiBoSS.wrappers.configure_PhysiBoSS import stage_physiboss_project
from tests.mock_data import (
    get_reference_mock_xml_string,
    get_multi_model_mock_xml_string
)

# Exception handling and structural edge-case testing
## Validate system behavior under faulty configuration constraints
def test_stage_project_missing_xml(tmp_path):
    """
    Verifies that a FileNotFoundError is raised if the primary configuration file is missing from disk.

    :param tmp_path: Pytest temporary directory fixture token.
    :type tmp_path: Path
    """
    # Environment initialization
    invalid_path = tmp_path / "non_existent_settings.xml"
    
    # Execute verification assertions
    ## Verify catch limits for missing root deployment files
    with pytest.raises(FileNotFoundError, match="Primary project layout XML missing at location"):
        stage_physiboss_project(
            xml_path=invalid_path,
            maboss_models_map={},
            physiboss_root=tmp_path / "engine"
        )


def test_stage_project_prefix_mismatch(mock_env_factory):
    """
    Verifies that a ValueError is raised when network and parameter filenames use asymmetrical stems.

    :param mock_env_factory: Reusable mock environment tracking generator wrapper.
    :type mock_env_factory: Callable
    """
    # Load default single-model template configurations
    xml_path, physiboss_root, models_dir = mock_env_factory(get_reference_mock_xml_string())

    # Mutate configuration tree to introduce a naming asymmetry fault
    ## Parse original layout and locate targeting file nodes
    tree = ET.parse(xml_path)
    root = tree.getroot()
    cfg_node = root.find(".//cell_definition[@name='stem']//phenotype/intracellular/cfg_filename")
    
    ## Alter string parameters to mismatch the BND prefix template tokens
    cfg_node.text = "./config/mismatched_network_stem.cfg"
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    # Map models correctly on disk to isolate naming structure checks
    maboss_map = {
        "boolean_network": {
            "bnd": models_dir / "boolean_network.bnd",
            "cfg": models_dir / "boolean_network.cfg"
        }
    }

    # Execute runtime exception validation assertions
    ## Check if validation catches asymmetrical naming boundaries across files
    with pytest.raises(ValueError, match="uses a different prefix than CFG filename"):
        stage_physiboss_project(
            xml_path=xml_path,
            maboss_models_map=maboss_map,
            physiboss_root=physiboss_root
        )


def test_stage_project_unmapped_model(mock_env_factory):
    """
    Verifies that an unmapped model reference triggers a ValueError during parsing validations.

    :param mock_env_factory: Reusable mock environment tracking generator wrapper.
    :type mock_env_factory: Callable
    """
    # Initialize workspace using multi-model definitions
    xml_path, physiboss_root, models_dir = mock_env_factory(get_multi_model_mock_xml_string())

    # Construct an incomplete translation mapping dictionary missing the immune activation entries
    incomplete_maboss_map = {
        "cell_fate": {
            "bnd": models_dir / "cell_fate.bnd",
            "cfg": models_dir / "cell_fate.cfg"
        }
    }

    # Execute orchestrator pipeline mapping error validations
    ## Check structural safety nets for missing tracking reference targets
    with pytest.raises(ValueError, match="references MaBoSS model prefix.*but this model was not found in your source map"):
        stage_physiboss_project(
            xml_path=xml_path,
            maboss_models_map=incomplete_maboss_map,
            physiboss_root=physiboss_root
        )


def test_stage_project_missing_tags(mock_env_factory):
    """
    Verifies that missing structural tags inside intracellular definition nodes raise a ValueError.

    :param mock_env_factory: Reusable mock environment tracking generator wrapper.
    :type mock_env_factory: Callable
    """
    # Load core configuration metrics and assets
    xml_path, physiboss_root, models_dir = mock_env_factory(get_reference_mock_xml_string())

    # Remove mandatory tags from the structural XML setup configuration
    ## Parse original document layout and track root references
    tree = ET.parse(xml_path)
    root = tree.getroot()
    intracellular_block = root.find(".//cell_definition[@name='stem']//phenotype/intracellular")
    
    ## Locate and remove the network architecture node completely
    bnd_tag = intracellular_block.find("bnd_filename")
    intracellular_block.remove(bnd_tag)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    maboss_map = {
        "boolean_network": {
            "bnd": models_dir / "boolean_network.bnd",
            "cfg": models_dir / "boolean_network.cfg"
        }
    }

    # Execute runtime missing tag structural checks
    ## Validate that omitting mandatory elements is caught by internal safety nets
    with pytest.raises(ValueError, match="is missing the <bnd_filename> tag"):
        stage_physiboss_project(
            xml_path=xml_path,
            maboss_models_map=maboss_map,
            physiboss_root=physiboss_root
        )


def test_stage_project_missing_external_csv(mock_env_factory):
    """
    Verifies that enabling external tracking sheets without placing them on disk triggers a FileNotFoundError.

    :param mock_env_factory: Reusable mock environment tracking generator wrapper.
    :type mock_env_factory: Callable
    """
    # Build complete baseline directory parameters environment
    xml_path, physiboss_root, models_dir = mock_env_factory(get_reference_mock_xml_string())

    # Delete mandatory spatial coordinate sheet tracking asset from storage directory
    coord_sheet_path = xml_path.parent / "cells.csv"
    if coord_sheet_path.exists():
        coord_sheet_path.unlink()

    maboss_map = {
        "boolean_network": {
            "bnd": models_dir / "boolean_network.bnd",
            "cfg": models_dir / "boolean_network.cfg"
        }
    }

    # Execute runtime configuration data completeness checks
    ## Verify that missing coordinates data parameters halt project staging
    with pytest.raises(FileNotFoundError, match="requires 'cells.csv', but it does not exist in your source directory"):
        stage_physiboss_project(
            xml_path=xml_path,
            maboss_models_map=maboss_map,
            physiboss_root=physiboss_root
        )