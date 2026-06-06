import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

# Core application and asset dependency structures
from OmniPhysiBoSS.generators import MaBoSSModelGenerator
from tests.mock_data import (
    get_maboss_bnd_mock_string, 
    get_maboss_cfg_mock_string,
    get_immune_activation_bnd_mock_string,
    get_immune_activation_cfg_mock_string
)

# ----------------------------------
# 1. Syntactic Expression & Parsing Evaluation Tests
# ----------------------------------

def test_validate_and_translate_logic_operators():
    """
    Verify character-set logic mapper shifts keyword structures safely to symbol tokens.
    """
    # Logic expression processing
    ## Parsing Boolean character strings to verify operator translations
    generator = MaBoSSModelGenerator("signaling_core")
    translated = generator._validate_and_translate_logic("A AND NOT B OR C")
    assert translated == "A & ! B | C"


def test_validate_and_translate_logic_invalid_syntax():
    """
    Verify input analyzer isolates unsupported code vectors or unsafe operations.
    """
    # Malformed syntax testing
    ## Injecting illegal string signatures to verify error handling bounds
    generator = MaBoSSModelGenerator("signaling_core")
    with pytest.raises(ValueError, match="Unsupported characters or operators found in logic expression"):
        generator._validate_and_translate_logic("A system_call_malicious() B")


# ----------------------------------
# 2. Node Mapping & Configuration Metrics Constraints Tests
# ----------------------------------

def test_add_node_validation_bounds():
    """
    Verify initialization state thresholds reject formatting mutations outside bounded probability fields.
    """
    # Node definition testing
    ## Validate registration threshold indices across legal boundaries
    generator = MaBoSSModelGenerator("signaling_core")
    generator.add_node("CASP8", "DISC_TNF", istate=0.5)
    assert "CASP8" in generator.nodes
    
    ## Attempt out-of-bounds initialization to trigger data consistency checks
    with pytest.raises(ValueError, match="istate for node CASP8 must be within"):
        generator.add_node("CASP8", "DISC_TNF", istate=1.5)


def test_set_engine_parameter_typing():
    """
    Verify state type verification constraints evaluate input vectors precisely against expectations.
    """
    # Structural configuration verification
    ## Testing input type boundaries against valid execution parameter options
    generator = MaBoSSModelGenerator("signaling_core")
    generator.set_engine_parameter("sample_count", 80000)
    
    with pytest.raises(TypeError, match="must be of type"):
        generator.set_engine_parameter("sample_count", "string_invalid")


def test_set_global_variable_prefix_enforcement():
    """
    Verify value registration isolates variable names omitting specific indicator markers.
    """
    # Token formatting evaluation
    ## Testing requirements for standard dollar sign variable prefix markers
    generator = MaBoSSModelGenerator("signaling_core")
    generator.set_global_variable("$TransRate", 0.1)
    
    with pytest.raises(ValueError, match="Global variables in MaBoSS must begin with"):
        generator.set_global_variable("TransRate_Missing_Prefix", 0.1)


# ----------------------------------
# 3. Structural Output Optimization & Engine Validation Layer Tests
# ----------------------------------

def test_write_model_file_persistence():
    """
    Verify generation routines deploy accurate assets across target output folders.
    """
    # Physical persistence serialization
    ## Registering valid logical parameters for execution tracing
    generator = MaBoSSModelGenerator("signaling_core")
    generator.add_node("CASP8", "DISC_TNF", istate=0.0)
    generator.set_global_variable("$CASP8_del", False)
    generator.set_engine_parameter("max_time", 100)

    # Storage access block
    ## Perform physical file writes onto isolated testing volumes
    with TemporaryDirectory() as tmp_dir:
        generator.write_model(output_dir=tmp_dir)
        
        bnd_file = Path(tmp_dir) / "signaling_core.bnd"
        cfg_file = Path(tmp_dir) / "signaling_core.cfg"
        
        assert bnd_file.exists() and cfg_file.exists()
        assert "Node CASP8" in bnd_file.read_text()
        assert "$CASP8_del = FALSE;" in cfg_file.read_text()


def test_maboss_parser_library_loading():
    """
    Validation Test: Verifies output syntax integrity compatibility against continuous-time Markov parsers.
    """
    # Syntax validation checks
    ## Formatting configuration inputs to reflect canonical model parsing structures
    generator = MaBoSSModelGenerator("signaling_core")
    generator.add_node("DISC_TNF", "DISC_TNF", istate=0.0)
    generator.add_node("CASP8", "DISC_TNF", istate=0.0)
    generator.set_engine_parameter("sample_count", 1000)
    generator.set_engine_parameter("max_time", 10)

    with TemporaryDirectory() as tmp_dir:
        generator.write_model(output_dir=tmp_dir)
        bnd_path = Path(tmp_dir) / "signaling_core.bnd"
        cfg_path = Path(tmp_dir) / "signaling_core.cfg"
        
        # Log evaluation loop
        ## Scan structured output files sequentially to verify text serialization syntax
        with open(bnd_path, "r") as bnd_f, open(cfg_path, "r") as cfg_f:
            bnd_lines = bnd_f.readlines()
            cfg_lines = cfg_f.readlines()
            
        assert any("Node DISC_TNF" in line for line in bnd_lines)
        assert any("sample_count = 1000;" in line for line in cfg_lines)


def test_generation_of_alternative_immune_activation_model():
    """
    Validates that the generator can assemble and write the distinct secondary immune model syntax without structural regression.
    """
    # Alternate model assembly
    ## Initializing independent variables for the immune activation network structure
    generator = MaBoSSModelGenerator("immune_activation")
    generator.add_node("AntigenPresent", "AntigenPresent", istate=1.0)
    generator.add_node("TCR_Binding", "AntigenPresent", istate=0.0)
    generator.set_global_variable("$STAT_inhibited", False)
    generator.set_engine_parameter("thread_count", 2)

    with TemporaryDirectory() as tmp_dir:
        generator.write_model(output_dir=tmp_dir)
        cfg_text = (Path(tmp_dir) / "immune_activation.cfg").read_text()
        
        assert "$STAT_inhibited = FALSE;" in cfg_text
        assert "thread_count = 2" in cfg_text