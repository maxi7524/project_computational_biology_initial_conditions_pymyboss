
# Wrappers Module: Multi-Scale Simulation Orchestrator

The `wrappers` module serves as the functional bridge between high-level Python pipeline operations and the low-level, compiled C++ multi-scale engine (`PhysiBoSS`). It decouples cellular personalization configuration from physical system execution by exposing a clean, two-step workflow: Staging/Validation and Execution/Monitoring. What is important here, we need to clone their repository from [github](https://github.com/PhysiBoSS/PhysiBoSS), as they do not provide official package as well as wrappers. Comprehensive instruction how to install everything is here (#TODO - odnośnik do dokumentacji z instalacja) 

---

## Architecture and Execution Pipeline

The execution life cycle of a spatiotemporal multicellular simulation model progresses through six sequential, isolated phases:


```

[ User Input Directories ]
│
▼

1. Validation (verify_xml.py)  ──► Checks XML tags, maps, disk locations, and prefixes.
│
▼
2. Transformation (patch_xml.py) ──► Mutates in-memory XML text nodes to match runtime paths.
│
▼
3. Staging (stage_xml.py)      ──► Cleans workspace, serializes XML, copies assets (.bnd, .cfg, .csv).
│
▼
4. Compilation (run_PhysiBoSS.py)─► Calls 'make clean && make' to ensure binary integrity.
│
▼
5. Monitoring (log_monitor.py) ──► Spawns process, streams metrics, strips verbose dumps.
│
▼
6. Migration (pathfinder.py)   ──► Pulls completed simulation frames into target data folders.

```

---

## Submodule Specifications

### 1. configure_PhysiBoSS.py
*   **Purpose:** Exposes the public `stage_physiboss_project` function.
*   **Mechanism:** Coordinates validation checks, in-memory tree manipulation, and directory staging. It processes all definitions inside the source project before writing anything to disk, preserving workspace isolation.

### 2. run_PhysiBoSS.py
*   **Purpose:** Exposes the public `run_physiboss_simulation` function.
*   **Mechanism:** Forces a clean compilation of the C++ codebase via a subprocess Makefile execution target. It spawns the native application runtime container (`subprocess.Popen`), pipes unbuffered outputs into a tracking file on disk, and routes live stdout streams through the telemetry filter.

### 3. _utils/ (Private Atomic Helpers)
*   `pathfinder.py`: Uses automated string stem evaluation to discover paired `.bnd`/`.cfg` Boolean definitions. Contains post-simulation utility routines to copy simulation trajectories out of the engine space.
*   `verify_xml.py`: Performs strict multi-stage cross-validation. Ensures file prefixes match, required tags (`<bnd_filename>`, `<cfg_filename>`) are explicitly declared, and external coordinates/rules exist locally.
*   `patch_xml.py`: Mutates text nodes within the XML tree layout, enforcing relative path parameters (`./OmniPhysiBoSS_projects/...`) matching the execution environment directory structure.
*   `log_monitor.py`: A stateful regex/substring scanner that filters out verbose print loops (such as individual cell coordinates creation tracks) to keep standard output logs human-readable and scannable.

---

## Operational Blueprint

The following execution script discovers local components, stages environment dependencies, builds the runtime framework, and monitors simulation steps:

```python
from pathlib import Path
from OmniPhysiBoSS.wrappers._utils.pathfinder import find_maboss_models
from OmniPhysiBoSS.wrappers.configure_PhysiBoSS import stage_physiboss_project
from OmniPhysiBoSS.wrappers.run_PhysiBoSS import run_physiboss_simulation

# Step 1: Initialize path mappings
source_xml = Path("data/models/TumorMicroenvironment.xml")
boolean_dir = Path("data/models/boolean_networks")
physiboss_root = Path("external/PhysiBoSS")

# Step 2: Automatically pair Boolean network assets by prefix
maboss_map = find_maboss_models(boolean_dir)

# Step 3: Run structural verification and stage project files
staged_xml_name = stage_physiboss_project(
    xml_path=source_xml,
    maboss_models_map=maboss_map,
    physiboss_root=physiboss_root
)

# Step 4: Compile engine and monitor simulation trajectory
run_physiboss_simulation(
    xml_path=source_xml,
    logs_output=Path("logs/simulations/TME_run.log"),
    physiboss_root=physiboss_root,
    executable_name="PhysiBoSS_Cell_Lines"
)

```

---

## Critical Troubleshooting and Edge Cases

### 1. File Access Permission Failures (`PermissionError: [Errno 13]`)

* **Root Cause:** The `executable_name` parameter passed to the runner defaults to a directory or does not match the actual string target defined under `PROGRAM_NAME` inside the native C++ `Makefile`. This causes the OS kernel to block python from executing a directory file block.
* **Resolution:** Verify the output token name of the target compiled executable in `external/PhysiBoSS/Makefile`. Ensure that `executable_name` matches this token string explicitly (e.g., `"PhysiBoSS_Cell_Lines"`).

### 2. File Read Aborts inside the C++ Engine (`Could not open BND file`)

* **Root Cause:** The working directory of the compiled C++ application is set to `external/PhysiBoSS`. If the relative paths declared inside the configuration XML point to external user folders, the engine cannot resolve them.
* **Resolution:** Do not hardcode paths in source templates. The `patch_xml_dependencies` module automatically updates these reference text fields to `./OmniPhysiBoSS_projects/[project_name]/filename.bnd`. If an extraction error occurs, check `verify_xml.py` to confirm the filename token strings are registered correctly in the mapping context.

### 3. Missing Spatial Initialization Files (`cells.csv not found`)

* **Root Cause:** The source XML references custom initial locations or behavior matrices (e.g., `<cell_positions enabled="true">`), but these supporting files are missing from the local folder where the source XML resides.
* **Resolution:** The orchestrator enforces strict co-location rules. Ensure that if your XML configuration references a layout file `cells.csv`, that file is stored in the same folder as the XML file itself. The validation logic will catch any mismatches before triggering a compilation run.

```

