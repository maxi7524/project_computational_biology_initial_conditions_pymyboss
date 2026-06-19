# Heading 1 (Broad context / Top-level block / Script section)
# Orchestration manager for cell lineage aggregation workflows.

from typing import Dict, Any, Type
import mudata as mu

from ...utils.logger import get_custom_logger
from .strategies.cell_types_base import BaseCellTypeExtractor

logger = get_custom_logger(__name__)

# Heading 1 (Broad context / Top-level block / Script section)
# Execution manager logic for dynamic strategy routing

def manage_cell_type_extraction(
    mdata: mu.MuData, 
    config: Dict[str, Any], 
    strategy_class: Type[BaseCellTypeExtractor]
) -> Dict[str, Any]:
    """
    Orchestrate the parsing, instantiation, and calculation phases of 
    cell lineage properties based on a selected strategy.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param config: Global or subdomain profile options defining operational variables.
    :type config: Dict[str, Any]
    :param strategy_class: Concrete constructor implementation derived from the base interface.
    :type strategy_class: Type[BaseCellTypeExtractor]
    :return: Compiled cell parameters compatible with structural configuration inputs.
    :rtype: Dict[str, Any]
    """
    # Module initialization phase
    logger.info("Initializing multi-cellular lineage extraction manager.")
    
    ## Instantiate the requested functional implementation engine
    extractor_instance = strategy_class()
    logger.debug("Successfully instantiated cell type extraction strategy of type: %s", strategy_class.__name__)

    try:
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Execute mathematical operations on cluster profiles
        compiled_results = extractor_instance.extract_cell_types(mdata=mdata, config=config)
        logger.info("Multi-cellular parameter compilation finished successfully.")
        return compiled_results

    except Exception as error:
        ### Handle structural tracking bugs and intercept compilation exceptions
        logger.error("Lineage aggregation stage failed during matrix operation.", exc_info=True)
        raise error