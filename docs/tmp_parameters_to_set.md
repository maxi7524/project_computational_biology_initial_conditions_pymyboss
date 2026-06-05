Jakie parametry będziem musieli ustalić do zdefiniowania modelu

## Co do dokumentacji
- jakie minimalne własności musi miec dataset żeby to miało sens (bo ja tu widzę oisy komóek RNA itd. wiec my tutaj potrzebujemy całej masy informacji żęby ten model wogóle miał prawo działać) 


## Globalne

<te wczęśnie overall i microveniiornemt  >
- #TODO - to trzeab wyciągnać z spatial data i spradzić po prostu metadane o tym 


## Pojedyncze 



<Cell_definitions>
    <Cell_definition name=...>
        - #TODO - charakteryzacja typów komórek !!! (inaczej złożóność zabija) 
        - rodzaje / typy komóek (nie może zdefiniować każdej komórki osobno, potrzebujemy scharakteryzować typy)
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
    