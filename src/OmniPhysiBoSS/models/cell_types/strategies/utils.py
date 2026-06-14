# Heading 1 (Broad context / Top-level block / Script section)
# Global assignment matching utilities for multi-scale omics cell type extraction.

from typing import Dict, Any, List, Set
import numpy as np
from scipy.optimize import linear_sum_assignment
import os
import pronto
import pandas as pd
from ....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


#################################
# Algorithms 
#################################


def resolve_global_assignments(scoring_manifest: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Resolve bipartite graph matches globally by maximizing alignment scores to prevent collisions
    anchored explicitly on unique cellontology_id parameters.

    :param scoring_manifest: Unfiltered list of potential matches containing cluster, cell_name, score, and metadata.
    :type scoring_manifest: List[Dict[str, Any]]
    :return: Optimized collision-free registry mapping clusters to their highest unique cell references.
    :rtype: Dict[str, Any]
    """
    # Heading 1 (Broad context / Top-level block / Script section)
    # Unique identifier extraction and tracking index matrices mapping
    logger.info("Executing global score optimization via linear sum assignment matching.")
    
    if not scoring_manifest:
        logger.warning("Scoring manifest array contains no candidate edges. Returning empty assignments.")
        return {}

    # Isolate unique clusters and unique cellontology_id values to build optimization coordinate maps
    unique_clusters = sorted(list({str(edge["cluster"]) for edge in scoring_manifest}))
    unique_ontology_ids = sorted(list({
        str(edge["metadata"].get("cellontology_id")) 
        for edge in scoring_manifest 
        if edge.get("metadata") and edge["metadata"].get("cellontology_id")
    }))

    cluster_to_idx = {cluster: idx for idx, cluster in enumerate(unique_clusters)}
    ontology_to_idx = {oid: idx for idx, oid in enumerate(unique_ontology_ids)}

    num_clusters = len(unique_clusters)
    num_ontology = len(unique_ontology_ids)

    if num_clusters > num_ontology:
        logger.error("Mathematical optimization failed. Count of clusters (%d) exceeds unique ontology IDs (%d).", 
                     num_clusters, num_ontology, exc_info=True)
        raise ValueError("Injective mapping impossible: cluster count exceeds unique ontology IDs.")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Construct weight coordinate matrix for the bipartite graph optimization matrix
    weight_matrix = np.zeros((num_clusters, num_ontology))
    best_edges: Dict[str, Dict[str, Any]] = {}

    for edge in scoring_manifest:
        cluster_id = str(edge["cluster"])
        meta = edge.get("metadata", {})
        cl_id = str(meta.get("cellontology_id", ""))
        score_val = float(edge["score"])
        
        if cl_id not in ontology_to_idx:
            continue
            
        c_idx = cluster_to_idx[cluster_id]
        o_idx = ontology_to_idx[cl_id]
        pair_key = f"{cluster_id}||{cl_id}"
        
        ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
        ### Isolate the maximal configuration score value for duplicate edge instances
        if score_val > weight_matrix[c_idx, o_idx]:
            weight_matrix[c_idx, o_idx] = score_val
            best_edges[pair_key] = edge

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Solve assignment matrix via Hungarian optimization by minimizing negative weights
    cost_matrix = -weight_matrix
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    resolved_assignments: Dict[str, Any] = {}

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Map the optimal configuration track arrays back to output payload schemas
    for r, c in zip(row_ind, col_ind):
        cluster_id = unique_clusters[r]
        cl_id = unique_ontology_ids[c]
        score_val = weight_matrix[r, c]
        
        pair_key = f"{cluster_id}||{cl_id}"
        edge_data = best_edges.get(pair_key, {})
        
        logger.debug("Globally bound cluster %s to cellontology_id %s with score: %s", 
                     cluster_id, cl_id, str(score_val))
        
        resolved_assignments[cluster_id] = {
            "identifier": edge_data.get("cell_name", "Unknown"),
            "confidence_score": score_val,
            "metadata_context": edge_data.get("metadata", {})
        }

    logger.info("Global score resolution completed. Assigned %d unique clusters.", len(resolved_assignments))
    return resolved_assignments

#################################
# Helpers
#################################


# Heading 1 (Broad context / Top-level block / Script section)
# Transformation utilities for structural cellular multi-omics lineage flattening.

def flatten_lineage_registry(cell_lineage_registry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten nested multi-layer extraction dictionaries into a streamlined tabular registry
    indexed by cluster keys to optimize functional ontology mapping performance.

    :param cell_lineage_registry: Structural complex lineage assignments map from strategy extractors.
    :type cell_lineage_registry: Dict[str, Any]
    :return: Flat structured schema containing normalized metadata attributes per cluster segment.
    :rtype: Dict[str, Any]
    """
    # Heading 1 (Broad context / Top-level block / Script section)
    # Registry dictionary layout conversion step
    logger.info("Executing relational flattening loop on nested lineage records.")
    flat_registry: Dict[str, Any] = {}

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Traverse hierarchical components to extract invariant cellontology parameters
    for cluster_id, details in cell_lineage_registry.items():
        ref_data = details.get("database_reference", {})
        meta_ctx = ref_data.get("metadata_context", {})
        
        ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
        ### Isolate core structural dimensions discarding high-dimensional coordinate vectors
        flat_registry[str(cluster_id)] = {
            "cell_count": int(details.get("cell_count", 0)),
            "cellontology_id": str(meta_ctx.get("cellontology_id", "CL:UNKNOWN")),
            "cell_type_name": str(ref_data.get("identifier", "Unknown")),
            "confidence_score": float(ref_data.get("confidence_score", 0.0)),
            "metadata_context": meta_ctx
        }
        
    logger.info("Lineage records successfully flattened. Total registered elements: %d", len(flat_registry))
    return flat_registry


def extract_go_validated_cl_ids(cl_ontology_path: str = 'resources/databases/go-basic.obo') -> Set[str]:
    """
    Scan the entire Gene Ontology graph structure to isolate every Cell Ontology (CL) 
    identifier that maps directly to at least one active GO term configuration.

    :param cl_ontology_path: Trajectory on the filesystem pointing to the go-basic.obo file.
    :type cl_ontology_path: str
    :return: Set of normalized valid CL string identifiers (e.g., 'CL:0000084').
    :rtype: Set[str]
    """
    # Heading 1 (Broad context / Top-level block / Script section)
    # Ingestion of the OBO file asset
    if not os.path.exists(cl_ontology_path):
        raise FileNotFoundError(f"Ontology asset tracking path missing: {cl_ontology_path}")

    cl_ontology = pronto.Ontology(cl_ontology_path)
    valid_cl_ids: Set[str] = set()

    for term in cl_ontology.terms():
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Analyze terms containing a valid GO namespace indicator token
        if "GO:" not in term.id:
            continue

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Parse structural cross-references for embedded CL elements
        if term.xrefs:
            for xref in term.xrefs:
                xref_id_norm = xref.id.replace("_", ":").upper().strip()
                if "CL:" in xref_id_norm:
                    ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
                    ### Clean the token string format to enforce clean standard syntax (CL:XXXXXXX)
                    start_idx = xref_id_norm.find("CL:")
                    cl_token = xref_id_norm[start_idx:].split()[0]  # Split handles trailing comments or spaces
                    valid_cl_ids.add(cl_token)

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Parse relationship dictionaries linking current GO term to external entities
        if term.relationships:
            for rel, related_terms in term.relationships.items():
                for rel_term in related_terms:
                    rel_id_norm = rel_term.id.replace("_", ":").upper().strip()
                    if "CL:" in rel_id_norm:
                        ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
                        ### Isolate identifier boundaries from graph relationship blocks
                        start_idx = rel_id_norm.find("CL:")
                        cl_token = rel_id_norm[start_idx:]
                        valid_cl_ids.add(cl_token)

    return valid_cl_ids