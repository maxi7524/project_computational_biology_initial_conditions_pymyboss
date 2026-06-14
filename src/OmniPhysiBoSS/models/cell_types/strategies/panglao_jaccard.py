# Heading 1 (Broad context / Top-level block / Script section)
# Discrete overlap coefficient extraction strategy with uniqueness constraint enforcement.

import os
from typing import Dict, Any, Set
import pandas as pd
import mudata as mu
import scanpy as sc

from ..cell_types_base import BaseCellTypeExtractor
from ....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

class PanglaoJaccardExtractor(BaseCellTypeExtractor):
    """
    Annotates cell clusters by calculating explicit binary Jaccard set intersections 
    between cluster markers and a local PanglaoDB reference file.
    """

    def extract_cell_types(
        self, 
        mdata: mu.MuData, 
        target_cluster_key: str, 
        marker_database_path: str = 'resources/databases/panglaoDB.tsv', 
        n_top_markers: int = 20,
        organism: str = 'mouse'
    ) -> Dict[str, Any]:
        """
        Execute Wilcoxon rank calculations and match phenotypes via collision-free overlap scores.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param target_cluster_key: Target column name inside rna metadata observing group labels.
        :type target_cluster_key: str
        :param marker_database_path: Trajectory on the filesystem containing the PanglaoDB TSV data.
        :type marker_database_path: str
        :param n_top_markers: Total count of top overexpressed features passed to set operations.
        :type n_top_markers: int
        :param organism: Focus model taxonomy template switch ('mouse' or 'human').
        :type organism: str
        :return: Completed identification registry containing cluster slice arrays with unique labels.
        :rtype: Dict[str, Any]
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural asset schema confirmation checks
        logger.info("Initializing unique Overlap Coefficient extraction strategy engine.")
        
        if 'rna' not in mdata.mod:
            logger.error("Aborting strategy calculation loop. Modality layer 'rna' missing.", exc_info=True)
            raise KeyError("Missing 'rna' modality container.")
            
        if not os.path.exists(marker_database_path):
            logger.error("Target database reference file missing at path: %s", marker_database_path, exc_info=True)
            raise FileNotFoundError(f"Database asset missing: {marker_database_path}")

        rna_adata = mdata.mod['rna']
        unique_clusters = rna_adata.obs[target_cluster_key].unique()

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Load local database matrix and force strict uppercase normalization
        db_df = pd.read_csv(marker_database_path, sep='\t')
        
        # Taxonomy mapping conversion logic from strategy parameters
        species_token = "Mm" if organism.lower() == 'mouse' else "Hs"
        db_df = db_df[db_df['species'].str.contains(species_token, na=False)]
        
        # Standardize gene naming keys to completely eliminate case mismatches
        db_df['official gene symbol'] = db_df['official gene symbol'].str.upper()
        panel_genes_upper = [str(g).upper() for g in rna_adata.var_names]
        filtered_db = db_df[db_df['official gene symbol'].isin(panel_genes_upper)]

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Calculate highly expressed differential markers per cluster using Wilcoxon rank sum tests
        sc.tl.rank_genes_groups(rna_adata, groupby=target_cluster_key, method='wilcoxon', n_genes=n_top_markers)
        
        cell_lineage_registry = {}
        assigned_identifiers: Set[str] = set()

        for clus in unique_clusters:
            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Process intersections over standardized uppercase string spaces
            raw_markers = rna_adata.uns['rank_genes_groups']['names'][str(clus)]
            cluster_markers_upper = [str(m).upper() for m in raw_markers]
            clus_cells = rna_adata.obs.index[rna_adata.obs[target_cluster_key] == clus].tolist()
            
            best_label = "Unknown"
            max_overlap = 0.0

            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Compute Simpson overlap coefficients against unique database reference cell types
            for cell_type, group in filtered_db.groupby('cell type'):
                ref_markers = group['official gene symbol'].tolist()
                
                intersection_set = set(cluster_markers_upper).intersection(set(ref_markers))
                union_set = set(cluster_markers_upper).union(set(ref_markers))
                
                jaccard_score = len(intersection_set) / len(union_set) if len(union_set) > 0 else 0.0

                if jaccard_score > max_overlap:
                    max_overlap = jaccard_score
                    best_label = cell_type

            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Enforce global uniqueness constraint on resolved identities to prevent identifier duplication
            base_label = best_label
            if base_label in assigned_identifiers:
                logger.debug("Collision detected for label: %s. Appending cluster token for unique resolution.", base_label)
                best_label = f"{base_label}_{clus}"
            
            assigned_identifiers.add(best_label)
            logger.info("Cluster %s assigned to unique identifier: %s (Score: %f)", str(clus), best_label, max_overlap)

            cell_lineage_registry[str(clus)] = {
                "cell_indices": clus_cells,
                "cell_count": len(clus_cells),
                "database_reference": {
                    "source": "PanglaoDB_Local_Overlap",
                    "identifier": best_label,
                    "confidence_score": float(max_overlap),
                    "status": "aligned"
                }
            }

        logger.info("Discrete matrix enrichment matching loop completed with absolute identifier uniqueness.")
        return cell_lineage_registry