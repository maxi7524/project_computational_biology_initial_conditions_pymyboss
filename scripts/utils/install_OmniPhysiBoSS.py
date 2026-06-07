# scripts/install_OmniPhysiBoSS.py
import subprocess
import sys
from pathlib import Path
import os

# Static environment lockdown parameters
TARGET_COMMIT_HASH = "7180dffc72d3ce021b2eff385ff49735de5f02d8"
PHYSIBOSS_REMOTE_URL = "https://github.com/PhysiBoSS/PhysiBoSS"

# Main setup choreography interface
## Executing step-by-step repository configuration sequence
def initialize_development_workspace(root_dir: Path) -> None:
    """
    Coordinates sub-routines to provision directories, link code submodules, and lock versions.

    :param root_dir: Full filesystem path to the root directory of the parent project repository.
    :type root_dir: Path
    """
    print("[WORKSPACE INITIALIZATION] Starting multi-scale toolchain setup...")
    external_dir = root_dir / "external" / "PhysiBoSS" # Core directory definitions

    # Step 1: Initialize Git layout validation checks
    print('Step 1: Initialize Git layout validation checks')
    _verify_git_repository_context(root_dir)
    # Step 2: Handle external engine directory allocation
    print('Step 2: Handle external engine directory allocation')
    _deploy_submodule_structure(root_dir, external_dir)

    # Step 3: Run checkout lockdown updates
    print('Step 3: Run checkout lockdown updates')
    _lockdown_engine_version(external_dir, TARGET_COMMIT_HASH)

    # Step 4: Run local editable developer package updates
    print('Step 4: Run local editable developer package updates')
    _install_editable_package(root_dir)

    print("\n[WORKSPACE INITIALIZATION COMPLETED] Setup successful. All dependencies configured.")


# ----------------------------------
# Internal Pipeline Sub-routines
# ----------------------------------

# Local version validation routines
## Confirm local working root is a valid git partition
def _verify_git_repository_context(root_dir: Path) -> None:
    """
    Ensures that target directories maintain valid git configurations.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    :raises RuntimeError: If git parameters cannot be matched.
    """
    if not (root_dir / ".git").exists() and not (root_dir / "pyproject.toml").exists():
        raise RuntimeError(
            f"Workspace validation error: '{root_dir}' is not recognized as the OmniPhysiBoSS root directory. "
            f"Ensure pyproject.toml or a valid .git structure is present at this path."
        )


# Submodule directory management routines
## Inject or restore submodule settings inside external/ folder paths
def _deploy_submodule_structure(root_dir: Path, external_dir: Path) -> None:
    """
    Ensures the C++ simulation codebase is mapped inside the local build directory.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    :param external_dir: Target destination path for the C++ code dependency repository.
    :type external_dir: Path
    """
    # Evaluate configuration states
    if not external_dir.exists() or not list(external_dir.iterdir()):
        ## Initialize configuration adjustments via active terminal calls
        print(f" -> Mapping core repository tracking dependencies to: {external_dir.name}")
        try:
            ### Bind subfolder configuration parameters smoothly using system pipelines
            subprocess.run(
                ["git", "submodule", "add", "-f", PHYSIBOSS_REMOTE_URL, "external/PhysiBoSS"],
                cwd=root_dir,
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            ### Alternative strategy for pre-existing tracking matrix parameters
            print(" -> Submodule tracking files match. Forcing local initialization update profiles...")
            subprocess.run(["git", "submodule", "init"], cwd=root_dir, check=True)
            subprocess.run(["git", "submodule", "update"], cwd=root_dir, check=True)
    else:
        print(" -> Pre-existing repository structures verified inside the destination tracking layouts.")


# System software lockdown operations
## Move detached heads cleanly to fixed checked release milestones
def _lockdown_engine_version(external_dir: Path, commit_hash: str) -> None:
    """
    Pins the codebase configuration version using explicit git checkout targets.

    :param external_dir: Path pointing to the mapped source directory.
    :type external_dir: Path
    :param commit_hash: Strict targeted alpha-numeric checksum string identifier.
    :type commit_hash: str
    """
    print(f" -> Execution locking engine checkout reference to: {commit_hash}")
    
    # Execute detached state revisions
    ## Move working directory to targeted file parameters
    subprocess.run(["git", "fetch", "origin"], cwd=external_dir, check=True, capture_output=True)
    subprocess.run(["git", "checkout", commit_hash], cwd=external_dir, check=True, capture_output=True)


# Package linking steps
## Link internal package models using editable parameters
def _install_editable_package(root_dir: Path) -> None:
    """
    Installs the source code folder in editable python mode using local package configurations.

    :param root_dir: Path to the root directory of the parent package.
    :type root_dir: Path
    """
    print(" -> Registering package dependency links using developer configuration guidelines...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=root_dir,
        check=True,
        capture_output=True
    )


# Standard terminal interface gateway wrapper
if __name__ == "__main__":
    # Infer root directory paths safely relative to script locations
    # ../utils (1) -> ../scripts (2) -> ../repo_dir (3)
    project_root = Path(__file__).resolve().parent.parent.parent
    try:
        initialize_development_workspace(project_root)
    except Exception as runtime_fault:
        print(f"\n[CRITICAL INITIALIZATION ERROR] Setup process failed: {runtime_fault}", file=sys.stderr)
        sys.exit(1)