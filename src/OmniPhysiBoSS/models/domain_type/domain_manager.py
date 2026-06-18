# Heading 1 (Broad context / Top-level block / Script section)
# Orchestration manager for spatial domain configuration workflows.

from typing import Dict, Any, Type
import mudata as mu

from ...utils.logger import get_custom_logger
from ...configurate.bindings import DomainType
from .strategies.domain_type_base import BaseDomainExtractor

logger = get_custom_logger(__name__)

# Heading 1 (Broad context / Top-level block / Script section)
# Execution manager logic for dynamic domain strategy routing

def manage_domain_extraction(
    mdata: mu.MuData, 
    config: Dict[str, Any], 
    strategy_class: Type[BaseDomainExtractor]
) -> DomainType:
    """
    Orchestrate the parsing, instantiation, and calculation phases of 
    spatial domain boundaries based on a selected strategy.

    :param mdata: Integrated multi-modal omics storage asset.
    :type mdata: mu.MuData
    :param config: Global or subdomain profile options defining operational variables.
    :type config: Dict[str, Any]
    :param strategy_class: Concrete constructor implementation derived from the base interface.
    :type strategy_class: Type[BaseDomainExtractor]
    :return: Constructed DomainType configuration block.
    :rtype: DomainType
    """
    # Module initialization phase
    logger.info("Initializing spatial domain extraction manager.")
    
    ## Instantiate the requested functional implementation engine
    extractor_instance = strategy_class()
    logger.debug("Successfully instantiated domain extraction strategy of type: %s", strategy_class.__name__)

    try:
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Execute spatial domain computations using the configured strategy matrix
        compiled_domain = extractor_instance.extract_domain(mdata=mdata, config=config)
        logger.info("Spatial domain parameter generation finished successfully.")
        return compiled_domain

    except Exception as error:
        ### Handle structural tracking bugs and intercept compilation exceptions
        logger.error("Domain setup stage failed during coordinate mapping operation.", exc_info=True)
        raise error