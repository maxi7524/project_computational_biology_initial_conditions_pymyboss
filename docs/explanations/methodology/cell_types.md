# Cell Type models

```{contents} Local Contents
:depth: 2
:local:

```

## Problem Statement

The cell type parameterization component resolves the challenge of mapping static, high-dimensional transcriptomic identities and spatial coordinate configurations into discrete, executable agent definitions (cells types). By aggregating individual cells into statistically robust functional populations, the component restricts the model's dimensional complexity and suppresses stochastic noise associated with low-confidence clusters.

---

## Foundations & Assumptions

### Biological Point of View [1]

Cells of identical transcriptomic lineages display phenotypic plasticity driven by localized spatial microenvironments, anatomical niches, or proximity to tissue boundaries. In multicellular systems, physical characteristics such as cell-cell adhesion strength, maximum motility speeds, and proliferation thresholds are not globally invariant across a specific cell line. Instead, they depend on spatial coordinates and local cell packing density.

* **Spatial/Temporal Scale Constraints**: Cell-to-cell mechanical interactions and localized clustering occur at the micrometer scale ($10\ \mu\text{m} - 200\ \mu\text{m}$ physical neighborhoods). The conversion models must capture these spatial features to prevent abnormal structural artifacts during simulation initialization.
* **Phenotypic Variation**: Distinct spatial zones (e.g., the core of a solid tumor vs. its invasive margin, or perivascular vs. hypoxic niches) alter physical cell behavior, modulating local matrix degradation capacities or adhesion characteristics.


### Mathematical Formulation
<!-- #TODO - przeformułować to później te3 x  -->

Let $\mathcal{X} = \{1, \dots, N\}$ represent the index space of all unique cells captured within the integrated multi-modal `mu.MuData` asset. Each cell $i \in \mathcal{X}$ is defined by its spatial coordinate vector $x_i$ inside the spatial coordinate matrix $S \in \mathbb{R}^{N \times D}$:

$$x_i = \begin{bmatrix} x_{i,1} & x_{i,2} & \dots & x_{i,D} \end{bmatrix}^T \in \mathbb{R}^D$$

Where $D \in \{2, 3\}$ represents the geometric spatial dimensions of the assay data. Let $Y \in \mathbb{R}^{N \times G}$ represent the normalized and log-transformed transcriptomic expression matrix across the isolated feature space of $G$ genes.

Let $G = (\mathcal{X}, \mathcal{E})$ represent a spatial neighborhood graph, where an edge $e_{ij} \in \mathcal{E}$ exists if cell $i$ and cell $j$ satisfy a localized proximity constraint (e.g., $K$-nearest spatial neighbors or a fixed Euclidean distance cutoff $d_{\text{max}}$). The network topology is defined by the adjacency matrix $A \in \mathbb{R}^{N \times N}$, where entries $\alpha_{i,j}$ represent the strength or type of the spatial relationship between cells:
$$
A_{ij} = \alpha_{i,j} = \begin{cases} \alpha_{i,j} \in [-R, R] & \text{if } (i,j) \in \mathcal{E} \\ 0 & \text{otherwise} \end{cases}
$$
Where $\alpha_{i,j}$ is a user-defined weight depending on the specific neighborhood model and the nature of the interaction



### Consolidated Problem Formulation

The fundamental objective of this component is to construct an analytical mapping operator $f$ that partitions the cell space $\mathcal{X}$ into $K$ disjoint cell types $\mathcal{C} = \{C_1, C_2, \dots, C_K\}$, such that:

$$\bigcup_{k=1}^K C_k = \mathcal{X} \quad \text{and} \quad C_a \cap C_b = \emptyset \quad \forall a \neq b$$

Each resolved population $C_k$ is associated with a specific biophysical parameter profile $\theta_k \in \Theta$. 

---

## Implemented Strategies

### Strategy 1: Categorical Pre-annotated Lookup (Baseline)

#### Idea

This strategy relies on pre-existing categorical adnotations computed during upstream bioinformatics processing workflows (e.g., manual cell-type curation or reference-based label transfer stored in `mdata.mod['rna'].obs`). It assumes that transcriptomic identity is the sole driver of physical parameter variations, grouping cells into global cell-type populations regardless of their spatial location.

#### Detailed Algorithmic Implementation

