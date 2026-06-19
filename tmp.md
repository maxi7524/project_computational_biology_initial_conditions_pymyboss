
## Struktura

### moduły i funckojanlnosć 

#### io
  - odpowiada za wczytwanie i obsługę danych
#### models
  - tutaj mamy modele które odpowiadają za przewidywanie parametrów
  - czyli tutaj moduły z pojedynczy rzecami oraz metode register, która dodaje wszystkie wpisane metody żeby ręcznei tego nie robić
  - czyli to daje TYLKO narzędzia 
  - KONCEPCJA 
    - jak będziemy uruchamiać te analizy to ostatecznie wyniki będa zapisywane w odpowiednich tabliach z pliku mdata (do uns będą dodawane tak jak inne metadata) 


#### configurate
  - tutaj zrobimy czytnik i edytor tych plików json itd. 
  - funkcjonalność
    - wybieramy folder w którym zapisujemy model, 
      - jak nie istnieje to wywala błedu jak znajdzie i są tam pliki to je wykrywa i informuje 
    - następnie mamy możliwość edycji dowolnego paramteru
      - ja się zastanawiam jak to uporzadkować, ale wydaje mi się że najsensowniejsze będzie: 
        - robienie tego według ich struktury pliku, ponieważ wted zachowujemy format
        - zmienie tego pod nasze moduły
          - wtedy byśmy mieli takie wewnętrzne mapowanie
        - wydaje mi się  żę można zaimplentować oba,
          - wtedy domyślna strukutra wszystkich folderów jest tak jak w oryginalnym pliku (łatwy zapis odczyt) i dodatkowo możemy dać metode .lib_loc (chodziło by mi bardziej chyba żeby to był słwonik) który odpowiednio mapuje te rzeczy, wtedy byśmy wpisyali np model.lib_loc['simulation_settings'] - i dostajemy te silmulation setings
    - mamy metody zapisu oraz odczyty (save / load) które pozwalają tym setrować 
    - dodatkowo validator, który informuje nas gdy czegoś brakuje i wypisuje, you lack ... i użytkownik może sobie to sprwadzić
  - jest to całkowicie niezalezna klasa od models, tamta klasa ma za zadanie zwracać odpowiednie parametru
  - implemetnacja
    - będziemy mieli config z xsd
    - następnie będziemy parsować te dane do configu, ponieważ automatycznie bęzie sprawdzane czy spełenia wszystkie wymagania
    - możemy dodać specjalny wtyckzi u nas które częściowo będą przenosić informacje (chociaż ten nowy schemat jest dosyć sensowny)
#### wrappers
  - to jest moduł odpowiedzialny za uruchamianie trenownia
#### utils 
  - funkcje pomocznie (jak logger)
#### visualization
  - to później do robienia plotów   
    - to będą skrypty z wykorzsytaniem tej ich biblioteki
- 

***

koncepcja jest taka:
- dostajemy dane, przynajmniej RNA (i tak teraz robimy bibliotekę, żeby to był RNA) 
- będziemy oferowali zaimplenmtnowaly model 
  - modele będą agregować te wszystkie rodzaje funkcjonalności, ale można będzie je też uruchamiać ososbno z rejestrów
  - taki model, zwraca znowu zestaw mdata
  - trick będzie polegał na tym że wszystkie informacje potrzebne do modelu będziemy trzymać w specjalnych słownikach
  - więc w configurators będą metody set i będziemy podawać ten moduły 
    - ponieważ wymuszamy kompletność wględem tych klas, wszystki output są takie same i będziemy mieli zaimplentowane po prostu funkcje pomocnicze które to ładują
      - te metody oczywićie też musza mieć doatkowe argumenty żeby móc nadpisać te ustawienia (ale ldmyślne rzadami naszego mdata)
  - będą też metody set od od parametrów ustawień treningowych

## Plan

1. Po kolei robimy moduł
   1. dodajemy funkcjonalnosć
   2. dodajemy ją do rejestru
   3. dodajemy testy do moduł żeby sprawdzić czy output się zgadza 
   4. robimy dokumentacje która to opisuje
2. niektóre inforamcje wolałbym osobno (parametry symulacyjne przed symulacją, żęby móć zmieniać)
   1. therads
   2. otuput folder
   3. czy jakieś ploty generować autoamtycznie ???
   4. jaki czas symulacji
   5. folder wynikowy z symulacją
3. jak będziemy mieli wszysktie moduły zapisujemy to do pliku eksportujemy do PhysiCella
   1. będziemy najpirew szli według instrukcji
      1. przenosimy plik
      2. ładujemy plik
      3. wykonujemy analize
      4. przenosimy pliki wynikowe do końcowego folderu
      5. wszystko powyżej wykonuje się jako jedna funkcja i są logi na bieżaca zwracana (to będzie pipeline tutaj szedł) 
4. 





## uwagi architektocznie 

### zrobić możłiwosć edycji istneijącego modelu
- zroibć skrypt który wczytuje tego jsona do takiej postaci jakmy to zapisujemy 

## Modele - do zrobienia

### Domain

#### cells sizes, spaces sizes

* [x] add x_min, x_max, y_min, y_max, z_min, z_max (Zaimplementowane w `PhysiCellAgentConfigurator.set_domain_parameters`)
* [x] add dx, dy, dz (Zaimplementowane w `PhysiCellAgentConfigurator.set_domain_parameters`)
* [ ] Wyznaczanie granic domeny ($\text{bounding box}$) bezpośrednio z macierzy współrzędnych przestrzennych (Brak w logice biznesowej)
* [ ] Automatyczne dobieranie rozmiaru woksela ($dx, dy$) na podstawie średniego dystansu między najbliższymi sąsiadami (Brak)

#### Time scales

* [x] set_overall_parameters (Zaimplementowane: max_time, dt_diffusion, dt_mechanics, dt_phenotype)
* [ ] Walidacja rygoru wieloskalowości: zapewnienie warunku $dt_{\text{diffusion}} \le dt_{\text{mechanics}} \le dt_{\text{phenotype}}$ (Brak)

### Environment

#### Substrates & Boundary Conditions

* [x] add_microenvironment_substrate (Zaimplementowane bazowe tworzenie węzła)
* [ ] Definiowanie niezależnych warunków brzegowych Dirichleta dla każdej krawędzi domeny (Brak)
* [ ] Automatyczna inicjalizacja dyfundujących substratów na podstawie par ligand-receptor zidentyfikowanych przez Liana+ (Brak)

### Cell Definitions (Phenotype)

#### Mechanics & Volume

* [x] register_allowed_cell_type (Inicjalizuje puste kontenery XML)
* [ ] Iniekcja parametrów mechanicznych (adhezja, repulsja, dystans maksymalny) (Brak)
* [ ] Definiowanie stanów objętościowych ($V_{\text{cell}}, V_{\text{nuclear}}, V_{\text{fluid}}$) (Brak)

#### Cycle & Death

* [ ] Mapowanie mechanizmów przejść fazowych i powiązanie ich z czasem biologicznym (Brak)
* [ ] Definiowanie parametrów apoptozy i nekrozy jako ujść funkcjonalnych (Brak)

