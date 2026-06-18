from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class AsymmetricDivisionType:
    asymmetric_division_probability: list[
        AsymmetricDivisionType.AsymmetricDivisionProbability
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class AsymmetricDivisionProbability:
        value: float = field()
        name: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
        units: None | str = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class CellAdhesionAffinitiesType:
    cell_adhesion_affinity: list[
        CellAdhesionAffinitiesType.CellAdhesionAffinity
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class CellAdhesionAffinity:
        value: float = field()
        name: str = field(
            metadata={
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class CellPositionsType:
    folder: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    filename: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class ChemotacticSensitivitiesType:
    chemotactic_sensitivity: list[
        ChemotacticSensitivitiesType.ChemotacticSensitivity
    ] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class ChemotacticSensitivity:
        value: float = field()
        substrate: str = field(
            metadata={
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class ChemotaxisType:
    enabled: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    substrate: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    direction: int = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CustomDataType:
    any_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass(kw_only=True)
class DirichletBctype:
    class Meta:
        name = "DirichletBCType"

    value: float = field()
    units: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DirichletOptionsType:
    boundary_value: list[DirichletOptionsType.BoundaryValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class BoundaryValue:
        value: float = field()
        id: str = field(
            metadata={
                "name": "ID",
                "type": "Attribute",
            }
        )
        enabled: None | bool = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class DistributionType:
    behavior: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    any_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    check_base: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DomainType:
    x_min: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    x_max: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    y_min: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    y_max: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    z_min: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    z_max: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dx: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dy: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dz: float = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    use_2_d: bool = field(
        metadata={
            "name": "use_2D",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class EnabledFlagType:
    enable: None | bool = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class EquilibriumDistanceType:
    value: float = field()
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    units: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MatFileRefType:
    filename: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: None | str = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class NamedRatesType:
    any_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass(kw_only=True)
class OptionsType:
    legacy_random_points_on_sphere_in_divide: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    virtual_wall_at_domain_edge: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    disable_automated_spring_adhesions: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    random_seed: int = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    mechanics_voxel_size: None | float = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class ParallelType:
    omp_num_threads: int = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class PhaseDurationsType:
    duration: list[PhaseDurationsType.Duration] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    units: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass(kw_only=True)
    class Duration:
        value: float = field()
        index: int = field(
            metadata={
                "type": "Attribute",
            }
        )
        fixed_duration: None | bool = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class PlotSubstrateType:
    substrate: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    colormap: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    min_conc: None | float | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_conc: None | float | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    limits: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RulesetType:
    folder: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    filename: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    protocol: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    format: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class UserParametersType:
    any_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass(kw_only=True)
class ValueWithUnits:
    value: float = field()
    units: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    description: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AdvancedChemotaxisType:
    enabled: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    normalize_each_gradient: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    chemotactic_sensitivities: ChemotacticSensitivitiesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CellIntegrityType:
    damage_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    damage_repair_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CellInteractionsType:
    apoptotic_phagocytosis_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    necrotic_phagocytosis_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    other_dead_phagocytosis_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    live_phagocytosis_rates: NamedRatesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    attack_rates: NamedRatesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    attack_damage_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    attack_duration: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    fusion_rates: NamedRatesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CellTransformationsType:
    transformation_rates: NamedRatesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CycleType:
    phase_durations: PhaseDurationsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    standard_asymmetric_division: None | AsymmetricDivisionType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    code: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DeathParametersType:
    unlysed_fluid_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    lysed_fluid_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cytoplasmic_biomass_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    nuclear_biomass_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    calcification_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    relative_rupture_volume: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class InitialConditionsType:
    cell_positions: None | CellPositionsType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class InitialParameterDistributionsType:
    distribution: list[DistributionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    enabled: None | bool = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MechanicsOptionsType:
    set_relative_equilibrium_distance: EquilibriumDistanceType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    set_absolute_equilibrium_distance: EquilibriumDistanceType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class MicroenvironmentOptionsType:
    calculate_gradients: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    track_internalized_substrates_in_each_agent: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    initial_condition: MatFileRefType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dirichlet_nodes: MatFileRefType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class OverallType:
    max_time: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    time_units: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    space_units: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dt_diffusion: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dt_mechanics: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dt_phenotype: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class PhysicalParameterSetType:
    diffusion_coefficient: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    decay_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class RulesetsType:
    ruleset: list[RulesetType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class SvgsaveType:
    class Meta:
        name = "SVGSaveType"

    interval: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    enable: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    plot_substrate: None | PlotSubstrateType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class SaveIntervalType:
    interval: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    enable: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class SubstrateSecretionType:
    secretion_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    secretion_target: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    uptake_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    net_export_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class VolumeType:
    total: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    fluid_fraction: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    nuclear: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    fluid_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cytoplasmic_biomass_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    nuclear_biomass_change_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    calcified_fraction: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    calcification_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    relative_rupture_volume: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class CellRulesType:
    rulesets: None | RulesetsType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    settings: None | object = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class DeathModelType:
    death_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    phase_durations: PhaseDurationsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    parameters: DeathParametersType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    code: None | int = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class MechanicsType:
    cell_cell_adhesion_strength: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_cell_repulsion_strength: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    relative_maximum_adhesion_distance: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_adhesion_affinities: CellAdhesionAffinitiesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    options: MechanicsOptionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    attachment_elastic_constant: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    attachment_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    detachment_rate: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    maximum_number_of_attachments: None | int = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class MotilityOptionsType:
    enabled: bool = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    use_2_d: bool = field(
        metadata={
            "name": "use_2D",
            "type": "Element",
            "namespace": "",
        }
    )
    chemotaxis: ChemotaxisType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    advanced_chemotaxis: AdvancedChemotaxisType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class SaveType:
    folder: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    full_data: SaveIntervalType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    svg: SvgsaveType = field(
        metadata={
            "name": "SVG",
            "type": "Element",
            "namespace": "",
        }
    )
    legacy_data: EnabledFlagType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class SecretionType:
    substrate: list[SubstrateSecretionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class SubstrateVariableType:
    physical_parameter_set: PhysicalParameterSetType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    initial_condition: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    dirichlet_boundary_condition: DirichletBctype = field(
        metadata={
            "name": "Dirichlet_boundary_condition",
            "type": "Element",
            "namespace": "",
        }
    )
    dirichlet_options: None | DirichletOptionsType = field(
        default=None,
        metadata={
            "name": "Dirichlet_options",
            "type": "Element",
            "namespace": "",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    units: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    id: None | int = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class DeathType:
    model: list[DeathModelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class MicroenvironmentSetupType:
    variable: list[SubstrateVariableType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    options: MicroenvironmentOptionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class MotilityType:
    speed: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    persistence_time: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    migration_bias: ValueWithUnits = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    options: MotilityOptionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(kw_only=True)
class PhenotypeType:
    cycle: CycleType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    death: DeathType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    volume: VolumeType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    mechanics: MechanicsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    motility: MotilityType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    secretion: SecretionType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_interactions: CellInteractionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_transformations: CellTransformationsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_integrity: None | CellIntegrityType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class CellDefinitionType:
    phenotype: PhenotypeType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    custom_data: None | CustomDataType = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    initial_parameter_distributions: (
        None | InitialParameterDistributionsType
    ) = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    id: int = field(
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class CellDefinitionsType:
    cell_definition: list[CellDefinitionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class PhysiCellSettings:
    class Meta:
        name = "PhysiCell_settings"

    domain: DomainType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    overall: OverallType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    parallel: ParallelType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    save: SaveType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    options: OptionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    microenvironment_setup: MicroenvironmentSetupType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_definitions: CellDefinitionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    initial_conditions: InitialConditionsType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    cell_rules: CellRulesType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    user_parameters: UserParametersType = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    version: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
