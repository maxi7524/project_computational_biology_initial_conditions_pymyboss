# PhysiCell configuration templates factory
## Standard and multi-model XML layout generators matching 1:1 regression requirements

def get_reference_mock_xml_string() -> str:
    """
    Returns the exact reference XML configuration layout including a single MaBoSS 
    intracellular core extension to support 1:1 structural regression testing.

    :return: A well-formatted XML string reflecting the complete configuration schema.
    :rtype: str
    """
    return """<?xml version='1.0' encoding='utf-8'?>
<PhysiCell_settings version="devel-version">
    <domain>
        <x_min>-500.0</x_min>
        <x_max>500.0</x_max>
        <y_min>-500.0</y_min>
        <y_max>500.0</y_max>
        <z_min>-10.0</z_min>
        <z_max>10.0</z_max>
        <dx>20.0</dx>
        <dy>20.0</dy>
        <dz>20.0</dz>
        <use_2D>true</use_2D>
    </domain>
    <overall>
        <max_time units="min">1440.0</max_time>
        <time_units>min</time_units>
        <space_units>micron</space_units>
        <dt_diffusion units="min">0.01</dt_diffusion>
        <dt_mechanics units="min">0.1</dt_mechanics>
        <dt_phenotype units="min">6.0</dt_phenotype>
    </overall>
    <parallel>
        <omp_num_threads>6</omp_num_threads>
    </parallel>
    <save>
        <folder>output</folder>
        <full_data>
            <interval units="min">6.0</interval>
            <enable>true</enable>
        </full_data>
        <SVG>
            <interval units="min">6.0</interval>
            <enable>true</enable>
        </SVG>
        <legacy_data>
            <enable>false</enable>
        </legacy_data>
    </save>
    <options>
        <legacy_random_points_on_sphere_in_divide>false</legacy_random_points_on_sphere_in_divide>
        <virtual_wall_at_domain_edge>true</virtual_wall_at_domain_edge>
        <disable_automated_spring_adhesions>false</disable_automated_spring_adhesions>
        <random_seed>0</random_seed>
    </options>
    <microenvironment_setup>
        <variable name="substrate" units="dimensionless" ID="0">
            <physical_parameter_set>
                <diffusion_coefficient units="micron^2/min">100000.0</diffusion_coefficient>
                <decay_rate units="1/min">10.0</decay_rate>
            </physical_parameter_set>
            <initial_condition units="mmHg">0.0</initial_condition>
            <Dirichlet_boundary_condition enabled="False" units="mmHg">0</Dirichlet_boundary_condition>
        </variable>
        <options>
            <calculate_gradients>true</calculate_gradients>
            <track_internalized_substrates_in_each_agent>true</track_internalized_substrates_in_each_agent>
        </options>
    </microenvironment_setup>
    <cell_definitions>
        <cell_definition name="stem" ID="0">
            <phenotype>
                <cycle code="5" name="live">
                    <phase_durations units="min">
                        <duration index="0" fixed_duration="false">1440.0</duration>
                    </phase_durations>
                </cycle>
                <volume>
                    <total units="micron^3">2494.0</total>
                    <fluid_fraction units="dimensionless">0.75</fluid_fraction>
                </volume>
                <intracellular type="maboss">
                    <bnd_filename>./config/boolean_network.bnd</bnd_filename>
                    <cfg_filename>./config/boolean_network.cfg</cfg_filename>
                    <time_step>1.0</time_step>
                </intracellular>
            </phenotype>
            <custom_data />
        </cell_definition>
    </cell_definitions>
    <initial_conditions>
        <cell_positions type="csv" enabled="true">
            <folder>./config</folder>
            <filename>cells.csv</filename>
        </cell_positions>
    </initial_conditions>
    <cell_rules>
        <rulesets>
            <ruleset protocol="CBHG" version="3.0" format="csv" enabled="true">
                <folder>./config</folder>
                <filename>cell_rules.csv</filename>
            </ruleset>
        </rulesets>
    </cell_rules>
    <user_parameters>
        <number_of_cells type="int" units="none" description="initial number of cells">0</number_of_cells>
    </user_parameters>
</PhysiCell_settings>
"""


