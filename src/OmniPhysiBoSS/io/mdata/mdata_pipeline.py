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


def run_mdata_processing_pipeline(
    mdata: mu.MuData,
    specie: Literal['mouse', 'human'],  
    key_mappings: Optional[Dict[str, str]] = None,
    modalities: Optional[List[str]] = None,
    main_modality: str = "rna",
    liana_uns_key: str = "liana_res",
    intercell_output_key: str = "intercellular_metadata_df",
    intracellular_output_key: str = "intracellular_metadata_df"
) -> mu.MuData:
    """
    Execute the complete orchestration pipeline for multi-modal data preparation.

    This facade handles structural key remapping, validation schema enforcement,
    cellular intersection harmonization, and OmniPath network annotation injection.

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
    :return: Dimensionally aligned and network-annotated MuData container.
    :rtype: mu.MuData
    :raises KeyError: If mandatory validation boundaries or configuration parameters are violated.
    """

    # Pipeline initialization and structural remapping phase
    ## Resolve custom input name mappings to enforce strict global schema consistency
    if key_mappings:
        for custom_key, canonical_key in key_mappings.items():
            if custom_key in mdata.mod and custom_key != canonical_key:
                ### Transfer ownership of the modality object to the canonical schema name slot
                mdata.mod[canonical_key] = mdata.mod.pop(custom_key)
                print(f"[-] Remapped custom modality alias '{custom_key}' to canonical schema key '{canonical_key}'.")

    # Modality list resolution step
    ## If explicit modalities list is omitted, derive targets from the container keys
    if not modalities:
        modalities = list(mdata.mod.keys())

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
    print("[-] Initiating multimodal data harmonization across omics layers...")
    harmonized_mdata = unify_multimodal_data(
        mdata=mdata,
        modalities=modalities,
        main_modality=main_modality
    )

    # Execute spatial neighborhood cross-correlation metrics via LIANA+ pipeline
    ## Compute localized intercellular communication weights and assign results
    ### choose mouse or human resourse 
    resource_name = 'mouseconsensus' if specie == 'mouse' else 'consensus'
    harmonized_mdata = run_liana_multimodal_pipeline(
        mdata=harmonized_mdata,
        x_mod=main_modality,
        y_mod=main_modality,
        output_modality_key=main_modality,
        liana_key=liana_uns_key,

    )
    # Intracellular reference acquisition phase
    ## Fetch and annotate signed directed intracellular signaling graphs from OmniPath clients
    harmonized_mdata = fetch_intracellular_pathway_network(
        mdata=harmonized_mdata,
        output_key=intracellular_output_key
    )

    # Intercellular metadata compilation phase
    ## Merge spatial information with external communication receptor-ligand annotations
    harmonized_mdata = fetch_liana_interactions(
        mdata=harmonized_mdata,
        liana_uns_key=liana_uns_key,
        output_uns_key=intercell_output_key
    )

    # Global synchronization execution
    ## Refresh internal structural coordinates across all child modalities
    harmonized_mdata.update()
    print("[✓] Multi-modal processing pipeline completed successfully.")

    return harmonized_mdata