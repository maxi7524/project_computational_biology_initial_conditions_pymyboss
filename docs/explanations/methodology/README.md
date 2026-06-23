# Methodology overview

This document formalizes the multiscale theoretical frameworks, modeling assumptions, and mathematical abstractions implemented across the **OmniPhysiBoSS** environment.

## Introduction

### Multiscale Computational Paradigm
The primary objective of the **OmniPhysiBoSS** framework is to bridge the scale gap between high-dimensional static observation spaces (multi-omics tissue profiling) and dynamic multicellular simulation environments. High-throughput single-cell assays capture high-resolution genomic snapshots but lack predictive spatial-temporal continuity. Conversely, agent-based physical modeling suites (such as PhysiCell) simulate mechanical interactions and nutrient diffusion across realistic temporal states but lack personalized, data-driven parameterization layers.

By projecting cross-modality coordinates and molecular networks into spatialized agent parameters, this framework provides a continuous translation interface. The mathematical blueprints detailed within this methodology subdirectory formalize how micro-scale molecular configurations dictate macro-scale cell behaviors.

For specific implementation blueprints of individual software assets, see the programmatic modules documentation in [Models Module](../modules/models_module.md).

***

## Core concepts 

### Introduction to Multiscale Inference
To construct a predictive model of tissue dynamics, the model must concurrently evaluate independent operational layers. We decouple biological complexity into two fundamental physical scales: *intracellular regulatory logic* and *extracellular spatial mechanics*.

#### Intracellular Communication
We leverage Boolean networks to simulate downstream intracellular signaling cascades and transcription factor regulatory logic. 
* **Prior Knowledge Representation**: Boolean formalisms allow the integration of directed topologies from curated database repositories (e.g., OmniPath). This serves as structural prior knowledge of the biological system.
* **Discrete State Dynamics**: By mapping high-dimensional expression matrices to binary states, we capture robust regulatory profiles without requiring explicit, uncalibrated kinetic reaction constants ($k_{\text{cat}}$, $K_m$), which are generally unobservable in spatial transcriptomics assays.

#### Extracellular Communication
Extracellular interactions are governed by discrete agent-based physical heuristics.
* **Probabilistic Micro-environments**: Due to missing kinetic data and structural stochasticity at the multicellular scale, cellular actions (such as phenotypic transitions or local boundary secretions) are modeled by probabilistic models.
* **Heuristic Robustness**: Incorporating probabilistic change matrices prevents the underuse of prior biological knowledge and avoids underestimating the stochastic complexity of micro-environmental spatial dynamics.

#TODO - sprawdzic, poprawić na końcu jeszcze 

***

## Components

The framework is subdivided into modular **independent** components.  

### 1. [Cell Type Lineage Aggregation Model](cell_types.md)
To instantiate a multiscale agent-based model, arbitrary cellular phenotypes identified in an experiment must be mapped to distinct agent types characterized by deterministic physical and mechanical constraints. 

Rather than manually defining properties for individual agents, we treat experimental cell clusters as statistical populations. By analyzing the spatial distributions and coordinate boundaries of these populations *in situ*, we derive descriptive geometrical properties relative to spatial packing densities.

***

### next component ... 
(#TODO - here next components will be described) 

***

### Summary Graph
```plaintext
#TODO: Insert an interactive spatial-operational workflow graph mapping experimental input states to executable methodology documentation.
```

***

## Results

```plaintext
#TODO: Implement a centralized bibliography schema.
# Dev Note: Evaluate Sphinx-Natbib or a top-level unified BibTeX (.bib) architecture cross-referenced via Sphinx {cite} directives across individual markdown files.
```

***

## Bibliography 
#TODO create common bibliography accross all docs. 