def get_multi_model_mock_xml_string() -> str:
    """
    Returns an advanced reference XML configuration containing multiple distinct 
    cell definitions mapping to independent Boolean network configurations.

    :return: A multi-model XML configuration schema layout string.
    :rtype: str
    """
    return """<?xml version='1.0' encoding='utf-8'?>
<PhysiCell_settings version="devel-version">
    <domain>
        <x_min>-100.0</x_min>
        <x_max>100.0</x_max>
        <y_min>-100.0</y_min>
        <x_max>100.0</x_max>
        <z_min>-10.0</z_min>
        <z_max>10.0</z_max>
        <dx>10.0</dx>
        <dy>10.0</dy>
        <dz>10.0</dz>
        <use_2D>true</use_2D>
    </domain>
    <overall>
        <max_time units="min">200.0</max_time>
        <time_units>min</time_units>
        <space_units>micron</space_units>
        <dt_diffusion units="min">0.01</dt_diffusion>
        <dt_mechanics units="min">0.1</dt_mechanics>
        <dt_phenotype units="min">10.0</dt_phenotype>
    </overall>
    <parallel>
        <omp_num_threads>4</omp_num_threads>
    </parallel>
    <save>
        <folder>output</folder>
        <full_data>
            <interval units="min">10.0</interval>
            <enable>true</enable>
        </full_data>
        <SVG>
            <interval units="min">10.0</interval>
            <enable>true</enable>
        </SVG>
        <legacy_data>
            <enable>false</enable>
        </legacy_data>
    </save>
    <options>
        <legacy_random_points_on_sphere_in_divide>false</legacy_random_points_on_sphere_in_divide>
        <virtual_wall_at_domain_edge>true</virtual_wall_at_domain_edge>
        <disable_automated_spring_adhesions>true</disable_automated_spring_adhesions>
        <random_seed>0</random_seed>
    </options>
    <microenvironment_setup>
        <variable name="oxygen" units="dimensionless" ID="0">
            <physical_parameter_set>
                <diffusion_coefficient units="micron^2/min">100000.0</diffusion_coefficient>
                <decay_rate units="1/min">0.1</decay_rate>
            </physical_parameter_set>
            <initial_condition units="dimensionless">38.0</initial_condition>
            <Dirichlet_boundary_condition enabled="False" units="dimensionless">38.0</Dirichlet_boundary_condition>
        </variable>
    </microenvironment_setup>
    <cell_definitions>
        <cell_definition name="default" ID="0">
            <phenotype>
                <cycle code="2" name="Flow cytometry model (basic)">
                    <phase_durations units="min">
                        <duration index="0" fixed_duration="false">inf</duration>
                        <duration index="1" fixed_duration="false">inf</duration>
                        <duration index="2" fixed_duration="false">inf</duration>
                    </phase_durations>
                </cycle>
                <intracellular type="maboss">
                    <bnd_filename>./config/cell_fate.bnd</bnd_filename>
                    <cfg_filename>./config/cell_fate.cfg</cfg_filename>
                    <time_step>1.0</time_step>
                </intracellular>
            </phenotype>
        </cell_definition>
        <cell_definition name="other" ID="1">
            <phenotype>
                <cycle code="2" name="Flow cytometry model (basic)">
                    <phase_durations units="min">
                        <duration index="0" fixed_duration="false">inf</duration>
                        <duration index="1" fixed_duration="false">inf</duration>
                        <duration index="2" fixed_duration="false">inf</duration>
                    </phase_durations>
                </cycle>
                <intracellular type="maboss">
                    <bnd_filename>./config/immune_activation.bnd</bnd_filename>
                    <cfg_filename>./config/immune_activation.cfg</cfg_filename>
                    <time_step>1.0</time_step>
                </intracellular>
            </phenotype>
        </cell_definition>
    </cell_definitions>
    <initial_conditions>
        <cell_positions type="csv" enabled="true">
            <folder>./config</folder>
            <filename>cells.csv</filename>
        </cell_positions>
    </initial_conditions>
    <cell_rules>
        <rulesets>
            <ruleset protocol="CBHG" version="3.0" format="csv" enabled="true">
                <folder>./config</folder>
                <filename>cell_rules.csv</filename>
            </ruleset>
        </rulesets>
    </cell_rules>
    <user_parameters>
        <random_seed type="int" units="dimensionless">0</random_seed>
    </user_parameters>
</PhysiCell_settings>
"""


def get_reference_cells_csv_string() -> str:
    """
    Returns the structured mock layout for spatial coordinate vector initialization.

    :return: A comma-separated string mapping baseline cell coordinates.
    :rtype: str
    """
    return "x,y,z,type\n0,0,0,default\n10,10,0,other"


def get_reference_rules_csv_string() -> str:
    """
    Returns the baseline cell behavior hypothesis grammar (CBHG) ruleset.

    :return: A comma-separated string mapping signal-to-behavior transitions.
    :rtype: str
    """
    return "default,volume,increases,cycle entry,0.17,1200.0,8,0\nother,volume,increases,cycle entry,0.1,1000.0,4,0"