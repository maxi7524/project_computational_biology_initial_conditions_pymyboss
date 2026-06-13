


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

#TODO 
Rather than manually defining properties for individual agents, we treat experimental cell clusters as statistical populations. By analyzing the spatial distributions and coordinate boundaries of these populations *in situ*, we derive descriptive geometrical properties (e.g., scaling baseline adhesion factors $\gamma_{\text{adhesion}}$ relative to spatial packing densities).

### 2. [Intracellular Boolean Network Mapping Component](intracellular_boolean.md) #TODO
* **Focus**: Parsing directed topologies into executable Boolean update logic for individual agent configurations.

### 3. [Extracellular Diffusion & Secretion Component](extracellular_diffusion.md) #TODO
* **Focus**: Deriving spatial partial differential equation (PDE) source/sink terms from localized ligand-receptor cross-correlations.


***

### next component ... 

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
#TODO czy da się współną bibliografie tutaj wgrywać jakoś na różne docsy ??





# DEPRACATED 
# Methodology of base model DEPRACATED
#TODO - o czym jest w docsie 


## Graph representation of analysis

#TODO - tak samo ja w methods, tylko że ttua jbędziemy dodawać sekcje z wyytłumaczenie oc się dzieje co uzyskujemy, jakie założenia tutaj są itd. 

### każdy krok po kolei (tytuł kroku oraz link do dokładniejszego wytłumaczenia)  
#TODO wstępne wytłumacznie 

### Signaling pathways

#### wstęp 

W wieloskalowym modelowaniu populacji komórkowych (takim jak połączenie platform PhysiCell i MaBoSS), zachowanie pojedynczego agenta zależy bezpośrednio od informacji odbieranych z jego otoczenia przestrzennego. Podejście to wymaga sformalizowanego mechanizmu pośredniczącego, który potrafi przełożyć ciągłe, zewnątrzkomórkowe pola stężeń ligandów lub sparowane korelacje dwuwymiarowe (bivariate) na dyskretne stany wewnątrzkomórkowych sieci logicznych.  Moduł szlaków sygnałowych (signaling_pathways) implementuje to zadanie poprzez reprezentację bazy wiedzy biologicznej jako skierowanego grafu topologicznego. Pozwala to na ścisłe i powtarzalne odnalezienie kaskad przekazywania sygnału łączących zidentyfikowane receptory z fenotypowymi punktami końcowymi modelu logicznego.  

#### Model Matematyczny

Niech baza interakcji molekularnych będzie reprezentowana jako skierowany graf wiedzy $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, gdzie $\mathcal{V}$ oznacza zbiór encji molekularnych (ligandów, receptorów, kinaz, czynników transkrypcyjnych oraz fenotypów), a $\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$ oznacza zbiór skierowanych krawędzi reprezentujących oddziaływania przyczynowo-skutkowe (aktywacje lub inhibicje).  Niech $\mathcal{P}_{\text{LR}}$ oznacza zbiór przestrzennie aktywnych par ligand-receptor wyekstrahowanych z potoku LIANA+. Definiujemy zbiór aktywnych receptorów wejściowych $\mathcal{R} \subset \mathcal{V}$ jako:  $$\mathcal{R} = \{r \in \mathcal{V} \mid \exists l \in \mathcal{V} \text{ s.t. } (l, r) \in \mathcal{P}_{\text{LR}}\}$$Dla zdefiniowanego przez użytkownika zbioru węzłów docelowych sieci Boolean $\mathcal{T} \subset \mathcal{V}$ (reprezentujących mierzalne punkty kontrolne fenotypu komórkowego, takie jak $\mathcal{T} = \{\text{Apoptosis}, \text{Survival}\}$), moduł oblicza zbiór wszystkich prostych ścieżek skierowanych $\mathcal{P}(r, t)$ o maksymalnej głębokości (odległości topologicznej) $\Lambda \in \mathbb{Z}^+$:  $$\mathcal{P}(r, t) = \left\{ (v_0, v_1, \dots, v_m) \mid v_0 = r, \, v_m = t, \, (v_k, v_{k+1}) \in \mathcal{E}, \, m \le \Lambda \right\}$$Wyekstrahowany podgraf $\mathcal{G}_{\text{sub}} = (\mathcal{V}_{\text{sub}}, \mathcal{E}_{\text{sub}})$, gdzie $\mathcal{V}_{\text{sub}} = \bigcup \mathcal{P}(r, t)$, stanowi zintegrowaną mapę topologiczną, która posłuży do automatycznej syntezy równań logicznych pliku .bnd.  Implementacja Komponentu: SignalingPathwaysComponentPoniższy kod implementuje klasę SignalingPathwaysComponent dziedziczącą po klasie abstrakcyjnej ModelComponent. Zgodnie z wytycznymi, cały kod źródłowy, nazwy oraz dokumentacja Sphinx zostały napisane w języku angielskim, a komentarze zachowują ścisłą hierarchię strukturalną. 

UWAGA
Ta topologia o odległość topologiczna będzie definiowana o tą metryke z liany, że bierze pod uwagę iloczyn skalarny ekspresja (L, R) oraz razy wartość tej odległości czy jakos tak


#### ten skrypt `archetype_interface_profiler.py` (ta nazw aw tytukle jest docelowa) i klasa `ArchetypeInterfaceProfiler`
Yes, ligand-receptor pairs must be explicitly included and filtered at this first stage. To effectively manage complexity downstream, we cannot simply look at highly expressed genes in isolation. We must intersect the spatial cross-correlation metrics from LIANA with the cell-type deconvolution matrices.To filter out non-critical pathways immediately, the selection is restricted using two strict criteria:Spatial Significance: Selecting only the top $N$ interactions sorted by their mean spatial similarity score (e.g., Cosine mean) or statistical significance ($p \le 0.05$).  Cellular Expression Breadth: Ensuring that the ligand or receptor is expressed by a minimum threshold percentage (e.g., $\ge 10\%$) of cells within that specific cell archetype cluster.Here is the implementation of the first standalone module, interface_isolator.py, conforming strictly to the ModelComponent abstraction boundary



