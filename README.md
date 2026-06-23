# OmniPhysiBoSS

> ⚠️ **Project Status Notice:** This library is **not fully completed**. Active development on the dynamic translation of high-dimensional transcriptomic states into functional MaBoSS phenotype vertices is currently halted due to methodological constraints in deriving time-dependent phenotype transitions from static scRNA-seq datasets. However, the structural core, including physical spatial domain mappings, coordinate translations, and omics data parsing layouts—is fully functional and preserved.

***

## Introduction

Standard multi-scale computational models within the PhysiCell and PhysiBoSS simulation suites are traditionally constructed using parameter values derived from generic literature sources to replicate generalized cell behaviors. While these models allow researchers to simulate external perturbations, such as drug administrations, to observe whether a specific stimulus inhibits a particular biochemical pathway, they possess a critical methodological limitation: they do not reflect the unique physical or molecular state of a specific organism, nor do they capture downstream disruptions across collateral signaling pathways and their collective impact on tissue morphology.

The **OmniPhysiBoSS** library extends the capabilities of the PhysiBoSS simulator by automating patient-specific model personalization and parameterization using multi-modal single-cell and spatial transcriptomics datasets. By anchoring agent initial conditions directly within raw spatial tissue geometry and high-throughput molecular footprints, the framework provides a structured pipeline to translate static experimental datasets into reproducible multi-scale simulations.

### Short Description

OmniPhysiBoSS is a Python library designed to programmatically generate, configure, and orchestrate multi-scale PhysiBoSS models directly via an automated API. The framework streamlines the initialization of agent-based microenvironments by unifiying cellular and spatial data layers. It establishes programmatic infrastructure to construct intracellular logic models (MaBoSS) and resolve cell-cell signaling interactions from scratch, leveraging state-of-the-art reference data from OmniPath and decoupleR.

### Key insights 

* **Programmatic Model Configuration:** Complete generation and initialization of structured PhysiCell and PhysiBoSS XML, BND, and CFG configuration assets directly from native Python data structures.
* **Modular Pipeline Architecture:** A decoupled design pattern that allows developers to modify, override, or replace individual computational steps (such as domain extraction or normalization) without disrupting the global pipeline orchestration.
* **Spatial Invariant Ingestion:** Automated translation of high-resolution pixel coordinates into physical micrometer coordinates based on spatial technology dimensions (e.g., Visium spot diameter properties).

### Goal & Motivation

My motivation was to create models that simulate inter-cellular communication on given single-cell spatial data. I utilized the state-of-the-art `PhysiBoSS` model to simulate the environment and isolate the functional components responsible for establishing initial conditions based on several biological modalities. 

The primary objective of OmniPhysiBoSS is to orchestrate intercellular and intracellular communication networks within highly resolved spatial single-cell datasets. By integrating agent-based environments with functional omics footprints (decoupleR, LIANA+, OmniPath), the framework automates the generation of baseline constraints, initial cellular states, and spatial initial conditions across distinct tissue modalities.

***

## Table of Contents
- **[Io Formats](docs/explanations/io_formats/README.md)**
  - [Maboss Configuration Format](docs/explanations/io_formats/maboss_configuration_format.md)
  - [Physicell Configuration Format](docs/explanations/io_formats/physicell_configuration_format.md)
  <!-- - [Physicell Output Format](docs/explanations/io_formats/physicell_output_format.md) 
  #TODO - this will be after all analysis will be completed-->
- **[Methodology](docs/explanations/methodology/README.md)**
  - [Cell Types](docs/explanations/methodology/cell_types.md)
  - [Component Docs Template](docs/explanations/methodology/component_docs_template.md)
  - [Domain Type](docs/explanations/methodology/domain_type.md)
  - [Overall Type](docs/explanations/methodology/overall_type.md)
- **[Modules](docs/explanations/modules/README.md)**
  <!-- - [Configuration Module](docs/explanations/modules/configuration_module.md)
  #TODO - this one is depracated, we will implement other version based on schema file. -->
  - [Io Module](docs/explanations/modules/io_module.md)
  - [Models Module](docs/explanations/modules/models_module.md)
  - [Module Docs Template](docs/explanations/modules/module_docs_template.md)
  <!-- - [Wrappers Module](docs/explanations/modules/wrappers_module.md) 
  #TODO - depracated, now we are using other library for this management-->


*** 

<!-- ## Technical Documentation & Methodology Core -->
## Documentation 

For detailed guidelines, implementation details, and theoretical background, navigate to the respective documentation sections below:

