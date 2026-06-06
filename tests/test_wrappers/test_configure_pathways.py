import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from OmniPhysiBoSS.wrappers.configure_PhysiBoSS import stage_physiboss_project
from tests.mock_data import (
    get_reference_mock_xml_string,
    get_multi_model_mock_xml_string,
    get_reference_cells_csv_string,
    get_reference_rules_csv_string,
    get_maboss_bnd_mock_string,
    get_maboss_cfg_mock_string,
    get_immune_activation_bnd_mock_string,
    get_immune_activation_cfg_mock_string
)

# Test environment preparation and success path validations
## Setup reusable temporary directory structure fixtures
@pytest.fixture
def mock_env_factory(tmp_path: Path):
    """
    Factory fixture providing localized structural directory setups for isolation.

    :param tmp_path: Built-in pytest path generator for a clean workspace.
    :type tmp_path: Path
    :return: A callable generator returning paths to user sources and engine roots.
    :rtype: Callable
    """
    def _create_env(xml_content: str, complete_assets: bool = True):
        ### Define internal storage layouts inside the mock environment
        user_source_dir = tmp_path / "user_data"
        physiboss_root = tmp_path / "engine_root"
        models_dir = tmp_path / "boolean_models"
        
        user_source_dir.mkdir(parents=True)
        physiboss_root.mkdir(parents=True)
        models_dir.mkdir(parents=True)

        ### Deploy core configuration xml file onto system volume
        xml_path = user_source_dir / "project_settings.xml"
        xml_path.write_text(xml_content, encoding="utf-8")

        if complete_assets:
            #### Deploy companion baseline spatial coordinate vectors and transition sheets
            cells_csv = user_source_dir / "cells.csv"
            cells_csv.write_text(get_reference_cells_csv_string(), encoding="utf-8")
            
            rules_csv = user_source_dir / "cell_rules.csv"
            rules_csv.write_text(get_reference_rules_csv_string(), encoding="utf-8")

            #### Build out disk assets for paired boolean networks
            (models_dir / "cell_fate.bnd").write_text(get_maboss_bnd_mock_string(), encoding="utf-8")
            (models_dir / "cell_fate.cfg").write_text(get_maboss_cfg_mock_string(), encoding="utf-8")
            (models_dir / "immune_activation.bnd").write_text(get_immune_activation_bnd_mock_string(), encoding="utf-8")
            (models_dir / "immune_activation.cfg").write_text(get_immune_activation_cfg_mock_string(), encoding="utf-8")
            
            ##### Legacy fallback files mapping for single-model test backwards compliance
            (models_dir / "boolean_network.bnd").write_text(get_maboss_bnd_mock_string(), encoding="utf-8")
            (models_dir / "boolean_network.cfg").write_text(get_maboss_cfg_mock_string(), encoding="utf-8")

        return xml_path, physiboss_root, models_dir

    return _create_env


## Execute regression assertions on positive control pathways
def test_stage_project_single_model_success(mock_env_factory):
    """
    Validates that a standard single-model system configuration coordinates all file transfers and remappings.

    :param mock_env_factory: Local custom workspace tracking environment generator.
    :type mock_env_factory: Callable
    """
    # Initialize workspace metrics using factory helpers
    xml_path, physiboss_root, models_dir = mock_env_factory(get_reference_mock_xml_string())

    # Map model prefix tokens to disk locations
    maboss_map = {
        "boolean_network": {
            "bnd": models_dir / "boolean_network.bnd",
            "cfg": models_dir / "boolean_network.cfg"
        }
    }

    # Execute orchestrator pipeline execution layer
    staged_xml_name = stage_physiboss_project(
        xml_path=xml_path,
        maboss_models_map=maboss_map,
        physiboss_root=physiboss_root
    )

    # Asset preservation assertions
    ## Check file naming normalization attributes
    assert staged_xml_name == "project_settings.xml"

    ## Verify physical project runtime directory allocation on hardware storage
    expected_proj_dir = physiboss_root / "OmniPhysiBoSS_projects" / "project_settings"
    assert expected_proj_dir.exists()
    assert (expected_proj_dir / "project_settings.xml").exists()
    assert (expected_proj_dir / "cells.csv").exists()
    assert (expected_proj_dir / "boolean_network.bnd").exists()

    ## Parse output data layout to verify that paths were rewritten inside runtime execution bounds
    parsed_tree = ET.parse(expected_proj_dir / "project_settings.xml")
    parsed_root = parsed_tree.getroot()
    bnd_text = parsed_root.find(".//cell_definition[@name='stem']//phenotype/intracellular/bnd_filename").text
    assert bnd_text == "./OmniPhysiBoSS_projects/project_settings/boolean_network.bnd"


def test_stage_project_multi_model_success(mock_env_factory):
    """
    Validates that complex setups deploying distinct models across heterogeneous cell populations compile without errors.

    :param mock_env_factory: Local custom workspace tracking environment generator.
    :type mock_env_factory: Callable
    """
    # Initialize system variables with secondary template structure matrices
    xml_path, physiboss_root, models_dir = mock_env_factory(get_multi_model_mock_xml_string())

    maboss_map = {
        "cell_fate": {
            "bnd": models_dir / "cell_fate.bnd",
            "cfg": models_dir / "cell_fate.cfg"
        },
        "immune_activation": {
            "bnd": models_dir / "immune_activation.bnd",
            "cfg": models_dir / "immune_activation.cfg"
        }
    }

    # Execute runtime orchestration routines
    staged_xml_name = stage_physiboss_project(
        xml_path=xml_path,
        maboss_models_map=maboss_map,
        physiboss_root=physiboss_root
    )

    # Perform structural consistency metrics regression
    expected_proj_dir = physiboss_root / "OmniPhysiBoSS_projects" / "project_settings"
    assert (expected_proj_dir / "cell_fate.bnd").exists()
    assert (expected_proj_dir / "immune_activation.cfg").exists()

    ## Verify independent target text mutation rules map correctly
    parsed_root = ET.parse(expected_proj_dir / "project_settings.xml").getroot()
    immune_bnd = parsed_root.find(".//cell_definition[@name='other']//phenotype/intracellular/bnd_filename").text
    assert immune_bnd == "./OmniPhysiBoSS_projects/project_settings/immune_activation.bnd"