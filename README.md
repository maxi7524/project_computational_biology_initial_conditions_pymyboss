



# Cel projektu

Chcemy stworzyć narzędzie które mapuje wyniki z LIANA+ (to jest mamy tutaj regulacje ich istotność itd.) na warunki początkowe pymyboss'a.

Będziemy chcieli to zrobić w kontekście klas komórek (bez danych przestrzennych) i z danymi przestrzennymi, wtedy będziemy uwzględniali dynamikę układu cząstek. CHcielibyśmy wtedy móc załadować taki układ. 



# Struktura biblioteki 

1. Inicjalizacja obiektu
   0. Podajemy mu adata z informacjaprzestrzenną oraz wyliczonymi parami ligand receptor (będziemy całość symulować na jakimś zbiorze)
   1. Podajemy mu informacje w jakims obiekcie w unstructured data znajduje się ten element
2. Zdefiniowanie modelu / konfiguracja ustawień
   1. MaBoss
      - Jaki model, to jest jakie pary ligand receptor będziemy brali pod uwagę:
        - Wgrywamy istniejacy model / modele i tylko te związki i szlaki bierzemy pod uwagę
        - robimy jakąś metodę która przeszukuje istniejące modele żeby wszysktie liczyć na raz (to nie jest aż takie złożone, ponieważ wszystkie te modele uruchamiamy naraz, NIEZALEŻNIE (ponieważ są to inne szlaki metaboliczne/sygnałowe))
   2. Informacja przestrzenna 
      - Ustalić jakie metryki i ustawienia będziemy stosować w przypadku korzystania z liany 
      - Tutaj jest to ważne ponieważ na podstawie tych informacji przestrzennych skonstruujemy zależności pomiędzy kolejnymi komórkami
   3. Konfiguracja lagów:
      - Zdefiniować w jaki sposób lagi będą konstruowane, muszą one brać pod uwagę i odległość przestrzenną i zależności znane już z "powszechnej wiedzy"
3. Ewaluacja
    1. Badany obszar
      - Nie jesteśmy w stanie badać całej tkanki, zatem będziemy musieli podać podzbiór komórek (niekoniecznie spójny), i wtedy dla KAŻDEJ badanej tkanki bierzemy otocznie (które w przypadku tej odłeglóści zdefionwanej w 2.2 nie jest zerowe) i tą komórke z TYM otoczeniem będziemy symulować)
      - Osobno mamy metode które bierzey te warunki początkowe podczas symulacji ...
    2. Warunki początkowe
        - Na początku trzeba wyliczyć warunki początkowe i dla komórki i dla otoczneia (dla tej jednej iteracji bierzemy pod uwagę otoczenie otoczenia) 
        - następnie przejdziemy to iteracji, i nie będziemy już liczyć warunków dla otoczenia otoczenia
    3. Symulacja
        - Następnie będziemy iterowac kolejne kroki, żeby otrzymać i będzimy zapisywać stężenia badanych związków podczas kolejnych iteracji. 
    > WAŻNE: wszystkie obliczenia są wykonywane DOPIERO na etapie ewaluacji, ponieważ w ten sposób oszczędzamy i pamięć i koszt obliczeniowy redukujemy. 
    



# NOTATKI

## Pytania koncepcyjne
Symulujemy taki układ globalnie, czy potrzebujemy już istniejący model, czym możemy to zrobić na samej zasadzie istniejących warunków, widzę nastęujące problemy 

Mamy informacje o komunikacje zewnątrz komórkowej oraz o intensywności występowania tych odczytów (receptor_means) więc na bazie tego możęmy to ustawić, ale w jaki sposób ustawić potem w jaki sposób następuje komunikacja wewnątrz komórkowa ??? 

Wydaje mi sie żę trzeba to zintegrować z istniejącymi modelami i wtedy podłączyćbo inaczej brakuje nam informacji wewntrz komórkowej skąd ewnetuanlie ją wziąć


## Przygotowanie danych

### 1. Pobranie danych spatial-sc 
Żeby wykonać

## LIANA

Pozwala na odczytanie przestrzennych danych SC a następnie przeprowadzenie analizy dotyczącej tego jakie *szlaki sygnałowe* są aktywne. 

Format danych:
```shell
ligand	ligand_complex	ligand_means	ligand_props	receptor	receptor_complex	receptor_means	receptor_props	source	target	lr_means	cellphone_pvals
482	HLA-DRA	HLA-DRA	4.537684	0.995833	CD4	CD4	0.612842	0.421053	Dendritic	CD4+/CD45RO+ Memory	2.575263	0.000
321	HLA-DRA	HLA-DRA	4.537684	0.995833	CD4	CD4	0.596125	0.500000	Dendritic	CD4+/CD45RA+/CD25- Naive T	2.566905	0.000
```

