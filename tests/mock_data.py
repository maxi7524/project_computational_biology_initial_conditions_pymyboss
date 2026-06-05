import anndata as ad
import pandas as pd
import numpy as np


# ----------------------------------
# mdata  
# ----------------------------------


#TODO - change it to mdata 
def create_mock_anndata() -> ad.AnnData:
    """
    Generates a standardized mock AnnData object for spatial transcriptomics unit tests.

    The object contains a small expression matrix (5 cells, 4 genes),
    2D spatial coordinates, 3D spatial coordinates for dimension pruning tests,
    and cell type metadata annotations.

    :return: A populated AnnData instance for testing.
    :rtype: anndata.AnnData
    """
    # Mock data generation
    ## Expression matrix setup
    ### Define 5 cells and 4 genes with normalized values
    X = np.array([
        [0.1, 0.8, 0.0, 0.4],
        [0.9, 0.2, 0.1, 0.0],
        [0.0, 0.0, 0.7, 0.9],
        [0.4, 0.5, 0.3, 0.2],
        [0.1, 0.1, 0.9, 0.8]
    ], dtype=np.float32)

    ## Metadata annotations
    ### Create cell identifiers and type assignments
    obs = pd.DataFrame(
        {"cell_type": ["Tumor", "T-Cell", "B-Cell", "Tumor", "Macrophage"]},
        index=[f"cell_{i}" for i in range(5)]
    )
    var = pd.DataFrame(index=["Gene_A", "Gene_B", "Gene_C", "Gene_D"])

    ## Spatial coordinates matrices
    ### Configure distinct 2D and 3D position spaces
    spatial_2d = np.array([
        [10.0, 20.0],
        [15.0, 25.0],
        [20.0, 30.0],
        [25.0, 35.0],
        [30.0, 40.0]
    ], dtype=np.float32)

    spatial_3d = np.array([
        [10.0, 20.0, 5.0],
        [15.0, 25.0, 6.0],
        [20.0, 30.0, 7.0],
        [25.0, 35.0, 8.0],
        [30.0, 40.0, 9.0]
    ], dtype=np.float32)

    ## Object instantiation
    ### Encapsulate matrices into the AnnData container
    adata = ad.AnnData(X=X, obs=obs, var=var)
    adata.obsm["spatial"] = spatial_2d
    adata.obsm["spatial_3d"] = spatial_3d

    return adata


# ----------------------------------
# PhysiCell objects 
# ----------------------------------

def get_reference_mock_xml_string() -> str:
    """
    Returns the exact reference XML configuration layout including the MaBoSS 
    intracellular core extensions to support 1:1 structural regression testing.

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

def get_reference_cells_csv_string() -> str:
    """
    Returns the structured mock layout for spatial coordinate vector initialization.

    :return: A comma-separated string mapping baseline cell coordinates.
    :rtype: str
    """
    return """x,y,z,type\\n0,0,0,stem"""

def get_reference_rules_csv_string() -> str:
    """
    Returns the baseline cell behavior hypothesis grammar (CBHG) ruleset.

    :return: A comma-separated string mapping signal-to-behavior transitions.
    :rtype: str
    """
    return """stem,volume,increases,cycle entry,0.17,1200.0,8,0"""

# ----------------------------------
# MaBoSS objects 
# ----------------------------------

def get_maboss_bnd_mock_string() -> str:
    """
    Returns the complete, expanded structural node configurations (.bnd)
    matching the entire CellFateModel topology for strict parsing regression.

    :return: Full string composition of the cellular death logic regulatory network.
    :rtype: str
    """
    return """node FASL
{
  rate_up = 0.0;
  rate_down = 0.0;
}
node TNF
{
  rate_up = 0.0;
  rate_down = 0.0;
}
node TNFR
{
  logic = TNF;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node DISC_TNF
{
  logic = FADD & TNFR;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node DISC_FAS
{
  logic = FASL & FADD;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node FADD
{
  rate_up = 0.0;
  rate_down = 0.0 + 1000*$FADD_del;
}
node RIP1
{
  logic = (DISC_FAS | TNFR) & (!CASP8);
  rate_up = (@logic & (!$RIP1_del)) ? 1.0 : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$RIP1_del;
}
node RIP1ub
{
  logic = cIAP & RIP1;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node RIP1K
{
  logic = RIP1;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node IKK
{
  logic = RIP1ub;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node NFkB
{
  logic = IKK & (!CASP3);
  rate_up = ((@logic & (!$NFkB_del)) ? 1.0 : 0.0) + 1000*$NFkB_oe;
  rate_down = ((@logic | $NFkB_oe) ? 0.0 : 1.0) + 1000*$NFkB_del;
}
node CASP8
{
  logic = (DISC_TNF | (DISC_FAS | CASP3) ) & (!cFLIP);
  rate_up = (@logic & (!$CASP8_del)) ? 1.0 : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$CASP8_del;
}
node BAX
{
  logic = CASP8 & (!BCL2);
  rate_up = (@logic & (!$BAX_del)) ? 1.0 : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$BAX_del;
}
node BCL2
{
  logic = NFkB;
  rate_up = (@logic ? $TransRate : 0.0) + 1000*$BCL2_oe;
  rate_down = (@logic | $BCL2_oe) ? 0.0 : 1.0; 
}
node ROS
{
  logic = (!NFkB) & (MPT | RIP1K );
  rate_up = @logic ? $TransRate : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node ATP
{
  logic = !MPT;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node MPT
{
  logic = (!BCL2) & ROS;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node MOMP
{
  logic = BAX | MPT;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node SMAC 
{
  logic = MOMP;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node cIAP
{
  rate_up = ((NFkB & (!SMAC)) & (!$cIAP_del)) ? $TransRate : 0.0;
  rate_down = ((SMAC) ? 1.0 : 0.0) + 1000*$cIAP_del;
}
node Cyt_c
{
  logic = MOMP;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node XIAP
{
  logic = (!SMAC) & NFkB;
  rate_up = (@logic & (!$XIAP_del)) ? $TransRate : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$XIAP_del; 
}
node apoptosome
{
  logic = Cyt_c & (ATP & (!XIAP));
  rate_up = (@logic & (!$APAF_del)) ? 1.0 : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$APAF_del ;
}
node CASP3
{
  logic = apoptosome & (!XIAP);
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node cFLIP
{
  logic = NFkB ;
  rate_up = (@logic & (!$cFLIP_del))  ? $TransRate : 0.0;
  rate_down = (@logic ? 0.0 : 1.0) + 1000*$cFLIP_del; 
}
node NonACD
{
  logic = !ATP;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node Apoptosis
{
  logic = CASP3;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
node Survival
{
  logic = NFkB;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0; 
}
"""

def get_maboss_cfg_mock_string() -> str:
    """
    Returns reference configuration runtime directives (.cfg).
    """
    return """$CASP8_del = FALSE;
$TransRate = 0.1;

[DISC_TNF].istate = 0.0;
DISC_TNF.is_internal = TRUE;
[CASP8].istate = 0.0;

sample_count = 80000;
max_time = 100;
time_tick = 0.1;
discrete_time = 0;
use_physrandgen = FALSE;
seed_pseudorandom = 300;
display_traj = FALSE;
thread_count = 4;
statdist_traj_count = 100;
statdist_cluster_threshold = 0.8;
"""