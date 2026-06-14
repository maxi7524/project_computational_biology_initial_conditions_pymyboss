# Heading 1 (Broad context / Top-level block / Script section)
# Modular processing utility for cellular graph clustering inside MuData containers.

from typing import Optional
import mudata as mu
import scanpy as sc

from ..common import safe_synchronize_mudata_layers
from .....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

# Heading 1 (Broad context / Top-level block / Script section)
# Core operational functions for unsupervised clustering pipelines

def compute_leiden_partitions(
    mdata: mu.MuData,
    resolution: float = 1,
    target_cluster_key: str = 'leiden',
    n_neighbors: int = 15,
    batch_key: Optional[str] = None,
    force_recompute: bool = False
) -> None:
    """
    Execute Shared Nearest Neighbor graph instantiation and Leiden community 
    detection over the high-dimensional transcriptomic modality layer.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param resolution: Modularity optimization resolution scaling parameter.
    :type resolution: float
    :param target_cluster_key: Target column key within mdata.mod['rna'].obs to store cluster assignments.
    :type target_cluster_key: str
    :param n_neighbors: Size of local neighborhood tracking domain for graph calculation.
    :type n_neighbors: int
    :param batch_key: Metadata variable identifying sample or technical batch groups for BBKNN correction.
    :type batch_key: Optional[str]
    :param force_recompute: Intercept existing calculations and force matrix regeneration.
    :type force_recompute: bool
    :raises KeyError: If the required 'rna' modality container cannot be resolved.
    """
    # Module initialization phase
    logger.info("Initializing multi-cellular unsupervised partitioning block.")
    
    if 'rna' not in mdata.mod:
        logger.error("Execution context execution aborted. Missing mandatory 'rna' modality data slice.", exc_info=True)
        raise KeyError("Missing 'rna' modality container inside the target MuData asset.")

    rna_adata = mdata.mod['rna']

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Check for existing structural annotations to prevent redundant matrix loops
    if target_cluster_key in rna_adata.obs.columns and not force_recompute:
        logger.info("Target cluster tracker key '%s' already exists inside metadata. Skipping evaluation loop.", target_cluster_key)
        return

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Evaluate spatial and transcriptomic connectivity structures based on batch indicators
    if batch_key and batch_key in rna_adata.obs.columns:
        ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
        ### Route computational flow through Batch Balanced K-Nearest Neighbors matrix pipeline
        logger.info("Batch index column detected. Invoking BBKNN graph integration via key: %s", batch_key)
        import scanpy.external as sce
        
        if 'X_pca' not in rna_adata.obsm:
            logger.debug("Prerequisite PCA coordinates missing from data matrix. Computing default sc.tl.pca reduction.")
            sc.tl.pca(rna_adata)
            
        ### obtain amount of types in batch 
        unique_batches = rna_adata.obs[batch_key].unique()
        n_unique_batches = len(unique_batches)
        neighbors_per_batch = n_neighbors // n_unique_batches

        sce.pp.bbknn(rna_adata, batch_key=batch_key, neighbors_within_batch= neighbors_per_batch)
    else:
        ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
        ### Fallback to standard standard graph metric evaluation routines
        if 'neighbors' not in rna_adata.uns or force_recompute:
            logger.info("Calculating single-cell proximity graphs using %d nearest neighbors parameters.", n_neighbors)
            if 'X_pca' not in rna_adata.obsm:
                logger.debug("Executing heuristic PCA reduction framework before computing neighbors matrix.")
                sc.tl.pca(rna_adata)
            sc.pp.neighbors(rna_adata, n_neighbors=n_neighbors, use_rep='X_pca')
        else:
            logger.debug("Pre-existing proximity graph connectivities detected. Reusing structural arrays.")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Run the final modularity optimization algorithm using the compiled network state
    ### Leiden graph partitioning
    logger.info("Triggering Leiden graph partitioning with resolution: %s", resolution)
    sc.tl.leiden(rna_adata, resolution=resolution, key_added=target_cluster_key)

    ### UMAP embedding computation
    logger.info("Computing UMAP embedding")
    sc.tl.umap(rna_adata)

    ### PCA visualization
    logger.info("Generating PCA plot")
    sc.pl.pca(rna_adata, return_fig=False)

    # Synchronize multimodal structural links across container arrays
    safe_synchronize_mudata_layers(mdata, True, True)
    logger.info("Multicellular clustering step completed successfully. Output injected under key: %s", target_cluster_key)