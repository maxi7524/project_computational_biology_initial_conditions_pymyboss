# PhysiCell / PhysiBoSS Multi-Scale Configuration Specification

This document defines the structural architecture of the PhysiCell/PhysiBoSS XML configuration file. It serves as the formal blueprint for `PhysiCellAgentConfigurator` class ( in moduel #TODO - moduł lepiej odnieść i klase) responsible for model initialization. 

---

## 1. Global Simulation Controls & Execution Framework

These sections dictate the temporal bounds, core discrete time steps, hardware parallelization, and data persistence rates.

### 1.1 Spatial and Temporal Discretization (`<overall>`)

Defines the boundary constraints for simulation time and the splitting intervals for distinct physical scales.

* **`<max_time>`**: Total temporal domain upper bound $T_{\max} \in \mathbb{R}^+$.
* **`<dt_diffusion>`**: Continuously evaluated partial differential equations (PDEs) time step $\Delta t_{\text{diffusion}}$.
* **`<dt_mechanics>`**: Agent-agent force interaction and translation step $\Delta t_{\text{mechanics}}$.
* **`<dt_phenotype>`**: Stochastic discrete state evaluations and metabolic shifts time step $\Delta t_{\text{phenotype}}$.

The temporal execution satisfies the discrete ordering restriction:


$$\Delta t_{\text{diffusion}} \le \Delta t_{\text{mechanics}} \le \Delta t_{\text{phenotype}}$$

### 1.2 Multi-Threaded Execution (`<parallel>`)

* **`<omp_num_threads>`**: Integer count specifying the shared-memory OpenMP concurrency allocation $N_{\text{threads}} \in \mathbb{Z}^+$.

### 1.3 Data Persistence Engine (`<save>`)

Governs the disk emission frequency of full field matrices and vector asset plots.

* **`<folder>`**: Target output path string.
* **`<full_data>`**: Matrix output interval ($\Delta t_{\text{save}}$). Emissions conform to the MultiCellDS standard.
* **`<SVG>`**: Cellular canvas output interval. Can isolate specific continuum tracking fields (`<plot_substrate>`) using customized color mappings (e.g., `YlOrRd`).

### 1.4 Global Algorithmic Policies (`<options>`)

* **`<legacy_random_points_on_sphere_in_divide>`**: Boolean switch forcing uniform spherical boundary daughter cell generation.
* **`<virtual_wall_at_domain_edge>`**: Boolean Dirichlet-style mechanical boundary constraint enforcing $\vec{v} \cdot \hat{n} \le 0$ at domain edges.
* **`<random_seed>`**: Pseudorandom number generator initialization vector $S_0 \in \mathbb{Z}^*$.

---

## 2. Spatial Domains and Continuum Formulations

These definitions formulate the physical substrate environment where agents operate.

### 2.1 Spatial Bounding Box (`<domain>`)

Specifies a 3D grid domain defined by:


$$[x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}] \times [z_{\min}, z_{\max}]$$


Discretized by spatial steps $\Delta x, \Delta y, \Delta z$ (`<dx>`, `<dy>`, `<dz>`). 2D confinement is toggled via `<use_2D>`.

### 2.2 Microenvironment Solutes (`<microenvironment_setup>`)

Each independent chemical species variable $\rho_k$ is tracked via an individual `<variable>` block implementing a generalized reaction-diffusion formulation:

$$\frac{\partial \rho_k}{\partial t} = D_k \nabla^2 \rho_k - \lambda_k \rho_k + S_k - U_k$$

* **`<diffusion_coefficient>`**: Transport rate scalar $D_k$.
* **`<decay_rate>`**: Natural fluid half-life consumption constant $\lambda_k$.
* **`<Dirichlet_boundary_condition>`**: Toggles static edge conditions at the boundaries:

$$\partial \Omega = \{x_{\min}, x_{\max}, y_{\min}, y_{\max}, z_{\min}, z_{\max}\}$$



---

## 3. Agent Archetypes and Phenotypic Blueprints (`<cell_definitions>`)

This block handles individual agent class definitions (`<cell_definition>`). It specifies how a given cellular archetype behaves and interacts with environmental fields.

### 3.1 Division Pathways (`<cycle>`)

Dictates cellular proliferation dynamics.

* **`<phase_durations>`**: Explicit time steps allocated to specific lifecycle states.
* **`<standard_asymmetric_division>`**: Probability vector mapping lineage transformation events at the point of mitotic cleavage:

