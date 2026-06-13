# Input/Output (IO) Module

## Introduction

### Abstract Functionality

The `io` module is responsible for the integration, harmonization, and annotation of multi-modal omics datasets. **Crucially, this module exclusively operates on and handles high-dimensional `mu.MuData` containers; it does not natively support or process individual `anndata.AnnData` objects at its top-level entry points.** Its primary objective is to take disparate data layers (such as single-cell transcriptomics and spatial profiling matrices), execute cross-modality barcode synchronization via mathematical inner joins, and automatically enrich the unified container with curated intercellular communication metrics (`LIANA+`) and signed, directed intracellular signaling networks (`OmniPath`).

### Structure

The exact directory layout of the `io` module is structured as follows:

```plaintext
maxi7524@DESKTOP-NKT8D63:~/repositories/project_computational_biology_initial_conditions_pymyboss/src/OmniPhysiBoSS/io$ tree
.
├── __init__.py
└── mdata
    ├── __init__.py
    ├── mdata_pipeline.py
    └── utils
        ├── signalling_pathways
        │   ├── __init__.py
        │   ├── intracelluar_network.py
        │   └── ligand_receptor_annotation.py
        ├── spatial
        │   ├── __init__.py
        │   └── liana_multimodal_pipeline.py
        ├── unify
        │   ├── __init__.py
        │   ├── unify_modalities.py
        │   └── validate_unify_modalities_overlap_failure.py
        └── validate
            ├── __init__.py
            ├── mdata_types.py
            └── mdata_validator.py

```

Detailed functional responsibilities of each module and script:

* `io/__init__.py`: Initializes the top-level input/output namespace.
* `io/mdata/__init__.py`: Exposes the public API for multi-modal processing, specifically binding the main facade function `run_mdata_processing_pipeline`.
* `io/mdata/mdata_pipeline.py`: Contains the core execution pipeline framework. It orchestrates the entire workflow by sequentially invoking data remapping, subset harmonization, neighbor graph calculations, and network injection modules.
* `io/mdata/utils/signalling_pathways`: Sub-package dedicated to external molecular database interactions and biological network curation.
* `intracelluar_network.py`: Implements `fetch_intracellular_pathway_network`, which programmatically queries OmniPath to pull down, filter, and format directed, signed signaling interaction cascades (kinase/phosphatase and transcription factor downstream networks).
* `ligand_receptor_annotation.py`: Implements `fetch_liana_interactions`, which cross-references computed cell-cell communication outputs with deep structural interaction metadata attributes sourced from external repositories.


* `io/mdata/utils/spatial`: Sub-package handling spatial neighborhood graphs and multi-scale localized calculations.
* `liana_multimodal_pipeline.py`: Implements `run_liana_multimodal_pipeline`, executing cell-to-cell contact and neighborhood communication modeling (bivariate cross-correlation engine) using `LIANA+` constraints.


* `io/mdata/utils/unify`: Sub-package responsible for rigorous matrix alignment and index synchronization.
* `unify_modalities.py`: Implements `unify_multimodal_data`, performing a strict mathematical intersection (inner join) across distinct single-cell modalities to guarantee identical cellular tracking arrays.
* `validate_unify_modalities_overlap_failure.py`: Implements `validate_separated_modalities_overlap`, providing diagnostic auditing tools to identify exactly which omics layer acts as a complete bottleneck when overlapping cell counts drop to zero.


* `io/mdata/utils/validate`: Sub-package reserved for structural layout assertions and schema evaluation.
* `mdata_types.py`: Defines `OMNI_PHYSIBOSS_SCHEMA` and `EXPECTED_TYPE_SIGNATURES` which formalize required data frames, slot labels, and mandatory cell-level annotation flags.
* `mdata_validator.py`: Implements `verify_structural_presence` to check the validity of individual slots and metadata blocks prior to pipeline initialization.



### Execution Pipeline

