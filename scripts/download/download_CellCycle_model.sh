# download bnd
wget https://maboss.curie.fr/files/CellCycle/cellcycle.bnd
# download cfg 
wget https://maboss.curie.fr/files/CellCycle/cellcycle_runcfg_randinit.cfg

mkdir -p data/maboss/CellCycle/model

mv cellcycle* data/maboss/CellCycle/model/