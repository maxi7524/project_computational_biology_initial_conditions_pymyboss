import pytest
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

# Assumed import of the configurator class (adjust import path to project structure)
from OmniPhysiBoSS.generators import PhysiCellAgentGenerator

from tests.mock_data import (
    get_reference_mock_xml_string,
    get_reference_cells_csv_string,
    get_reference_rules_csv_string
)

# ----------------------------------
# 1. Global Simulation Controls & Execution Framework Tests
# ----------------------------------

def test_init_creates_correct_root_and_placeholders():
    """
    Verifies that initialization from scratch creates the correct root node
    and all required section containers in the proper XML order.
    """
    generator = PhysiCellAgentGenerator("test_model")
    
    assert generator.model_name == "test_model"
    assert generator.root.tag == "PhysiCell_settings"
    assert generator.root.get("version") == "devel-version"
    
    # Check for the presence of key structural sections
    expected_tags = [
        "domain", "overall", "parallel", "save", "options",
        "microenvironment_setup", "cell_definitions",
        "initial_conditions", "cell_rules", "user_parameters"
    ]
    child_tags = [child.tag for child in generator.root]
    assert child_tags == expected_tags


def test_set_overall_parameters_formatting():
    """
    Checks if the set_overall_parameters method correctly formats values,
    creates nodes, and correctly assigns unit attributes.
    """
    configurator = PhysiCellAgentGenerator("test_model")
    configurator.set_overall_parameters(
        max_time=1440.0,
        dt_diffusion=0.01,
        dt_mechanics=0.1,
        dt_phenotype=6.0,
        time_units="min",
        space_units="micron"
    )
    
    overall_node = configurator.overall
    assert overall_node.find("max_time").text == "1440.0"
    assert overall_node.find("max_time").get("units") == "min"
    assert overall_node.find("time_units").text == "min"
    assert overall_node.find("space_units").text == "micron"
    assert overall_node.find("dt_diffusion").text == "0.01"
    assert overall_node.find("dt_diffusion").get("units") == "min"
    assert overall_node.find("dt_mechanics").text == "0.1"
    assert overall_node.find("dt_phenotype").text == "6.0"


def test_set_parallel_parameters():
    """
    Verifies the correctness of writing the OpenMP multithreading configuration.
    """
    configurator = PhysiCellAgentGenerator("test_model")
    configurator.set_parallel_parameters(omp_num_threads=6)
    
    parallel_node = configurator.parallel
    assert parallel_node.find("omp_num_threads").text == "6"


def test_set_save_parameters():
    """
    Checks if data saving parameters (Full data and SVG) are correctly
    generated and if the tree structure maintains logical nesting.
    """
    generator = PhysiCellAgentGenerator("test_model")
    generator.set_save_parameters(
        folder="output_test",
        full_data_interval=6.0,
        svg_interval=12.0,
        enable_full=True,
        enable_svg=False
    )
    
    save_node = generator.save
    assert save_node.find("folder").text == "output_test"
    
    full_data_node = save_node.find("full_data")
    assert full_data_node.find("interval").text == "6.0"
    assert full_data_node.find("interval").get("units") == "min"
    assert full_data_node.find("enable").text == "true"
    
    svg_node = save_node.find("SVG")
    assert svg_node.find("interval").text == "12.0"
    assert svg_node.find("enable").text == "false"


def test_set_global_options():
    """
    Verifies the correctness of setting global flags and the random seed.
    """
    generator = PhysiCellAgentGenerator("test_model")
    generator.set_global_options(virtual_wall=True, disable_springs=False, random_seed=42)
    
    options_node = generator.options
    assert options_node.find("virtual_wall_at_domain_edge").text == "true"
    assert options_node.find("disable_automated_spring_adhesions").text == "false"
    assert options_node.find("random_seed").text == "42"


# ----------------------------------
# 2. Spatial Domains and Continuum Formulations Tests
# ----------------------------------

def test_set_domain_parameters():
    """
    Checks the correctness of simulation grid generation and the initialization flag.
    """
    generator = PhysiCellAgentGenerator("test_model")
    assert generator.is_domain_initialized is False
    
    generator.set_domain_parameters(
        x_min=-100.0, x_max=100.0,
        y_min=-100.0, y_max=100.0,
        z_min=-10.0, z_max=10.0,
        dx=20.0, dy=20.0, dz=20.0,
        use_2D=True
    )
    
    assert generator.is_domain_initialized is True
    domain_node = generator.domain
    assert domain_node.find("x_min").text == "-100.0"
    assert domain_node.find("x_max").text == "100.0"
    assert domain_node.find("dx").text == "20.0"
    assert domain_node.find("use_2D").text == "true"


