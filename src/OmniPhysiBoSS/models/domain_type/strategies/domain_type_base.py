# Heading 1 (Broad context / Top-level block / Script section)
# Abstract base interface structure for spatial configuration routing.

from abc import ABC, abstractmethod
from typing import Dict, Any
import mudata as mu

from ....utils.logger import get_custom_logger
from ....configurate.bindings import DomainType

# Instantiation Protocol
logger = get_custom_logger(__name__)

class BaseDomainExtractor(ABC):
    """
    Abstract base class defining the execution interface for spatial domain 
    extraction and calculation strategies within the OmniPhysiBoSS framework.
    """

    @abstractmethod
    def extract_domain(self, mdata: mu.MuData, config: Dict[str, Any]) -> DomainType:
        """
        Extract spatial limits and construct a validated DomainType object 
        from multi-modal omics storage and runtime configuration options.

        :param mdata: Integrated multi-modal omics storage asset containing spatial layers.
        :type mdata: mu.MuData
        :param config: Dictionary containing runtime hyperparameters and grid resolutions.
        :type config: Dict[str, Any]
        :return: A fully constructed and scaled DomainType instance.
        :rtype: DomainType
        """
        pass