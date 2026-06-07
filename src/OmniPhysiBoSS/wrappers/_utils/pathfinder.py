"""
OmniPhysiBoSS/wrappers/_utils/pathfinder.py
---
This utility submodule isolates file system scanning, grouping logic, and simulation data migration functions.
"""

import os
import shutil
from pathlib import Path
from typing import Dict

# File discovery and output asset management utilities
## Scan directory and pair boolean model components by prefix
def find_maboss_models(models_dir: Path) -> Dict[str, Dict[str, Path]]:
    """
    Scans a directory for .bnd and .cfg files, pairing them by their common prefix.

    :param models_dir: Path to the directory containing MaBoSS model files.
    :type models_dir: Path
    :return: A dictionary where keys are model prefixes and values are dicts with 'bnd' and 'cfg' paths.
    :rtype: Dict[str, Dict[str, Path]]
    """
    # Directory initialization
    ## Ensure directory format resolution
    models_dir = Path(models_dir)
    discovered_pairs: Dict[str, Dict[str, Path]] = {}

    # Processing loop
    ## Iterate over directory contents to extract structural targets
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
                key_type = suffix[1:]
                discovered_pairs[prefix][key_type] = file_path

    # Model resolution filtering
    ## Filter out incomplete models lacking paired components
    final_models_map: Dict[str, Dict[str, Path]] = {}
    for prefix, components in discovered_pairs.items():
        if "bnd" in components and "cfg" in components:
            ## Retain fully qualified model pairs
            final_models_map[prefix] = components
        else:
            ### Broadcast diagnostic warnings for isolated structural targets
            print(f"[WARNING] Incomplete model pair detected for prefix '{prefix}'. Missing .bnd or .cfg file.")

    return final_models_map


## Relocate completed multi-scale simulation datasets
def migrate_simulation_outputs(
    destination_dir: Path,
    output_src: Path = Path('external/PhysiBoSS/output'), 
) -> None:
    """
    Copies all simulation output data matrix frames from the engine directory to a targeted project folder.

    :param output_src: Path to the internal engine output generation directory.
    :type output_src: Path
    :param destination_dir: Path to the target user project directory where output data is stored.
    :type destination_dir: Path
    :raises FileNotFoundError: If the source output directory cannot be found.
    """
    # Directory verification
    ## Convert arguments to concrete path definitions
    output_src = Path(output_src)
    destination_dir = Path(destination_dir)

    ## Validate source file container existence before executing transfer loops
    if not output_src.exists():
        raise FileNotFoundError(f"Source output generation directory does not exist at: {output_src}")

    ## Allocate target directory infrastructure paths on disk
    os.makedirs(destination_dir, exist_ok=True)

    # Asset transfer execution
    ## Scan source directory and execute batch transfers
    for item in output_src.iterdir():
        if item.is_file():
            ### Execute clean stream copies across partitions
            shutil.copy(item, destination_dir / item.name)
            print(f" -> Migrated simulation trajectory asset: {item.name}")