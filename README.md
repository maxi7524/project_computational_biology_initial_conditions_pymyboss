
# OmniPhysiBoSS

***

## Introduction

#TODO - poprawić sekcje 

### Short description

#TODO POPRAWIĆ 

OmniPhysiBoSS is library which creates `PhysiBoSS` models based on given configuration. It allows to create models for `PhysiBoSS` from scratch in by using python code. Repository also contains prepared pipeline to for simulating spatial-sc tissue (#TODO - to co przewiduja te modele...) which, were i created of maboss models and intercelluar communication, from scratch based on `Omnitpath` and `decoupleR` references.  

OmniPhysiBoSS is a Python library designed to programmatically generate and configure multi-scale PhysiBoSS models. It enables to construct complex agent-based models from scratch directly via Python code. The repository also includes a streamlined execution pipeline for simulating single-cell tissue dynamics. 
#TODO - porawić
This pipeline automates the generation of Boolean intracellular networks (MaBoSS) and intercellular signaling interactions by leveraging state-of-the-art reference data from OmniPath and decoupleR .

### Key insights 

- (#TODO - later) - Integration with `PhysiBoSS` via python code allowing to:
  - ...
  -fds
- basic model for sc-spatial simulations, allowing to examine possible states / outcomes of tissue fragment

- **Pythonic Model Generation:** Native programmatic interaction with the PhysiBoSS C++ core engine, eliminating the need for manual XML configuration.
- **Multi-Scale Spatial Simulations:** Modeling framework to evaluate tissue-level behaviors, state transitions, and spatial cellular patterns from single-cell transcriptomics data.


### Goal & Motivation

My motivation was create models, which simulates inter-cellular communication on given sc-spatial data. I used already state-of-art model `PhysiBoSS` to simulate environment and figure out part responsible for giving initial conditions, based on several modalities, that is:
-( #TODO - later tutaj muszę wypisać ponieważ ta część nie jest jeszcze gotowa) 

The primary objective of OmniPhysiBoSS is to orchestrate intercellular and intracellular communication networks within highly resolved spatial single-cell datasets . By integrating state-of-the-art agent-based environments (PhysiCell/PhysiBoSS) with functional omics footprints (decoupleR, LIANA+, OmniPath), the framework automates the generation of baseline constraints, initial cellular states, and spatial initial conditions across distinct tissue modalities.

<!-- Tutaj est to lepiej napisne   -->



***

## Table of contents 

#TODO - do it with markdown-toc generator 

*** 

<!-- ## Technical Documentation & Methodology Core -->
## Documentation 

For detailed guidelines, implementation details, and theoretical background, navigate to the respective documentation sections below:

- **[Modules](./resources/docs/explanations/modules/README.md)**: Contains a comprehensive technical description of the implemented library modules. It explains the architectural design, internal code construction, and provides explicit instructions on how to modify or extend the codebase.
- **[I/O Formats](./resources/docs/explanations/io_formats/README.md)**: Serves as a developer-focused reference for debugging and system configuration. It specifies exact specifications for input and output data structures, detailing the files involved in the analysis pipeline (including parsing mechanisms, schema definitions, and expected formats).
- **[Methodology](./resources/docs/explanations/methodology/README.md)**: Combines the formal theoretical foundation of the problem with a detailed rationale behind our specific implementation. It explains the mathematical or biological modeling abstractions selected and justifies the algorithmic execution flow.

## Installation & usage

### Tutorials & reproduction

To learn how to use library go to `docs/tutorials/introduction_to_omniphysiboss.md.md`

To reproduce results from `report.pdf` go to  `docs/how_to/base_model-reproduction.md`

***

### comprehensive  explanation of documentation & methodology

<!-- Here is explanations folder brief summary -->

#TODO - napisć żę dokładnie to jest opisane tam i tam 

### Environment setup and activation

To use repository you first need to clone it and instantiate environment as follows:

```bash
# create `OmniPhysiBoss_env` environment 
micromamba create -f workflow/envs/environment.yaml -y

# Installs the local OmniPhysiBoss package 
pip install -e .           

# activation of new environment
micromamba activate OmniPhysiBoss_env 

# run script that clone OmniPhysiBoSS repository and sets it checked version
python scripts/utils/install_OmniPhysiBoSS.py
```

> REMARK - everyone: Do not clone OmniPhysiBoSS separately. If commits would change critical paths (f.e. compilation files) whole script will broke. 

> REMARK - developer: If you want to change repository i advice you to install addiotnal dependencies:
> ```bash
> pip install -e .[docs]
> ```
>

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

* **OmniPhysiBoSS (This Framework):** Stróżyk M, et al. (2026). OmniPhysiBoSS: Programmatic Generation and Orchestration of Multi-Scale Spatial Boolean Microenvironment Models.
* **PhysiBoSS (Multi-Scale Core Engine):** Ponce-de-Leon M, et al. *Bioinformatics*, 2023. DOI: [10.1038/s41540-023-00314-4](https://doi.org/10.1038/s41540-023-00314-4) .
* **PhysiCell (Spatial Agent-Based Framework):** Ghaffarizadeh A, et al. *PLoS Computational Biology*, 2018. DOI: [10.1371/journal.pcbi.1005991](https://doi.org/10.1371/journal.pcbi.1005991) .
* **MaBoSS (Continuous-Time Boolean Core):** Stoll G, et al. *Bioinformatics*, 2017. DOI: [10.1093/bioinformatics/btx139](https://doi.org/10.1093/bioinformatics/btx139) .
* **decoupleR (Footprint Phenotype Inference):** Badia-i-Mompel J, et al. *Bioinformatics Advances*, 2022. DOI: [10.1093/bioinformaticsadvances/vbac016](https://doi.org/10.1093/bioinformaticsadvances/vbac016) .
* **LIANA+ (Intercellular Communication):** Dimitrov D, et al. *Bioinformatics*, 2022. DOI: [10.1093/bioinformatics/btac286](https://doi.org/10.1093/bioinformatics/btac286) .

***

## Author
**Max Stróżyk** - University of Warsaw

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

