Jakie parametry będziem musieli ustalić do zdefiniowania modelu

## Co do dokumentacji
- jakie minimalne własności musi miec dataset żeby to miało sens (bo ja tu widzę oisy komóek RNA itd. wiec my tutaj potrzebujemy całej masy informacji żęby ten model wogóle miał prawo działać) 


## Globalne

<te wczęśnie overall i microveniiornemt  >
- #TODO - to trzeab wyciągnać z spatial data i spradzić po prostu metadane o tym 


## Pojedyncze 



szlaki sygnałowe 
- to będzie trzeba najpierw znaleźć ponieawż od tego zależy jak będziemy definować komunikacje zewnatrz i wewnątrz komórkową

maboss
    - mamy kilka różnych rodzajów modeli 
      - 
      - zasady (operacje) definiujemy z tej sieci skierowanej, ponieważ tawm z decoupleR z omnipathem powinny być inforamcje o tym (osobna funkcja) 
      - wartości początkowe bym zadefiniował tak że to byłby rozkładu po jakieś funkcji (do przemyślenia) żęby dawało 1 kiedy to jest najwieksza / od jakiegoś odcięcia, żeby dawała odpowiednio proporcje (ale liniowo jest absuradlne jakis artykuł znaleźć który to opisuje sensowniej) (osobna funkcja) 
        - PYTANIE: jaka jest szansa że szlak jest aktywny mając tyle i tyle transkryptu (można też wartości z testów statystycznych wyciągać)  (osobne funkcje)
      - szanasy zmiany (te infinitezyalne wartości) 0 też jakoś trzeba wyciągnać z informacji o szlakach sygnałowych (osobne funkcje)


<Cell_definitions>
    <Cell_definition name=...>
        - #TODO - charakteryzacja typów komórek !!! (inaczej złożóność zabija) 
        - rodzaje / typy komóek (nie może zdefiniować każdej komórki osobno, potrzebujemy scharakteryzować typy)
        - typy komórek defniują nam ilość modeli mabossa
          - 
    <phenotype>
        - #TODO ilosć fenotypów i od czego zależ 
        - ile fenotypów defniujemy, ?? wyglądają jakby się miały powtsarażć 
        - mamy np różne rodzaje umierania - jak to zaimplementować ??? 
    <mechanics> i <motility>
        - #TODO - uśrednich / uzyskać z danych przestrzennych (one będą odległości i rozmiary determinować !!!) 
        - to trzeba dostosowaywać do odległóści na klastrze którą dostjaemy
    <cell_interactions>
        - #TODO - definicja interakcji pomiędzy grupamia na bazie **zaagregowanych par receptor ligand z liana+ + szlaki metaboliczne z decoupleR**
        - tutaj defniujemy interakcje pomiędzy typami komórek zdefniowanymi wczęśniej (skąd my będziemy mieli te oznaczenia) 
        - UWAGA - to są interkacji nie wymiany (inne bazy danych które zawierają takie informacje) 
    <cell_transitions>
        - #TODO - znowu, 
        - tutaj będzie trezba zdefiniować różne stany / albo jak nie będzie różnych to strywializować to jednego. też z jkaieś bazy danych to trzeba wziąć
    <initial_parameter_distributions>
    
tam jest jeszcze dużo interakcji związanych  zsiłya adhezyjny kohezyjny itd. skad wogóle wziąć takie informacje i jak to zdefniować


do przemyślenia te dirichleta itd. sprawdzić któe ustawienia nie powinny być ruszane i dodać do nich moduł ale żęby tylko przkazywał default values (sama funckja też set_default czy coś) i wyraźny komenatrz że to nie było ruzsznae (to są jakeiś szczegóły implementacyjne - pominiemy je) 