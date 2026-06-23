# Heading 1 (Broad context / Top-level block / Script section)
# Analytical figure matrix and visualization rendering pipeline.

#TODO - będzie trzeba zrobić tak, że 


import os
from typing import List, Dict, Any, Union
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import mudata as mu
import decoupler as dc

from ...utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

# Heading 1 (Broad context / Top-level block / Script section)
# Shared plotting pipeline input schema assertion checks

def _validate_visualization_slots(mdata: mu.MuData, required_obs: List[str]) -> None:
    """
    Assert structural compliance of critical measurement entries before rendering figures.

    :param mdata: Target container asset.
    :type mdata: mu.MuData
    :param required_obs: List of observation strings that must exist in data slots.
    :type required_obs: List[str]
    :raises KeyError: If columns or modalities are missing from validation bounds.
    """
    if 'rna' not in mdata.mod:
        logger.error("Analysis initialization aborted. Missing 'rna' modality container.", exc_info=True)
        raise KeyError("Missing rna modality.")
    for key in required_obs:
        if key not in mdata.mod['rna'].obs.columns:
            logger.error("Required key %s missing from observation data slots.", key, exc_info=True)
            raise KeyError(f"Missing required annotation tracker: {key}")

# Heading 1 (Broad context / Top-level block / Script section)
# Programmatic rendering plot definitions

def plot_leiden_spatial_comparison(mdata: mu.MuData, output_dir: str, cluster_key: str = 'leiden') -> None:
    """
    Render a composite plot showing the Leiden clustering projection in UMAP 
    latent space alongside its physical spatial coordinate coordinates.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param cluster_key: Key under mdata.mod['rna'].obs identifying target cluster tracking groups.
    :type cluster_key: str
    :param output_dir: Target filesystem folder path for vector asset saving operations.
    :type output_dir: str
    """
    _validate_visualization_slots(mdata, [cluster_key])
    logger.info("Generating latent vs physical spatial comparison grids.")
    
    os.makedirs(output_dir, exist_ok=True)
    rna_adata = mdata.mod['rna']

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Initialize structural figure canvases
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left subplot panel: UMAP latent space distribution
    sc.pl.umap(rna_adata, color=cluster_key, ax=axes[0], show=False)
    axes[0].set_title("Latent Space Embedding (UMAP)")
    
    # Right subplot panel: Physical coordinates distribution on the tissue slide
    sc.pl.spatial(rna_adata, color=cluster_key, ax=axes[1], show=False)
    axes[1].set_title("Physical Spatial Matrix Alignment")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Save high-resolution vector layout to the output directory
    save_path = os.path.join(output_dir, "leiden_spatial_comparison.png")
    plt.tight_layout()
    fig.savefig(save_path, dpi=180, bbox_inches='tight')
    plt.close(fig)
    logger.debug("Comparison grid saved successfully to target file: %s", save_path)


def plot_cell_type_validation_trio(mdata: mu.MuData, cell_type_key: str, output_dir: str, cluster_key: str = 'leiden') -> None:
    """
    Generate a 3-panel figure showing the selected cell type's UMAP score, 
    its spatial distribution, and a cluster-level validation violin plot.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param cell_type_key: Target cell identity string to plot from the score matrix.
    :type cell_type_key: str
    :param cluster_key: Observation category key used to group violin arrays.
    :type cluster_key: str
    :param output_dir: Target folder directory path.
    :type output_dir: str
    """
    if "score_ulm" not in mdata.mod['rna'].obsm:
        logger.error("Decoupler score array data missing from target .obsm slot.", exc_info=True)
        raise KeyError("Missing score_ulm slot.")
        
    logger.info("Generating 3-panel validation grid for targeted cell type: %s", cell_type_key)
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract continuous profile data objects from .obsm space
    score_adata = dc.pp.get_obsm(mdata.mod['rna'], key="score_ulm")
    
    if cell_type_key not in score_adata.var_names:
        logger.error("Target lineage key %s is missing from score matrices variables.", cell_type_key, exc_info=True)
        raise KeyError(f"Cell type {cell_type_key} not in score matrices data array.")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Build a 1 row by 3 column figure layout
    fig = plt.figure(figsize=(18, 5))
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    sc.pl.umap(score_adata, color=cell_type_key, cmap="RdBu_r", ax=ax1, show=False)
    ax1.set_title(f"{cell_type_key} - Latent UMAP Weight")

    sc.pl.spatial(score_adata, color=cell_type_key, cmap="RdBu_r", ax=ax2, show=False)
    ax2.set_title(f"{cell_type_key} - Physical Tissue Gradient")

    sc.pl.violin(score_adata, keys=cell_type_key, groupby=cluster_key, rotation=90, ax=ax3, show=False)
    ax3.set_title(f"Cluster Profile Expression Bounds")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Save programmatic output to the output folder path trajectory
    save_path = os.path.join(output_dir, f"validation_trio_{cell_type_key.replace(' ', '_')}.png")
    plt.tight_layout()
    fig.savefig(save_path, dpi=180, bbox_inches='tight')
    plt.close(fig)
    logger.debug("Validation trio file saved successfully to: %s", save_path)


