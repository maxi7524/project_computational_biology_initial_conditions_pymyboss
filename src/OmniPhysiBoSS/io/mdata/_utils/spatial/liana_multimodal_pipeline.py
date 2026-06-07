import anndata
import mudata as mu
import scanpy as sc
import liana as li
import pandas as pd
from typing import Tuple

# Main functional cross-correlation pipeline interface
def run_liana_multimodal_pipeline(
    mdata: mu.MuData,
    x_mod: str = "rna",
    y_mod: str = "rna",
    output_modality_key: str = "rna",
    resource_name: str = "mouseconsensus",
    connectivity_key: str = "spatial_connectivities",
    liana_key: str = "liana_res",
    local_name: str = "cosine",
    seed: int = 1337,
    x_name: str = "ligand",
    y_name: str = "receptor"
) -> mu.MuData:
    """
    Executes spatial neighbor graphs and customizable bivariate cross-correlation
    analyses natively over an aligned, harmonized MuData container configuration.

    **Nomenclature Selection Guide for `x_name` and `y_name`**:
    To avoid structural KeyError tracking faults, you must align `x_name` and `y_name` 
    with the column headers of your chosen resource database. 
    
    - For standard Ligand-Receptor databases (e.g., 'mouseconsensus', 'humanconsensus'):
      Set `x_name='ligand'` and `y_name='receptor'`.
    - For custom multi-omics or Transcription Factor pairs (e.g., cell-type to TF cross products):
      Set `x_name='celltype'` and `y_name='tf'` (or matching custom column keys).
    
    You can inspect columns via: `print(liana.rs.select_resource(resource_name).columns)`.

    :param mdata: The aligned, pre-harmonized MuData container.
    :type mdata: mu.MuData
    :param x_mod: Modality key representing the source/ligand features, defaults to "rna".
    :type x_mod: str
    :param y_mod: Modality key representing the target/receptor features, defaults to "rna".
    :type y_mod: str
    :param output_modality_key: Target modality slot where the final bivariate DataFrame is saved, defaults to "rna".
    :type output_modality_key: str
    :param resource_name: Name of the ligand-receptor or molecular database, defaults to "mouseconsensus".
    :type resource_name: str
    :param connectivity_key: Target key for storage of the spatial adjacency matrix, defaults to "spatial_connectivities".
    :type connectivity_key: str
    :param liana_key: Target key under .uns where results are stored, defaults to "liana_res".
    :type liana_key: str
    :param local_name: Local scoring metric style (e.g., 'cosine', 'pearson', 'morans'), defaults to "cosine".
    :type local_name: str
    :param seed: Pseudorandom number generator initialization seed, defaults to 1337.
    :type seed: int
    :param x_name: Column name for the source entities in the resource, defaults to "ligand".
    :type x_name: str
    :param y_name: Column name for the target entities in the resource, defaults to "receptor".
    :type y_name: str
    :return: Processed MuData instance with populated spatial annotations.
    :rtype: mu.MuData
    """
    # Parameter derivation and optimization phase
    ## Extract spatial coordinates matrix from the source modality workspace
    adata_spatial = mdata[x_mod]
    spatial_coords = adata_spatial.obsm['spatial']
    
    ## Sanitize input connectivity strings using the idempotent helper logic
    base_conn_key, expected_obsp_key = _sanitize_connectivity_key(connectivity_key)

    # Dynamic bandwidth scanning loop
    print(f"\n[-] Scanning spatial density distributions for modality: '{x_mod}'...")
    _, df_bandwidth = li.ut.query_bandwidth(
        coordinates=spatial_coords,
        start=0,
        end=50_000,
        interval_n=30
    )

    ## Extract valid bandwidth constants satisfying the strict k >= 6 condition
    valid_rows = df_bandwidth[df_bandwidth['neighbours'] >= 6]
    if not valid_rows.empty:
        min_bandwidth = float(valid_rows['bandwith'].min())
        print(f" -> Optimal mathematical bandwidth isolated (k >= 6): {min_bandwidth}")
    else:
        min_bandwidth = float(df_bandwidth['bandwith'].max())
        print(f"[!] Warning: Safe bandwidth bound (k >= 6) unreached. Utilizing max fallback: {min_bandwidth}")

    # Spatial graph generation block
    ## Package optimized neighbor configuration constraints for the spatial matrix
    neighbors_config = {
        'adata': adata_spatial,
        "kernel": "gaussian",
        "bandwidth": min_bandwidth,
        "cutoff": 0.1,
        "set_diag": False,
        "key_added": base_conn_key
    }

    print(f"[-] Computing spatial neighbors into modality '{x_mod}'].obsp['{expected_obsp_key}']...")
    li.ut.spatial_neighbors(**neighbors_config)

    # Global tracking sync phase
    ## Mirror internal graph structural allocations to the global root pointers
    mdata.obsp = mdata[x_mod].obsp
    mdata.update()

    # Local bivariate association scoring block
    ## Package customized multimodal tracking options into the payload array
    bivariate_config = {
        'mdata': mdata,
        'x_mod': x_mod,
        'y_mod': y_mod,
        'local_name': local_name,
        # TODO experiment - for finding if spatial positions are important
        'global_name': 'morans',
        'resource_name': resource_name,
        # TODO experiment - for finding randomness of certain signals (permutation tests)
        'n_perms': 1_000,
        # 'n_perms': None,
        # TODO experimental 
        'add_categories': True,
        'mask_negatives': True,
        'seed': seed,
        'connectivity_key': expected_obsp_key,
        'x_use_raw': False,
        'y_use_raw': False,
        'x_name': x_name,
        'y_name': y_name
    }

    print(f"[-] Computing bivariate association scores via '{local_name}'...")
    bivariate_res = li.mt.bivariate(**bivariate_config)

    # Post-processing result mapping phase
    ## Route computed data tables back into the requested output modality workspace
    if bivariate_res is not None:
        mdata[output_modality_key].uns[liana_key] = bivariate_res
        print(f"[✓] Local bivariate metrics mapped to mdata['{output_modality_key}'].uns['{liana_key}']")
    else:
        print("[!] Critical: Bivariate execution returned empty context framework.")

    ## Finalize data update sequences across all managed modules
    mdata.update()
    return mdata


# ----------------------------------
# Helpers 
# ----------------------------------

# Idempotent connectivity metadata key handling helper
def _sanitize_connectivity_key(connectivity_key: str) -> Tuple[str, str]:
    """
    Sanitizes connectivity string inputs to derive key names idempotently.

    :param connectivity_key: The input raw tracking key parameter string.
    :type connectivity_key: str
    :return: A tuple containing (base_connectivity_key, expected_obsp_key).
    :rtype: tuple of (str, str)
    """
    # String pattern matching and reduction
    ## Prevent trailing appending faults if the configuration key already contains the suffix
    if connectivity_key.endswith("_connectivities"):
        base_conn_key = connectivity_key.replace("_connectivities", "")
        expected_obsp_key = connectivity_key
    else:
        base_conn_key = connectivity_key
        expected_obsp_key = f"{connectivity_key}_connectivities"
        
    return base_conn_key, expected_obsp_key