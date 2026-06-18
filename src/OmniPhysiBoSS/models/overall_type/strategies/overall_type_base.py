# Heading 1 (Broad context / Top-level block / Script section)
# Abstract base interface structure for overall simulation time and space scaling configurations.

from abc import ABC, abstractmethod
from typing import Dict, Any
import mudata as mu

from ....utils.logger import get_custom_logger
from ....configurate.bindings import OverallType

# Instantiation Protocol
logger = get_custom_logger(__name__)

class BaseOverallExtractor(ABC):
    """
    Abstract base class defining the execution interface for simulation timeline
    and scaling extraction strategies within the OmniPhysiBoSS framework.
    """

    @abstractmethod
    def extract_overall(self, mdata: mu.MuData, config: Dict[str, Any]) -> OverallType:
        """
        Extract timeline configurations and construct a validated OverallType object
        from multi-modal omics datasets and runtime parameters.

        :param mdata: Integrated multi-modal omics storage asset containing biological profiles.
        :type mdata: mu.MuData
        :param config: Dictionary containing explicit time scales and custom step overrides.
        :type config: Dict[str, Any]
        :return: A fully populated and validated OverallType binding instance.
        :rtype: OverallType
        """
        pass