- **[Modules](./docs/explanations/modules/README.md)**: Contains a comprehensive technical description of the implemented library modules. It explains the architectural design, internal code construction, and provides explicit instructions on how to modify or extend the codebase.
- **[I/O Formats](./docs/explanations/io_formats/README.md)**: Serves as a developer-focused reference for debugging and system configuration. It specifies exact specifications for input and output data structures, detailing the files involved in the analysis pipeline (including parsing mechanisms, schema definitions, and expected formats).
- **[Methodology](./docs/explanations/methodology/README.md)**: Combines the formal theoretical foundation of the problem with a detailed rationale behind our specific implementation. It explains the mathematical or biological modeling abstractions selected and justifies the algorithmic execution flow.

## Installation & usage

### Tutorials & reproduction

To learn how to use library go to `docs/tutorials/introduction_to_omniphysiboss.md.md`

To reproduce results from `report.pdf` go to  `docs/how_to/base_model-reproduction.md`

***

<!-- ### comprehensive  explanation of documentation & methodology

#TODO Here is explanations folder brief summary -->


### Environment setup and activation

To use repository you first need to clone it and instantiate environment as follows:

```bash
# create `OmniPhysiBoss_env` environment 
micromamba create -f workflow/envs/environment.yaml -y

# Installs the local OmniPhysiBoss package 
pip install -e .           

# activation of new environment
micromamba activate OmniPhysiBoss_env 
```

> REMARK - developer: If you want to change repository i advice you to install addiotnal dependencies:
> ```bash
> pip install -e .[docs]
> ```
>

Then you need to install PhysiCell offical repository and link it. Script below does it automatically from my forked repository to ensure version compatibility.

```bash
# run script that clone OmniPhysiBoSS repository and sets it checked version
# REMARK: it takes around ~ 1-2gb of memory 
# REMARK: do not move this file, it searches repo clone base on its position in repository folder.  
python resources/scripts/utils/install_OmniPhysiBoSS.py
```

> REMARK - everyone: Do not clone OmniPhysiBoSS separately. If commits would change critical paths (f.e. compilation files) whole script will broke. 

To be able to perform analysis you also need to download [panglaoDB markbers database](https://panglaodb.se/index.html), and [go-basic database](https://geneontology.org/docs/download-ontology/) . You can use scripts below. It will automatically move it to `resources/databases` folder. 

```bash
# panglaoDB markbers database
bash resources/scripts/download/download_panglaoDB.sh 
# go-basic database
bash bash resources/scripts/download/download_go-basicDB.sh 
```



### Resource Requirements & Deployment Timeline
The installation requires **3.1 – 3.7 GB** of disk space and takes approximately **13 – 25 minutes** to complete, depending on your network speed and CPU performance.

| Component | Est. Size | Description |
| --- | --- | --- |
| **Micromamba Env** | 1.8 – 2.2 GB | Python 3.12, Snakemake, C++ toolchains. |
| **Omics Deps** | 0.8 – 1.1 GB | `scanpy`, `anndata`, `liana`, `decoupler`. |
| **PhysiBoSS Engine** | ~0.4 GB | Source code & compiled binaries. |


***

## Contributing

Contributions to OmniPhysiBoSS are welcome. Please read `CONTRIBUTING.md` for detailed instructions regarding our dewatering environment setup, code formatting standards, and testing suites.

### Academic Attributions & Citations

If you use OmniPhysiBoSS in your research, please cite this framework alongside the foundational upstream multi-scale engines :

<!-- * **OmniPhysiBoSS (This Framework):** Stróżyk M, et al. (2026). OmniPhysiBoSS: Programmatic Generation and Orchestration of Multi-Scale Spatial Boolean Microenvironment Models. -->
* **PhysiBoSS (Multi-Scale Core Engine):** Ponce-de-Leon M, et al. *Bioinformatics*, 2023. DOI: [10.1038/s41540-023-00314-4](https://doi.org/10.1038/s41540-023-00314-4) .
* **PhysiCell (Spatial Agent-Based Framework):** Ghaffarizadeh A, et al. *PLoS Computational Biology*, 2018. DOI: [10.1371/journal.pcbi.1005991](https://doi.org/10.1371/journal.pcbi.1005991) .
* **MaBoSS (Continuous-Time Boolean Core):** Stoll G, et al. *Bioinformatics*, 2017. DOI: [10.1093/bioinformatics/btx139](https://doi.org/10.1093/bioinformatics/btx139) .
* **decoupleR (Footprint Phenotype Inference):** Badia-i-Mompel J, et al. *Bioinformatics Advances*, 2022. DOI: [10.1093/bioinformaticsadvances/vbac016](https://doi.org/10.1093/bioinformaticsadvances/vbac016) .
* **LIANA+ (Intercellular Communication):** Dimitrov D, et al. *Bioinformatics*, 2022. DOI: [10.1093/bioinformatics/btac286](https://doi.org/10.1093/bioinformatics/btac286) .

***

## Author
**Max Stróżyk** - University of Warsaw

<!-- ## License
#TODO - add when library is finished -->

