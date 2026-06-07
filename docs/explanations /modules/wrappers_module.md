# Wrappers Module: Multi-Scale Simulation Orchestrator

## Introduction

### Abstract Functionality

The `wrappers` module serves as the functional bridge between high-level Python pipeline operations and the low-level, compiled C++ multi-scale engine (`PhysiBoSS`). The module transfers the model from our target folder to the downloaded `external/PhysiBoSS` repository for its simulation. It validates settings, captures logs, and ensures the transfer of result files to the folder specified in the target file (by default `output`).

### Structure

The `wrappers` module is divided into public execution scripts and a private utility subpackage (`_utils`), which isolates functionality related to:
- validation of configuration files ([PhysiCell](https://www.google.com/search?q=../io_formats/physicell_configuration_format.md), [MaBoSS](https://www.google.com/search?q=../io_formats/maboss_configuration_format.md)) and their transfer to the execution engine (`stage_PhysiBoSS.py`)
- launching the execution engine via the wrapper and collecting its logs (`run_PhysiBoSS.py`)
- disk operations and parsing analysis (`pathfinder.py`).

```
wrappers/
├── **init**.py                # Exposes public execution interfaces
├── stage_PhysiBoSS.py     # Orchestration of verification, mutation, and asset deployment
├── run_PhysiBoSS.py           # C++ code compilation and binary process supervision
└── _utils/                    # Private utility modules (Atomic Helpers)
    ├── **init**.py
    ├── log_monitor.py         # Real-time filtering and cleaning of stdout logs
    ├── patch_xml.py           # Updating relative paths in the XML tree structure
    ├── pathfinder.py          # Disk scanning and pairing of MaBoSS models
    ├── stage_xml.py           # Physical clearing of workspace and file serialization
    └── verify_xml.py          # Multi-stage validation of input data consistency

```

* **`stage_PhysiBoSS.py`**: Coordinates the validation and preparation pipeline of the development project before running the simulation.
* **`run_PhysiBoSS.py`**: Invokes the C++ engine compilation, launches the system child process, and redirects diagnostic streams.
* **`_utils/pathfinder.py`**: Automatically pairs `.bnd` and `.cfg` files with common prefixes and migrates resulting trajectories.
* **`_utils/verify_xml.py`**: Checks the correctness of intracellular tags, prefix compatibility, and the physical presence of configuration files on the disk.
* **`_utils/patch_xml.py`**: Overwrites XML text nodes, modifying paths to Boolean files and output folders to maintain isolation.
* **`_utils/stage_xml.py`**: Validates user configurations and stages the verified file matrix inside the operational C++ engine layout.
* **`_utils/log_monitor.py`**: Captures the low-level output pipeline, discarding repetitive cell position dumps.

### Execution Pipeline

Simulation execution proceeds in six isolated technological steps:

1. **Input verification (`verify_xml.py`)**: Checking the presence of key XML tags, validating the consistency of MaBoSS structures, and coordinating spatial files.
2. **Memory modification (`patch_xml.py`)**: Dynamic rewriting of relative paths in the XML tree to match the execution structure of the development folder.
3. **Asset deployment (`stage_xml.py`)**: Clearing the destination directory, writing the modified configuration file, and physically copying the associated `.bnd`, `.cfg`, and `.csv` files.
4. **Engine compilation (`run_PhysiBoSS.py`)**: Invoking the `make clean && make` sequence in the C++ environment to exclude linking errors.
5. **Process monitoring (`log_monitor.py`)**: Launching the binary container, capturing the output pipeline, and filtering log messages.
6. **Data migration (`pathfinder.py`)**: Transferring the generated matrices and MultiCellDS files to the user's output directories.

## Submodule Specifications

### stage_PhysiBoSS

```{eval-rst}
.. automodule:: OmniPhysiBoSS.wrappers.stage_PhysiBoSS
   :members:
   :undoc-members:
   :show-inheritance:


```

### run_PhysiBoSS

```{eval-rst}
.. automodule:: OmniPhysiBoSS.wrappers.run_PhysiBoSS
   :members:
   :undoc-members:
   :show-inheritance:


```

## Developer & Modification Guide

### Usage Blueprint

The following script presents a complete, automated operational cycle of model orchestration using the `wrappers` module:

```python
from pathlib import Path
from OmniPhysiBoSS.wrappers._utils.pathfinder import find_maboss_models, migrate_simulation_outputs
from OmniPhysiBoSS.wrappers.stage_PhysiBoSS import stage_physiboss_project
from OmniPhysiBoSS.wrappers.run_PhysiBoSS import run_physiboss_simulation

# Main preparation of data context and development paths
## Defining locations of source files and the root directory of the C++ engine
source_xml = Path("data/models/TumorMicroenvironment.xml")
boolean_dir = Path("data/models/boolean_networks")
physiboss_root = Path("external/PhysiBoSS")
output_target_dir = Path("results/simulations/TME_experiment_v1")

# Step 1: Automatic disk scanning and grouping of Boolean network files
maboss_map = find_maboss_models(boolean_dir)

# Step 2: Execution of the structure verification pipeline and deployment of configuration assets
staged_xml_name = stage_physiboss_project(
    xml_path=source_xml,
    maboss_models_map=maboss_map,
    physiboss_root=physiboss_root
)

# Step 3: Cleaning the compiler, building the system binary, and monitoring the simulation
run_physiboss_simulation(
    xml_path=source_xml,
    logs_output=Path("logs/simulations/TME_run.log"),
    physiboss_root=physiboss_root,
    executable_name="PhysiBoSS_Cell_Lines"
)

# Step 4: Displacing output simulation trajectories to the dedicated project folder
migrate_simulation_outputs(
    destination_dir=output_target_dir,
    output_src=physiboss_root / "output"
)


```

### Tests

The package features a dedicated suite of regression and validation tests based on the `pytest` library:

* **Success paths (`test_stage_project_single_model_success`, `test_stage_project_multi_model_success`)**: Verify the correctness of asset copying, allocation of project structures within `OmniPhysiBoSS_projects`, and check whether XML tree modifiers correctly rewrite development paths relative to the execution directory.
* **Configuration exception handling (`test_stage_project_missing_xml`, `test_stage_project_prefix_mismatch`, `test_stage_project_unmapped_model`, `test_stage_project_missing_tags`, `test_stage_project_missing_external_csv`)**: Test the resilience of the validator against corrupted XML files, missing coordinate `cells.csv` files, asymmetrical prefixes of Boolean file names, and missing structural tags.
* **Execution tests of the binary environment (`test_compile_engine_failure`, `test_runner_missing_executable`, `test_log_monitor_mesh_and_rng_parsing`, `test_run_simulation_pipeline_success`)**: Check the correctness of capturing C++ compiler errors, the proper functioning of regular expression parsers within the telemetry log manager, and simulate full completion of the orchestrator task.

### Troubleshooting

#### 1. Kernel permissions error (`PermissionError: [Errno 13]`)

* **Cause**: The `executable_name` parameter passed to the interpreter points to a directory, or the name of the executable file is not identical to the `PROGRAM_NAME` flag defined in the `Makefile` of the C++ engine.
* **Solution**: Check the physical name of the compilation output token in `external/PhysiBoSS/Makefile`. Ensure that the passed text string matches this value exactly (e.g., `"PhysiBoSS_Cell_Lines"`).

#### 2. Read interruption in the C++ engine (`Could not open BND file`)

* **Cause**: The working directory of the compiled C++ application is hardcoded as `external/PhysiBoSS`. If paths in the source XML file point to external user folders, the application cannot locate them.
* **Solution**: Do not hardcode development paths. The `patch_xml_dependencies` module automatically reconstructs these references into the form `./OmniPhysiBoSS_projects/[project_name]/file.bnd`. If an error occurs, verify whether the file names in the mapping dictionary correspond to the input structures.

#### 3. Missing spatial initialization files (`cells.csv not found`)

* **Cause**: The `<cell_positions enabled="true">` tag has been activated in the configuration file, but the associated coordinate file is not located in the same directory as the input XML file.
* **Solution**: The framework enforces absolute collocation of input assets. Ensure that the `cells.csv` file is placed in the exact same folder where the input XML resides.