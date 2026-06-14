# Cell Type models

```{contents} Local Contents
:depth: 2
:local:

```

## Problem Statement

The cell type parameterization component handles the translation of static, high-dimensional transcriptomic profiles and cluster divisions into discrete simulation definitions. It formalizes an automated framework to group individual cells into functional populations based on available experimental annotations or unsupervised data-driven partitions.


---

## Foundations & Assumptions

### Biological Point of View 

Cells of identical transcriptomic lineages display phenotypic plasticity driven by localized spatial microenvironments, anatomical niches, or proximity to tissue boundaries. In multicellular systems, physical characteristics such as cell-cell adhesion strength, maximum motility speeds, and proliferation thresholds are not globally invariant across a specific cell line. Instead, they depend on spatial coordinates and local cell packing density [1]. 

* **Spatial/Temporal Scale Constraints**: Cell-to-cell mechanical interactions and localized clustering occur at the micrometer scale ($10\ \mu\text{m} - 200\ \mu\text{m}$ physical neighborhoods). The conversion models must capture these spatial features to prevent abnormal structural artifacts during simulation initialization.
* **Phenotypic Variation**: Distinct spatial zones (e.g., the core of a solid tumor vs. its invasive margin, or perivascular vs. hypoxic niches) alter physical cell behavior, modulating local matrix degradation capacities or adhesion characteristics.


Once populations are structured, the module enriches each lineage using external biological knowledge bases to lay down the baseline properties required for subsequent physical and mechanical scaling modules.

<!-- 
#TODO - reformulate a little 
To initialize an agent-based simulation, continuous cellular expression profiles must be grouped into operational lineages. When experimental data includes pre-assigned cell-type annotations, the system maps these classes directly. In unannotated datasets, cells are grouped using unsupervised transcriptomic distributions to reveal underlying tissue heterogeneity.

Database Curation Niche: Functional attributes, canonical markers, and baseline phenotypic characteristics are extracted programmatically from reference knowledge bases, specifically the Cell Ontology (CL) database for anatomical nomenclature, and PanglaoDB or CellMarker for tissue-specific marker profiling.

Physical Decoupling: Biophysical property derivation (such as cell-cell adhesion forces or localized elasticity matrices) is explicitly excluded from this structural classification phase. Population characterization and metadata annotation are resolved here, while all mechanical parameter estimation tasks are deferred to downstream simulation configuration modules. -->

### Mathematical Formulation
<!-- #TODO - przeformułować to później te3 x  -->

<!-- 
Wersja ciągła
Let $\mathcal{X} = \{1, \dots, N\}$ represent the index space of all unique cells captured within the integrated multi-modal `mu.MuData` asset. Each cell $i \in \mathcal{X}$ is defined by its spatial coordinate vector $x_i$ inside the spatial coordinate matrix $S \in \mathbb{R}^{N \times D}$:

$$x_i = \begin{bmatrix} x_{i,1} & x_{i,2} & \dots & x_{i,D} \end{bmatrix}^T \in \mathbb{R}^D$$

Where $D \in \{2, 3\}$ represents the geometric spatial dimensions of the assay data. Let $Y \in \mathbb{R}^{N \times G}$ represent the normalized and log-transformed transcriptomic expression matrix across the isolated feature space of $G$ genes.

Let $G = (\mathcal{X}, \mathcal{E})$ represent a spatial neighborhood graph, where an edge $e_{ij} \in \mathcal{E}$ exists if cell $i$ and cell $j$ satisfy a localized proximity constraint (e.g., $K$-nearest spatial neighbors or a fixed Euclidean distance cutoff $d_{\text{max}}$). The network topology is defined by the adjacency matrix $A \in \mathbb{R}^{N \times N}$, where entries $\alpha_{i,j}$ represent the strength or type of the spatial relationship between cells:
$$
A_{ij} = \alpha_{i,j} = \begin{cases} \alpha_{i,j} \in [-R, R] & \text{if } (i,j) \in \mathcal{E} \\ 0 & \text{otherwise} \end{cases}
$$
Where $\alpha_{i,j}$ is a user-defined weight depending on the specific neighborhood model and the nature of the interaction
 -->

