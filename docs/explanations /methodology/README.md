# Methodology of base model 
#TODO - o czym jest w docsie 

***

## Core concepts 

### Introduction to topic 
#### Intracellular communication
Here also briefly, maybe another docs to which it would be pointing for comprehensive explanation
#### Extracellular communication 

### My methodology summary 

#### Part 1
...

#TODO here briefly


***

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

