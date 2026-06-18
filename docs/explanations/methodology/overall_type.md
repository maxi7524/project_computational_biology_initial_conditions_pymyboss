# Overall type

```{contents} Local Contents
:depth: 2
:local:


```

## Problem Statement

Definition and structuring of global simulation timeline parameters ($\Delta t$ for diffusion, mechanics, and phenotype processes) and the maximum simulation duration ($T_{\max}$) to ensure numerical stability of solvers and physical consistency of the multi-scale agent-based model.

---

## Foundations & Assumptions

### Biological Point of View

The time scales of key biological processes in tissue vary by orders of magnitude: mass transport of signaling molecules (diffusion) occurs in fractions of a second, biomechanical coordination of agents (adhesion, repulsion) requires minute-level resolution, and phenotypic transformations (cell cycle, apoptosis, necrosis) occur slowest—on an hourly scale.

The timeline parameter values ($\Delta t_{\text{diffusion}} = 0.01\,\text{min}$, $\Delta t_{\text{mechanics}} = 0.1\,\text{min}$, $\Delta t_{\text{phenotype}} = 6.0\,\text{min}$) are directly adopted from the literature of the primary developers of the PhysiCell platform (Ghaffarizadeh et al., 2018). The authors did not propose an explicit mechanism for dynamically determining these constants. Consequently, the OmniPhysiBoSS framework allows for their flexible reconfiguration at the launch of the computational pipeline, but it does not perform any automated estimation or fitting based on the input omics data.

**Literature Reference:**
Ghaffarizadeh, A., Heiland, R., Friedman, S. H., Mumenthaler, S. M., & Macklin, P. (2018). PhysiCell: An open source physics-based cell simulator for 3-D multicellular systems. PLOS Computational Biology.

### Mathematical Formulation

The multi-scale model enforces a strict hierarchy and sequential execution of numerical integration steps. The time-splitting relation is described by a system of inclusions, where each larger time step is a multiple of the lower-level step:

$$\Delta t_{\text{diffusion}} \le \Delta t_{\text{mechanics}} \le \Delta t_{\text{phenotype}}$$

The sequence and schedule of process updates in the simulation loop for a given global time $t$ proceed according to the following operational algorithm:

1. **Microenvironment Update (Diffusion):** The PDE solver executes $K_1$ iterations with a step size of $\Delta t_{\text{diffusion}}$ to solve the chemical transport equations until the mechanics time step is reached:

$$K_1 = \frac{\Delta t_{\text{mechanics}}}{\Delta t_{\text{diffusion}}}$$


2. **Biomechanics Update:** Every $\Delta t_{\text{mechanics}}$ interval, cell-cell adhesion and repulsion force vectors are recalculated, and cell agent positions are translated:

$$x_i(t + \Delta t_{\text{mechanics}}) = x_i(t) + v_i(t) \cdot \Delta t_{\text{mechanics}}$$


3. **Cellular State Update (Phenotype and Boolean Networks):** Every $K_2$ mechanics steps (when the $\Delta t_{\text{phenotype}}$ interval elapses), phenotypic models and stochastic runs of MaBoSS logical networks are invoked:

$$K_2 = \frac{\Delta t_{\text{phenotype}}}{\Delta t_{\text{mechanics}}}$$



#### System Implications:

* **Stability:** Separation of time steps prevents numerical oscillations. The step $\Delta t_{\text{diffusion}}$ must satisfy the Courant-Friedrichs-Lewy (CFL) condition for parabolic equations, guaranteeing the convergence of the diffusion solver. Modifying the proportions without maintaining the hierarchy risks immediate numerical explosion of the system.
* **Computational Complexity:** Using an asynchronous update schedule (sub-sampling) reduces the system's computational complexity. Expensive operations for updating intracellular states (Boolean networks) and phenotypes are executed less frequently than dense solute diffusion calculations, optimizing the execution time of the main loop.

---

## Implemented Strategies

### Strategy 1: Default Literature-Based Timeline Assignment

#### Idea

Since the authors of the original PhysiCell and PhysiBoSS software did not suggest a mathematical method or algorithm for dynamically selecting or estimating these parameters based on input data, this strategy adopts their time constants directly from the literature. This guarantees the numerical stability of the solvers and preserves the native physical properties of the multi-scale models.

#### Detailed Algorithmic Implementation

1. **Step 1 (Value Extraction):** Extract the scalar values for `max_time`, `dt_diffusion`, `dt_mechanics`, and `dt_phenotype` from the user-provided runtime configuration profile.
2. **Step 2 (Value Overwriting):** Overwrite the corresponding fields within the `OverallType` data structure directly with the extracted configuration values, wrapping them into the automated schema binding objects (`ValueWithUnits` where applicable).

---

## To Consider

* **Interaction with Stochastic Models:** Analyze whether strictly enforcing a step size of $\Delta t_{\text{phenotype}} = 6.0\,\text{min}$ distorts phase transition trajectories in MaBoSS networks for specific intracellular logical architectures.

---

## Discussion

### Strategy 1:

This strategy eliminates the risk of PDE solver destabilization and minimizes computational pipeline overhead. The main limitation is the lack of adaptability—the timeline grid does not dynamically adjust to the rate of chemical concentration changes or cell population density fluctuations within the tissue domain.