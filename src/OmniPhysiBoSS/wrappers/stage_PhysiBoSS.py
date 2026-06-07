"""
OmniPhysiBoSS/wrappers/configure_PhysiBoSS.py
---
This refactored script acts as a clean orchestration interface. It coordinates verification, transformation, and storage deployment steps using modular components imported from _utils.
"""

from pathlib import Path
from typing import Dict

# Internal private structural dependencies
from OmniPhysiBoSS.wrappers._utils.verify_xml import verify_xml_dependencies
from OmniPhysiBoSS.wrappers._utils.patch_xml import patch_xml_dependencies
from OmniPhysiBoSS.wrappers._utils.stage_xml import execute_file_staging

# Pipeline orchestration block
## Main interface to execute validation pipelines and migrate files to execution environments
def stage_physiboss_project(
    xml_path: Path, 
    maboss_models_map: Dict[str, Dict[str, Path]], 
    physiboss_root: Path = Path(__file__).resolve().parent.parent.parent.parent / 'external/PhysiBoSS'
) -> str:
    """
    Validates user configurations and stages the verified file matrix inside the operational C++ engine layout.

    :param xml_path: Direct path to the input simulation setup XML file.
    :type xml_path: Path
    :param maboss_models_map: Nested map containing model prefixes linked to paired asset paths.
    :type maboss_models_map: Dict[str, Dict[str, Path]]
    :param physiboss_root: Path to the root directory of the cloned PhysiBoSS engine.
    :type physiboss_root: Path
    :return: Allocated filename string of the staged project configuration XML.
    :rtype: str
    """
    print("[STAGE 1/3] Initiating multi-scale structure verification routines...")
    xml_path = Path(xml_path)
    physiboss_root = Path(physiboss_root)
    
    # Establish project directory naming metrics safely avoiding type coercion faults
    runtime_project_dir = Path("OmniPhysiBoSS_projects") / xml_path.stem
    target_config_dir = physiboss_root / runtime_project_dir

    # Execute functional validation check profiles
    ## Verify physical file layout integrity
    if not xml_path.exists():
        raise FileNotFoundError(f"Primary project layout XML missing at location: {xml_path}")
        
    ## Execute pure structural dependency error inspection
    verify_xml_dependencies(xml_path, maboss_models_map)
    
    # Execute structural text remapping operations
    ## Remap target folders and Boolean file vectors inside an in-memory tree instance
    print("\n[STAGE 2/3] Executing in-memory XML structural modification routines...")
    patched_xml_tree = patch_xml_dependencies(xml_path, maboss_models_map, runtime_project_dir)
    print(" -> All internal cell definitions and intracellular reference paths mutated successfully.")

    # Execute file migration and serialization routines
    ## Delegate workspace cleanup, file building, and asset copies to the staging sub-module
    print("\n[STAGE 3/3] Deploying project asset configurations onto system storage volumes...")
    staged_xml_name = execute_file_staging(
        xml_path=xml_path,
        target_config_dir=target_config_dir,
        physiboss_root=physiboss_root,
        patched_xml_tree=patched_xml_tree,
        maboss_models_map=maboss_models_map
    )

    print("\n[PIPELINE CONFIGURATION CONFIGURATION MATCHED] All assets staged successfully.")
    return staged_xml_name