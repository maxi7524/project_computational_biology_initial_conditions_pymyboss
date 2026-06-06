
# depracated 

#TODO - trzeba przemyśleć strukture tych plików (zaproponuj jakbyś to widział / co byś poprawił w tej strukturze) 

Ogólnie, zastanawiam się czy:
- zrobić w docsach, w odpowiednich częściach explanation pewien ogólny docs (modules.md albo README.md - rozumiem że konwencja jest taka, że to mówi - co jest w tym folderze, wtedy to jest bardziej intuicyjne) dokładny opis i streszczenie co się tam znajduje i powiedze tutaj tylko że zapoznać się dokładnie z metodologią proszę przejść tutaj: (odnośnik do pliku)
- czy częścio pominąć taki docs i tutaj zgrubsz to opisać (wtedy mamy dużo tych parafgrafów jak niżej i moim zdaniem to traci na czytelności ..., ale jest bardziej zwarte, co może powodwać żę zyskuje) 

zamieszzma jaka wyglądająścieżki w doscahc

```markdown
├── explanations 
│   ├── io_structure
│   │   └── PhysiCell_and_PhysiBoSS_configuration_format.md
│   ├── methodology
│   └── modules
│       ├── configuration_module.md
│       ├── modules.md
│       └── wrappers_module.md
├── how_to
│   └── README.md
├── references
│   └── later_render_Sphinx
├── tmp_parameters_to_set.md
└── tutorials
```

#### Models
w folderach to jest `methodology`, chodzilo by mi tutaj o to, żeby opisać jak konstruowałem te model, jakie założenia tutaj przyjmujemy, intuicje za tymi modelami z PhysiBoSSa (moja intuicja częściow za tym) wtedy bym to zrobił tak że była by jedna głowna notatka gdzie to wszystko zbieram i opisuje gdzie czego szukać i w tych mniejszych były by - konkretne rzeczy typu - (zmień ten prefiks bo jest nie intuicyjny- na cał grupe to będzie) initialize_intercellular_communication, initialize_intercell_communication ... oraz jeszcze extracellular_communication_models intercellular_communication itd. (najlepiej slowo ujednolicić ...) więc tu byśmy opisywali dokladnie 

##### Methodology

#### Implementation details

Tutaj rozróżnilibyśmy dwa foldery `io_structure` (a możę po prostu `io_formats` ??? - sugeruj), gdzie będzie krótka notatka mówiąca o tym, jakei dane są na wejściu i w skócie co one mówią (że pliki `cells.csv` zawierają informacje o  tym jak mapować komórki z macierzy na typy komórek w `PhysiBoSS`, żę xml definiuje wszystkie zachownia między komórkowe, defniuje typy komórek i pod każdy typ komórki podpina model bossa, że output zawiear to i to) każdy taki format po krótce ma linka i tam jest BARDZO dokładne omówienie wszystkich szczegółów takiego pliku (ogólnie to kazdy plik byłby sekcjami opisany co robi dany fragment itd. analiogicznie jak ten od settings.xml, tylko tutaj podział jest na sekcje w maboss byłby podział na pliki itd.) 

Drugi folder to by był `modules` tutaj było by opisane najpierw jaka jest ogólna struktura architektury (można by tuaj przeniesć ten graf ze wszystkimi fragmentami albo rodzielić wtedy taki graf osobno - tutaj ogólne tylko testy z testami itd. a w modules dokładne omówienie co jest w tesach jak to jest połączone z modułami w bibliotece itd.) wiec byla by tutaj ogólna struktura implementacji bardzo dokłądnie wtłumaczony potok (ja bym zrobił taki graf potoku tego naszego modelu co się dziej po krótce i tutaj zrobił do niego reference (żęby tylko jeden plik zmieniać i to by się przenosiło)  ) i potem odnoszenia do każdego modułu ze szczegółąmi (najpirew warstwa abstrakcyjna w tym głównym pliku co robi w naszym potoku +- ja kdziała) i w wejściu w moduł dokładnie opisane (dla każdego modułu bym chciał zrobić analogiczne sekcje):

Możęmy następnie poprawić wrappers (on jest skończony) według tego template'u żeby w innych chatach bot wiedział jak to uzupełniać (tempplate zostawie jako osobny plik) prześlę tobie wtedy pliki (za kilka promptów) 

W głownym pliku powiedzielibyśmy też o templatcie testów itd. że biblitoeka jest zrobiona library_folder/module_name/sub_module_name and file_1 /file_2 (jakiś graf tutaj zrobić) i że wtedy testy mają postać: tests/module_name/test_file_1_(sometimes part of functionality).py (testy będą jako moduł też osobno opisane, ale to musi być w głównym, żeby zrozumieć działanie)  


##### IO formats

##### Modules 

##### Sphinx 

#### Repository structure

(#TODO - later - graf z opisanymi bibliotekami (można też to przenieśc do sekcji modukes ??? - opisane wszystkie skrypty co robią) - powiedz, mi jakbyś to rozwiązał )