Access to the functionalities within this module follows a strict architectural hierarchy. The outer namespace (`io.mdata`) intentionally exposes only a single functional entry point: the `run_mdata_processing_pipeline` orchestration facade. All underlying algorithmic steps, data mutation tools, and external client scripts are encapsulated within the `utils` directory. Users wishing to run specific sub-steps or fine-grained transformations must explicitly navigate through the internal namespace (e.g., `OmniPhysiBoSS.io.mdata.utils.unify`).

The step-by-step sequential data flow within the execution potok proceeds as follows:

```plaintext
             Input: Raw unaligned mu.MuData Container
                                ↓
           Remapping of Custom Multi-Modal Key Layouts
                                ↓
            Resolution of Active Computational Modalities
                                ↓
        [Bypassed / Validation Fault Detection Phase]
         Structural Integrity Checking (mdata_validator)
                                ↓
         Mathematical Matrix Intersections (unify_multimodal_data)
                                ↓
     Spatial Neighborhood Graph & Adjacency Calculations (LIANA+)
                                ↓
      Remote Extraction of Intracellular Networks (OmniPath)
                                ↓
     Intercellular Ligand-Receptor Coordinate Annotation
                                ↓
        Global Structure State Re-indexing (mudata.update())
                                ↓
           Output: Fully Aligned & Annotated MuData Asset

```

#### Technical Debt & Validation Warnings:

> ⚠️ **CRITICAL DEVELOPMENT NOTE:** The structural validation submodule located at `io/mdata/utils/validate/mdata_validator.py` **is currently non-functional**. The function `verify_structural_presence` behaves too rigidly, triggering false-positive structural mismatch exceptions and rejecting valid multi-modal inputs even when required data slots are present. As a temporary workaround, this validation stage has been explicitly commented out and disabled within the main execution routine (`mdata_pipeline.py`). Users are fully responsible for manually auditing and ensuring structural layout consistency across their input `MuData` modalities before executing the potok.

## Submodule Specifications

### mdata_pipeline

```{eval-rst}
.. automodule:: OmniPhysiBoSS.io.mdata.mdata_pipeline
   :members:
   :undoc-members:
   :show-inheritance:

```

### unify_modalities

```{eval-rst}
.. automodule:: OmniPhysiBoSS.io.mdata.utils.unify.unify_modalities
   :members:
   :undoc-members:
   :show-inheritance:

```

### liana_multimodal_pipeline

```{eval-rst}
.. automodule:: OmniPhysiBoSS.io.mdata.utils.spatial.liana_multimodal_pipeline
   :members:
   :undoc-members:
   :show-inheritance:

```

### intracelluar_network

```{eval-rst}
.. automodule:: OmniPhysiBoSS.io.mdata.utils.signalling_pathways.intracelluar_network
   :members:
   :undoc-members:
   :show-inheritance:

```

### ligand_receptor_annotation

```{eval-rst}
.. automodule:: OmniPhysiBoSS.io.mdata.utils.signalling_pathways.ligand_receptor_annotation
   :members:
   :undoc-members:
   :show-inheritance:

```

## Developer & Modification Guide

### Usage blueprint

The following blueprint demonstrates how to correctly initialize and run the public processing pipeline via the programmatic API:

```python
import mudata as mu
from OmniPhysiBoSS.io.mdata.mdata_pipeline import run_mdata_processing_pipeline

# Import an unaligned, multi-modal container asset
mdata_raw = mu.read("raw_experimental_data.h5mu")

# Execute the integrated multi-modal synchronization and enrichment pipeline
processed_mdata = run_mdata_processing_pipeline(
    mdata=mdata_raw,
    modalities=["rna", "spatial"],
    main_modality="rna",
    liana_uns_key="liana_res",
    intercell_output_key="intercellular_metadata_registry",
    intracellular_output_key="omnipath_intracellular"
)

# The returned processed_mdata object features synchronized observation names
# and has network annotation registries seamlessly injected inside .uns slots

```

### Tests

> 🚧 **PROJECT STATUS NOTE:** The unit tests and automation testing frameworks for the mathematical data transformations, inner-join compliance validations, and external API retrieval states within the `io` module **have not been implemented yet**. Writing complete test suits for matrix intersection invariants and mock network behaviors remains an active task for future development.