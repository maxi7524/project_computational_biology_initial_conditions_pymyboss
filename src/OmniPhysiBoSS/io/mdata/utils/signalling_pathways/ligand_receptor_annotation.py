# =============================================================================
# Curated Intercellular Metadata Enrichment Module
# =============================================================================

import mudata as mu
import pandas as pd
import omnipath as op
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


def fetch_liana_interactions(
    mdata: mu.MuData,
    liana_uns_key: str = "liana_res",
    output_uns_key: str = "intercellular_metadata_registry",
    liana_ligand_col: str = "ligand",
    liana_receptor_col: str = "receptor",
    op_source_col: str = "genesymbol_intercell_source",
    op_target_col: str = "genesymbol_intercell_target"
) -> mu.MuData:
    """
    Extract unique interactions from LIANA .var dataframe, map them with complete
    OmniPath intercell metadata columns using parameterized tracking keys, deduplicate 
    redundant structural matches, and handle missing references using explicit None values.

    :param mdata: High-dimensional aligned multi-modal container asset.
    :type mdata: mu.MuData
    :param liana_uns_key: Key under root .uns accessing the LIANA AnnData object, defaults to "liana_res".
    :type liana_uns_key: str
    :param output_uns_key: Destination target key under root .uns for the merged dataframe, defaults to "intercellular_metadata_registry".
    :type output_uns_key: str
    :param liana_ligand_col: Target column name for ligands inside LIANA .var, defaults to "ligand".
    :type liana_ligand_col: str
    :param liana_receptor_col: Target column name for receptors inside LIANA .var, defaults to "receptor".
    :type liana_receptor_col: str
    :param op_source_col: Target column name for sources inside OmniPath database, defaults to "genesymbol_intercell_source".
    :type op_source_col: str
    :param op_target_col: Target column name for targets inside OmniPath database, defaults to "genesymbol_intercell_target".
    :type op_target_col: str
    :return: The updated multimodal container with integrated database assets.
    :rtype: mu.MuData
    """
    # Environment and structural boundary validation
    if liana_uns_key not in mdata.uns:
        raise KeyError(f"Critical error: LIANA structural object '{liana_uns_key}' absent from root .uns registry.")

    # Data extraction phase
    ## Extract the variable annotations dataframe directly from the stored LIANA AnnData workspace
    liana_var_df = mdata.uns[liana_uns_key].var.copy().reset_index()

    # Resolution of matching columns inside LIANA data
    if liana_ligand_col not in liana_var_df.columns or liana_receptor_col not in liana_var_df.columns:
        ## Parse composite index or string headers if parameterized columns are missing
        composite_col = "index" if "index" in liana_var_df.columns else "var_names"
        if composite_col in liana_var_df.columns:
            separator = "_" if liana_var_df[composite_col].astype(str).str.contains("_").any() else "-"
            split_tracks = liana_var_df[composite_col].astype(str).str.split(separator, n=1, expand=True)
            liana_var_df[liana_ligand_col] = split_tracks[0]
            liana_var_df[liana_receptor_col] = split_tracks[1]
        else:
            raise KeyError(f"Specified tracking keys '{liana_ligand_col}' and '{liana_receptor_col}' cannot be resolved.")

    ## Create standardized upper-case string columns to guarantee match compatibility across organisms
    liana_var_df["_ligand_join_key"] = liana_var_df[liana_ligand_col].astype(str).str.upper()
    liana_var_df["_receptor_join_key"] = liana_var_df[liana_receptor_col].astype(str).str.upper()

    # Database query phase
    ## Request the complete intercell annotation database from OmniPath web service clients
    logger.info("Requesting comprehensive intercellular metadata network from OmniPath.")
    omnipath_intercell_df = op.interactions.import_intercell_network()

    # Database key validation and fallback tracking
    if op_source_col not in omnipath_intercell_df.columns:
        logger.warning("Parametrized source column '%s' missing in OmniPath. Falling back to 'source'.", op_source_col)
        op_source_col = "source"
    if op_target_col not in omnipath_intercell_df.columns:
        logger.warning("Parametrized target column '%s' missing in OmniPath. Falling back to 'target'.", op_target_col)
        op_target_col = "target"

    omnipath_intercell_df["_op_source_join_key"] = omnipath_intercell_df[op_source_col].astype(str).str.upper()
    omnipath_intercell_df["_op_target_join_key"] = omnipath_intercell_df[op_target_col].astype(str).str.upper()

    # Core table reconciliation execution
    ## Merge full metadata attributes from OmniPath table into the existing LIANA row framework via left join
    logger.debug("Executing database table reconciliation via left join mapping strategy.")
    merged_metadata_df = pd.merge(
        liana_var_df,
        omnipath_intercell_df,
        left_on=["_ligand_join_key", "_receptor_join_key"],
        right_on=["_op_source_join_key", "_op_target_join_key"],
        how="left"
    )

    # Integrity optimization and deduplication block
    ## Isolate and eliminate duplicate interaction records to keep a strict 1-to-1 relationship mapping
    merged_metadata_df = merged_metadata_df.drop_duplicates(subset=[liana_ligand_col, liana_receptor_col], keep="first")

    # Missing values normalization phase
    ## Explicitly fill unmapped or missing database fields with pythonic None references instead of NaN
    merged_metadata_df = merged_metadata_df.where(pd.notnull(merged_metadata_df), None)

    # Post-processing cleanup logic
    ## Evict intermediate technical tracking vectors used for key uppercase comparisons
    cleanup_cols = ["_ligand_join_key", "_receptor_join_key", "_op_source_join_key", "_op_target_join_key"]
    merged_metadata_df = merged_metadata_df.drop(columns=[c for c in cleanup_cols if c in merged_metadata_df.columns], errors="ignore")

    # Unstructured global metadata slot registration
    ## Save the complete annotated data frame directly to the root container storage
    mdata.uns[output_uns_key] = merged_metadata_df.reset_index(drop=True)
    logger.info("Completed metadata attachment. Stored annotated dataframe under mdata.uns['%s'].", output_uns_key)

    return mdata