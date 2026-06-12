# download bnd
wget https://maboss.curie.fr/files/DrosoPattern/D_Pattern_ContT.bnd
# download cfg (no noise)
wget https://maboss.curie.fr/files/DrosoPattern/D_Pattern_ContT_noIntNode.cfg
# download cfg (noise)
wget https://maboss.curie.fr/files/DrosoPattern/D_Pattern_ContT_noIntNode_noise.cfg

mkdir -p data/maboss/DrosophilaPatterning/model

mv D_Pattern_ContT* data/maboss/DrosophilaPatterning/model/