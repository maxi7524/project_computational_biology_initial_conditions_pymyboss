import mudata as mu
import warnings
from typing import List
from .validate_unify_modalities_overlap_failure import validate_separated_modalities_overlap
from OmniPhysiBoSS.utils.logger import get_custom_logger
from ..common import safe_synchronize_mudata_layers

logger = get_custom_logger(__name__)

# ==============================================================================
# Data Intersection Alignment Layer
# ==============================================================================


def unify_multimodal_data(
    mdata: mu.MuData, 
    modalities: List[str],
    main_modality: str = "rna"
) -> mu.MuData:
    """
    Performs a strict mathematical inner join across specified omics layers,
    enforces feature index uniqueness, and synchronizes structural references.

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
    logger.info("Starting multimodal data intersection alignment matrix pipeline.")
    ## Validate that the requested omics layers list contains entries
    if not modalities:
        raise ValueError("The modalities list cannot be empty for alignment.")

    logger.info("--- MULTIMODAL DATA INTERSECTION ALIGNMENT & DATA LOSS REPORT ---")

    # Modality size profiling and index sanitization loop
    ## Record initial observation counts and force variable name uniqueness
    initial_sizes = {}
    for mod in modalities:
        if mod in mdata.mod:
            initial_sizes[mod] = mdata[mod].n_obs
            
            ### Enforce variable name uniqueness to prevent downstream mapping collisions
            logger.debug("Enforcing unique variable names for modality layer: %s", mod)
            mdata[mod].var_names_make_unique()
            
            logger.info("Modality Input Size - Layer '%s': initially contains %s cells.", mod, initial_sizes[mod])
        else:
            raise KeyError(f"Requested modality '{mod}' not located in MuData object.")

    # Mathematical intersection calculation
    ## Isolate initial index arrays from the first tracking layer
    shared_cells = set(mdata[modalities[0]].obs_names)
    
    ## Intersect iteratively with the remaining observation axes
    for mod in modalities[1:]:
        if mod in mdata.mod:
            shared_cells = shared_cells.intersection(mdata[mod].obs_names)
            logger.debug("Calculated iterative intersection subset size after modality %s: %s", mod, len(shared_cells))

    shared_cells_list = list(shared_cells)
    final_count = len(shared_cells_list)

    # Data loss auditing block
    ## Compute exact data attrition metrics and retention percentages
    logger.info("Data Retention Audit Trail:")
    for mod in modalities:
        lost_cells = initial_sizes[mod] - final_count
        retention_pct = (final_count / initial_sizes[mod]) * 100
        logger.info(" -> Modality '%s': Retained %s/%s cells (%s%%). Lost %s cells.", mod, final_count, initial_sizes[mod], f"{retention_pct:.2f}", lost_cells)

    if final_count == 0:
        logger.error("Strict intersection resulted in 0 shared cellular barcodes across specified layers.")
        diag_report = validate_separated_modalities_overlap(mdata, modalities)
        logger.debug("Intersection failure diagnostics report: %s", diag_report)
        raise RuntimeError("Strict intersection resulted in 0 shared cellular barcodes.")
    
    logger.info("Intersection Alignment Complete: %s cells mutually shared across all layers.", final_count)

    # Container slice and reconstruction phase
    ## Extract synchronized deep copies of independent sub-modules
    synchronized_modules = {}
    for mod in modalities:
        synchronized_modules[mod] = mdata[mod][shared_cells_list].copy()
        logger.debug("Synchronized slice extracted for modality module: %s", mod)

    ## Reconstruct the unified multimodal array framework pod wyciszonym filtrem ostrzeżeń
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning, module="mudata")
        harmonized_mdata = mu.MuData(synchronized_modules)
    
    ## Enforce global MuData level variable name uniqueness to clean up multi-omics cross-collisions
    logger.debug("Enforcing global variable name uniqueness across combined omics layers.")
    harmonized_mdata.var_names_make_unique()
    
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
    logger.info("Linking main modality '%s' tracking dictionaries directly to global root references.", main_modality)
    harmonized_mdata.obsp = main_adata.obsp
    harmonized_mdata.uns = main_adata.uns
    harmonized_mdata.obsm = main_adata.obsm
    
    ## Synchronize internal structure states explicitly enforcing forward-compatible conventions
    logger.debug("Executing explicit structural data pulls to global containers.")
    safe_synchronize_mudata_layers(harmonized_mdata, pull_obs=True, pull_var=False, inplace=True)
    
    logger.info("Global structural array updates synchronized.")
    return harmonized_mdata