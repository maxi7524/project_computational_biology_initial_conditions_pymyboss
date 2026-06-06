import pytest
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open
from OmniPhysiBoSS.wrappers.run_PhysiBoSS import run_physiboss_simulation, _compile_physiboss_engine
from OmniPhysiBoSS.wrappers._utils.log_monitor import PhysiBoSSLogMonitor

# Test suite for simulation runner and output telemetry streaming
## Test runtime compilation error handling routines
def test_compile_engine_failure():
    """
    Verifies that a compilation breakdown throws a RuntimeError containing stderr details.

    :raises RuntimeError: Captured from the failed subprocess.
    """
    # Mock compilation process crash
    ## Setup mock return code throwing a CalledProcessError
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=2,
            cmd=["make"],
            stderr=b"G++ Linker Error: undefined reference to main"
        )

        # Execute build validation assertions
        ### Verify that a compilation fault halts execution immediately with proper regex escaping
        with pytest.raises(RuntimeError, match=r"C\+\+ Compilation failed: G\+\+ Linker Error"):
            _compile_physiboss_engine(Path("/mock/engine_root"))


## Test simulation executable existence check paths
@patch("OmniPhysiBoSS.wrappers.run_PhysiBoSS._compile_physiboss_engine")
@patch("os.makedirs")
def test_runner_missing_executable(mock_makedirs, mock_compile, tmp_path):
    """
    Verifies that a FileNotFoundError is raised if the target binary is missing post-compilation.

    :param mock_makedirs: Mocked directory allocation interface.
    :type mock_makedirs: MagicMock
    :param mock_compile: Mocked engine compiler routine.
    :type mock_compile: MagicMock
    :param tmp_path: Pytest temporary workspace path token.
    :type tmp_path: Path
    """
    # Setup paths pointing to missing file bounds
    xml_path = tmp_path / "settings.xml"
    logs_output = tmp_path / "sim.log"
    
    # Execute runner validation loop assertions
    ## Verify catch statements block operations if compiled binary references are broken
    with pytest.raises(FileNotFoundError, match="Target executable file not found"):
        run_physiboss_simulation(
            xml_path=xml_path,
            logs_output=logs_output,
            physiboss_root=tmp_path / "engine",
            executable_name="non_existent_binary"
        )


## Test standard telemetry streaming and state log monitoring
def test_log_monitor_mesh_and_rng_parsing(capsys):
    """
    Validates that the log monitor extracts domain properties and handles random seed indicators.

    :param capsys: Pytest standard output interception capture token.
    :type capsys: CaptureFixture
    """
    # Instantiate atomic log analysis engine instance
    monitor = PhysiBoSSLogMonitor()

    # Generate sequence lines matching standard output streams
    log_sequence = [
        "Mesh information:",
        "type: uniform Cartesian",
        "Domain: [-100,200] micron x [-100,100] micron x [-20,20] micron",
        "resolution: dx = 10 micron",
        "voxels: 2400",
        "WARNING: Setting the random seed again.",
        "Setting up RNG with seed 42"
    ]

    # Process logs lines sequentially
    ## Iterate over log sequences to capture state translations
    for line in log_sequence:
        monitor.process_line(line)

    # Capture standard terminal stdout states
    captured = capsys.readouterr().out

    # Perform structured parsing metrics assertions
    ## Check for mesh data encapsulation text markers
    assert "[SYSTEM INFRASTRUCTURE] Extracting Cartesian mesh domain layout..." in captured
    assert "Domain: [-100,200] micron x [-100,100] micron x [-20,20] micron" in captured
    
    ## Check for randomized configuration handling state shifts
    assert "[RNG WARNING] Duplicate random seed variable found in user parameters." in captured
    assert "[RNG CONFIGURATION] Successfully setting up rng with seed 42" in captured


def test_log_monitor_preprocessing_and_metrics_parsing(capsys):
    """
    Validates that line parsers capture lineage initialization states and step outputs.

    :param capsys: Pytest standard output interception capture token.
    :type capsys: CaptureFixture
    """
    monitor = PhysiBoSSLogMonitor()

    log_sequence = [
        "Pre-processing type 0 named default",
        "Processing default ... ",
        "current simulated time: 50 min (max: 200 min)",
        "total agents: 486"
    ]

    # Process telemetry text buffers
    for line in log_sequence:
        monitor.process_line(line)

    captured = capsys.readouterr().out

    # Assert processing translation patterns
    ## Verify lineage structural setup trackers
    assert "⚙️ [PRE-PROCESSING] Initializing structural cell properties for lineage: 'default'" in captured
    assert "✅ [PRE-PROCESSING] Completed pipeline setup configuration for: 'default'" in captured
    
    ## Verify multiscale trajectory step outputs matching time increments
    assert "⏱️ [SIMULATION METRIC] current simulated time: 50 min (max: 200 min)" in captured
    assert "👥 [SIMULATION POPULATION] total agents: 486" in captured


## Test end-to-end simulated orchestration execution
@patch("OmniPhysiBoSS.wrappers.run_PhysiBoSS._compile_physiboss_engine")
@patch("os.makedirs")
@patch("builtins.open", new_callable=mock_open)
def test_run_simulation_pipeline_success(mock_file, mock_makedirs, mock_compile, tmp_path):
    """
    Validates the end-to-end execution path, standard output tracking, and log file writing.

    :param mock_file: Mocked open interface wrapper for file writing validations.
    :type mock_file: MagicMock
    :param mock_makedirs: Mocked directory infrastructure manager.
    :type mock_makedirs: MagicMock
    :param mock_compile: Mocked compilation lifecycle process tool.
    :type mock_compile: MagicMock
    :param tmp_path: Pytest temporary system workspace root.
    :type tmp_path: Path
    """
    # Setup physical environment mock references
    ## Configure mock paths on disk layouts
    physiboss_root = tmp_path / "engine"
    xml_path = tmp_path / "PhysiCell_settings.xml"
    executable_name = "PhysiBoSS_Cell_Lines"
    binary_path = physiboss_root / executable_name
    
    ## Allocate physical placeholders on disk space
    binary_path.parent.mkdir(parents=True, exist_ok=True)
    binary_path.touch()

    # Configure Popen simulation process mockup environment
    ## Setup context mocks for background streams execution tracking
    mock_process = MagicMock()
    mock_process.stdout = ["current simulated time: 10 min", "total agents: 100\n", "Total simulation runtime:\n"]
    mock_process.wait.return_value = 0
    
    ### Bind context manager entry returns back to the configured tracking mock instance
    mock_process.__enter__.return_value = mock_process

    with patch("subprocess.Popen", return_value=mock_process) as mock_popen:
        # Invoke orchestrator runner module logic
        run_physiboss_simulation(
            xml_path=xml_path,
            physiboss_root=physiboss_root,
            executable_name=executable_name
        )

        # Assert correct process instantiation metrics
        ## Verify that sub-processes target the newly staged configuration file path structure
        expected_staged_xml = physiboss_root / "OmniPhysiBoSS_projects" / "PhysiCell_settings" / "PhysiCell_settings.xml"
        mock_popen.assert_called_once_with(
            [str(binary_path), str(expected_staged_xml)],
            cwd=physiboss_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Verify background telemetry writing tasks
        ## Ensure logs output is written to disk partitions
        mock_file.assert_called_once()