import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any


# ----------------------------------
# Main 
# ----------------------------------

# Pipeline orchestration block
## Main interface to execute validation pipelines and migrate files to execution environments
def stage_physiboss_project(
    xml_path: Path, 
    maboss_models_map: Dict[str, Dict[str, Path]], 
    # ../wrappers (1) -> ../OmniPhysiBoSS (2) -> ../src (3) -> ../repo_dir (4) 
    physiboss_root: Path = Path(__file__).resolve().parent.parent.parent.parent / 'external/PhysiBoSS'
) -> str:
    """
    Validates user configurations and stages the verified file matrix inside the operational C++ engine layout.

    :param user_xml_path: Direct path to the input simulation setup XML file.
    :type user_xml_path: Path
    :param maboss_models_map: Nested map containing model prefixes linked to paired asset paths.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :param physiboss_root: Path to the root directory of the cloned PhysiBoSS engine.
    :type physiboss_root: Path
    :return: Allocated filename string of the staged project configuration XML.
    :rtype: str
    """
    print("[STEP 1/3] Initiating configuration profile validation pipelines...")
    xml_path = Path(xml_path)
    physiboss_root = Path(physiboss_root)
    
    # Define isolated path tokens safely avoiding string division errors
    #TODO - CONFIG PARAMETER - physiboss project folder
    ## Construct explicit sub-paths for runtime data access
    runtime_project_dir = Path("OmniPhysiBoSS_projects") / xml_path.stem
    target_config_dir = physiboss_root / runtime_project_dir

    # Execute functional verification blocks
    ## Verify physical file layout integrity
    if not xml_path.exists():
        raise FileNotFoundError(f"Primary project layout XML missing at location: {xml_path}")
        
    ## Verify syntax binding rules inside structural files via strict sequential validation
    ## Execute pure structural error inspection
    _verify_xml_dependencies(xml_path, maboss_models_map)
    
    ## Perform path mutations isolated within memory trees
    #TODO - CONFIG PARAMETER - physiboss project folder
    patched_xml_tree = _patch_xml_dependencies(xml_path, maboss_models_map, runtime_project_dir)
    print(" -> All cell definitions and intracellular reference bounds successfully verified.")

    # Environment isolation sequence
    ## Refresh target directories to prevent historical file contamination
    if target_config_dir.exists():
        shutil.rmtree(target_config_dir)
    os.makedirs(target_config_dir, exist_ok=True)

    # File migration phase
    ## Save modified in-memory XML matrix structure to destination directory
    ## Stage simulation setup layout XML
    staged_xml_name = xml_path.name
    patched_xml_tree.write(target_config_dir / staged_xml_name, encoding="utf-8", xml_declaration=True)
    print(f" -> Deployed simulation architecture definition: {staged_xml_name}")

    # File migration phase: External initialization assets
    ## Copy detected tracking data formats (cells.csv / cell_rules.csv) directly to the target project workspace
    source_base_dir = xml_path.parent
    
    ## Stage spatial layout definitions if activated in configuration
    initial_conditions = patched_xml_tree.getroot().find(".//initial_conditions/cell_positions")
    if initial_conditions is not None and initial_conditions.attrib.get("enabled") == "true":
        file_node = initial_conditions.find("filename")
        if file_node is not None and file_node.text:
            base_name = Path(file_node.text.strip()).name
            src_file = source_base_dir / base_name
            if src_file.exists():
                shutil.copy(src_file, target_config_dir / base_name)
                print(f" -> Staged external initialization asset: {base_name} -> {target_config_dir.relative_to(physiboss_root)}")

    ## Stage custom behavioral rulesets if activated in configuration
    cell_rules = patched_xml_tree.getroot().find(".//cell_rules/rulesets")
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

    ## Stage boolean asset dependencies into the active runtime workspace
    for prefix, paths in maboss_models_map.items():
        ### Construct destination file boundaries matching expected structural inputs
        dest_bnd = target_config_dir / paths["bnd"].name
        dest_cfg = target_config_dir / paths["cfg"].name
        
        ### Perform physical storage copies
        shutil.copy(paths["bnd"], dest_bnd)
        shutil.copy(paths["cfg"], dest_cfg)
        print(f" -> Staged Boolean component pair: [{prefix}] -> {target_config_dir.relative_to(physiboss_root)}")

    print("[STEP 1/3] Validation completed. System workspace fully staged.")
    return staged_xml_name


# ----------------------------------
# Helpers 
# ----------------------------------

