# =============================================================================
# Global Truth Validator and Preprocessing Orchestration Decorator
# =============================================================================

from functools import wraps
from typing import Any, Callable, Dict, List

# Relative module references compilation
## Import sister structures using explicit pythonic dot notations
from ._utils.validate.mdata_types import OMNI_PHYSIBOSS_SCHEMA
from ._utils.validate.mdata_validator import (
    validate_container_mapping,
    check_array_integrity
)
from ._utils.preprocessing.preprocessing import (
    preprocess_spatial_data,
    preprocess_decouple_networks,
    preprocess_liana_signaling
)


def enforce_mdata_validation(target_function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator tracking multi-modal integrity and executing isolated preprocessing blocks.

    :param target_function: The pipeline or model function being guarded.
    :type target_function: Callable[..., Any]
    :return: Wrapped execution gate function.
    :rtype: Callable[..., Any]
    :raises TypeError: If data structures violate formatting rules or type mutations occur.
    :raises ValueError: If base structural coordinate components fail mapping discovery.
    """
    @wraps(target_function)
    def execution_gate(*args: Any, **kwargs: Any) -> Any:
        # Context discovery and structural extraction
        ## Extract main objects from parameters without configuring any defaults
        mdata = args[0] if args else kwargs.get("data_container")
        key_mappings = kwargs.get("key_mappings")
        species = kwargs.get("species")

        if mdata is None:
            return target_function(*args, **kwargs)

        # Isolated validation pass: Core raw structures verification
        ## Verify raw baseline matrix parameters exist before tackling downstream calculations
        raw_errors = validate_container_mapping(mdata, key_mappings)
        critical_raw_faults = [err for err in raw_errors if "layer" in err and ("obs" in err or "spatial" in err)]

        if critical_raw_faults:
            ### Terminate immediately if core coordinate axes are missing from execution domains
            fault_summary = " | ".join(critical_raw_faults)
            raise ValueError(f"Core physical tissue layers missing. Mapping failed: {fault_summary}")

        # Targeted preprocessing evaluations loop
        ## Evaluate structural discrepancies to invoke custom processing subroutines
        pre_errors = validate_container_mapping(mdata, key_mappings) + check_array_integrity(mdata, key_mappings)

        if pre_errors:
            ### Evaluate isolated subroutines step-by-step based on logged missing parameters
            if any("spatial" in err for err in pre_errors):
                preprocess_spatial_data(mdata, key_mappings)

            if any("decoupleR" in err for err in pre_errors):
                if species is None:
                    raise TypeError("decoupleR layer missing: Pass 'species' parameter to auto-trigger network calculations.")
                preprocess_decouple_networks(mdata, species, key_mappings)

            if any("liana_res" in err for err in pre_errors):
                if species is None:
                    raise TypeError("Liana+ layer missing: Pass 'species' parameter to auto-trigger pairing calculations.")
                preprocess_liana_signaling(mdata, species, key_mappings)

            # Final validation re-check pass
            ## Verify all components align perfectly after preprocessing runs complete
            post_prep_errors = validate_container_mapping(mdata, key_mappings) + check_array_integrity(mdata, key_mappings)
            if post_prep_errors:
                fault_summary = " | ".join(post_prep_errors)
                raise TypeError(f"Validation constraints breached after automated subroutines run: {fault_summary}")

        # Capture pre-execution data type state signatures
        ## Track object class namespaces to monitor destructive mutations during runtime execution
        reverse_lookup = {v: k for k, v in key_mappings.items()}
        type_signatures: Dict[str, str] = {}
        for layer in OMNI_PHYSIBOSS_SCHEMA.keys():
            active_key = reverse_lookup.get(layer, layer)
            layer_obj = getattr(mdata, active_key, None) or mdata.get(active_key)
            if layer_obj is not None:
                type_signatures[active_key] = type(layer_obj).__name__

        # Primary workflow execution
        ## Run the wrapped pipeline calculation block
        function_payload = target_function(*args, **kwargs)

        # Post-execution structural mutation validation pass
        ## Check tracking layers to block unintended type switches inside code operations
        for active_key, expected_type_name in type_signatures.items():
            current_obj = getattr(mdata, active_key, None) or mdata.get(active_key)
            current_type_name = type(current_obj).__name__ if current_obj is not None else "NoneType"
            
            if current_type_name != expected_type_name:
                raise TypeError(
                    f"Destructive structural mutation caught: Layer '{active_key}' altered type "
                    f"from '{expected_type_name}' to '{current_type_name}' inside function execution bounds."
                )

        return function_payload

    return execution_gate