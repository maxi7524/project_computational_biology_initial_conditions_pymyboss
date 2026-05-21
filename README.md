



# Cel projektu

Chcemy stworzyć narzędzie które mapuje wyniki z LIANA+ (to jest mamy tutaj regulacje ich istotność itd.) na warunki początkowe pymyboss'a.

Będziemy chcieli to zrobić w kontekście klas komórek (bez danych przestrzennych) i z danymi przestrzennymi, wtedy będziemy uwzględniali dynamikę układu cząstek. CHcielibyśmy wtedy móc załadować taki układ. 


# NOTATKI

## Pytania koncepcyjne
Symulujemy taki układ globalnie, czy potrzebujemy już istniejący model, czym możemy to zrobić na samej zasadzie istniejących warunków, widzę nastęujące problemy 

Mamy informacje o komunikacje zewnątrz komórkowej oraz o intensywności występowania tych odczytów (receptor_means) więc na bazie tego możęmy to ustawić, ale w jaki sposób ustawić potem w jaki sposób następuje komunikacja wewnątrz komórkowa ??? 

Wydaje mi sie żę trzeba to zintegrować z istniejącymi modelami i wtedy podłączyćbo inaczej brakuje nam informacji wewntrz komórkowej skąd ewnetuanlie ją wziąć


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