$$\sum_{m} P(\text{lineage}_m) = 1.0$$



### 3.2 Programmed Clearance (`<death>`)

Houses structural models for cell degradation workflows (typically `apoptosis` and `necrosis`).

* **`<death_rate>`**: Instancy of state transitions ($r_{\text{death}}$).
* **`<parameters>`**: Rate constants regulating structural degradation, fluid shifts, biomass structural changes, and target volume calculation triggers:

$$\frac{dV_{\text{fluid}}}{dt} = r_{\text{fluid\_change}} \cdot (V_{\text{target}} - V_{\text{fluid}})$$



### 3.3 Biophysical Scaling Constants (`<volume>`)

Defines the spatial footprint and internal volume allocation:

* **`<total>`**: Basal volume metric $V_{\text{basal}}$.
* **`<fluid_fraction>`**: Ratio of intracellular fluid volume to the total cell volume.
* **`<nuclear>`**: Nuclear absolute baseline size configuration.

### 3.4 Spatial Interactions (`<mechanics>`)

Models cell-to-cell forces using potential energy representations.

* **`<cell_cell_adhesion_strength>`**: Adhesion scalar $W_{\text{adhesion}}$.
* **`<cell_cell_repulsion_strength>`**: Repulsion scalar $W_{\text{repulsion}}$.
* **`<cell_adhesion_affinities>`**: Direct weighting matrices controlling affinity interactions between distinct archetypes.

### 3.5 Directional Realignment (`<motility>`)

Handles cell movement and biasing vectors.

* **`<speed>`**: Random walk velocity coefficient $v_0$.
* **`<migration_bias>`**: Alignment probability scalar $b \in [0, 1]$.
* **`<chemotaxis>`**: Couples migration bias vector $\vec{d}$ directly to solute scalar fields:

$$\vec{d} = \pm \frac{\nabla \rho_k}{\|\nabla \rho_k\|}$$



### 3.6 Biomolecule Exchange Fluxes (`<secretion>`)

Defines local sources and sinks at an agent's current position $\vec{x}_i$:

* **`<secretion_rate>`**: Linear substrate secretion velocity $S_k$.
* **`<secretion_target>`**: Saturation boundary $\rho_{k,\text{sat}}$ where secretion terminates.
* **`<uptake_rate>`**: Linear consumption constant $U_k$.

### 3.7 Population Dynamics (`<cell_interactions>`)

Controls aggressive or cooperative actions like phagocytosis, attack damage, or fusion events across specific cell variants.

### 3.8 Lineage Shifts (`<cell_transformations>`)

* **`<transformation_rate>`**: Stochastic transition probability matrix tracking switches from archetype $\alpha$ to state $\beta$.

### 3.9 Structural Degradation (`<cell_integrity>`)

Tracks accumulative stress markers via discrete tracking metrics (`<damage_rate>`, `<damage_repair_rate>`).

### 3.10 Epigenetic Context & State Tracking Variables (`<custom_data>`)

Arbitrary numeric registries initialized globally to track agent variables during custom pipeline loops.

### 3.11 Parameter Stochastics (`<initial_parameter_distributions>`)

Defines population heterogeneity by sampling foundational parameters from parametric probability distributions (e.g., `Log10Normal`, `LogUniform`).

### 3.12 Boolean Network Core (`<intracellular type="maboss">`)

*PhysiBoSS specific block embedded natively inside a cell definition.*

* **`<bnd_filename>`**: System layout configurations mapping discrete node behaviors.
* **`<cfg_filename>`**: Boundary initialization values and state space constraints for Markov models.
* **`<time_step>`**: Update step size $\Delta t_{\text{maboss}}$.

---

## 4. Initialization Vectors and Boundary Rules

### 4.1 Particle Instantiation (`<initial_conditions>`)

* **`<cell_positions>`**: Points to a structural file (e.g., `cells.csv`) mapping Cartesian locations to cellular lineages:

$$\mathbf{X}_i = [x_i, y_i, z_i, \text{type}_i]$$



### 4.2 Behavior Rulesets (`<cell_rules>`)

* **`<rulesets>`**: Implements the Cell Behavior Hypothesis Grammar (CBHG). This framework links microenvironmental concentrations directly to cell characteristics using mathematical logic gates or Hill equations:

$$f(\rho) = \frac{\rho^n}{K^n + \rho^n}$$



### 4.3 Runtime Variables (`<user_parameters>`)

Custom operational fields parsed directly into execution memory blocks at program setup.
