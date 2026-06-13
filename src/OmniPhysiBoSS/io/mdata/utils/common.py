# =============================================================================
# MuData Backward and Forward Compatibility Layer
# =============================================================================

import mudata as mu
import warnings
from typing import Optional
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


def safe_synchronize_mudata_layers(
    mdata: mu.MuData,
    pull_obs: bool = True,
    pull_var: bool = False,
    inplace: bool = True
) -> Optional[mu.MuData]:
    """
    Idempotently synchronizes global MuData slots with underlying modalities,
    ensuring seamless cross-version compatibility and suppressing FutureWarnings.

    :param mdata: The multi-modal container tracking asset to synchronize.
    :type mdata: mu.MuData
    :param pull_obs: Flag to force inheritance of observation dataframes, defaults to True.
    :type pull_obs: bool
    :param pull_var: Flag to force inheritance of variable dataframes, defaults to False.
    :type pull_var: bool
    :param inplace: If True, modifies container asset directly and returns None, defaults to True.
    :type inplace: bool
    :return: The updated MuData container instance if inplace=False, else None.
    :rtype: Optional[mu.MuData]
    """
    logger.info("Initiating safe structural synchronization pipeline for MuData container.")
    
    # Inplace operation preprocessing branch
    if not inplace:
        logger.debug("Inplace flag disabled. Generating deep structural copy of MuData object.")
        mdata = mdata.copy()

    # Contextual warning suppression block
    ## Context manager isolates and catches internal mudata legacy update warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning, module="mudata")

        # Structural state synchronization phase
        ## Execute explicit forward-compatible data pulling if methods are exposed (MuData >= 0.4)
        if pull_obs:
            if hasattr(mdata, "pull_obs") and callable(getattr(mdata, "pull_obs")):
                logger.debug("Executing explicit forward-compatible pull_obs sequence.")
                mdata.pull_obs()
            else:
                logger.debug("Legacy MuData infrastructure detected; skipping explicit pull_obs invocation.")

        if pull_var:
            if hasattr(mdata, "pull_var") and callable(getattr(mdata, "pull_var")):
                logger.debug("Executing explicit forward-compatible pull_var sequence.")
                mdata.pull_var()
            else:
                logger.debug("Legacy MuData infrastructure detected; skipping explicit pull_var invocation.")

        # Global index coordination branch
        ## Enforce internal multi-scale alignment calculations natively across all versions
        logger.debug("Invoking global container update graph routing algorithm.")
        mdata.update()
    
    logger.info("MuData structural state synchronization completed successfully.")
    
    if inplace:
        return None
    return mdata