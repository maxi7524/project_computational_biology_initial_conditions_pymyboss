"""
OmniPhysiBoSS/wrappers/_utils/patch_xml.py
---
This sub-module handles in-memory alterations of file paths inside the configuration tree. The logic is decoupled into three independent atomic helpers coordinated by a single public entry point function.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

# ----------------------------------
# Main wrapper  
# ----------------------------------

# Orchestration mutation interface
## Global structural transformation routine
def patch_xml_dependencies(
    xml_path: Path, 
    maboss_models_map: Dict[str, Dict[str, Path]], 
    runtime_maboss_dir_name: Path
) -> ET.ElementTree:
    """
    Parses configuration files, applies sequential structural modifications, and returns the modified XML tree.

    :param xml_path: Path to the target simulation XML setup layout file.
    :type xml_path: Path
    :param maboss_models_map: Structured map linking model prefixes to asset files.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :param runtime_maboss_dir_name: Relative engine subfolder project workspace path.
    :type runtime_maboss_dir_name: Path
    :return: Mutated XML object tree architecture ready for disk serialization.
    :rtype: ET.ElementTree
    """
    # Parse target simulation XML layout configuration
    ## Extract tree reference pointers
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Execute atomic patch routines sequentially
    ## Update boolean logic paths
    _patch_maboss_paths(root, runtime_maboss_dir_name)
    
    ## Update initialization positions
    _patch_initial_conditions(root, runtime_maboss_dir_name)
    
    ## Update execution transition rulesets
    _patch_cell_rules(root, runtime_maboss_dir_name)

    ## Isolate simulation results output directories per project target
    _patch_output_folder(root, project_name=xml_path.stem)

    return tree

# ----------------------------------
# Helpers 
# ----------------------------------

# XML structural patch sub-layer
## Atomic helper to remap MaBoSS configuration entries
def _patch_maboss_paths(root: ET.Element, runtime_maboss_dir_name: Path) -> None:
    """
    Mutates BND and CFG text nodes inside cell definition intracellular configuration blocks.

    :param root: Root element of the parsed XML tree layout.
    :type root: ET.Element
    :param runtime_maboss_dir_name: Relative execution workspace folder destination.
    :type runtime_maboss_dir_name: Path
    """
    # Iterate through cell definitions to update network configurations
    ## Locate all matching cell definition blocks
    for cell_def in root.findall(".//cell_definition"):
        intracellular = cell_def.find(".//phenotype/intracellular")
        
        if intracellular is not None and intracellular.attrib.get("type") == "maboss":
            ### Extract and isolate file nodes
            bnd_node = intracellular.find("bnd_filename")
            cfg_node = intracellular.find("cfg_filename")
            
            if bnd_node is not None and cfg_node is not None:
                #### Extract core filenames and re-assign runtime values relative to engine root
                bnd_filename = Path(bnd_node.text.strip()).name
                cfg_filename = Path(cfg_node.text.strip()).name
                
                bnd_node.text = f"./{runtime_maboss_dir_name}/{bnd_filename}"
                cfg_node.text = f"./{runtime_maboss_dir_name}/{cfg_filename}"


## Atomic helper to adjust spatial layout folder references
def _patch_initial_conditions(root: ET.Element, runtime_maboss_dir_name: Path) -> None:
    """
    Mutates the folder configuration text node inside the cell positions initial conditions block.

    :param root: Root element of the parsed XML tree layout.
    :type root: ET.Element
    :param runtime_maboss_dir_name: Relative execution workspace folder destination.
    :type runtime_maboss_dir_name: Path
    """
    # Locate cell positioning block frameworks
    ## Inspect initial conditions configuration nodes
    initial_conditions = root.find(".//initial_conditions/cell_positions")
    if initial_conditions is not None and initial_conditions.attrib.get("enabled") == "true":
        folder_node = initial_conditions.find("folder")
        if folder_node is not None:
            ### Overwrite file location with targeted runtime destination directory
            folder_node.text = f"./{runtime_maboss_dir_name}"
            print(f" -> Patched cell_positions runtime folder to: {folder_node.text}")


## Atomic helper to alter behavioral rule references
def _patch_cell_rules(root: ET.Element, runtime_maboss_dir_name: Path) -> None:
    """
    Mutates folder configuration text nodes across all enabled behavioral cell rulesets.

    :param root: Root element of the parsed XML tree layout.
    :type root: ET.Element
    :param runtime_maboss_dir_name: Relative execution workspace folder destination.
    :type runtime_maboss_dir_name: Path
    """
    # Locate cell rules element container
    ## Inspect rulesets configuration options
    cell_rules = root.find(".//cell_rules/rulesets")
    if cell_rules is not None:
        ### Process every individual ruleset sub-node layout configuration
        for ruleset in cell_rules.findall("ruleset"):
            if ruleset.attrib.get("enabled") == "true":
                folder_node = ruleset.find("folder")
                if folder_node is not None:
                    #### Overwrite folder paths with the target project directory execution route
                    folder_node.text = f"./{runtime_maboss_dir_name}"
                    print(f" -> Patched ruleset runtime folder to: {folder_node.text}")


## Atomic helper to isolate project-specific simulation output paths
def _patch_output_folder(root: ET.Element, project_name: str) -> None:
    """
    Mutates the save folder configuration text node to isolate project simulation outputs.

    :param root: Root element of the parsed XML tree layout.
    :type root: ET.Element
    :param project_name: Core name stem of the active project layout configuration.
    :type project_name: str
    """
    # Locate filesystem storage saving configuration boundaries
    ## Inspect save layout node blocks
    save_node = root.find(".//save")
    if save_node is not None:
        folder_node = save_node.find("folder")
        if folder_node is not None and folder_node.text:
            ### Isolate original output directory prefix token
            base_output_dir = folder_node.text.strip()
            
            ### Enforce structured isolated sub-directory execution route
            folder_node.text = f"./{base_output_dir}/{project_name}"
            print(f" -> Patched data tracking output folder to: {folder_node.text}")