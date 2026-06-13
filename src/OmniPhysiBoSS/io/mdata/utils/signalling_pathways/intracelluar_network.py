# =============================================================================
# Intracellular Signaling Pathway Extraction Script
# =============================================================================

import mudata as mu
import pandas as pd
import omnipath as op
from typing import List, Optional
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


def fetch_intracellular_pathway_network(
    mdata: mu.MuData,
    output_key: str = "omnipath_intracellular",
    resources: Optional[List[str]] = ["SIGNOR", "NetPath"],
    datasets: Optional[List[str]] = ["omnipath"]
) -> mu.MuData:
    """
    Query and format the directed, signed intracellular signaling network from OmniPath.

    :param mdata: High-dimensional aligned multi-modal container asset.
    :type mdata: mu.MuData
    :param output_key: Target metadata storage key under root .uns, defaults to "omnipath_intracellular".
    :type output_key: str
    :param resources: Core database registries to filter source pathways, defaults to ["SIGNOR", "NetPath"].
    :type resources: Optional[List[str]]
    :param datasets: Broad OmniPath specific network datasets to pull, defaults to ["omnipath"].
    :type datasets: Optional[List[str]]
    :return: The updated multimodal container updated with the structured intracellular network.
    :rtype: mu.MuData
    """

    # Remote database acquisition phase
    ## Pull curated kinase/phosphatase and transcriptional pathways from server using strict parameter definitions
    logger.info("Requesting intracellular pathways from OmniPath. Filtering via datasets: %s, resources: %s", datasets, resources)
    raw_network = op.interactions.AllInteractions.get(
        resources=resources,
        datasets=datasets
    )

    # Topological consistency constraint selection
    ## Filter rows keeping only those with established consensus directionality
    processing_df = raw_network[raw_network["consensus_direction"] == 1].copy()
    processing_df["sign"] = 0

    # Causal sign extraction logic
    if "is_stimulation" in processing_df.columns and "is_inhibition" in processing_df.columns:
        ## Compute definite directional signs mapping biological logic
        ### Set purely inductive pathways to positive unity constants
        stimulation_mask = (processing_df["is_stimulation"] == 1) & (processing_df["is_inhibition"] == 0)
        processing_df.loc[stimulation_mask, "sign"] = 1

        ### Set purely repressive pathways to negative unity constants
        inhibition_mask = (processing_df["is_stimulation"] == 0) & (processing_df["is_inhibition"] == 1)
        processing_df.loc[inhibition_mask, "sign"] = -1

    # Structural cleanup block
    ## Eliminate ambiguous interactions or missing node records
    filtered_network = processing_df[processing_df["sign"] != 0].copy()
    final_edgelist = filtered_network[["source", "target", "sign"]].dropna()
    final_edgelist = final_edgelist.drop_duplicates().reset_index(drop=True)
    logger.debug("Filtered network compiled. Rows retained: %s", final_edgelist.shape[0])

    # Persistence operation
    ## Bind the resulting structural interaction dataframe into unstructured metadata
    mdata.uns[output_key] = final_edgelist
    logger.info("Stored intracellular network under uns['%s']. Total edges: %s", output_key, final_edgelist.shape[0])

    return mdata