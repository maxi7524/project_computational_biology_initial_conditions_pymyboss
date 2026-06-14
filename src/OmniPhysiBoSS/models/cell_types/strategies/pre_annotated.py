# Heading 1 (Broad context / Top-level block / Script section)
# Categorical pre-annotated identification parsing engine.

from typing import Dict, Any, List
import mudata as mu

from .cell_types_base import BaseCellTypeExtractor
from ....utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

class PreAnnotatedExtractor(BaseCellTypeExtractor):
    """
    Extracts cell lineage cohorts using pre-existing categorical observation arrays.
    """

    def extract_cell_types(self, mdata: mu.MuData, target_annotation_key: str) -> Dict[str, Any]:
        """
        Execute explicit dictionary mapping over target categorical columns.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param target_annotation_key: Metadata annotation column label string.
        :type target_annotation_key: str
        :return: Compiled cell mapping registries grouped by lineage identity.
        :rtype: Dict[str, Any]
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Validation checks of modal arrays
        logger.info("Initializing pre-annotated classification lookup pipeline.")
        
        if 'rna' not in mdata.mod:
            logger.error("Mandatory rna modality missing from execution space.", exc_info=True)
            raise KeyError("Missing 'rna' modality.")
            
        obs_df = mdata.mod['rna'].obs
        if target_annotation_key not in obs_df.columns:
            logger.error("Target metadata layer column label %s missing.", target_annotation_key, exc_info=True)
            raise KeyError(f"Column {target_annotation_key} missing.")

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Grouping matrix index elements by unique categorical assignments
        unique_labels = obs_df[target_annotation_key].dropna().unique()
        lineage_registry = {}

        for label in unique_labels:
            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Slicing cell trackers matching target category label
            cell_indices = obs_df.index[obs_df[target_annotation_key] == label].tolist()
            cell_count = len(cell_indices)
            logger.debug("Group %s isolated containing %d individual cell units.", str(label), cell_count)

            if cell_count == 0:
                ### Handle zero-allocation anomalies gracefully
                logger.debug("Skipping entry processing loop for blank partition: %s", str(label))
                continue

            lineage_registry[str(label)] = {
                "cell_indices": cell_indices,
                "cell_count": cell_count,
                "database_reference": {
                    "source": "PreAnnotatedMetadata",
                    "identifier": str(label),
                    "status": "aligned"
                }
            }

        logger.info("Categorical parameter categorization finished processing safely.")
        return lineage_registry