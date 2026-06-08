# =============================================================================
# Functional Multi-Modal Structural Integrity Checking Layer
# =============================================================================

import mudata as mu
from typing import Dict, List, Any


def verify_structural_presence(
    mdata: mu.MuData, 
    schema: Dict[str, List[str]], 
    mappings: Dict[str, str],
    modalities: List[str]
) -> List[str]:
    """
    Verify the presence of required multimodal layers and metadata columns dynamically
    based on the active execution modalities specified for the current run.

    :param mdata: The main multimodal data container asset.
    :type mdata: mu.MuData
    :param schema: Hardcoded layout rules mapping main attributes to nested keys.
    :type schema: Dict[str, List[str]]
    :param mappings: User-defined variable name translation dictionary.
    :type mappings: Dict[str, str]
    :param modalities: List of active modality keys targeted for this execution run.
    :type modalities: List[str]
    :return: Collected strings detailing missing structural blocks.
    :rtype: List[str]
    """
    # Error aggregation initialization
    errors: List[str] = []

    # Modality registry presence validation loop
    ## Filter schema keys to validate only layers that are requested in active modalities
    for base_layer in schema.keys():
        if base_layer in ["obs", "uns"]:
            continue

        ## Resolve runtime structural names from the mapping definition
        mapped_layer = mappings.get(base_layer, base_layer)

        ## Only validate if this schema layer is part of the requested pipeline modalities
        if mapped_layer in modalities:
            if mapped_layer not in mdata.mod:
                ### Register failure if a requested modality is missing from the container
                errors.append(f"Mandatory multi-modal layer registry slot missing: '{mapped_layer}'")
                continue

            # Nested structural slot validation phase
            layer_object = mdata.mod[mapped_layer]
            for required_key in schema[base_layer]:
                mapped_key = mappings.get(required_key, required_key)
                
                if not hasattr(layer_object, mapped_key) and mapped_key not in getattr(layer_object, "keys", lambda: [])():
                    errors.append(f"Modality '{mapped_layer}' is missing target reference component slot: '{mapped_key}'")

    # Root observation columns validation branch
    if "obs" in schema:
        ## Scan global tracking observation dataframe and local modality dataframes for structural columns
        for col in schema["obs"]:
            ### Resolve missing global keys by checking fallback columns inside active child modalities
            in_global = col in mdata.obs.columns
            in_local = any(col in mdata.mod[m].obs.columns for m in modalities if m in mdata.mod)
            
            if not (in_global or in_local):
                errors.append(f"Mandatory global or local observation data column missing: '{col}'")

    return errors