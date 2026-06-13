import mudata as mu
from typing import List, Dict, Set, Any
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

def validate_separated_modalities_overlap(
    mdata: mu.MuData, 
    modalities: List[str]
) -> Dict[str, Any]:
    """
    Diagnoses intersection failures across multiple modalities by computing 
    pairwise cardinalities and leave-one-out isolation metrics.

    :param mdata: The unaligned input multimodal container.
    :type mdata: mu.MuData
    :param modalities: List of modality keys to evaluate.
    :type modalities: list of str
    :return: A dictionary containing diagnostic metrics, problematic layers, and overlap matrix data.
    :rtype: dict
    """
    # Diagnostic initialization
    logger.info("Starting intersection failure diagnosis for modalities.")
    ## Validate execution boundary conditions
    if len(modalities) < 2:
        raise ValueError("Diagnostics require at least 2 modalities to compute intersection shifts.")

    ## Initialize results registries and extract cell sets
    report = {
        "independent_sizes": {},
        "pairwise_overlaps": {},
        "leave_one_out_sizes": {},
        "completely_isolated_modalities": []
    }
    mod_sets: Dict[str, Set[str]] = {}

    # Extraction loop
    for mod in modalities:
        ## Extract raw cell barcode name sets from independent layers
        if mod in mdata.mod:
            mod_sets[mod] = set(mdata[mod].obs_names)
            report["independent_sizes"][mod] = len(mod_sets[mod])
            logger.debug("Extracted cell set for modality: %s with size: %s", mod, len(mod_sets[mod]))
        else:
            raise KeyError(f"Modality '{mod}' missing from input MuData container.")

    # Pairwise evaluation matrix loop
    for i, mod_a in enumerate(modalities):
        for mod_b in modalities[i+1:]:
            ## Compute strict intersection cardinality between pairs
            overlap_set = mod_sets[mod_a].intersection(mod_sets[mod_b])
            pair_key = f"{mod_a}<->{mod_b}"
            report["pairwise_overlaps"][pair_key] = len(overlap_set)
            logger.debug("Computed pairwise overlap for %s: %s cells", pair_key, len(overlap_set))
            
            ### Detect absolute decoupling between two layers
            if len(overlap_set) == 0:
                logger.error("Critical Decoupling: Pairs %s and %s share 0 overlapping cells.", mod_a, mod_b)
                # print(f"[!] Critical Decoupling: Pairs '{mod_a}' and '{mod_b}' share 0 overlapping cells.")

    # Higher-order structural leave-one-out isolation audit
    for target_mod in modalities:
        ## Accumulate cell arrays excluding the active target layer
        other_mods = [m for m in modalities if m != target_mod]
        partial_intersection = mod_sets[other_mods[0]]
        
        for next_mod in other_mods[1:]:
            partial_intersection = partial_intersection.intersection(mod_sets[next_mod])
            
        report["leave_one_out_sizes"][f"excluding_{target_mod}"] = len(partial_intersection)
        
        ## Check if removing this target layer converts a zero intersection into a valid subset
        global_intersection = partial_intersection.intersection(mod_sets[target_mod])
        if len(global_intersection) == 0 and len(partial_intersection) > 0:
            ### The target layer is identified as the singular bottleneck driving global overlap to zero
            report["completely_isolated_modalities"].append(target_mod)
            logger.error("Intersection Bottleneck: Modality %s isolates the global union framework.", target_mod)
            # print(f"[!] Intersection Bottleneck: Modality '{target_mod}' isolates the global union framework.")

    logger.info("Intersection failure diagnosis processing complete.")
    return report