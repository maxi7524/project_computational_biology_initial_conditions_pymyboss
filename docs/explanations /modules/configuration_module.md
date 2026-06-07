## PhysiCell and PhysiBoSS Configuration Explained

This documentation outlines the of the multi-scale agent-based modeling configuration framework utilized by PhysiCell and its Boolean network extension, PhysiBoSS.

#TODO - przepisać ten fragment 
#TODO - to będzie dokumetncja dotycząca ostatecznie zdefiniowanego modelu, będzie trzeba tutaj w każdym zrobić sekcje #### Explanation / #### Implementation czy coś takiego (bo chodzi o to, że jaka jest idea tej struktury i jak my do niej parametry dobraliśmy) 

### 1. Domain and Environment Architecture

The simulation workspace is defined within the `<domain>` and `<microenvironment_setup>` elements.

* **Computational Domain**: Governed by a 3D Cartesian tensor grid where the coordinates span across $[x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}] \times [z_{\min}, z_{\max}]$. Spatial discretization steps ($\Delta x, \Delta y, \Delta z$) determine the voxel volume where continuum partial differential equations (PDEs) are solved.
* **Microenvironment Substrates**: Modeled via a reaction-diffusion equation system representing chemical gradients (e.g., oxygen, glucose, drugs):

$$\frac{\partial \rho}{\partial t} = D \nabla^2 \rho - \lambda \rho + S - U$$

Where:

* $D$ is the `diffusion_coefficient` ($\mu m^2/\text{min}$).
* $\lambda$ is the `decay_rate` ($1/\text{min}$).
* $S$ and $U$ represent bulk or agent-localized secretion and uptake terms.

### 2. Cell Definitions and Phenotypic Properties

Individual agents belong to specific functional lineages declared inside `<cell_definitions>`. Each `<cell_definition>` contains modular operational descriptions:

* **`<cycle>`**: Dictates state transitions (e.g., using transition rates or fixed durations between phases).
* **`<volume>`**: Manages structural mass. Total cellular volume $V$ is partitioned into cytoplasmic and nuclear fluids and solids. For standard spherical abstractions, the radius $r$ relates directly to total volume via:

$$V = \frac{4}{3}\pi r^3$$

* **`<mechanics>`**: Sets cross-agent interactions such as `cell_cell_adhesion_strength` and `cell_cell_repulsion_strength`.
* **`<secretion>`**: Defines agent-level interaction with the continuum fields via localized substrate uptake and export rates.

### 3. Intracellular MaBoSS Integration (PhysiBoSS Specifics)

PhysiBoSS extends standard agent definitions by embedding a continuous-time Markovian Boolean network execution core inside each agent instance. This is declared within the `<intracellular type="maboss">` container inside a `<cell_definition>`:

* **`<bnd_filename>`**: Relative or absolute path to the `.bnd` file, which formally specifies the network topology, node descriptions, and transition rate functions (up/down formulas).
* **`<cfg_filename>`**: Reference to the `.cfg` file holding simulation parameters, node initialization states, and internal evaluation parameters.
* **`<time_step>`**: The updating interval ($\Delta t_{\text{maboss}}$) at which the stochastic Boolean model updates its state and maps internal node configurations to macro-level phenotypic parameters (e.g., mapping a `Death` node activation to an increased apoptosis transition rate).

### 4. Spatiotemporal Initialization and Constraints

* **`<initial_conditions>`**: Points to spatial layout matrices (e.g., `cells.csv`) mapping initial Cartesian coordinate tensors to agent classes.
* **`<cell_rules>`**: Enables or disables the Cell Behavior Hypothesis Grammar (CBHG) schema to map environmental signals directly to behavior changes using parameterized Hill functions.

