Markdown
# Software Architecture & Library Modules

> REMARK: Currently wrapper module need to be rebuild as we find 'UQ-PhysiCell' library which manages simulation in PhysiBoSS. We also need to rewrite configuration module as now we obtained .xsd file which allows us to create much cleaner version. Previous one was created from scratch. 

The `OmniPhysiBoSS` framework is constructed using an decoupled, modular architecture. It allows for modification of certain parts.

Library also provides tests for inputs and outputs to ensure formats are valid. 
---

## The Core Concept

The library partitions data preparation, parsing, validation, and C++ process orchestration into standalone modules:

*   **[`io`](./../io_formats/README.md)** and **[`models`](./models.md)**: Tasked with parsing upstream structural layouts, checking data, and enforcing rigorous configuration compatibility rules across distinct computational layers.
*   **[`configurators`](./configurators.md)** and **[`wrappers`](./wrappers_module.md)**: Programmatically assemble simulation-ready variables, coordinate spatial metadata profiles, safely deploy assets inside the engine workspace, and supervise the native execution runtime.

---

## Unified Data Flow & Lifecycle Topology

The execution lifecycle transitions sequentially through four functional boundaries, ensuring data consistency before binary invocation:

```plaintext
[ scRNA-seq Parameters / Spatial Data ]
                     │
                     ▼
       ┌───────────────────────────┐
       │         io module         │ ──► Validates input formats and decorates metadata.
       └───────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │       models module       │ ──► Implements standardized model templates.
       └───────────────────────────┘
                     │
                     ▼
       ┌───────────────────────────┐
       │   configuration module    │ ──► Builds XML + CSV object structures in memory.
       └───────────────────────────┘
                     │
                     │ (Generates a validated set of files)
                     ▼
       ┌───────────────────────────┐
       │      wrappers module      │ ──► Launches the multi-stage binary orchestration pipeline:
       └───────────────────────────┘
         ├── 1. verify_xml.py          ──► Verifies correctness and presence of linked files.
         ├── 2. patch_xml.py           ──► Translates paths within the configuration tree structure.
         ├── 3. stage_xml.py           ──► Prepares an isolated execution environment on disk.
         ├── 4. run_PhysiBoSS.py       ──► Compiles the engine and supervises the binary child process.
         └── 5. migrate outputs        ──► Transfers resulting MultiCellDS matrices to user structures.
```


### 1. [IO Module](./io_module.md)
Acts as an initial validation layer and metadata decorator. It ingests raw configuration structures, checks text formats, validates spatial constraints, and handles descriptive error parsing to provide clear feedback during execution bottlenecks.

<!-- ### 2. [Models Module](./models_module.md) -->
### 2. Models Module
Houses standalone, standardized computational abstractions. Every independent simulation model inherits from a rigid abstract base class wrapper to guarantee structural and functional validity before entering down-stream compilers.

<!-- ### 3. [Configurators Module](./configurators_module.md) -->
### 3. Configurators Module
An orchestration layer that programmatically builds, alters, and manages standalone input profiles for MaBoSS networks and PhysiCell spatial engines. It abstracts complex XML transformations into simple, atomic functional commands.

<!-- ### 4. [Wrappers Module](./wrappers_module.md) -->
### 4. Wrappers Module
Orchestrates low-level environment deployment, clears stale execution directories, initializes compiler building steps via Makefile execution, forks the native child process, and pipes filtered telemetry back to standard output streams.

<!-- ---

## Specific Modules Specification

#TODO write here comprehensive description of all modules. -->