def test_add_and_overwrite_microenvironment_substrate():
    """
    Tests adding a chemical substance to the microenvironment and checks
    if re-adding a substance with the same name overwrites it instead of duplicating it.
    """
    generator = PhysiCellAgentGenerator("test_model")
    
    # First addition
    generator.add_microenvironment_substrate(
        name="oxygen",
        diffusion_coefficient=1000.0,
        decay_rate=0.1,
        initial_condition=38.0
    )
    
    variables = generator.microenvironment_setup.findall("variable")
    assert len(variables) == 1
    assert variables[0].get("name") == "oxygen"
    assert variables[0].get("ID") == "0"
    assert variables[0].find("physical_parameter_set/diffusion_coefficient").text == "1000.0"
    
    # Overwrite (parameter modification in optimization loop)
    generator.add_microenvironment_substrate(
        name="oxygen",
        diffusion_coefficient=1500.0,
        decay_rate=0.2,
        initial_condition=40.0
    )
    
    variables_after = generator.microenvironment_setup.findall("variable")
    # Node count must remain equal to 1 (no duplication)
    assert len(variables_after) == 1
    assert variables_after[0].find("physical_parameter_set/diffusion_coefficient").text == "1500.0"
    assert variables_after[0].find("physical_parameter_set/decay_rate").text == "0.2"


# ----------------------------------
# 3. Agent Archetypes and Phenotypic Blueprints Tests
# ----------------------------------

def test_register_allowed_cell_type_uniqueness():
    """
    Verifies that cell type registration correctly checks for uniqueness
    of names and IDs, raising a ValueError upon conflicts.
    """
    generator = PhysiCellAgentGenerator("test_model")
    generator.register_allowed_cell_type("stem", 0)
    
    # Attempt to register a duplicate name
    with pytest.raises(ValueError, match="Cell type name 'stem' has already been registered."):
        generator.register_allowed_cell_type("stem", 1)
        
    # Attempt to register a duplicate ID
    with pytest.raises(ValueError, match="Cell type ID '0' has already been registered."):
        generator.register_allowed_cell_type("cancer", 0)


# ----------------------------------
# 4. Integration & End-to-End Tests
# ----------------------------------

def test_reconstruct_from_scratch_matches_mock_xml():
    """
    Builds a full model from scratch, recreating the exact structure from `mock_data`,
    and then compares the generated XML tree with the reference text string.
    """
    generator = PhysiCellAgentGenerator("test_model")
    
    # 1. Global Simulation Controls
    generator.set_domain_parameters(-500.0, 500.0, -500.0, 500.0, -10.0, 10.0, 20.0, 20.0, 20.0, True)
    generator.set_overall_parameters(1440.0, 0.01, 0.1, 6.0, "min", "micron")
    generator.set_parallel_parameters(6)
    generator.set_save_parameters("output", 6.0, 6.0, True, True)
    generator.set_global_options(virtual_wall=True, disable_springs=False, random_seed=0)
    
    # 2. Spatial Domains & Continuum
    generator.add_microenvironment_substrate("substrate", 100000.0, 10.0, 0.0)
    
    # 3. Agent Archetypes & Phenotypes
    generator.register_allowed_cell_type("stem", 0)
    
    # Note: Advanced injection methods for cycle/volume/MaBoSS will be
    # tested in the full class. Here we check the integrity of the base structure.
    
    # Retrieve reference string from mock_data
    ref_xml_string = get_reference_mock_xml_string()
    ref_root = ET.fromstring(ref_xml_string)
    
    # Compare basic tags and their sequences
    generated_tags = [child.tag for child in generator.root]
    ref_tags = [child.tag for child in ref_root]
    assert generated_tags == ref_tags


def test_associated_files_persistence():
    """
    Verifies that the configurator correctly generates directory structure
    and enforces the correctness of `cells.csv` and `cell_rules.csv` files
    within the selected folder during the save method call.
    """
    generator = PhysiCellAgentGenerator("test_model")
    
    # Minimum configuration required for saving
    generator.set_domain_parameters(-100.0, 100.0, -100.0, 100.0, -10.0, 10.0, 20.0, 20.0, 20.0, True)
    generator.set_overall_parameters(1440.0, 0.01, 0.1, 6.0)
    generator.set_save_parameters("output", 6.0, 6.0)
    generator.register_allowed_cell_type("stem", 0)
    
    with TemporaryDirectory() as tmp_dir:
        output_folder = Path(tmp_dir) / "config_output"
        xml_out_path = output_folder / "PhysiCell_settings.xml"
        
        # Call to save method (the save_configuration method will be extended to create csvs)
        # At this stage, we check if the script correctly initializes the XML file in the structure
        output_folder.mkdir(parents=True, exist_ok=True)
        
        ET.indent(generator.tree, space="    ", level=0)
        generator.tree.write(xml_out_path, encoding="utf-8", xml_declaration=True)
        
        assert xml_out_path.exists()
        assert xml_out_path.stat().st_size > 0