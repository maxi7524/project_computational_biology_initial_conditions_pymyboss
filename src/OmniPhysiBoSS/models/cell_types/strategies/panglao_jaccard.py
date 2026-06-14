# Heading 1 (Broad context / Top-level block / Script section)
# Discrete overlap coefficient extraction strategy using CellMarker 2.0 anchored directly on ontology identifiers.

import os
from typing import Dict, Any, List
import pandas as pd
import mudata as mu
import scanpy as sc

from .utils import resolve_global_assignments, flatten_lineage_registry
from .cell_types_base import BaseCellTypeExtractor
from ....utils.logger import get_custom_logger


logger = get_custom_logger(__name__)

class CellMarkerJaccardExtractor(BaseCellTypeExtractor):
    """
    Annotates cell clusters by calculating explicit binary Jaccard set intersections 
    between cluster markers and the CellMarker 2.0 reference database, mapped directly to Cell Ontology IDs.
    """

    def extract_cell_types(
        self, 
        mdata: mu.MuData, 
        organism: str,
        target_cluster_key: str = 'leiden', 
        marker_database_path: str = 'resources/databases/Cell_marker_All.xlsx', 
        n_top_markers: int = 20,
    ) -> Dict[str, Any]:
        """
        Execute Wilcoxon rank calculations and match phenotypes via CellMarker 2.0 repository.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param target_cluster_key: Target column name inside rna metadata observing group labels.
        :type target_cluster_key: str
        :param marker_database_path: Trajectory on the filesystem containing the CellMarker 2.0 Excel data.
        :type marker_database_path: str
        :param n_top_markers: Total count of top overexpressed features passed to set operations.
        :type n_top_markers: int
        :param organism: Focus model taxonomy template switch ('human' or 'mouse').
        :type organism: str
        :return: Completed identification registry containing cluster slice arrays with extended metadata.
        :rtype: Dict[str, Any]
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural asset schema confirmation checks
        
        logger.info("Initializing unique Overlap Coefficient extraction strategy engine using CellMarker 2.0.")
        
        if 'rna' not in mdata.mod:
            logger.error("Aborting strategy calculation loop. Modality layer 'rna' missing.", exc_info=True) 
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

        # Standardize organism string to match CellMarker 2.0 capitalization format
        species_filter = "Human" if organism.lower() == 'human' else "Mouse" 
        db_df = db_df[db_df['species'].str.lower() == species_filter.lower()] 
        
        # Standardize gene symbols and cross-reference with available RNA data dataset
        db_df['Symbol'] = db_df['Symbol'].astype(str).str.upper() 
        panel_genes_upper = [str(g).upper() for g in rna_adata.var_names] 
        filtered_db = db_df[db_df['Symbol'].isin(panel_genes_upper)] 

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Calculate highly expressed differential markers per cluster using Wilcoxon rank sum tests
        
        sc.tl.rank_genes_groups(rna_adata, groupby=target_cluster_key, method='wilcoxon', n_genes=n_top_markers)
        
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Populate complete bipartite graph weight edges across all clusters and database markers grouped by ontology
        
        scoring_manifest: List[Dict[str, Any]] = []
        for clus in unique_clusters:
            raw_markers = rna_adata.uns['rank_genes_groups']['names'][str(clus)] 
            cluster_markers_upper = [str(m).upper() for m in raw_markers] 
            clus_cells = rna_adata.obs.index[rna_adata.obs[target_cluster_key] == clus].tolist() 
            
            # Group directly by cellontology_id to eliminate redundant naming layers
            for cl_id, group in filtered_db.groupby('cellontology_id'):
                ref_markers = group['Symbol'].dropna().unique().tolist() 
                
                intersection_set = set(cluster_markers_upper).intersection(set(ref_markers)) 
                union_set = set(cluster_markers_upper).union(set(ref_markers)) 
                jaccard_score = len(intersection_set) / len(union_set) if len(union_set) > 0 else 0.0 

                # Retain all score parameters to supply the linear sum assignment grid with global configuration choices
                first_row = group.iloc[0] 
                meta = {
                    "cellontology_id": str(cl_id),
                    "uberonontology_id": str(first_row.get('uberonongology_id', 'NaN')), 
                    "tissue_class": str(first_row.get('tissue_class', 'NaN')), 
                    "tissue_type": str(first_row.get('tissue_type', 'NaN')), 
                    "cancer_type": str(first_row.get('cancer_type', 'NaN')), 
                    "cell_type": str(first_row.get('cell_name', 'NaN')), 
                    "uniprot_id": str(first_row.get('UNIPROTID', 'NaN')), 
                    "marker_source": str(first_row.get('marker_source', 'NaN')), 
                    "pmid": str(first_row.get('PMID', 'NaN')), 
                    "publication_title": str(first_row.get('Title', 'NaN')) 
                }
                scoring_manifest.append({
                    "cluster": clus, 
                    "cell_name": meta["cell_type"], 
                    "score": jaccard_score, 
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
                        "source": "CellMarker2.0_Global_Jaccard_Optimization", 
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

        logger.info("Discrete matrix enrichment matching loop completed with absolute identifier uniqueness.") 
        return flat_registry 