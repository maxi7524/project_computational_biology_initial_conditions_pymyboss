# OmniPhysiBoss
#TODO

## Introduction

### Goal & Motivation

***

### Key Features 


### Future plans

***

## Summary 

###

### Methodology (briefly)

### Implementation details 

***

## Installation and Environment Verification

To initialize the environment and verify the installation follow these steps.

### 1. Environment Provisioning via Micromamba

```bash
# Create the environment
micromamba create -f workflow/envs/environment.yaml

# Activate the environment
micromamba activate OmniPhysiBoss_env
```

### 2. Verification of Python Package Installation

Verify that the `OmniPhysiBoss` source package has been correctly resolved and linked in editable development mode (`-e .` constraint handled by the environment file):

```bash
python -c "import OmniPhysiBoss; print('OmniPhysiBoss successfully resolved at:', OmniPhysiBoss.__file__)"
```

If you obtain error, you nee to install it manually by resolving bugs:

```bash
pip install -e .
```

### 3. Check Computational Backends and Compiled Core Dependencies

Since downstream integration relies on direct interaction with `MaBoSS` and multi-scale execution engines, verify that package managers can resolve the core functional libraries:

```bash
# MaBoSS
python -c "import maboss; print('MaBoSS import successful.'); print('Location:', maboss.__file__)"
# decoupleR
python -c "import decoupler; print('Decoupler version:', decoupler.__version__)"
```

*Note: If automated package installation fails to resolve native C++ compilation routines or internal library flags for structural simulation tools (`MaBoSS` binary dependencies or `PhysiCell` execution environments), custom compilation blocks must be executed via the local installation scripts.*


## Project structure

```Plaintext
OmniPhysiBoss/
├── .gitignore
├── README.md
├── pyproject.toml              # Central package configuration (PEP 621)
├── external/                           # Third-party compiled engine installations
│   └── PhysiBoSS/                      # Shallow clone source repository of the C++ engine
│       ├── Makefile                    # Low-level build file compiling object frameworks
│       ├── PhysiBoSS_Cell_Lines        # Compiled multi-scale binary executable file
│       ├── OmniPhysiBoSS_projects/     # Isolated runtime directories partitioned by workflow
│       │   └── [project_name]/         # Active configuration target workspace folder
│       │       ├── cells.csv           # Staged initial agent position sheet
│       │       ├── cell_rules.csv      # Staged behavior transformation matrix
│       │       ├── [project_name].xml  # Patched XML execution configuration
│       │       ├── model_0.bnd         # Transported Boolean network structure
│       │       └── model_0.cfg         # Transported Boolean probability rules
│       └── output/                     # Target folder where the C++ engine dumps simulation data
├── logs/
│   └── physiboss_simulation/           # Directory capturing simulation run logs
│       └── [project_name].log          # Telemetry output file captured by the runner stream
├── src/                        # Library source code
│   └── OmniPhysiBoss/
│       ├── __init__.py         # Public API exposure
│       ├── py.typed            # Type hinting marker (PEP 561)
│       ├── io/                 # Data input/output processing
│       │   ├── __init__.py
│       │   └── anndata_io.py   # AnnData parsing and matrix extraction
│       ├── omics/             # Graph integration and footprint inference (tutaj będziemy pozyskiwać informacje z mdata 1.)
│       │   ├── __init__.py
│       │   ├── signaling.py    # OmniPath and Liana+ interfaces
│       │   ├── activity.py     # decoupleR transcription factor activity
│       │   └── logic.pycytacje # Boolean rule generation (for .bnd configuration)
│       ├── personalization/    # Kinetic parameterization (tutaj będziemy dobierać paramtery )
│       │   ├── __init__.py
│       │   ├── profile.py      # PROFILE calculation for k_up and k_down
│       │   └── steady_state.py # Master equation solver for t_max tracking
│       ├── configure/          # Graph integration and footprint inference (tutaj będziemy po)
│       │   ├── __init__.py
│       │   ├── maboss_initializer.py    # tutaj będzie klasa do tworzenia obiektów maboss (cfg . bnd)
│       │   ├── agent_initializer.py     # tutaj będzie klasa do tworzenia obiektów physicell (xml with cell rules and cells)
│       │   └── ???.py        # jakieś helpery ewentualnie do etgo 
│       ├── wrapper/            # Multi-scale orchestrator
│       │   ├── __init__.py
│       │   └── configurator.py # Structural export of XML and MaBoSS entrypoints
│       └── wrappers/                   # Multi-scale execution orchestration layer
│           ├── __init__.py             # Public boundary interface exposition
│           ├── configure_PhysiBoSS.py  # Validation and configuration assembly orchestrator
│           ├── run_PhysiBoSS.py        # Clean build manager and execution supervisor
│           └── _utils/                 # Private atomic helper modules
│               ├── __init__.py
│               ├── pathfinder.py       # File discovery and output asset migration tools
│               ├── verify_xml.py       # Modular structural validation routines
│               ├── patch_xml.py        # Modular in-memory structural path patching routines
│               └── log_monitor.py      # Real-time C++ stream telemetry parsing filters
├── workflow/                   # Snakemake orchestrator
│   ├── Snakefile               # Global Directed Acyclic Graph (DAG) definition
│   ├── config/
│   │   └── config.yaml         # Execution parameters, cutoffs, tolerances
│   ├── envs/
│   │   └── environment.yaml    # Conda/Micromamba operational environment configuration
│   ├── rules/                  # Isolated Snakemake rule definitions (.smk)
│   └── scripts/                # Execution and bridging scripts
├── notebooks/                  # Exploratory Data Analysis (EDA)
│   └── eda_validation.ipynb    # Downstream verification notebooks
tests/
├── __init__.py
├── mock_data/                     # <--- Dedytowany podmoduł zasobów mockowych
│   ├── __init__.py
│   ├── omics_data.py             # Generowanie obiektów AnnData i macierzy ekspresji
│   ├── physicell_templates.py    # Pełne struktury XML, CSV i reguły CBHG
│   └── maboss_templates.py       # Pliki .bnd oraz .cfg modeli Boolean
├── test_io.py
├── test_network.py
├── test_personalization.py
└── test_wrappers/                 # <--- Nowe odizolowane testy modułu orkiestracji
    ├── test_configure.py
    └── test_runner.py
```