## pymyboss 

Tworzymy obiekt z wierzchołkami, czym one są ??

Format 
```python
nd_dnaDam = Node('DNAdam', '!p53_b1 & DNAdam', 1, 1)
nd_p53_b1 = Node('p53_b1', '!p53_b2 & !Mdm2nuc | p53_b2', 1, 1)
nd_p53_b2 = Node('p53_b2', 'p53_b1 & !Mdm2nuc', 1, 1)
nd_mdm2cyt = Node('Mdm2cyt', 'p53_b1 & p53_b2', 1, 1)
nd_mdm2nuc = Node('Mdm2nuc', '!p53_b1 & !Mdm2cyt & !DNAdam | !p53_b1 & Mdm2cyt| p53_b1 & Mdm2cyt', 1, 1)
```

Stany początkowe:
```python
testNet.set_istate(['p53_b1', 'p53_b2'],
                   {(0, 0): 1, (1, 0): 0, (1, 1): 0})
testNet.set_istate('Mdm2cyt', [1, 0])
testNet.set_istate('Mdm2nuc', [1, 0])
testNet.set_istate('DNAdam', [0.4, 0.6])
```

Mamy także metodę `mutate`, pozwala ona na włączanie wyłączanie genu (to by mogło być dobre do danych przestrzennych, to jest byśmy mieli ogólny model dla pewnych komórek itd. i byśmy uruchamiali on/off dla różnych ??? 

```md
UpPMaBoSS computes the evolution and the dynamics of a population of cells taking into account both their intracellular and intercellular regulations.

Simulations with UpPMaBoSS are based on a logical model describing the intracellular regulations (logical regulatory graph complemented with logical rules), taking into account cell death, cell division, and intercellular communications.
```


# Dokumentacja do zrobienia 

Dokumentacja będzie rozbita na główne README.md w którym będą linki do poszczególnych plików .md w folderze `docs`

## Description 
Ogólny opis co jest zaimplementowane w bibliotece, jak tego używać 

## Installation (separate .md)
Jak zainstalować tą bibliotekę,
- instrukcja jak zainstalować maboss'a 
- gotowy skrypt do środowiska micromamba/conda
- informacja jak uruchomić bibliotekę w trybie developerskim (jak to ustawić inaczej)

## Report file (separate .md)

Here we will present report in our .md with links to given .ipynb notebooks which contains scripts with remarks about methodology, and gathered information about results. 

## Tutorial - basics (separate .md) 
Wytłumaczenie jak z tego korzystać, co jest ważne w użyciu i dlaczego, więc kolejno będziemy omawiać
- jakie dane potrzebujemy 
- jak procesować takie dane
- jak potem ustawić Liane żeby odpowiednio przejść potok (resources, dla myszy i człowieka omówić) 
- potem jak ustawić model i dlaczego
- jak potem wywołać trenowanie
- jak interpretować wyniki, na co zwrócić uwagę

> Format .ipynb który opisuje to kroki, musi być taki ze się odpala: uruchom wszystko u góry i to idzie (z uwagą że trzeba osobno dane pobrać)
>

### Data type

#### Goal
We want to load `spatial-sc` into `adata` object. 

#### Explanation 
In pipeline we use `spatial-sc` data. Our data consists of:
- `HDF5` file, which contains compressed count matrix ($\mathrm{positions} \times \mathrm{genes}$) representing UMI barcodes counts 
- `spatial` folder, which contains tissue positions which contains mapping of $\mathrm{barcode_i} \rightarrow \mathrm{pixel\ coordination}:=(X_i,Y_i)$


#### Methodology - data loading examples 

##### 10x Genomics
- [Example download script](link do skryptu)
- [Example load example](link do notebook'a i odpowiedniego paragrafu)


##### ...
#TODO - dodać kolejne typy, (bazując na tych naszych analizach, ponieważ będziemy odpalać rózne typy danych więc będziemy mieli już gotowe skrypty które to ładują) 

### Preprocessing data

#### Preserving raw matrix
To preserve raw matrix (which is later used), we save by:
```python
adata.raw = raw
``` 

#### Normalization 

### Liana setup 
About ghow 


### Model setup 

### Training settings and how to run it 


## Tutorial - results interpretation (separate .md)

Here we will present simple




## Model adjustment (separate .md) 
Here we will describe how to change certain modules of models, and describe structure of library for users who want to modify existing model. 




## General remarks 