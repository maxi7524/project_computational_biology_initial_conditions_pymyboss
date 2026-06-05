import subprocess
import sys
from pathlib import Path

import subprocess
import sys
import os
from pathlib import Path

# ----------------------------------
# Main 
# ----------------------------------

## Functional interface to execute and stream telemetry data to files and stdout
def run_physiboss_simulation(
    xml_path: Path,
    logs_output: Path = None,
    physiboss_root: Path = Path(__file__).resolve().parent.parent.parent.parent / 'external/PhysiBoSS',
    executable_name: str = "PhysiBoSS_Cell_Lines"
) -> None:
    """
    Run a multi-scale simulation and dumps captured operational log streams into a target file.

    :param xml_path: Path to the source user XML configuration file.
    :type xml_path: Path
    :param physiboss_root: Path to the root directory of the PhysiBoSS engine.
    :type physiboss_root: Path
    :param logs_output: Path where the generated operational log file should be stored.
    :type logs_output: Path
    :param executable_name: Name of the compiled C++ binary executable file, defaults to "PhysiBoSS_Cell_Lines".
    :type executable_name: str
    :raises FileNotFoundError: If the compiled binary executable cannot be located.
    :raises RuntimeError: If compilation fails or the simulation terminates with an error code.
    """
    # Environment initialization and path deduction
    ## Isolate project workspace token from the XML configuration filename stem
    xml_path = Path(xml_path)
    physiboss_root = Path(physiboss_root)
    if logs_output is None:
        logs_output = Path(__file__).resolve().parent.parent.parent.parent / 'logs/physiboss_simulation' / xml_path.stem
    else:
        logs_output = Path(logs_output)
    project_name = xml_path.stem
    
    ## Define isolated runtime configuration boundaries matching the project hierarchy
    #TODO - CONFIG PARAMETER - physiboss project folder
    project_work_dir = physiboss_root / "OmniPhysiBoSS_projects" / project_name
    staged_xml_path = project_work_dir / xml_path.name
    executable_path = physiboss_root / executable_name

    # Engine compilation phase invocation
    ## Delegate building process to the local compiler utility function
    _compile_physiboss_engine(physiboss_root)

    # Executable structural confirmation
    ## Ensure the compiled target path references an active file layout boundary
    if not executable_path.exists() or executable_path.is_dir():
        ### Terminate processing context to avoid directory invocation faults
        raise FileNotFoundError(
            f"Target executable file not found or is a directory at: {executable_path}. "
            f"Verify that the executable_name parameter matches your Makefile binary target target."
        )

    # Logging infrastructure initialization
    ## Ensure target output log directories are fully allocated on the hardware
    os.makedirs(logs_output.parent, exist_ok=True)

    # Simulation pipeline execution loop
    print(f"[STEP 3/3] Launching multi-scale simulation container for project: {project_name}")
    print("----------------------------------------------------------------------")
    
    ## Build execution command payload array referencing the isolated directory configuration
    command_payload = [str(executable_path), str(staged_xml_path)]

    ## Stream low-level stdout descriptors and write to disk simultaneously
    with open(logs_output, "w", encoding="utf-8") as log_file:
        with subprocess.Popen(
            command_payload,
            cwd=physiboss_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        ) as process:
            
            ### Read real-time diagnostic output streams from the running binary
            for log_line in process.stdout:
                cleaned_line = log_line.strip()
                
                ### Write all raw standard output lines into the persistent log storage file
                log_file.write(log_line)
                log_file.flush()
                
                ### Filter and expose telemetry tracking patterns to the active terminal stdout
                if "Currenttime" in cleaned_line or "agents" in cleaned_line or "Simulation" in cleaned_line:
                    print(f"[RUNTIME TELEMETRY] {cleaned_line}")
                    sys.stdout.flush()
                elif "Error" in cleaned_line or "Exception" in cleaned_line:
                    #### Catch core operational exception crashes immediately
                    print(f"[CRITICAL ENGINE FAULT] {cleaned_line}", file=sys.stderr)

            ### Synchronize process termination statuses
            exit_code = process.wait()
            
            if exit_code != 0:
                ### Break loop on engine failure crash signals
                raise RuntimeError(f"Simulation execution failed with exit code: {exit_code}")

    print("----------------------------------------------------------------------")
    print(f"[PROCESS COMPLETED] Simulation logs written to: {logs_output}")

# ----------------------------------
# Helpers 
# ----------------------------------

# Execution and runtime logging layer
## Helper function to isolate C++ project compilation steps
def _compile_physiboss_engine(physiboss_root: Path) -> None:
    """
    Executes the clean and build automation sequence via the project Makefile.

    :param physiboss_root: Path to the root directory of the PhysiBoSS engine.
    :type physiboss_root: Path
    :raises RuntimeError: If any step of the C++ compilation pipeline fails.
    """
    print(f"[STEP 2/3] Compiling PhysiBoSS C++ engine in: {physiboss_root}")
    try:
        # Clear historic object frameworks to prevent linker caching issues
        ## Execute clean build target sequence
        subprocess.run(["make", "clean"], cwd=physiboss_root, check=True, capture_output=True)
        
        # Build optimized multi-scale binary execution package
        ## Execute global build target
        subprocess.run(["make"], cwd=physiboss_root, check=True, capture_output=True)
        print(" -> C++ Engine compilation completed successfully.")
    except subprocess.CalledProcessError as compile_err:
        ### Intercept, decode, and forward low-level compilation error diagnostics
        raise RuntimeError(f"C++ Compilation failed: {compile_err.stderr.decode('utf-8')}")