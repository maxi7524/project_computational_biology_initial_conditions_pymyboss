"""
OmniPhysiBoSS/wrappers/_utils/stage_xml.py
---
This sub-module encapsulates all physical disk operations, directory management, and asset transfers, separating IO code from orchestration logic.
"""

import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

# ----------------------------------
# Main wrapper  
# ----------------------------------

# Orchestrated entrypoint configuration routing interface
## Main pipeline entrypoint for physical file assembly
def execute_file_staging(
    xml_path: Path,
    target_config_dir: Path,
    physiboss_root: Path,
    patched_xml_tree: ET.ElementTree,
    maboss_models_map: Dict[str, Dict[str, Path]]
) -> str:
    """
    Coordinates atomic helpers to clean workspaces, write configurations, and copy assets.

    :param xml_path: Path to the original source XML document configuration.
    :type xml_path: Path
    :param target_config_dir: Destination path inside the C++ engine directory tree.
    :type target_config_dir: Path
    :param physiboss_root: Root path of the PhysiBoSS engine.
    :type physiboss_root: Path
    :param patched_xml_tree: Mutated configuration XML state tree.
    :type patched_xml_tree: ET.ElementTree
    :param maboss_models_map: Map linking model prefix stems to paired asset files.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :return: Filename string of the deployed configuration file.
    :rtype: str
    """
    # Prepare workspace environments
    _prepare_target_directory(target_config_dir)

    # Save mutated configuration XML matrix
    staged_xml_name = xml_path.name
    _write_patched_xml(patched_xml_tree, target_config_dir / staged_xml_name)
    print(f" -> Deployed simulation architecture definition: {staged_xml_name}")

    # Transfer external cell positions and behavior sheets
    _stage_spatial_assets(patched_xml_tree, xml_path.parent, target_config_dir, physiboss_root)

    # Transfer mapped Boolean network elements
    _stage_maboss_assets(maboss_models_map, target_config_dir, physiboss_root)

    return staged_xml_name


# ----------------------------------
# Helpers 
# ----------------------------------

# File staging utility sub-layer
## Atomic helper to refresh target project workspace allocations
def _prepare_target_directory(target_config_dir: Path) -> None:
    """
    Cleans historical data contaminations and prepares a fresh target directory.

    :param target_config_dir: Path to the target project directory inside the engine.
    :type target_config_dir: Path
    """
    # Clear directory tree if it exists on disk
    if target_config_dir.exists():
        shutil.rmtree(target_config_dir)
    os.makedirs(target_config_dir, exist_ok=True)


## Atomic helper to serialize modified tree states
def _write_patched_xml(patched_xml_tree: ET.ElementTree, target_path: Path) -> None:
    """
    Writes the patched in-memory XML tree configuration file to disk.

    :param patched_xml_tree: Mutated XML configuration layout state tree.
    :type patched_xml_tree: ET.ElementTree
    :param target_path: Full destination path for the staged XML configuration file.
    :type target_path: Path
    """
    patched_xml_tree.write(target_path, encoding="utf-8", xml_declaration=True)


## Atomic helper to transfer spatial layout configurations
def _stage_spatial_assets(
    patched_xml_tree: ET.ElementTree, 
    source_base_dir: Path, 
    target_config_dir: Path, 
    physiboss_root: Path
) -> None:
    """
    Scans the configuration tree and copies active position sheets and rule matrices to the workspace.

    :param patched_xml_tree: The in-memory mutated configuration XML state.
    :type patched_xml_tree: ET.ElementTree
    :param source_base_dir: Directory where the user's source files are stored.
    :type source_base_dir: Path
    :param target_config_dir: Destination path inside the C++ engine directory tree.
    :type target_config_dir: Path
    :param physiboss_root: Root path of the PhysiBoSS engine.
    :type physiboss_root: Path
    """
    root = patched_xml_tree.getroot()

    # Stage active initial condition cells data matrices
    initial_conditions = root.find(".//initial_conditions/cell_positions")
    if initial_conditions is not None and initial_conditions.attrib.get("enabled") == "true":
        file_node = initial_conditions.find("filename")
        if file_node is not None and file_node.text:
            base_name = Path(file_node.text.strip()).name
            src_file = source_base_dir / base_name
            if src_file.exists():
                shutil.copy(src_file, target_config_dir / base_name)
                print(f" -> Staged external initialization asset: {base_name} -> {target_config_dir.relative_to(physiboss_root)}")

    # Stage active cell behavioral rule descriptions
    cell_rules = root.find(".//cell_rules/rulesets")
    if cell_rules is not None:
        for ruleset in cell_rules.findall("ruleset"):
            if ruleset.attrib.get("enabled") == "true":
                file_node = ruleset.find("filename")
                if file_node is not None and file_node.text:
                    base_name = Path(file_node.text.strip()).name
                    src_file = source_base_dir / base_name
                    if src_file.exists():
                        shutil.copy(src_file, target_config_dir / base_name)
                        print(f" -> Staged external behavior asset: {base_name} -> {target_config_dir.relative_to(physiboss_root)}")


## Atomic helper to transfer boolean logic dependencies
def _stage_maboss_assets(
    maboss_models_map: Dict[str, Dict[str, Path]], 
    target_config_dir: Path, 
    physiboss_root: Path
) -> None:
    """
    Copies network and configuration files from the source map to the project directory.

    :param maboss_models_map: Map linking model prefix stems to paired asset files.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :param target_config_dir: Destination path inside the C++ engine directory tree.
    :type target_config_dir: Path
    :param physiboss_root: Root path of the PhysiBoSS engine.
    :type physiboss_root: Path
    """
    for prefix, paths in maboss_models_map.items():
        dest_bnd = target_config_dir / paths["bnd"].name
        dest_cfg = target_config_dir / paths["cfg"].name
        
        shutil.copy(paths["bnd"], dest_bnd)
        shutil.copy(paths["cfg"], dest_cfg)
        print(f" -> Staged Boolean component pair: [{prefix}] -> {target_config_dir.relative_to(physiboss_root)}")