1. **Step 1 (Annotation Extraction)**: Query a target annotation key $\kappa$ within the discrete metadata frame to retrieve the cell-type assignment vector $L \in \mathcal{L}^N$.
2. **Step 2 (Population Isolation)**: Subset the index space into distinct categories matching each unique label $l \in \mathcal{L}$:

$$C_l = \{i \in \mathcal{X} \mid L_i = l\}$$


3. **Step 3 (Macro-Parameter Calculation)**: Compute the mean global centroid $\mu_l$ and assign invariant baseline fallback physical traits from the user configuration to the entire population:

$$\theta_l = \theta_{\text{fallback}}(l)$$



---

### Strategy 2: Spatial Niche Community Partitioning

#### Idea

This strategy separates cells based on their localized spatial microenvironment ("niches") rather than relying on transcriptomics alone. By executing community detection on the spatial adjacency graph $G$, cells of the same cell type that reside in structurally distinct areas (e.g., dense cellular nests vs. isolated stromal regions) are assigned to separate simulation cohorts with distinct physical configurations.

#### Detailed Algorithmic Implementation

1. **Step 1 (Spatial Graph Construction)**: Generate the spatial adjacency matrix $A$ by applying a localized Euclidean distance threshold $d_{\text{max}}$ on the coordinate space $S$:

$$A_{ij} = \begin{cases} 1 & \text{if } \|x_i - x_j\|_2 \le d_{\text{max}} \\ 0 & \text{otherwise} \end{cases}$$


2. **Step 2 (Graph-Based Partitioning)**: Apply the Louvain or Leiden community detection algorithm directly to $A$ to maximize network modularity $Q$, resolving $M$ spatial niches $\mathcal{N} = \{N_1, \dots, N_M\}$.
3. **Step 3 (Cross-Product Lineage Assignment)**: Intersect the spatial niche groups with the baseline transcriptomic annotations $C_l$ from Strategy 1 to form spatialized cell-type archetypes:

$$C_{l,m} = C_l \cap N_m$$


4. **Step 4 (Local Packing Parameterization)**: Adjust cell mechanical attributes, such as the cell-cell adhesion strength $\gamma_{l,m}$, based on the localized packing density of subpopulation $C_{l,m}$:

$$\gamma_{l,m} = \gamma_0 \cdot \left( 1 + \alpha \frac{|C_{l,m}|}{\sum_{j \in C_{l,m}} A_{jj}} \right)$$



---

### Strategy 3: Distance-to-Landmark Radial Partitioning

#### Idea

This strategy accounts for continuous spatial gradients driven by structural tissue landmarks, such as blood vessels, necrotic cores, or invasive margins. Cells are partitioned into concentric structural shells or zones based on their distance from these landmarks, capturing functional variations across a spatial axis.

#### Detailed Algorithmic Implementation

1. **Step 1 (Landmark Specification)**: Define a target reference landmark subset $\mathcal{L}_{\text{ref}} \subset \mathcal{X}$ within the coordinate matrix (e.g., cells identified as endothelial or localized along a user-specified tissue boundary).
2. **Step 2 (Distance Transformation)**: For every cell $i \in \mathcal{X}$, calculate the minimum Euclidean distance to the nearest reference landmark point:

$$\delta_i = \min_{j \in \mathcal{L}_{\text{ref}}} \|x_i - x_j\|_2$$


3. **Step 3 (Radial Zone Bounding)**: Discretize the continuous distance profile $\delta$ into $B$ operational spatial radial bins using user-defined physical boundaries $[b_0, b_1, \dots, b_B]$:

$$Z_b = \{i \in \mathcal{X} \mid b_{b-1} \le \delta_i < b_b\}$$


4. **Step 4 (Gradient Parameterization)**: Scale agent physical parameters (e.g., proliferation rates or maximum motility speed) as a direct mathematical function of the zone radius to mimic microenvironmental nutrient or signaling gradients:

$$\theta_{i \in Z_b} = \theta_{\text{base}} \cdot f_{\text{grad}}(\bar{\delta}_{Z_b})$$



## Bibliography

[1] Da Silva André, G., & Labouesse, C. (2024). Mechanobiology of 3D cell confinement and extracellular crowding. Biophysical Reviews, 16, 833–849. https://doi.org/10.1007/s12551-024-01244-z