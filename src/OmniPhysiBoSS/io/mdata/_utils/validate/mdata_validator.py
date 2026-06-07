# Functional Multi-Modal Structural Integrity Checking Layer

from typing import Any, Dict, List


def verify_structural_presence(mdata: Any, schema: Dict[str, List[str]], mappings: Dict[str, str]) -> List[str]:
    """
    Verify the absolute presence of required multimodal layers and slots using a mapping table.

    :param mdata: The main multimodal data container.
    :type mdata: Any
    :param schema: Hardcoded layout rules mapping main attributes to nested keys.
    :type schema: Dict[str, List[str]]
    :param mappings: User-defined variable name translation dictionary.
    :type mappings: Dict[str, str]
    :return: Collected strings detailing missing structural blocks.
    :rtype: List[str]
    """
    # Error aggregation initialization
    errors = []

    for base_layer, required_keys in schema.items():
        ## Resolve runtime structural names from the mapping definition
        mapped_layer = mappings.get(base_layer, base_layer)

        ## Check high-level attribute existence within the data container
        if not hasattr(mdata, mapped_layer) and mapped_layer not in getattr(mdata, "keys", lambda: [])():
            errors.append(f"Mandatory data layer registry missing: '{mapped_layer}'")
            continue

        layer_object = getattr(mdata, mapped_layer, None) or mdata.get(mapped_layer)

        for key in required_keys:
            ### Resolve nested slot names using translation tables
            mapped_key = mappings.get(key, key)

            ### Validate presence inside dataframes, array keys, or columns matrix
            if not hasattr(layer_object, mapped_key) and mapped_key not in getattr(layer_object, "keys", lambda: [])():
                if hasattr(layer_object, "columns") and mapped_key in layer_object.columns:
                    #### Allow dataframe column matches to pass validation smoothly
                    continue
                errors.append(f"Layer '{mapped_layer}' is missing mandatory data entry slot: '{mapped_key}'")

    return errors


def verify_data_type_sanity(mdata: Any, schema: Dict[str, List[str]], mappings: Dict[str, str]) -> List[str]:
    """
    Examine data slots to ensure data types are sensible and uncorrupted.

    :param mdata: The main multimodal data container.
    :type mdata: Any
    :param schema: Hardcoded layout rules mapping main attributes to nested keys.
    :type schema: Dict[str, List[str]]
    :param mappings: User-defined variable name translation dictionary.
    :type mappings: Dict[str, str]
    :return: Strings detailing type incompatibility faults.
    :rtype: List[str]
    """
    # Type tracking initialization
    type_errors = []

    for base_layer in schema.keys():
        ## Resolve runtime names
        mapped_layer = mappings.get(base_layer, base_layer)
        layer_object = getattr(mdata, mapped_layer, None) or mdata.get(mapped_layer)

        if layer_object is None:
            continue

        ## Validate specific architectural types for critical processing paths
        if base_layer == "spatial" and not hasattr(layer_object, "shape"):
            ### Spatial coordinate blocks must support array structural properties
            type_errors.append(f"Spatial layer '{mapped_layer}' does not expose shape attributes (invalid array type).")

    return type_errors


def verify_spatial_rna_alignment(mdata: Any, mappings: Dict[str, str]) -> List[str]:
    """
    Check the structural alignment between the spatial coordinate matrix and the RNA matrix.

    Verifies that the spatial tracking coordinates tensor dimensions match the array size 
    of the single-cell expression matrix transcript profiles:
    $$\dim(\mathbf{X}_{\text{spatial}}) = \dim(\mathbf{X}_{\text{RNA}})_{rows}$$

    :param mdata: The main multimodal data container.
    :type mdata: Any
    :param mappings: User-defined variable name translation dictionary.
    :type mappings: Dict[str, str]
    :return: Array containing dimensional misalignment diagnostic strings.
    :rtype: List[str]
    """
    # Multi-scale boundary checks
    alignment_errors = []

    # Extract target structures via mappings
    ## Isolate spatial coordinates block from container parameters
    spatial_layer = mappings.get("spatial", "spatial")
    spatial_obj = getattr(mdata, spatial_layer, None) or mdata.get(spatial_layer)

    ## Isolate matching cell matrix metadata tracking framework
    obs_layer = mappings.get("obs", "obs")
    obs_obj = getattr(mdata, obs_layer, None) or mdata.get(obs_layer)

    if spatial_obj is not None and obs_obj is not None:
        ## Extract row count scalars using structural metadata interfaces
        spatial_rows = getattr(spatial_obj, "shape", [0])[0]
        obs_rows = getattr(obs_obj, "shape", [0])[0]

        if spatial_rows != obs_rows:
            ### Coordinate matrices must share identical observation boundaries to prevent parsing faults
            alignment_errors.append(
                f"Critical dimensional mismatch: Spatial layout specifies {spatial_rows} rows, "
                f"but expression index tracking contains {obs_rows} cells."
            )

    return alignment_errors


def capture_type_signature(mdata: Any, schema: Dict[str, List[str]], mappings: Dict[str, str]) -> Dict[str, str]:
    """
    Generate a lightweight snapshot mapping active keys to their string data type labels.

    :param mdata: The main multimodal data container.
    :type mdata: Any
    :param schema: Hardcoded layout rules mapping main attributes to nested keys.
    :type schema: Dict[str, List[str]]
    :param mappings: User-defined variable name translation dictionary.
    :type mappings: Dict[str, str]
    :return: A lookup table mapping resolved keys to internal type names.
    :rtype: Dict[str, str]
    """
    # Registry signature map assembly
    signature = {}

    for base_layer in schema.keys():
        ## Identify active keys matching execution bounds
        mapped_layer = mappings.get(base_layer, base_layer)
        layer_object = getattr(mdata, mapped_layer, None) or mdata.get(mapped_layer)

        if layer_object is not None:
            signature[mapped_layer] = type(layer_object).__name__

    return signature