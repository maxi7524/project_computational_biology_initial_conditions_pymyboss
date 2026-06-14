# Heading 1 (Broad context / Top-level block / Script section)
# Continuous Univariate Linear Model enrichment strategy using decoupler wrappers with direct ontology targeting.

import os
from typing import Dict, Any, List
import pandas as pd
import mudata as mu
import decoupler as dc

from .cell_types_base import BaseCellTypeExtractor
from .utils import resolve_global_assignments, flatten_lineage_registry
from ....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

class DecouplerULMExtractor(BaseCellTypeExtractor):
    """
    Annotates clusters by computing statistical enrichment scores with continuous 
    Univariate Linear Models using CellMarker 2.0 reference data anchored directly on Cell Ontology IDs.
    """

    def extract_cell_types(
        self, 
        mdata: mu.MuData, 
        organism: str, 
        target_cluster_key: str = 'leiden',
        marker_database_path: str = 'resources/databases/Cell_marker_All.xlsx',
        tmin: int = 1
    ) -> Dict[str, Any]:
        """
        Execute continuous matrix regression profiles and resolve unique dominant identities globally.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param organism: Taxonomy selector token for tracking ('human' or 'mouse').
        :type organism: str
        :param target_cluster_key: Key label specifying group columns inside rna observations dataframe.
        :type target_cluster_key: str
        :param marker_database_path: Trajectory on the filesystem containing the CellMarker 2.0 Excel data.
        :type marker_database_path: str
        :return: Map structure connecting cluster tags to index blocks with unique database identities.
        :rtype: Dict[str, Any]
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural schemas validation checks
        logger.info("Initializing continuous Decoupler ULM identification pipeline with CellMarker 2.0.")
        
        if 'rna' not in mdata.mod:
            logger.error("Aborting Decoupler execution loop. Modality slice 'rna' missing.", exc_info=True)
            raise KeyError("Missing 'rna' modality container.")
            
        if not os.path.exists(marker_database_path):
            logger.error("Target database reference file missing at path: %s", marker_database_path, exc_info=True)
            raise FileNotFoundError(f"Database asset missing: {marker_database_path}")

        rna_adata = mdata.mod['rna']
        unique_clusters = rna_adata.obs[target_cluster_key].unique()

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Load local database matrix and format source-target network links
        logger.info("Loading database from %s", marker_database_path)
        db_df = pd.read_excel(marker_database_path)
        initial_count = len(db_df)
        
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Filter out missing entries and evaluate vectorized prefix matching via string accessors
        db_df = db_df[db_df['cellontology_id'].notna()]
        db_df = db_df[db_df['cellontology_id'].notnull()]
        db_df = db_df[db_df['cellontology_id'].astype(str).str.startswith('CL')]
        
        ## Log filtering metrics
        logger.debug("Rows before filtering: %s", initial_count)
        logger.debug("Rows after filtering: %s", len(db_df))

        species_filter = "Human" if organism.lower() == 'human' else "Mouse"
        db_df = db_df[db_df['species'].str.lower() == species_filter.lower()]
        
        db_df['Symbol'] = db_df['Symbol'].astype(str).str.upper()
        panel_genes_upper = [str(g).upper() for g in rna_adata.var_names]
        filtered_db = db_df[db_df['Symbol'].isin(panel_genes_upper)]
        
        # Format network using cellontology_id directly as the source node
        dc_network = filtered_db.rename(columns={"cellontology_id": "source", "Symbol": "target"})
        dc_network = dc_network[["source", "target"]].drop_duplicates()

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Fit the cell expression matrix against network links using Univariate Linear Models
        logger.info("Fitting expression vectors via Univariate Linear Model (ulm) regression steps.")
        dc.mt.ulm(data=rna_adata, net=dc_network, tmin=tmin)
        
        score_adata = dc.pp.get_obsm(rna_adata, key="score_ulm")
        ranking_df = dc.tl.rankby_group(adata=score_adata, groupby=target_cluster_key, reference="rest", method="t-test_overestim_var")
        
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Compile metadata lookup profiles grouped directly by cellontology_id
        meta_lookup = {}
        for cl_id, group in filtered_db.groupby('cellontology_id'):
            first_row = group.iloc[0]
            meta_lookup[str(cl_id)] = {
                "cellontology_id": str(cl_id),
                "uberonontology_id": str(first_row.get('uberonongology_id', 'NaN')),
                "tissue_class": str(first_row.get('tissue_class', 'NaN')),
                "tissue_type": str(first_row.get('tissue_type', 'NaN')),
                "cancer_type": str(first_row.get('cancer_type', 'NaN')),
                "cell_type": str(first_row.get('cell_name', 'NaN')),  # Preserved original descriptive string name
                "uniprot_id": str(first_row.get('UNIPROTID', 'NaN')),
                "marker_source": str(first_row.get('marker_source', 'NaN')),
                "pmid": str(first_row.get('PMID', 'NaN')),
                "publication_title": str(first_row.get('Title', 'NaN'))
            }

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Populate unstructured scoring manifest tracking all statistical coefficients to ensure complete coverage
        scoring_manifest: List[Dict[str, Any]] = []
        for _, row in ranking_df.iterrows():
            clus = row["group"]
            cl_id = row["name"]  # Contains cellontology_id directly from the network source
            score_val = float(row["stat"])
            clus_cells = rna_adata.obs.index[rna_adata.obs[target_cluster_key] == clus].tolist()
            
            meta = meta_lookup.get(str(cl_id), {})
            
            scoring_manifest.append({
                "cluster": clus,
                "cell_name": meta.get("cell_type", "Unknown"),
                "score": score_val,
                "metadata": meta,
                "cells": clus_cells
            })

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Resolve assignments via global score optimization utility
        global_assignments = resolve_global_assignments(scoring_manifest)
        
        cell_lineage_registry = {}
        for clus in unique_clusters:
            cluster_str = str(clus)
            clus_cells = rna_adata.obs.index[rna_adata.obs[target_cluster_key] == clus].tolist()
            
            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Enforce comprehensive matching constraint and inject into cell lineage registry
            if cluster_str in global_assignments:
                assignment = global_assignments[cluster_str]
                cell_lineage_registry[cluster_str] = {
                    "cell_indices": clus_cells,
                    "cell_count": len(clus_cells),
                    "database_reference": {
                        "source": "CellMarker2.0_OmniPath_Decoupler_ULM_Global",
                        "identifier": assignment["identifier"],
                        "confidence_score": assignment["confidence_score"],
                        "status": "aligned",
                        "metadata_context": assignment["metadata_context"]
                    }
                }
            else:
                ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
                ### Mathematical safety block to capture unexpected optimization failures
                logger.error("Absolute coverage constraint violated: Cluster %s was left unassigned.", cluster_str, exc_info=True)
                raise ValueError(f"Absolute coverage constraint violated: Cluster {cluster_str} has no valid unique assignment.")

        flat_registry = flatten_lineage_registry(cell_lineage_registry)

        logger.info("Continuous Decoupler ULM global execution loop finished safely.")
        return flat_registry