def plot_expression_matrix_dendrogram(mdata: mu.MuData, markers_dict: Dict[str, List[str]], output_dir: str, cluster_key: str = 'leiden') -> None:
    """
    Render clustered matrix plots alongside derived hierarchical trees 
    mapping gene expressions or enrichment values across resolved group ids.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param markers_dict: Named reference sets list mapped to biological cluster indices.
    :type markers_dict: Dict[str, List[str]]
    :param cluster_key: Observation partition grouping ID label tracker string.
    :type cluster_key: str
    :param output_dir: Target filesystem location folder directory path.
    :type output_dir: str
    """
    _validate_visualization_slots(mdata, [cluster_key])
    logger.info("Generating expression matrix layouts alongside cluster tree dendrogram graphs.")
    os.makedirs(output_dir, exist_ok=True)
    
    # Fall back to using the enrichment score layer if available, otherwise use log-transformed rna counts
    if "score_ulm" in mdata.mod['rna'].obsm:
        plotting_asset = dc.pp.get_obsm(mdata.mod['rna'], key="score_ulm")
        logger.debug("Routing dendrogram plot data flow through Decoupler score matrices arrays.")
    else:
        plotting_asset = mdata.mod['rna']
        logger.debug("Routing plotting pipelines using baseline modality observation matrices.")

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Render matrix plot layout matrix structure
    mp = sc.pl.matrixplot(
        adata=plotting_asset,
        var_names=markers_dict,
        groupby=cluster_key,
        dendrogram=True,
        standard_scale="var",
        cmap="RdBu_r",
        show=False
    )
    
    save_path = os.path.join(output_dir, "cluster_expression_matrixplot.png")
    mp.savefig(save_path, dpi=180)
    logger.debug("Matrixplot file written successfully to file destination tracker: %s", save_path)


def plot_population_distribution_grid(mdata: mu.MuData, metrics_to_plot: List[str], output_dir: str, cluster_key: str = 'leiden') -> None:
    """
    Construct an adaptive grid layout (K rows by 4 columns) to visualize the 
    distribution profiles of biological variables across cell cohorts.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param metrics_to_plot: Metric variable labels inside observations layers.
    :type metrics_to_plot: List[str]
    :param cluster_key: Focus categorical grouping variable flag identifier string.
    :type cluster_key: str
    :param output_dir: Destination folder directory tracker path.
    :type output_dir: str
    """
    _validate_visualization_slots(mdata, [cluster_key])
    logger.info("Building distribution layout matrices grid canvas shapes.")
    os.makedirs(output_dir, exist_ok=True)
    
    obs_df = mdata.mod['rna'].obs
    valid_metrics = [m for m in metrics_to_plot if m in obs_df.columns]
    
    if not valid_metrics:
        logger.error("Supplied parameter metric list does not overlap observation columns data frames.", exc_info=True)
        return

    total_plots = len(valid_metrics)
    cols = 4
    # Dynamically scale grid rows based on the requested target variables list count
    rows = (total_plots + cols - 1) // cols

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Generate composite subplot arrays
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes_flat = axes.flatten() if total_plots > 1 else [axes]

    for index, metric in enumerate(valid_metrics):
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Loop through variables to draw box plots across cluster indices
        sns.boxplot(
            data=obs_df,
            x=cluster_key,
            y=metric,
            ax=axes_flat[index],
            palette="Set2"
        )
        axes_flat[index].set_title(f"Distribution: {metric}")
        axes_flat[index].tick_params(axis='x', rotation=45)

    ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
    ### Remove unused grid slots to keep layouts clean
    for empty_index in range(index + 1, len(axes_flat)):
        fig.delaxes(axes_flat[empty_index])

    save_path = os.path.join(output_dir, "population_distribution_grid.png")
    plt.tight_layout()
    fig.savefig(save_path, dpi=160, bbox_inches='tight')
    plt.close(fig)
    logger.info("Distribution visualization engine written to destination output directory tracker safely.")