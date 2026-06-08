
import mudata as mu
from typing import List
from .validate_unify_modalities_overlap_failure import validate_separated_modalities_overlap

# ==============================================================================
# Data Harmonization Layer
# ==============================================================================
# TODO tests
# check if mdata contains all needed dictonaries
# check intersection functinnality very 


def unify_multimodal_data(
    mdata: mu.MuData, 
    modalities: List[str],
    main_modality: str = "rna"
) -> mu.MuData:
    """
    Performs a strict mathematical inner join across specified omics layers,
    logs detailed data retention statistics, and synchronizes reference arrays.

    :param mdata: The unaligned input multimodal container.
    :type mdata: mu.MuData
    :param modalities: List of modality keys to include in the intersection.
    :type modalities: list of str
    :param main_modality: The primary modality key used to anchor global tracking arrays, defaults to "rna".
    :type main_modality: str
    :return: A completely synchronized and dimensionally aligned MuData object.
    :rtype: mu.MuData
    """
    # Structural configuration and boundary checks
    ## Validate that the requested omics layers list contains entries
    if not modalities:
        raise ValueError("The modalities list cannot be empty for alignment.")

    print("=" * 80)
    print("           MULTIMODAL DATA HARMONIZATION & DATA LOSS REPORT")
    print("=" * 80)

    # Modality size profiling loop
    ## Record initial observation counts for every independent tracking layer
    initial_sizes = {}
    for mod in modalities:
        if mod in mdata.mod:
            initial_sizes[mod] = mdata[mod].n_obs
            print(f"[-] Modality Input Size  : '{mod}' contains initially {initial_sizes[mod]} cells.")
        else:
            raise KeyError(f"Requested modality '{mod}' not located in MuData object.")

    # Mathematical intersection calculation
    ## Isolate initial index arrays from the first tracking layer
    shared_cells = set(mdata[modalities[0]].obs_names)
    
    ## Intersect iteratively with the remaining observation axes
    for mod in modalities[1:]:
        if mod in mdata.mod:
            shared_cells = shared_cells.intersection(mdata[mod].obs_names)

    shared_cells_list = list(shared_cells)
    final_count = len(shared_cells_list)


    # Data loss auditing block
    ## Compute exact data attrition metrics and retention percentages
    print("[-] Data Retention Audit Trail:")
    for mod in modalities:
        lost_cells = initial_sizes[mod] - final_count
        retention_pct = (final_count / initial_sizes[mod]) * 100
        print(f"    -> Modality '{mod}': Retained {final_count}/{initial_sizes[mod]} cells "
              f"({retention_pct:.2f}%). Lost {lost_cells} cells.")
    print("=" * 80)

    if final_count == 0:
        print(validate_separated_modalities_overlap(mdata, modalities))
        raise RuntimeError("Strict intersection resulted in 0 shared cellular barcodes.")
    
    # Logger: final count
    print("-" * 80)
    print(f"[✓] Harmonization Complete: {final_count} cells mutually shared across all layers.")
    print("-" * 80)

    # Container slice and reconstruction phase
    ## Extract synchronized deep copies of independent sub-modules
    synchronized_modules = {}
    for mod in modalities:
        synchronized_modules[mod] = mdata[mod][shared_cells_list].copy()

    ## Reconstruct the unified multimodal array framework
    harmonized_mdata = mu.MuData(synchronized_modules)
    
    # Global tracking array initialization block
    ## Ensure that the anchor modality contains fully instantiated tracking dicts
    main_adata = harmonized_mdata[main_modality]
    
    ## Explicitly initialize dictionaries to prevent missing proxy registration faults
    if not hasattr(main_adata, 'obsp') or main_adata.obsp is None:
        main_adata.obsp = {}
    if not hasattr(main_adata, 'uns') or main_adata.uns is None:
        main_adata.uns = {}
    if not hasattr(main_adata, 'obsm') or main_adata.obsm is None:
        main_adata.obsm = {}

    ## Bind sub-modality tracking mappings directly to the root MuData structure
    print(f"[-] Linking initialized main modality '{main_modality}' tracking maps to global root...")
    harmonized_mdata.obsp = main_adata.obsp
    harmonized_mdata.uns = main_adata.uns
    harmonized_mdata.obsm = main_adata.obsm
    print(f"[✓] Linking complete")
    
    ## Synchronize internal structure states globally
    harmonized_mdata.update()
    return harmonized_mdata