# Model discovery utilities
## Helper function to scan directory and pair boolean model components by prefix
def find_maboss_models(models_dir: Path) -> Dict[str, Dict[str, Path]]:
    """
    Scans a directory for .bnd and .cfg files, pairing them by their common prefix.

    :param models_dir: Path to the directory containing MaBoSS model files.
    :type models_dir: Path
    :return: A dictionary where keys are model prefixes and values are dicts with 'bnd' and 'cfg' paths.
    :rtype: Dict[str, Dict[str, Path]]
    """
    # Initialize storage for found components
    ## Temporary tracking containers
    models_dir = Path(models_dir)
    discovered_pairs: Dict[str, Dict[str, Path]] = {}

    # Iterate over directory contents to extract structural targets
    ## Match file extensions independently
    for file_path in models_dir.iterdir():
        if file_path.is_file():
            ### Extract prefix grouping token and extension type
            prefix = file_path.stem
            suffix = file_path.suffix.lower()

            if suffix in [".bnd", ".cfg"]:
                #### Initialize sub-dictionary structure for new prefixes
                if prefix not in discovered_pairs:
                    discovered_pairs[prefix] = {}
                
                #### Assign specific path reference based on configuration syntax
                key_type = suffix[1:]  # Extracts 'bnd' or 'cfg'
                discovered_pairs[prefix][key_type] = file_path

    # Filter out incomplete models lacking paired components
    ## Validate that each prefix group contains both network structure and configurations
    final_models_map: Dict[str, Dict[str, Path]] = {}
    for prefix, components in discovered_pairs.items():
        if "bnd" in components and "cfg" in components:
            ## Retain fully qualified model pairs
            final_models_map[prefix] = components
        else:
            ### Broadcast diagnostic warnings for isolated structural targets
            print(f"[WARNING] Incomplete model pair detected for prefix '{prefix}'. Missing .bnd or .cfg file.")

    return final_models_map


# XML configuration analysis and validation layer
## Helper function to strictly cross-verify XML cell definitions against active models map
def _verify_xml_dependencies(xml_path: Path, maboss_models_map: Dict[str, Dict[str, Path]]) -> None:
    """
    Parses the target configuration XML and performs strict checks to ensure every 
    referenced MaBoSS model by any cell definition is fully present in the models map and on disk.
    Additionally validates that any external CSV/TSV cell layout files declared in user parameters exist.

    :param xml_path: Path to the simulation setup XML file.
    :type xml_path: Path
    :param maboss_models_map: Paired model structure dictionary generated by discovery utilities.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :raises FileNotFoundError: If a referenced file is missing from the disk.
    :raises ValueError: If a cell references a model that was not provided in the mapping context.
    """
    # Parse document structure tree
    ## Build element root references
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Flag to track if at least one intracellular model was found
    intracellular_found = False

    # Scan agent configuration definitions
    ## Inspect intracellular parameters matching the maboss type tag
    for cell_def in root.findall(".//cell_definition"):
        cell_name = cell_def.attrib.get("name", "Unknown_Cell")
        intracellular = cell_def.find(".//phenotype/intracellular")
        
        if intracellular is not None and intracellular.attrib.get("type") == "maboss":
            intracellular_found = True
            
            ### Retrieve declared file paths from text nodes
            bnd_node = intracellular.find("bnd_filename")
            cfg_node = intracellular.find("cfg_filename")
            
            ### CRITICAL ERROR: XML tags missing entirely inside the intracellular definition
            if bnd_node is None or bnd_node.text is None:
                raise ValueError(f"Validation Error: Cell '{cell_name}' has a MaBoSS intracellular block but is missing the <bnd_filename> tag.")
            if cfg_node is None or cfg_node.text is None:
                raise ValueError(f"Validation Error: Cell '{cell_name}' has a MaBoSS intracellular block but is missing the <cfg_filename> tag.")
            
            ### Isolate exact filenames from the XML text contents
            bnd_filename = Path(bnd_node.text.strip()).name
            cfg_filename = Path(cfg_node.text.strip()).name
            
            ### Isolate prefixes to identify model identity
            bnd_prefix = Path(bnd_filename).stem
            cfg_prefix = Path(cfg_filename).stem
            
            ### CRITICAL ERROR: Cell references mismatched network and configuration architectures
            if bnd_prefix != cfg_prefix:
                raise ValueError(
                    f"Validation Error in Cell '{cell_name}': "
                    f"BND filename '{bnd_filename}' uses a different prefix than CFG filename '{cfg_filename}'."
                )
            
            ### CRITICAL ERROR: The model prefix declared in the cell configuration does not exist in our system map
            if bnd_prefix not in maboss_models_map:
                raise ValueError(
                    f"Validation Error: Cell '{cell_name}' references MaBoSS model prefix '{bnd_prefix}' "
                    f"({bnd_filename}/{cfg_filename}), but this model was not found in your source directory or map."
                )
            
            ### CRITICAL ERROR: The model exists in the dictionary, but physical files were deleted/missing on disk
            target_paths = maboss_models_map[bnd_prefix]
            if not target_paths["bnd"].exists():
                raise FileNotFoundError(
                    f"Validation Error: Cell '{cell_name}' references '{bnd_filename}', "
                    f"but the file does not physically exist at: {target_paths['bnd']}"
                )
            if not target_paths["cfg"].exists():
                raise FileNotFoundError(
                    f"Validation Error: Cell '{cell_name}' references '{cfg_filename}', "
                    f"but the file does not physically exist at: {target_paths['cfg']}"
                )
                
            print(f" -> Cell '{cell_name}' structural binding verified with MaBoSS model: '{bnd_prefix}'")

    # CRITICAL ERROR: The XML file contains no active multicellular Boolean logic profiles
    if not intracellular_found:
        raise ValueError(f"Validation Error: The configuration file {xml_path} contains no cell definitions with an intracellular MaBoSS engine.")

    # Validate external cellular initialization files
    ## Scan structural spatial containers for custom initialization matrices
    initial_conditions = root.find(".//initial_conditions/cell_positions")
    if initial_conditions is not None and initial_conditions.attrib.get("enabled") == "true":
        ### Extract target nodes from the condition block
        folder_node = initial_conditions.find("folder")
        file_node = initial_conditions.find("filename")
        
        if folder_node is not None and file_node is not None:
            #### Isolate filename from paths and verify physical existence on disk
            base_filename = Path(file_node.text.strip()).name
            source_base_dir = xml_path.parent
            resolved_file_path = source_base_dir / base_filename

            if not resolved_file_path.exists():
                ##### Abort pipeline sequence if initialization positions are missing
                raise FileNotFoundError(
                    f"Validation Error: <initial_conditions> requires '{base_filename}', "
                    f"but it does not exist in your source directory: {source_base_dir}"
                )
            print(f" -> External cell tracking file verified locally: '{base_filename}'")

    ## Scan structural rule containers for custom behavioral rulesets
    cell_rules = root.find(".//cell_rules/rulesets")
    if cell_rules is not None:
        ### Iterate over individual rule definitions mapped in the XML layout
        for ruleset in cell_rules.findall("ruleset"):
            if ruleset.attrib.get("enabled") == "true":
                folder_node = ruleset.find("folder")
                file_node = ruleset.find("filename")
                
                if folder_node is not None and file_node is not None:
                    #### Isolate filename descriptor matching csv/tsv frameworks
                    base_filename = Path(file_node.text.strip()).name
                    source_base_dir = xml_path.parent
                    resolved_file_path = source_base_dir / base_filename

                    if not resolved_file_path.exists():
                        ##### Abort pipeline sequence if behavior files are missing
                        raise FileNotFoundError(
                            f"Validation Error: <ruleset> requires '{base_filename}', "
                            f"but it does not exist in your source directory: {source_base_dir}"
                        )
                    print(f" -> External cell behavioral ruleset verified locally: '{base_filename}'")


