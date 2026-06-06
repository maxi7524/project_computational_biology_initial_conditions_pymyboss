# Input/Output Formats Specification

This document provides a rigorous, developer-focused reference for all input mdata, metadata templates, and output trajectories processed throughout the `OmniPhysiBoSS` multi-scale pipeline. It defines structural schemas to streamline collaborative development, simplify pipeline modifications, and accelerate debugging.

---

## Data Structure and Formats Architecture

The execution pipeline standardizes data transformations by categorizing files into native Python validation schemas and external upstream core configuration files.

```
                  ┌────────────────────────────────────────┐
                  │      Simulation Data Entrypoints       │
                  └────────────────────────────────────────┘
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
     ┌─────────────────────────┐               ┌─────────────────────────┐
     │    Internal IO Formats  │               │ Upstream Engine Formats │
     └─────────────────────────┘               └─────────────────────────┘
      ├── Runtime Configuration                 ├── MaBoSS Core (.bnd, .cfg)
      └── Validation Meta-Diction.              └── PhysiCell Setup (XML, CSV)
```

---

## Internal IO Module Formats

The pythonic handling layer utilizes specialized runtime definitions to capture configuration metrics prior to file serialization:

*   **Runtime Parameter Blueprints:** Structured python dictionaries specifying workspace boundaries, folder location references, parallel computing directives, and multi-scale simulation timesteps.
*   **Validation Metadata Profiles:** Strict data typing schemas that intercept parameters, enforce domain restrictions, and verify pathing tokens before staging operations begin.

---

## Upstream Engine Native Formats

### 1. MaBoSS Intracellular Network Blueprints
Continuous-time Markovian Boolean models are declared using two tightly coupled text assets:
*   **Network Layout (`model.bnd`):** Defines the structural graph topology. It specifies all node names, upstream activation/inhibition links, and mathematical transition rate formulas (`logic rules`).
*   **Configuration Parameters (`model.cfg`):** Controls boundary bounds and probability vectors. Sets node initial states ($P(\text{node}=1)$), structural simulation parameters, maximum transition bounds, and output tracking flags.

### 2. PhysiCell Spatial Engine Settings
The agent-based physical simulation relies on co-located configuration templates:
*   **Initial Conditions Matrix (`cells.csv`):** A dense Cartesian tensor file mapping exact spatial initial states. Each comma-separated row strictly follows the structural coordinate convention:
    $$\mathbf{X}_i = [x_i, y_i, z_i, \text{cell\_type}_i]$$
*   **Cell Behavior Grammar (`cell_rules.csv` / rule sheets):** Extends baseline behaviors by linking environmental solute fields to phenotypic transitions using parameterized logic functions and Hill equations.
*   **Global Structural Configuration (`model_settings.xml`):** The primary hierarchical document. It covers bounding box domain parameters, OpenMP threading boundaries, microenvironment solutes reaction-diffusion rates, and detailed cellular lineage blueprints.

### 3. PhysiBoSS Output Trajectories Data Layout
Upon completion, the internal C++ output engine emits a structured data dump:
```
output/
├── initial_mesh0.mat         # Cartesian tissue grid structure snapshot
├── final_microenvironment.mat# Solute concentration tensors across voxels
├── Slovak_Model_00000000.xml # MultiCellDS cell metadata descriptor frame
├── Slovak_Model_00000000.mat # Dense cell matrix tracking positions and states
└── simulation_telemetry.log  # Raw unbuffered terminal logs from the execution run
```
*   **MultiCellDS XML Framework:** Describes experiment metadata timelines and tracks structural state pointers.
*   **Dense Matrix Files (`.mat`):** Store individual cell positions, phenotypic states, solid/fluid volume distributions, and active intracellular Boolean node configurations at predefined persistence rates.