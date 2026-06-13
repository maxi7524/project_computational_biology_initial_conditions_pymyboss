# =============================================================================
# Multi-Modal Data Pipeline Orchestration Facade
# =============================================================================

import mudata as mu
from typing import Dict, List, Optional, Literal

# Structural package imports for pipeline stage execution
from .utils.unify.unify_modalities import unify_multimodal_data
from .utils.signalling_pathways.intracelluar_network import fetch_intracellular_pathway_network
from .utils.signalling_pathways.ligand_receptor_annotation import fetch_liana_interactions
from .utils.spatial.liana_multimodal_pipeline import run_liana_multimodal_pipeline
# Validation functions will be imported from the restructured validate submodule
from .utils.validate.mdata_validator import verify_structural_presence
from .utils.validate.mdata_types import OMNI_PHYSIBOSS_SCHEMA
from .utils.common import safe_synchronize_mudata_layers

from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


# Global configuration and warning management
## Suppress future compatibility warnings from the MuData library
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="mudata")

## Enforce safe library behavior by disabling pull_on_update
import mudata as mu
mu.set_options(pull_on_update=False)




def run_mdata_processing_pipeline(
    mdata: mu.MuData,
    specie: Literal['mouse', 'human'],  
    key_mappings: Optional[Dict[str, str]] = None,
    modalities: Optional[List[str]] = None,
    main_modality: str = "rna",
    liana_uns_key: str = "liana_res",
    intercell_output_key: str = "intercellular_metadata_df",
    intracellular_output_key: str = "intracellular_metadata_df",
    intracellular_resources: Optional[List[str]] = None,
    intracellular_datasets: Optional[List[str]] = None
) -> mu.MuData:
    """
    Execute the complete orchestration pipeline for multi-modal data preparation.

    This facade handles structural key remapping, validation schema enforcement,
    cellular intersection alignment, and OmniPath network annotation injection.

    :param mdata: High-dimensional multi-modal container asset.
    :type mdata: mu.MuData
    :param specie: Target organism for Liana+ resource selection; must be 'mouse' or 'human'.
    :type specie: Literal['mouse', 'human']
    :param key_mappings: Dict translating custom runtime names to canonical schema names (e.g., {'xxx': 'spatial'}).
    :type key_mappings: Optional[Dict[str, str]]
    :param modalities: List of modality keys to include in the alignment join.
    :type modalities: Optional[List[str]]
    :param main_modality: Primary omics layer anchoring the tracking arrays, defaults to "rna".
    :type main_modality: str
    :param liana_uns_key: Source dictionary key containing LIANA results inside the modality, defaults to "liana_res".
    :type liana_uns_key: str
    :param intercell_output_key: Destination root .uns key for intercellular metadata, defaults to "intercellular_metadata_registry".
    :type intercell_output_key: str
    :param intracellular_output_key: Destination root .uns key for intracellular network edgelist, defaults to "omnipath_intracellular".
    :type intracellular_output_key: str
    :param intracellular_resources: Filter registries for OmniPath intracellular network, defaults to None.
    :type intracellular_resources: Optional[List[str]]
    :param intracellular_datasets: Broad database datasets selection for OmniPath signaling, defaults to None.
    :type intracellular_datasets: Optional[List[str]]
    :return: Dimensionally aligned and network-annotated MuData container.
    :rtype: mu.MuData
    :raises KeyError: If mandatory validation boundaries or configuration parameters are violated.
    """
    # Pipeline initialization and structural remapping phase
    logger.info("Starting multi-modal processing pipeline orchestration.")
    
    ## Resolve custom input name mappings to enforce strict global schema consistency
    if key_mappings:
        for custom_key, canonical_key in key_mappings.items():
            if custom_key in mdata.mod and custom_key != canonical_key:
                ### Transfer ownership of the modality object to the canonical schema name slot
                mdata.mod[canonical_key] = mdata.mod.pop(custom_key)
                logger.debug("Remapped custom modality alias: %s to canonical schema key: %s", custom_key, canonical_key)

    # Modality list resolution step
    ## If explicit modalities list is omitted, derive targets from the container keys
    if not modalities:
        modalities = list(mdata.mod.keys())
        logger.debug("Derived active modalities list from container keys: %s", modalities)

    # TODO - does not work properly 
    # # Data integrity validation phase
    # ## Execute stateless checking functions to verify expected column slots and metadata arrays
    # ### Pass active modalities to prevent rigid schema checks on excluded data layers
    # validation_errors = verify_structural_presence(mdata, OMNI_PHYSIBOSS_SCHEMA, key_mappings or {}, modalities)
    # if validation_errors:
    #     error_message = "\n".join(validation_errors)
    #     raise KeyError(f"Container failed structural schema validation: {error_message}")
    
    # Mathematical join alignment phase
    ## Execute the inner join operation to synchronize cellular observation tracking indexes
    logger.info("Initiating multimodal data intersection alignment across omics layers.")
    synchronized_mdata = unify_multimodal_data(
        mdata=mdata,
        modalities=modalities,
        main_modality=main_modality
    )

    # Execute spatial neighborhood cross-correlation metrics via LIANA+ pipeline
    ## Compute localized intercellular communication weights and assign results
    resource_name = 'mouseconsensus' if specie == 'mouse' else 'consensus'
    logger.info("Executing spatial neighborhood cross-correlation metrics using resource: %s", resource_name)
    synchronized_mdata = run_liana_multimodal_pipeline(
        mdata=synchronized_mdata,
        x_mod=main_modality,
        y_mod=main_modality,
        output_modality_key=main_modality,
        liana_key=liana_uns_key,
    )
    
    # Intracellular reference acquisition phase
    ## Fetch and annotate signed directed intracellular signaling graphs from OmniPath clients using dynamic variables
    logger.info("Fetching directed intracellular signaling graphs from OmniPath.")
    synchronized_mdata = fetch_intracellular_pathway_network(
        mdata=synchronized_mdata,
        output_key=intracellular_output_key,
        resources=intracellular_resources,
        datasets=intracellular_datasets
    )

    # Intercellular metadata compilation phase
    ## Merge spatial information with external communication receptor-ligand annotations
    logger.info("Compiling intercellular metadata with OmniPath intercell annotations.")
    synchronized_mdata = fetch_liana_interactions(
        mdata=synchronized_mdata,
        liana_uns_key=liana_uns_key,
        output_uns_key=intercell_output_key
    )

    # Global synchronization execution
    ## Refresh internal structural coordinates across all child modalities
    logger.info("Refreshing internal structural coordinates globally.")
    safe_synchronize_mudata_layers(synchronized_mdata, pull_obs=True, pull_var=False, inplace=True)
    logger.info("Multi-modal processing pipeline completed successfully.")

    return synchronized_mdata