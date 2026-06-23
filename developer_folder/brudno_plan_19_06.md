


### MaBoss

jak to zintegrować 



#### plan jest taki 
- mamy jakieś bazowe modele które dodajemy (ich warunki poczatkowe dodamy do całej próbki i później wspólnie wyestymujemy warunki początkowe) 
  - najpierw trzeba dodać modele
  - potem trzeba wyestymować szlaki (ponieważ odwrotnei będzie to cięzko zintegrowac, a tak mamy sieć którą możemy rozbudowywać i może byc łatwiej) 
    - jak to zrobić dokładnie 
  - jak wyestymujemy te wartosci. 


w tle
- te informacje dotyczące elementów biorących udział w sieci będziemy nazywać network_metadata
  - zawiera on informacje o **występujacych związkach**
    - jakie związki (wszystkie) 
      - rozróżnienie kategorii
        - wewwnętrzen zewnętrzen itd.
        - 
    - jak z tego realcje opisać ?? 
    - TODO - jak zrobić tak ze zachowujemy w całej sieci informacje o relacji 

implementacja (maboss sieci) 
- robimy który:
  - będzie przyjmował JUŻ gotowy model maboss (jaki kolwiek - najlepiej to z nowotworami) 
  - następnie będziemy **dobudowywac do już istniejącego modelu** dodatkowe szlaki sygnalizacyjne 
    - co zrobić w przypadku komórek które nie mają szlaku konfiguracyjnego ??? 
  - dobudowane szlaki sygnalizacyjne będziemy mogli potem analizować (jak ???) 
  - 

implementacja (environment)
- biorąc informacje z mabosas
  




    - model nam będzie też determinował podstawowe cykle, wiec też uprościmy całość, będziemy jedynie dodawać **nowe typy komórkowe** (jak?) 