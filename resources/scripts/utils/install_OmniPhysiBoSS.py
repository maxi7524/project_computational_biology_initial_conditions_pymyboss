# Heading 1 (Broad context / Top-level block / Script section)
# Deployment script utilizing user-managed custom fork configurations for PhysiCell.

import sys
import subprocess
from pathlib import Path

from OmniPhysiBoSS.utils.logger import get_custom_logger

# Instantiation Protocol: Centralized module logger setup
logger = get_custom_logger(__name__)

# Remote configuration targeting the user's explicit fork architecture
PHYSICELL_REMOTE_URL = "https://github.com/maxi7524/PhysiCell"


# Main setup choreography interface
def initialize_development_workspace(root_dir: Path) -> None:
    """
    Coordinates multi-scale engine workspace provisioning using fork-based alignment.

    :param root_dir: Full filesystem path to the root directory of the parent project repository.
    :type root_dir: Path
    """
    logger.info("Starting multi-scale toolchain workspace initialization via user fork setup.")
    external_dir = root_dir / "external" / "PhysiCell"

    ## Execute step 1: Validate local repository initialization context
    logger.info("Executing step 1: Git layout validation checks.")
    _verify_git_repository_context(root_dir)

    ## Execute step 2: Submodule allocation and location tracking
    logger.info("Executing step 2: Handle external engine directory allocation.")
    _deploy_submodule_structure(root_dir, external_dir)

    ## Execute step 3: Local environment linking via pip package parameters
    logger.info("Executing step 3: Run local editable developer package updates.")
    _install_editable_package(root_dir)

    logger.info("Workspace initialization completed successfully. Fork workspace is active.")


# ----------------------------------
# Internal Pipeline Sub-routines
# ----------------------------------


def _verify_git_repository_context(root_dir: Path) -> None:
    """
    Ensures that target directories maintain valid git configurations.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    :raises RuntimeError: If git parameters cannot be matched.
    """
    if not (root_dir / ".git").exists() and not (root_dir / "pyproject.toml").exists():
        error_msg = (
            f"Workspace validation error: '{root_dir}' is not recognized as the OmniPhysiBoSS root directory. "
            f"Ensure pyproject.toml or a valid .git structure is present at this path."
        )
        raise RuntimeError(error_msg)


def _deploy_submodule_structure(root_dir: Path, external_dir: Path) -> None:
    """
    Ensures the C++ simulation codebase is mapped inside the local build directory.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    :param external_dir: Target destination path for the C++ code dependency repository.
    :type external_dir: Path
    """
    # Evaluate configuration states and determine if reuse is applicable
    if not external_dir.exists() or not list(external_dir.iterdir()):
        ## Initialize configuration adjustments via active terminal calls
        logger.debug("Target directory empty. Mapping repository tracking dependencies to: %s", external_dir.name)
        try:
            ### Bind subfolder configuration parameters smoothly using system pipelines
            subprocess.run(
                ["git", "submodule", "add", "-f", PHYSICELL_REMOTE_URL, "external/PhysiCell"],
                cwd=root_dir,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            ### Handle pre-existing tracking matrix parameters or manual moves
            logger.error("Direct submodule addition failed. Executing local tracking fallback sequence.", exc_info=True)
            subprocess.run(["git", "submodule", "init"], cwd=root_dir, check=True)
            subprocess.run(["git", "submodule", "update"], cwd=root_dir, check=True)
    else:
        ## Skip downloading or cloning since files are already present in the target location
        logger.debug("Existing engine files detected at: %s. Reusing directory asset directly.", external_dir)


def _install_editable_package(root_dir: Path) -> None:
    """
    Installs the source code folder in editable python mode using local package configurations.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    """
    logger.debug("Registering package dependency links using developer configuration guidelines.")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=root_dir,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as err:
        logger.error("Editable installation process failed via pip execution.", exc_info=True)
        raise err


# Standard terminal interface gateway wrapper
if __name__ == "__main__":
    # Resolve project workspace root using four-level parent directory inversion:
    # utils (1) -> scripts (2) -> resources (3) -> repo_root (4)
    project_root = Path(__file__).resolve().parent.parent.parent.parent

    try:
        initialize_development_workspace(project_root)
    except Exception as runtime_fault:
        logger.error("Critical initialization failure encountered during script runtime setup.", exc_info=True)
        sys.exit(1)