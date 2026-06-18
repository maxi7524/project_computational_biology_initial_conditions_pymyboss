# Heading 1 (Broad context / Top-level block / Script section)
# Default strategy for spatial domain extraction from Visium data.

import numpy as np
from typing import Dict, Any
import mudata as mu

from ....utils.logger import get_custom_logger
from ....configurate.bindings import DomainType
from .domain_type_base import BaseDomainExtractor

# Instantiation Protocol
logger = get_custom_logger(__name__)

class DefaultDomainExtractor(BaseDomainExtractor):
    """
    Concrete implementation of BaseDomainExtractor that calculates physical domain
    boundaries from Visium spatial pixel coordinates using spot diameter ratios.
    """

    def extract_domain(self, mdata: mu.MuData, config: Dict[str, Any] = {}) -> DomainType:
        """
        Extract spatial coordinates, scale them to micrometers using full resolution
        spot dimensions, and construct the DomainType configuration block.

        :param mdata: Integrated multi-modal omics storage asset containing spatial layers.
        :type mdata: mu.MuData
        :param config: Dictionary containing resolution steps and padding configurations.
        :type config: Dict[str, Any]
        :return: A fully constructed and scaled DomainType instance.
        :rtype: DomainType
        """
        # Heading 1 (Domain extraction pipeline orchestration)
        logger.info("Starting default spatial domain extraction workflow.")

        try:
            ## Fetch configuration hyperparameters from execution context
            dx = float(config.get("dx", 20.0))
            dy = float(config.get("dy", 20.0))
            dz = float(config.get("dz", 20.0))
            ### Parameters responsible for additional frame for avoiding collisions, i added it so 
            padding = float(config.get("padding", 55.0))
            
            ## Access primary RNA modality layer
            rna_mod = mdata.mod["rna"]
            spatial_dict = rna_mod.uns["spatial"]
            sample_keys = list(spatial_dict.keys())

            if not sample_keys:
                ### Handle empty spatial registries in modality structures
                logger.error("The spatial metadata dictionary inside rna.uns is empty.")
                raise KeyError("Missing spatial dictionary keys in MuData object.")

            ## Unpack dynamic key to calculate pixel conversion scale
            sample_key = sample_keys[0]
            scalefactors = spatial_dict[sample_key]["scalefactors"]
            spot_diameter_fullres = float(scalefactors["spot_diameter_fullres"])
            
            ## Compute micrometer per pixel conversion ratio (Visium spot diameter = 55.0 um)
            microns_per_pixel = 55.0 / spot_diameter_fullres
            logger.debug("Extracted sample: %s | Conversion scale: %s um/px", sample_key, microns_per_pixel)

            ## Extract raw pixel positions from observation matrices
            spatial_coords = rna_mod.obsm["spatial"]
            x_px = spatial_coords[:, 0]
            y_px = spatial_coords[:, 1]

            ## Map pixel coordinate boundaries to micron physical space
            x_min_scaled = float(np.min(x_px) * microns_per_pixel)
            x_max_scaled = float(np.max(x_px) * microns_per_pixel)
            y_min_scaled = float(np.min(y_px) * microns_per_pixel)
            y_max_scaled = float(np.max(y_px) * microns_per_pixel)

            ## Apply boundary padding transformations
            x_min = x_min_scaled - padding
            x_max = x_max_scaled + padding
            y_min = y_min_scaled - padding
            y_max = y_max_scaled + padding
            z_min = -(dz / 2.0)
            z_max = dz / 2.0

            ### Contextual Transparency: Persist calculations inside the multi-modal container
            metadata_payload = {
                "microns_per_pixel": microns_per_pixel,
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
            }
            rna_mod.uns["domain_type_metadata_dict"] = metadata_payload
            logger.info("Persisted domain spatial metadata dictionary into rna.uns.")

            ## Construct automated binding instance
            domain_instance = DomainType(
                x_min=float(x_min),
                x_max=float(x_max),
                y_min=float(y_min),
                y_max=float(y_max),
                z_min=float(z_min),
                z_max=float(z_max),
                dx=float(dx),
                dy=float(dy),
                dz=float(dz),
                use_2_d=True,
            )
            return domain_instance

        except Exception as e:
            ### Capture mathematical and key extraction anomalies
            logger.error("Critical failure during spatial domain mapping: %s", e, exc_info=True)
            raise