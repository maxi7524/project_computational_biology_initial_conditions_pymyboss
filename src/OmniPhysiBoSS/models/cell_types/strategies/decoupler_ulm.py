# Heading 1 (Broad context / Top-level block / Script section)
# Continuous Univariate Linear Model enrichment strategy using decoupler wrappers.

from typing import Dict, Any, Set
import mudata as mu
import decoupler as dc

from .cell_types_base import BaseCellTypeExtractor
from ....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

class DecouplerULMExtractor(BaseCellTypeExtractor):
    """
    Annotates clusters by computing statistical enrichment scores with continuous 
    Univariate Linear Models, ensuring strict cross-species gene case synchronization.
    """

    def extract_cell_types(
        self, 
        mdata: mu.MuData, 
        organism: str, 
        target_cluster_key: str = 'leiden'
    ) -> Dict[str, Any]:
        """
        Execute continuous matrix regression profiles and resolve dominant identities per cluster.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param target_cluster_key: Key label specifying group columns inside rna observations dataframe.
        :type target_cluster_key: str
        :param organism: Taxonomy selector token for API queries ('human' or 'mouse').
        :type organism: str
        :return: Map structure connecting cluster tags to index blocks.
        :rtype: Dict[str, Any]
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural schemas validation checks
        logger.info("Initializing continuous Decoupler ULM identification pipeline.")
        
        if 'rna' not in mdata.mod:
            logger.error("Aborting Decoupler execution loop. Modality slice 'rna' missing.", exc_info=True)
            raise KeyError("Missing 'rna' modality container.")

        rna_adata = mdata.mod['rna']
        unique_clusters = rna_adata.obs[target_cluster_key].unique()

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Fetch continuous marker lists over remote client bridges from OmniPath networks
        logger.info("Pulling PanglaoDB networks from OmniPath server endpoints for organism: %s", organism)
        markers_resource = dc.op.resource("PanglaoDB", organism=organism)
        
        # Enforce canonical panel validation rules on download frames
        filtered_resource = markers_resource[
            markers_resource[organism].astype(bool) & 
            markers_resource["canonical_marker"].astype(bool)
        ]
        
        # Formulate core structural source-target network links
        dc_network = filtered_resource.rename(columns={"cell_type": "source", "genesymbol": "target"})
        dc_network = dc_network[["source", "target"]].drop_duplicates()

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Case synchronization logic based on target taxonomy model
        if organism.lower() == 'mouse':
            logger.debug("Formatting network gene symbols to Title Case for mouse alignment matching.")
            dc_network['target'] = dc_network['target'].str.lower().str.capitalize()
        else:
            logger.debug("Formatting network gene symbols to UPPERCASE for human alignment matching.")
            dc_network['target'] = dc_network['target'].str.upper()

        # Intersect network targets with the available dataset gene universe
        dc_network = dc_network[dc_network['target'].isin(rna_adata.var_names)]

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Fit the cell expression matrix against network links using Univariate Linear Models
        logger.info("Fitting expression vectors via Univariate Linear Model (ulm) regression steps.")
        dc.mt.ulm(data=rna_adata, net=dc_network, tmin=3)
        
        # Derive statistical overrepresentation metrics across cluster separations
        score_adata = dc.pp.get_obsm(rna_adata, key="score_ulm")
        ranking_df = dc.tl.rankby_group(adata=score_adata, groupby=target_cluster_key, reference="rest", method="t-test_overestim_var")
        
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Extract dominant assignments alongside their associated statistical t-test scores
        top_hits_df = ranking_df[ranking_df["stat"] > 0].groupby("group").head(1).set_index("group")
        dominant_names = top_hits_df["name"].to_dict()
        dominant_scores = top_hits_df["stat"].to_dict()
        
        cell_lineage_registry = {}
        assigned_identifiers: Set[str] = set()

        for clus in unique_clusters:
            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Populate registration records matching the dominant statistical hits and scale metrics
            clus_cells = rna_adata.obs.index[rna_adata.obs[target_cluster_key] == clus].tolist()
            base_cell_type = dominant_names.get(clus, "Unknown/Unassigned")
            confidence_score = float(dominant_scores.get(clus, 0.0))
            
            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Enforce absolute identifier uniqueness to prevent cross-cohort naming collisions
            unique_cell_type = base_cell_type
            if unique_cell_type in assigned_identifiers and unique_cell_type != "Unknown/Unassigned":
                logger.debug("Collision detected for label: %s. Appending cluster token for unique resolution.", unique_cell_type)
                unique_cell_type = f"{base_cell_type}_{clus}"
            
            assigned_identifiers.add(unique_cell_type)
            logger.info("Cluster %s statistically mapped to decoupler identity: %s (Score: %s)", str(clus), unique_cell_type, str(confidence_score))

            cell_lineage_registry[str(clus)] = {
                "cell_indices": clus_cells,
                "cell_count": len(clus_cells),
                "database_reference": {
                    "source": "OmniPath_PanglaoDB_Decoupler_ULM",
                    "identifier": unique_cell_type,
                    "confidence_score": confidence_score,
                    "status": "aligned"
                }
            }

        logger.info("Continuous Decoupler ULM strategy matrix loops finished processing.")
        return cell_lineage_registry