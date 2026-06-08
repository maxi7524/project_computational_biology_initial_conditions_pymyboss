# =============================================================================
# Intracellular Signaling Pathway Extraction Script
# =============================================================================

import mudata as mu
import pandas as pd
import omnipath as op
from typing import List, Optional


def fetch_intracellular_pathway_network(
    mdata: mu.MuData,
    output_key: str = "omnipath_intracellular",
    resources: Optional[List[str]] = ["OmniPath", "SIGNOR", "NetPath"]
) -> mu.MuData:
    """
    Query and format the directed, signed intracellular signaling network from OmniPath.

    :param mdata: High-dimensional aligned multi-modal container asset.
    :type mdata: mu.MuData
    :param output_key: Target metadata storage key under root .uns, defaults to "omnipath_intracellular".
    :type output_key: str
    :param resources: Core database source registries to filter directed pathways, defaults to ["OmniPath", "SIGNOR", "NetPath"].
    :type resources: Optional[List[str]]
    :return: The updated multimodal container updated with the structured intracellular network.
    :rtype: mu.MuData
    """
    # Remote database acquisition phase
    ## Pull curated kinase/phosphatase and transcriptional pathways from server
    print("[-] Requesting intracellular interaction pathways from OmniPath...")
    raw_network = op.interactions.AllInteractions.get(
        resources=resources
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

    # Persistence operation
    ## Bind the resulting structural interaction dataframe into unstructured metadata
    mdata.uns[output_key] = final_edgelist
    print(f"[✓] Stored intracellular network under uns['{output_key}']. Total edges: {final_edgelist.shape[0]}")

    return mdata