We adopt the following notation for the `mu.MuData` asset. Let:

* **Cell Index Space**: $\mathcal{X} = \{1, \dots, N\}$ be the set of all unique cells.
* **Spatial Coordinates**: Each cell $i \in \mathcal{X}$ be defined by a coordinate vector $x_i$ within the matrix $S \in \mathbb{R}^{N \times D}$: 
$$x_i = \begin{bmatrix} x_{i,1} & x_{i,2} & \dots & x_{i,D} \end{bmatrix}^T \in \mathbb{R}^D$$
where $D \in \{2, 3\}$ denotes the geometric spatial dimensions of the assay.
* **Transcriptomic Profile**: $Y \in \mathbb{R}^{N \times G}$ be the normalized and log-transformed expression matrix across the isolated feature space of $G$ genes.
* **Spatial Graph and Adjacency Matrix**: $G = (\mathcal{X}, \mathcal{E})$ be the spatial graph defined by the adjacency matrix $A \in \mathbb{R}^{N \times N}$ (derived via Liana+), where an edge $e_{ij} \in \mathcal{E}$ exists if cell $i$ and cell $j$ satisfy a localized proximity constraint. The entries $\alpha_{i,j}$ represent the strength or type of interaction:
$$  A_{ij} = \alpha_{i,j} = \begin{cases} \alpha_{i,j} \in [-R, R] & \text{if } (i,j) \in \mathcal{E} \\ 0 & \text{otherwise} \end{cases}$$


Here, $\alpha_{i,j}$ is a user-defined weight parameter dependent on the specific neighborhood model and the nature of the cellular interaction.


### Consolidated Problem Formulation

The fundamental objective of this component is to construct an analytical mapping operator $f$ that partitions the cell space $\mathcal{X}$ into $K$ disjoint cell types $\mathcal{C} = \{C_1, C_2, \dots, C_K\}$, such that:

$$\bigcup_{k=1}^K C_k = \mathcal{X} \quad \text{and} \quad C_a \cap C_b = \emptyset \quad \forall a \neq b$$

Each resolved population $C_k$ is associated with a specific biophysical parameter profile $\theta_k \in \Theta$. 

---

## Implemented Strategies

### Strategy 1: Categorical Pre-annotated Lookup (Baseline)

#### Idea

This strategy assumes that the input dataset has undergone manual curation or reference-based label transfer during prior bioinformatics workflows. The system parses existing categorical strings or numerical identifiers embedded within the metadata slots and directly assigns them to uniform simulation slots.

#### Detailed Algorithmic Implementation

1. **Step 1 (Annotation Key Extraction)**: Query the user-specified configuration key `target_annotation_key` inside the transcriptomics metadata observation frame (`mdata.mod['rna'].obs`).
2. **Step 2 (Direct Mapping)**: Group individual cell indices matching each unique categorical string identifier found in the column array:

$$C_l = \{i \in \mathcal{X} \mid \text{obs}[\text{key}]_i = l\}$$


3. **Step 3 (Knowledge Base Enrichment)**: For each isolated cell-type string $l$, query the **Cell Ontology (CL)** programmatic interface to fetch the standardized structural definition, associated cross-references, and canonical biological pathways. Physical parameter configurations are left as default templates to be adjusted by later physical scaling components.

---

### Strategy 2: Unsupervised Graph Partitioning & Reference Mapping

#### Idea

When raw input datasets do not contain pre-existing labels, this strategy applies graph-based community detection algorithms to find functional cell populations. Once distinct clusters are resolved, the module identifies their highly expressed marker genes and matches them against reference expression databases to assign biological identities.

#### Detailed Algorithmic Implementation

