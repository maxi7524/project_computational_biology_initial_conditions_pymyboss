"""
network/signaling.py
----------------------------


"""

import anndata as ad
import pandas as pd
import omnipath as op
import liana as li

class SignalingNetworkBuilder:
    """
    Manages external biological database queries and spatial communication inference.
    Integrates Liana+ spatial ligand-receptor scoring with OmniPath intracellular pathways.

    :param adata: Annotated data matrix containing spatial transcriptomics profiles.
    :type adata: anndata.AnnData
    """

    def __init__(self, adata: ad.AnnData) -> None:
        # structural setup
        ## data binding
        ### retain internal reference to sample matrix
        self.adata: ad.AnnData = adata
        self.liana_results: pd.DataFrame = None
        self.raw_network: pd.DataFrame = None

    def run_liana_spatial(self, coordinate_key: str = "spatial", cell_type_key: str = "cell_type") -> pd.DataFrame:
        """
        Executes Liana+ spatial pipeline to infer ligand-receptor interactions bounded by 2D coordinates.

        :param coordinate_key: Array key within .obsm containing spatial positions.
        :type coordinate_key: str
        :param cell_type_key: Column name within .obs specifying cell populations.
        :type cell_type_key: str
        :return: Filtered ligand-receptor interactions with spatial scoring metrics.
        :rtype: pandas.DataFrame
        """
        # external resource fetching
        ## spatial communication inference
        ### execute rank aggregate scoring with geometric constraints via liana
        self.liana_results = li.multi.bivariate(
            self.adata,
            cluster_key=cell_type_key,
            spatial_key=coordinate_key,
            output_dict=False
        )
        return self.liana_results

    def query_omnipath_topology(self, receptors: list) -> pd.DataFrame:
        """
        Queries OmniPath database for directed post-translational and transcriptional interactions.

        :param receptors: Extracted target node identifiers acting as structural inputs.
        :type receptors: list
        :return: Network topology containing source, target, and sign attributes.
        :rtype: pandas.DataFrame
        """
        # external resource fetching
        ## database network queries
        ### download signed directed connections from omnipath server
        network = op.interactions.import_intercell_network(
            categories=["signaling"],
            transmitter_components=receptors
        )
        
        # topological cleaning
        ## matrix filtering
        ### restrict database entries to directed signed interactions
        self.raw_network = network[
            (network["is_directed"] == True) & 
            (network["consensus_direction"] == 1)
        ][["source_genesymbol", "target_genesymbol", "consensus_stimulation", "consensus_inhibition"]]
        
        return self.raw_network