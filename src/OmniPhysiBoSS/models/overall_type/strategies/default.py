# Heading 1 (Broad context / Top-level block / Script section)
# Default strategy implementation for overall simulation timeline setup.

from typing import Dict, Any
import mudata as mu

from ....utils.logger import get_custom_logger
from ....configurate.bindings import OverallType, ValueWithUnits
from .overall_type_base import BaseOverallExtractor

# Instantiation Protocol
logger = get_custom_logger(__name__)

class DefaultOverallExtractor(BaseOverallExtractor):
    """
    Concrete implementation of BaseOverallExtractor providing default 
    PhysiCell timeline parameters and scaling constants.
    """

    def extract_overall(self, mdata: mu.MuData, config: Dict[str, Any] = {}) -> OverallType:
        """
        Extract simulation duration and time-step intervals from configuration profiles.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param config: Dictionary containing pipeline time parameters and scale overrides.
        :type config: Dict[str, Any]
        :return: A fully populated OverallType configuration block.
        :rtype: OverallType
        """
        # Heading 1 (Overall configurations collection pipeline)
        logger.info("Executing default overall simulation time parameters extraction.")

        try:
            ## Fetch values or fall back to default standardized PhysiCell constants
            time_units = str(config.get("time_units", "min"))
            space_units = str(config.get("space_units", "micron"))
            
            max_time_val = float(config.get("max_time", 1440.0))
            dt_diffusion_val = float(config.get("dt_diffusion", 0.01))
            dt_mechanics_val = float(config.get("dt_mechanics", 0.1))
            dt_phenotype_val = float(config.get("dt_phenotype", 6.0))

            ### Contextual Transparency: Log extracted mathematical milestones before binding
            logger.debug("Timeline parameters resolved - Max Time: %s, dt_diffusion: %s, dt_mechanics: %s, dt_phenotype: %s",
                         max_time_val, dt_diffusion_val, dt_mechanics_val, dt_phenotype_val)

            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Instantiate ValueWithUnits objects for each architectural metric
            max_time_obj = ValueWithUnits(value=max_time_val, units=time_units)
            dt_diffusion_obj = ValueWithUnits(value=dt_diffusion_val, units=time_units)
            dt_mechanics_obj = ValueWithUnits(value=dt_mechanics_val, units=time_units)
            dt_phenotype_obj = ValueWithUnits(value=dt_phenotype_val, units=time_units)

            ## Construct the final structured automated xsdata binding instance
            overall_instance = OverallType(
                max_time=max_time_obj,
                time_units=time_units,
                space_units=space_units,
                dt_diffusion=dt_diffusion_obj,
                dt_mechanics=dt_mechanics_obj,
                dt_phenotype=dt_phenotype_obj
            )

            logger.info("OverallType data block successfully synthesized.")
            return overall_instance

        except Exception as e:
            ### Capture error stack traces inside computational orchestration exceptions
            logger.error("Critical failure during overall timeline initialization: %s", e, exc_info=True)
            raise