1. **Step 1 (Community Detection)**: Apply the Louvain or Leiden clustering algorithm to the transcriptomic adjacency matrix $A$ to maximize graph modularity $Q$, splitting the cells into $K$ unannotated clusters.
2. **Step 2 (Cluster Size Configuration & Optimization)**: The total cluster count $K$ is controlled via the configuration parameters. The framework supports two operational tracking modes:
   * **Manual Resolution**: A fixed resolution multiplier or target cluster count specified directly in the configuration file.
   * **Automated Optimization**: The system sweeps across a range of resolution values and automatically selects the parameter that maximizes the mean Silhouette width or the network modularity score:

$$Q = \frac{1}{2m} \sum_{ij} \left( A_{ij} - \frac{k_i k_j}{2m} \right) \delta(C_i, C_j)$$

1. **Step 3 (Differential Expression Evaluation)**: For each resolved cluster $C_k$, compute the mean expression vector $\bar{y}_k \in \mathbb{R}^G$ and extract the top ranking overexpressed genes compared to background populations.
2. **Step 4 (Database Reference Alignment)**: Cross-reference the discovered marker gene sets against **PanglaoDB** or **CellMarker** matrices using a cosine similarity score or hypergeometric enrichment test:

$$\text{Score}(k, l) = \frac{\bar{y}_k \cdot R_l}{\|\bar{y}_k\|_2 \|R_l\|_2}$$

Where $R_l$ represents the binary reference vector for cell type $l$ inside the marker database. The cell type with the highest similarity score is assigned to cluster $C_k$.


---

## Considerations 

### Databases for cells annotation

I evaluated five reference knowledge bases for this library. From these, I selected PanglaoDB for implementation due to their seamless integration via Python-native packages. The following tables summarize the most relevant information about these datasets, including curation methodology, sample/tissue volume, and target identification resolution.

<!-- TODO sprwadzite dae jeszcz raz -->

#### 1. Reference Databases for Human (*Homo sapiens*)

