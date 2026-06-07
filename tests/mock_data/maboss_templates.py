# MaBoSS logical engine mock templates factory
## Reference strings matching cell fate model topologies
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
    Returns reference configuration runtime directives (.cfg) for cell fate model.

    :return: Configuration parameters mapping execution tick increments.
    :rtype: str
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


# Alternative logic profile generation
## Functions to return a secondary independent signaling structure mapping immune activation loops
def get_immune_activation_bnd_mock_string() -> str:
    """
    Returns a valid secondary signaling network model (.bnd) representing an activation loop.

    :return: Full string composition of the alternative logic topology network.
    :rtype: str
    """
    return """node AntigenPresent
{
  rate_up = 0.0;
  rate_down = 0.0;
}
node TCR_Binding
{
  logic = AntigenPresent;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node JAK_Pathway
{
  logic = TCR_Binding;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node STAT_Activation
{
  logic = JAK_Pathway & (!$STAT_inhibited);
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
node CytokineProduction
{
  logic = STAT_Activation;
  rate_up = @logic ? 1.0 : 0.0;
  rate_down = @logic ? 0.0 : 1.0;
}
"""

def get_immune_activation_cfg_mock_string() -> str:
    """
    Returns reference configuration runtime directives (.cfg) for the immune activation model.

    :return: Configuration parameter string specifying probability profiles.
    :rtype: str
    """
    return """$STAT_inhibited = FALSE;

[AntigenPresent].istate = 1.0;
[TCR_Binding].istate = 0.0;

sample_count = 40000;
max_time = 50;
time_tick = 0.2;
discrete_time = 0;
use_physrandgen = FALSE;
seed_pseudorandom = 42;
display_traj = FALSE;
thread_count = 2;
statdist_traj_count = 50;
statdist_cluster_threshold = 0.7;
"""
