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

***

## Internal IO Module Formats

The pythonic handling layer utilizes specialized runtime definitions to capture configuration metrics prior to file serialization:

- **Runtime Parameter Blueprints:** Structured python dictionaries specifying workspace boundaries, folder location references, parallel computing directives, and multi-scale simulation timesteps.
- **Validation Metadata Profiles:** Strict data typing schemas that intercept parameters, enforce domain restrictions, and verify pathing tokens before staging operations begin.

***

## Upstream Engine Native Formats

### 1. MaBoSS Intracellular Network Blueprints
Continuous-time Markovian Boolean models are declared using two tightly coupled text assets:
- **Network Layout (`model.bnd`):** Defines the structural graph topology. It specifies all node names, upstream activation/inhibition links, and mathematical transition rate formulas (`logic rules`).
- **Configuration Parameters (`model.cfg`):** Controls boundary bounds and probability vectors. Sets node initial states ($P(\text{node}=1)$), structural simulation parameters, maximum transition bounds, and output tracking flags.

### 2. PhysiCell Spatial Engine Settings
The agent-based physical simulation relies on co-located configuration templates:
- **Initial Conditions Matrix (`cells.csv`):** A dense Cartesian tensor file mapping exact spatial initial states. Each comma-separated row strictly follows the structural coordinate convention:
    $$\mathbf{X}_i = [x_i, y_i, z_i, \text{cell\_type}_i]$$
- **Cell Behavior Grammar (`cell_rules.csv` / rule sheets):** Extends baseline behaviors by linking environmental solute fields to phenotypic transitions using parameterized logic functions and Hill equations.
- **Global Structural Configuration (`model_settings.xml`):** The primary hierarchical document. It covers bounding box domain parameters, OpenMP threading boundaries, microenvironment solutes reaction-diffusion rates, and detailed cellular lineage blueprints.

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
- **MultiCellDS XML Framework:** Describes experiment metadata timelines and tracks structural state pointers.
- **Dense Matrix Files (`.mat`):** Store individual cell positions, phenotypic states, solid/fluid volume distributions, and active intracellular Boolean node configurations at predefined persistence rates.
   
*** 

## Compatibility & Integration Blueprint

This framework establishes structural parameters to guarantee exact alignment between the agent-based physical spatial simulation (`PhysiCell`) and the continuous-time Boolean signaling layer (`MaBoSS`) inside the multi-scale `OmniPhysiBoSS` pipeline.

### Temporal Scale Alignment and Scaling Formulas
PhysiCell tracks spatial mechanics, diffusion, and phenotype changes over continuous timelines using explicit discretization intervals. MaBoSS updates discrete state configurations stochastically within localized windows. To enforce strict physical compatibility, the execution time step sizes must obey strict hierarchical bounds.

#### Time Steps Formal Inequality Hierarchy
The global multi-scale execution flow requires that the distinct temporal scales satisfy the matching constraints:

$$\Delta t_{\text{diffusion}} \le \Delta t_{\text{mechanics}} \le \Delta t_{\text{phenotype}} = \Delta t_{\text{intracellular}}$$

Where:
*   $\Delta t_{\text{phenotype}}$ is the configuration token `<dt_phenotype>` in PhysiCell.
*   $\Delta t_{\text{intracellular}}$ is the update window token `<time_step>` declared inside the `<intracellular type="maboss">` block within the XML file.

#### The Rate Scaling Mechanism
MaBoSS rates are expressed in terms of transitions per arbitrary time unit ($1/\tau_{\text{maboss}}$). To map these trajectories onto the physical minutes domain utilized by PhysiCell, you must adjust the MaBoSS time bounds using the system relation defined by the core simulation logic:

$$\text{scaling} = \frac{\Delta t_{\text{intracellular}}}{T_{\text{maboss}}}$$

Where $T_{\text{maboss}}$ corresponds to the parameter `max_time` declared in the MaBoSS `.cfg` file. To ensure that a single update step across the Boolean network corresponds exactly to the physical cell phenotype update step, you must configure:

$$T_{\text{maboss}} = \Delta t_{\text{intracellular}}$$

This equality forces the absolute timescale of the continuous-time Markov chains inside MaBoSS to line up perfectly with the physical minutes elapsed in the microenvironment. If they diverge, kinetic rates defined inside the `.bnd` file will operate on an uncalibrated scale, causing premature phenotype updates or delayed signal transduction.

### XML Integration Schema Configuration
To bind a validated MaBoSS network configuration to an explicit cell definition archetype within the `model_settings.xml` file, the `<intracellular>` configuration block must be structured inside the target `<cell_definition>` node:

```xml
<cell_definition id="0" name="cancer_cell">
    <!-- ... physical properties (cycle, volume, mechanics) ... -->
    <intracellular type="maboss">
        <bnd_filename>./config/model.bnd</bnd_filename>
        <cfg_filename>./config/model.cfg</cfg_filename>
        <time_step>6.0</time_step> <!-- Enforces dt_intracellular = dt_phenotype -->
    </intracellular>
</cell_definition>
```

## Reference 
- **PhysiBoSS 2.0 Core Architecture:** [PhysiBoSS 2.0: A sustainable integration of stochastic Boolean and agent-based modelling frameworks](https://pmc.ncbi.nlm.nih.gov/articles/PMC10616087/)
- **Upstream Repository Specifications:** Detailed implementation examples and the original multi-scale mapping parameters are cataloged directly within the [gletort/PhysiBoSS GitHub Repository](https://github.com/gletort/PhysiBoSS).