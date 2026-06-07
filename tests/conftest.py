import pytest
from pathlib import Path
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

# Global test environment configuration configurations
## Shared factory fixture providing isolated temporary directory trees
@pytest.fixture
def mock_env_factory(tmp_path: Path):
    """
    Factory fixture providing localized structural directory setups for isolation across all wrapper tests.

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
        
        user_source_dir.mkdir(parents=True, exist_ok=True)
        physiboss_root.mkdir(parents=True, exist_ok=True)
        models_dir.mkdir(parents=True, exist_ok=True)

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