# XML path adaptation layer
## Helper function to isolate node text alteration routines
def _patch_xml_dependencies(
    xml_path: Path, 
    maboss_models_map: Dict[str, Dict[str, Path]], 
    runtime_maboss_dir_name: Path
) -> ET.ElementTree:
    """
    Modifies internal XML configuration text nodes to point to runtime execution path locations.

    :param xml_path: Path to the target simulation XML setup layout file.
    :type xml_path: Path
    :param maboss_models_map: Structured map linking model prefixes to asset files.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :param runtime_maboss_dir_name: Relative engine subfolder path string.
    :type runtime_maboss_dir_name: Path
    :return: Mutated XML object tree architecture ready for disk serialization.
    :rtype: ET.ElementTree
    """
    # Parse existing configuration structural tree
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate structural components to adjust layout tokens
    for cell_def in root.findall(".//cell_definition"):
        intracellular = cell_def.find(".//phenotype/intracellular")
        
        if intracellular is not None and intracellular.attrib.get("type") == "maboss":
            ## Isolate tag entries needing string updates
            bnd_node = intracellular.find("bnd_filename")
            cfg_node = intracellular.find("cfg_filename")
            
            if bnd_node is not None and cfg_node is not None:
                ### Extract core names to drop structural discrepancies
                bnd_filename = Path(bnd_node.text.strip()).name
                cfg_filename = Path(cfg_node.text.strip()).name
                
                ### Overwrite matching targets with path schemas built relative to C++ engine root
                bnd_node.text = f"./{runtime_maboss_dir_name}/{bnd_filename}"
                cfg_node.text = f"./{runtime_maboss_dir_name}/{cfg_filename}"


    # Update spatial initialization path dependencies
    ## Remap folder pointers for explicit cell positioning frameworks
    initial_conditions = root.find(".//initial_conditions/cell_positions")
    if initial_conditions is not None and initial_conditions.attrib.get("enabled") == "true":
        folder_node = initial_conditions.find("folder")
        if folder_node is not None:
            ### Enforce global execution root relativity targeting the isolated project workspace
            folder_node.text = f"./{runtime_maboss_dir_name}"
            print(f" -> Patched cell_positions runtime folder to: {folder_node.text}")

    ## Remap folder pointers for explicit behavioral cellular rulesets
    cell_rules = root.find(".//cell_rules/rulesets")
    if cell_rules is not None:
        ### Process every enabled ruleset sub-node layout configuration
        for ruleset in cell_rules.findall("ruleset"):
            if ruleset.attrib.get("enabled") == "true":
                folder_node = ruleset.find("folder")
                if folder_node is not None:
                    #### Overwrite hardcoded structural directories with the managed runtime destination
                    folder_node.text = f"./{runtime_maboss_dir_name}"
                    print(f" -> Patched ruleset runtime folder to: {folder_node.text}")

    return tree