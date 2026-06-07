
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