| Database | Curation Class | Python Integration Strategy | Tissues / Sub-tissues | Samples | Cells | Clusters | Cell Types | Markers | Primary Literature & Resource Access |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **CellMarker 2.0** | Manual | None (Requires flat file parsing) | 158 | No data | No data | No data | 467 | 13 605 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/36300619/) \| [URL](http://www.bio-bigdata.center/)  |
| **PanglaoDB** | Automatic | External library wrapper (`decoupler`) | 74 | 305 | 1 126 580 | 1 748 | No data | No data | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6450036/) \| [URL](https://decoupler.readthedocs.io/en/latest/notebooks/scell/rna_sc.html) |
| **CellTypist** | Mixed | Native library (`celltypist`) | Multiple organs / Immune atlases | No data | No data | No data | High-resolution multi-tissue models | No data | [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.05.01.538994v1) |
| **DISCO** | Automatic | Programmatic client (`discotoolkit`) | 107 | >4 500 | >18 000 000 (Global & 27 sub-atlases) | No data | No data | No data | [PubMed](https://pubmed.ncbi.nlm.nih.gov/34791375/) |
| **Azimuth (HuBMAP)** | Manual | External tool / CLI (`panhumanpy`) | 23 | No data | No data | No data | 380 unified cell types | No data | [DOI](https://doi.org/10.1016/j.cell.2021.04.048) |

---

#### 2. Reference Databases for Mouse (*Mus musculus*)

| Database | Curation Class | Python Integration Strategy | Tissues / Sub-tissues | Samples | Cells | Clusters | Cell Types | Markers | Primary Literature & Resource Access |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **CellMarker 2.0** | Manual | None (Requires flat file parsing) | 81 | No data | No data | No data | 389 | 9 148 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/36300619/) \| [URL](http://www.bio-bigdata.center/) |
| **PanglaoDB** | Automatic | External library wrapper (`decoupler`) | 184 | 1 063 | 4 459 768 | 8 651 | No data | No data | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6450036/) \| [URL](https://decoupler.readthedocs.io/en/latest/notebooks/scell/rna_sc.html) |
| **CellTypist** | Mixed | Native library (`celltypist`) | Dedicated murine tissue models | No data | No data | No data | Lineage-specific classification models | No data | [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.05.01.538994v1) |
| **DISCO** | Automatic | Programmatic client (`discotoolkit`) | Minimal (Predominantly human-centric) | Minimal | Excluded from primary murine pipelines | No data | No data | No data | [PubMed](https://pubmed.ncbi.nlm.nih.gov/34791375/) |
| **Azimuth (HuBMAP)** | Manual | External tool / CLI (`panhumanpy`) | Selected aging / Motor cortex atlases | No data | No data | No data | Tissue-bounded cell ontologies | No data | [DOI](https://doi.org/10.1016/j.cell.2021.04.048) |

---

#### Methodological Constraint: Targeted Gene Universe Restructuring

When mapping cell identities via statistical enrichment paradigms—specifically the standard hypergeometric distribution test—the evaluation profile must be structurally bounded to prevent systemic false discovery rates.

Let $N$ denote the total background gene universe size, $M$ represent the total number of curated reference marker genes linked to a candidate cell phenotype, $n$ define the total count of significantly overexpressed differential features isolated from the spatial cluster, and $k$ correspond to the size of the overlapping intersect. The formal cumulative probability of observing an alignment equal to or greater than $k$ is formulated as:

$$P(X \ge k) = \sum_{x=k}^{\min(n, M)} \frac{\binom{M}{x} \binom{N-M}{n-x}}{\binom{N}{n}}$$

In targeted, image-based *in situ* spatial transcriptomics platforms (e.g., 10x Xenium, NanoString CosMx, MERSCOPE), the biological feature matrix is bounded by a restricted custom probe panel containing $300 - 1000$ fixed genes, rather than a non-targeted full-transcriptome array ($\sim 20,000$ genes).

**Statistical Violation**: Setting $N \approx 20,000$ (the full genomic scale available in static databases like PanglaoDB or CellMarker) distorts the underlying distribution probability mass. It yields artificially deflated $p$-values and leads to significant false-positive assignments.

**Correction Constraint**: The background universe variable $N$ must be dynamically constrained to exactly match the total count of unique genes present within the targeted physical spatial assay panel ($N = N_{\text{panel}}$). All reference database markers falling outside the explicit boundary of the operational assay panel must be filtered out prior to computing the combinatorial coefficients.


---

## Discussion

### Overcorrection and the Spatial Safety Check

When integrating single-cell or spatial transcriptomics datasets across multiple technical batches or replicates ($s \in S$), a critical trade-off emerges between removing technical variance and preserving true biological architecture. The inclusion of an optional `batch_key` enables alignment algorithms like Batch Balanced K-Nearest Neighbors (BBKNN) to adjust the expression graph topology. However, if applied indiscriminately, these methods introduce a high risk of **overcorrection**, a state where distinct spatial niches or microenvironmental gradients are artificially compressed or forced to mix to minimize batch-specific variance.

#### The Overcorrection Dilemma
Mathematically, the integration optimization problem can be framed as a multi-objective optimization function under tension. Let $BM \in [0, 1]$ represent the normalized batch mixing entropy across all resolved communities $K$, and let $SI \in [0, 1]$ denote the spatial structural invariance metric calculated via the Frobenius norm distance of localized spatial co-occurrence matrices across replicates.

Standard single-cell integration benchmarks typically optimize for a balance between batch clearance and cell-type conservation. In spatial single-cell pipelines, however, we enforce a strict **Defensive Architecture Pattern** (Overcorrection Safety Check) because technical alignment must never happen at the expense of tissue topography.

#### Automated Defensive Guardrail Mechanics
To operationalize this safeguard, the pipeline executes a parallel evaluation graph before committing the final adjacency matrix to the root `mu.MuData` asset. 

1. **Baseline Graph Construction**: Compute the uncorrected global neighbor graph $G_{\text{neigh}}$ using standard principal component projections, yielding a reference spatial structural invariance score $SI_{\text{neighbors}}$.
2. **Integrated Graph Construction**: Compute the batch-balanced graph $G_{\text{bbknn}}$ conditioned on the user-defined `batch_key`, yielding the integrated spatial structural invariance score $SI_{\text{bbknn}}$.
3. **Delta Degradation Evaluation**: Calculate the absolute structural degradation coefficient $\Delta_{\text{spatial}}$:
   $$\Delta_{\text{spatial}} = SI_{\text{neighbors}} - SI_{\text{bbknn}}$$

The execution framework evaluates $\Delta_{\text{spatial}}$ against a strict mathematical degradation tolerance threshold $\theta$:
$$\text{Condition: } \Delta_{\text{spatial}} > \theta$$

If the condition evaluates to true, an automated fallback mechanism triggers. The pipeline rejects the BBKNN graph topology, logs an overcorrection anomaly trace via the centralized logger, and restores the standard $G_{\text{neigh}}$ matrix. This guarantees that spatial niches remain topologically stable across identical tissue environments.

#### Methodological Origins
This defensive paradigm adapts the core validation principles established by the **scIB (single-cell Integration Benchmark)** framework formulated by Luecken et al. (2022) [7]. While the original scIB framework measures biological conservation using transcriptomic silhouettes and cell-type labels, our implementation extends this logic to spatial coordinates by substituting categorical variance tests with a structural matrix distance evaluation over spatial proximity networks derived via Liana+.

### Overcorrection and Batch Integration Caveats in Spatial Contexts

When configuring graph-based downstream pipelines, the selection between a standard global neighborhood graph (`scanpy.pp.neighbors`) and an integrated batch-balanced variant (`scanpy.external.pp.bbknn`) presents a structural trade-off. While the inclusion of a user-defined `batch_key` (such as `sample_id`) is intended to clear non-biological technical variance, executing graph-level batch integration blindly poses an operational risk of **overcorrection** in spatial transcriptomics data.

#### The Risk of Structural Smearing
As established by Polański et al. (2020) [7], Batch Balanced K-Nearest Neighbors (BBKNN) alters the graph construction topology by forcing each cell to find a specific number of neighbors within each designated batch rather than across the global feature space. This graph-level integration is highly efficient for single-cell suspension data; however, in spatial multi-modal assays, true biological spatial gradients or highly localized anatomical niches can easily be misidentified as batch-specific artifacts. 

If different tissue replicates capture slightly shifted morphological zones, forcing a batch-balance constraint across those matrices will artificially mix distinct cell neighborhoods. This effectively flattens continuous spatial diffusion profiles into homogeneous, artificial clusters.


<!-- ```plaintext
#TODO - zarys strategii na kiedyś
[ Raw Multi-Modal Input Matrix ]
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
     [ Standard K-NN Graph ]            [ BBKNN Graph Variant ]
     (scanpy.pp.neighbors)          (scanpy.external.pp.bbknn)
                 │                                 │
                 ▼                                 ▼
     [ Preserves Local Topography ]     [ Forces Cross-Batch Mixing ]
                 │                                 │
                 └────────────────┬────────────────┘
                                  │
                                  ▼
              [ Overcorrection Validation Checkpoint ]
           Is Delta Invariance > Threshold Theta?
                 ├──► YES: Reject BBKNN -> Fallback to Neighbors
                 └──► NO : Accept BBKNN Topology
``` -->

#### Proposed Structural Validation Framework (Implementation Note)
To prevent irreversible data destruction during unsupervised partitioning, it is highly recommended to introduce an independent **Overcorrection Safety Check** layer before committing the graph topology to the final `mu.MuData` registry. Rather than assuming that batch correction is globally optimal, the pipeline should treat it as a **candidate configuration** that must pass spatial structural validation constraints.

A robust mathematical methodology involves measuring the degradation of the spatial co-occurrence profiles between the uncorrected baseline graph $G_{\text{neigh}}$ and the integrated graph $G_{\text{bbknn}}$. Let $SI_{\text{neighbors}} \in [0, 1]$ and $SI_{\text{bbknn}} \in [0, 1]$ represent the spatial invariance scores derived from the Frobenius norms of localized neighborhood density matrices. The integration matrix should only be retained if the structural degradation remains bounded by a strict safety threshold $\theta$:

$$\Delta_{\text{spatial}} = SI_{\text{neighbors}} - SI_{\text{bbknn}} \le \theta$$

If $\Delta_{\text{spatial}} > \theta$, the system should automatically trigger a fallback sequence to the standard neighbor graph to prioritize anatomical truth over technical alignment. This evaluation strategy builds upon the multi-objective benchmarking principles outlined in atlas-level integration paradigms [8], adapted specifically here to protect geometric spatial attributes.
Updated Section: Bibliography


### Strategy 3: Distance-to-Landmark Radial Partitioning

#### Idea
This strategy accounts for continuous spatial gradients driven by major structural tissue landmarks, such as blood vessels, necrotic cores, or tissue boundaries, where cell phenotypes shift as a continuous function of their distance from an anatomical reference. Cells are partitioned into concentric structural zones or shells relative to these markers, allowing for the discrete discretization of continuous microenvironmental gradients (e.g., oxygen, nutrient, or morphogen diffusion profiles) across a spatial axis.

#### Detailed Algorithmic Implementation
1. **Step 1 (Landmark Registration and Multi-Modal Identification)**:
The structural landmark index subset $\mathcal{L}_{\text{ref}} \subset \mathcal{X}$ must be mapped and registered from the experimental coordinate space. Methodologically, landmarks are identified and encoded via two distinct pipelines depending on the upstream data modality:
* *Transcriptomic/Omics Annotation*: Interrogating the multi-modal container (`mdata.mod['rna'].obs`) to isolate specific cellular lineages that form physical barriers or structures. For instance, endothelial cells forming the vasculature network are registered by filtering for established marker genes (e.g., *PECAM1*/*CD31*, *VWF*):
$$\mathcal{L}_{\text{ref}} = \{i \in \mathcal{X} \mid \text{Annotation}_i = \text{'Endothelial'}\}$$
* *Image-Based Segmented Masks (Spatial Proteomics/Histology)*: In spatial assays coupled with co-registered H&E or high-plex immunofluorescence (IF) images, landmarks such as blood vessel lumens, necrotic areas, or fibrous capsules are delineated via computer vision segmentations (e.g., DeepCell, CellPose, or pixel-intensity thresholding). The continuous boundary of the segmented structure is mapped to the coordinate tensor. If the landmark is a hollow structure (e.g., a vessel lumen), $\mathcal{L}_{\text{ref}}$ is operationalized as the set of point coordinates defining the boundary perimeter or the centroid trajectory of that structure in $\mathbb{R}^D$:
$$\mathcal{L}_{\text{ref}} = \{x_{\text{pixel}} \in \mathbb{R}^D \mid x_{\text{pixel}} \in \partial\Omega_{\text{landmark}}\}$$

2. **Step 2 (Distance Transformation Calculation)**:
For every individual cell agent $i \in \mathcal{X}$, compute the shortest Euclidean distance to the nearest point on the registered landmark boundary $\mathcal{L}_{\text{ref}}$:
$$\delta_i = \min_{j \in \mathcal{L}_{\text{ref}}} \|x_i - x_j\|_2$$

This operation yields a continuous distance vector $\Delta \in \mathbb{R}^N$ representing the spatial positioning of the entire cellular cohort relative to the microenvironmental source or sink.

3. **Step 3 (Spatial Radial Discretization)**:
To prevent continuous, high-dimensional parameter spaces from introducing uncalibrated noise into the simulation engine, the continuous vector $\Delta$ is discretized into $B$ disjoint radial zones $\mathcal{Z} = \{Z_1, Z_2, \dots, Z_B\}$ using user-defined physical distance thresholds $[b_0, b_1, \dots, b_B]$, where $b_0 = 0$ and $b_B = \max(\Delta)$:
$$Z_b = \{i \in \mathcal{X} \mid b_{b-1} \le \delta_i < b_b\}$$
This clustering forces cells within the same spatial shell to be aggregated into a uniform, robust operational subpopulation, minimizing individual tracking noise.

4. **Step 4 (Gradient-to-Parameter Profile Mapping)**:
Each radial zone $Z_b$ is mapped to a specific biophysical parameter profile $\theta_b \in \Theta$, where the parameter vector scales as a mathematical function of the mean shell radius $\bar{\delta}_{Z_b}$:
$$\theta_{i \in Z_b} = g(Z_b) = \theta_{\text{base}} \cdot f_{\text{grad}}(\bar{\delta}_{Z_b})$$
where $f_{\text{grad}}$ models the underlying physical phenomenon (e.g., exponential decay for oxygen diffusion $e^{-\chi \delta}$ or linear steps for morphogen signaling). This maps spatial tissue-level structures directly onto discrete, executable agent definitions.

## Bibliography

[1] Da Silva André, G., & Labouesse, C. (2024). Mechanobiology of 3D cell confinement and extracellular crowding. *Biophysical Reviews*, 16, 833–849. https://doi.org/10.1007/s12551-024-01244-z

[2] Zhang, X., Lan, Y., Xu, J., Quan, F., An, E., Ma, L., Luo, J., Meng, Q., Fan, G., Wang, J., & Li, X. (2023). CellMarker 2.0: an updated database of cell marker genes in human and mouse. *Nucleic Acids Research*, 51(D1), D1029–D1036. https://doi.org/10.1093/nar/gkac947

[3] Franzén, O., Gan, L. M., & Björkegren, J. L. (2019). PanglaoDB: a web server for exploration of mouse and human single-cell RNA sequencing datasets. *Database*, 2019, baz046. https://doi.org/10.1093/database/baz046

[4] Domínguez Conde, C., Xu, C., Jarvis, L. B., Rosenberg, I. R., Popescu, D. M., Forster, A. M., ... & Teichmann, S. A. (2022). Cross-tissue immune cell analysis reveals tissue-specific features in humans. *Science*, 376(6594), eabl5197. https://doi.org/10.1126/science.abl5197

[5] Li, Z., Lin, W., Liu, J., Ding, W., Wang, S., Rong, X., ... & Chen, J. (2022). DISCO: a database of deep single-cell omics data for exploration of human immunology and diseases. *Nucleic Acids Research*, 50(D1), D1054–D1063. https://doi.org/10.1093/nar/gkab1022

[6] Hao, Y., Hao, S., Andersen-Nissen, E., Mauck, W. M., Zheng, S., Frangieh, C. J., ... & Satija, R. (2021). Integrated analysis of multimodal single-cell data. *Cell*, 184(13), 3573-3587. https://doi.org/10.1016/j.cell.2021.04.048

[7] Polański, K., Young, M. D., Miao, Z., Meyer, K. B., Tegner, J., & Teichmann, S. A. (2020). BBKNN: fast and scalable batch-effect correction for single-cell RNA-seq data. *Bioinformatics*, 36(3), 964–965. https://doi.org/10.1093/bioinformatics/btz625

[8] Luecken, M. D., Büttner, M., Chaichoompu, K., Danese, A., Interlandi, M., Mueller, M. F., ... & Theis, F. J. (2022). Benchmarking atlas-level data integration in single-cell genomics. *Nature Methods*, 19(1), 31-41. https://doi.org/10.1038/s41592-021-01336-8