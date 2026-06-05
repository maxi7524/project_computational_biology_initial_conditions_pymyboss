import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union, Dict, Set, List

class PhysiCellAgentGenerator:
    """
    Builds a complete PhysiCell and PhysiBoSS XML configuration file from scratch
    and manages associated environment initialization and validation rules.
    """

    def __init__(self, model_name: str):
        """
        Initialize the configurator with a model name and base XML structure.

        :param model_name: Name of the multi-scale model.
        :type model_name: str
        """
        # Core initialization
        ## Establish root element and model identifiers
        self.model_name = model_name
        self.root = ET.Element("PhysiCell_settings", {"version": "devel-version"})
        self.tree = ET.ElementTree(self.root)
        
        # Internal state tracking
        ## Registers valid cell type names and IDs to perform structural cross-validation
        self.registered_cell_types: Dict[str, int] = {}
        self.registered_cell_ids: Set[int] = set()
        
        # Grid definition tracking
        ## Track whether the spatial domain has been explicitly initialized
        self.is_domain_initialized = False

        # Structural placeholders
        ## Pre-create top-level container nodes to maintain sequence constraints
        self.domain = ET.SubElement(self.root, "domain")
        self.overall = ET.SubElement(self.root, "overall")
        self.parallel = ET.SubElement(self.root, "parallel")
        self.save = ET.SubElement(self.root, "save")
        self.options = ET.SubElement(self.root, "options")
        self.microenvironment_setup = ET.SubElement(self.root, "microenvironment_setup")
        self.cell_definitions = ET.SubElement(self.root, "cell_definitions")
        self.initial_conditions = ET.SubElement(self.root, "initial_conditions")
        self.cell_rules = ET.SubElement(self.root, "cell_rules")
        self.user_parameters = ET.SubElement(self.root, "user_parameters")

    
    # ----------------------------------
    # 1. Global Simulation Controls & Execution Framework
    # ----------------------------------

    def set_overall_parameters(self, 
                               max_time: float, 
                               dt_diffusion: float, 
                               dt_mechanics: float, 
                               dt_phenotype: float, 
                               time_units: str = "min", 
                               space_units: str = "micron") -> None:
        """
        Configure the global execution time limits and multiscale step splits.

        :param max_time: Maximum simulation time bounds.
        :type max_time: float
        :param dt_diffusion: Continuum solver step size.
        :type dt_diffusion: float
        :param dt_mechanics: Agent mechanical interaction step size.
        :type dt_mechanics: float
        :param dt_phenotype: Discrete state machine execution step size.
        :type dt_phenotype: float
        :param time_units: Unit of time tracking, defaults to 'min'.
        :type time_units: str
        :param space_units: Spatial unit metric, defaults to 'micron'.
        :type space_units: str
        """
        # Node clearing
        ## Remove pre-existing sub-elements to support safe re-configurations
        for child in list(self.overall):
            self.overall.remove(child)

        # Value injection
        ## Appending explicit leaf nodes for physical parameters
        ET.SubElement(self.overall, "max_time", {"units": time_units}).text = str(max_time)
        ET.SubElement(self.overall, "time_units").text = time_units
        ET.SubElement(self.overall, "space_units").text = space_units
        ET.SubElement(self.overall, "dt_diffusion", {"units": time_units}).text = str(dt_diffusion)
        ET.SubElement(self.overall, "dt_mechanics", {"units": time_units}).text = str(dt_mechanics)
        ET.SubElement(self.overall, "dt_phenotype", {"units": time_units}).text = str(dt_phenotype)

    def set_parallel_parameters(self, omp_num_threads: int) -> None:
        """
        Set OpenMP shared-memory parallel execution thread constraints.

        :param omp_num_threads: Total system thread concurrency limit.
        :type omp_num_threads: int
        """
        # Thread management
        ## Purge existing elements and update execution width
        for child in list(self.parallel):
            self.parallel.remove(child)
        ET.SubElement(self.parallel, "omp_num_threads").text = str(omp_num_threads)

    def set_save_parameters(self, 
                            folder: str, 
                            full_data_interval: float, 
                            svg_interval: float,
                            enable_full: bool = True, 
                            enable_svg: bool = True) -> None:
        """
        Configure the data logging mechanics and output frequency rules.

        :param folder: Target folder for files.
        :type folder: str
        :param full_data_interval: Tracking interval for complete state metrics.
        :type full_data_interval: float
        :param svg_interval: Tracking interval for vector graphics snapshots.
        :type svg_interval: float
        :param enable_full: Toggle flag for numeric matrices, defaults to True.
        :type enable_full: bool
        :param enable_svg: Toggle flag for image canvases, defaults to True.
        :type enable_svg: bool
        """
        # Save setup
        ## Rebuild structured nested file persistence tracking schemas
        for child in list(self.save):
            self.save.remove(child)
            
        ET.SubElement(self.save, "folder").text = folder
        
        # Raw data node
        ## Inject full data matrix output criteria
        full_node = ET.SubElement(self.save, "full_data")
        ET.SubElement(full_node, "interval", {"units": "min"}).text = str(full_data_interval)
        ET.SubElement(full_node, "enable").text = str(enable_full).lower()
        
        # Canvas node
        ## Inject graphic matrix properties
        svg_node = ET.SubElement(self.save, "SVG")
        ET.SubElement(svg_node, "interval", {"units": "min"}).text = str(svg_interval)
        ET.SubElement(svg_node, "enable").text = str(enable_svg).lower()
        
        # Legacy node
        ## Append standard fallback configurations for full schema alignment
        legacy_node = ET.SubElement(self.save, "legacy_data")
        ET.SubElement(legacy_node, "enable").text = "false"

    def set_global_options(self, 
                           virtual_wall: bool = True, 
                           disable_springs: bool = False, 
                           random_seed: int = 0) -> None:
        """
        Configure internal processing flags and optimization triggers.

        :param virtual_wall: Toggle boundary force confinement field.
        :type virtual_wall: bool
        :param disable_springs: Toggle automation rules for mechanical linkages.
        :type disable_springs: bool
        :param random_seed: Seed coordinate vector for execution stochastics.
        :type random_seed: int
        """
        # Logic parameters execution
        ## Clear and write operational execution profiles
        for child in list(self.options):
            self.options.remove(child)
            
        ET.SubElement(self.options, "legacy_random_points_on_sphere_in_divide").text = "false"
        ET.SubElement(self.options, "virtual_wall_at_domain_edge").text = str(virtual_wall).lower()
        ET.SubElement(self.options, "disable_automated_spring_adhesions").text = str(disable_springs).lower()
        ET.SubElement(self.options, "random_seed").text = str(random_seed)

    # ----------------------------------
    # 2. Spatial Domains and Continuum Formulations
    # ----------------------------------

    def set_domain_parameters(self, 
                              x_min: float, x_max: float, 
                              y_min: float, y_max: float, 
                              z_min: float, z_max: float, 
                              dx: float, dy: float, dz: float, 
                              use_2D: bool = True) -> None:
        """
        Configure the continuous 3D/2D spatial simulation grid mapping domain bounds.

        :param x_min: Minimum x coordinate space boundary.
        :type x_min: float
        :param x_max: Maximum x coordinate space boundary.
        :type x_max: float
        :param y_min: Minimum y coordinate space boundary.
        :type y_min: float
        :param y_max: Maximum y coordinate space boundary.
        :type y_max: float
        :param z_min: Minimum z coordinate space boundary.
        :type z_min: float
        :param z_max: Maximum z coordinate space boundary.
        :type z_max: float
        :param dx: Voxel size step along the X tensor axis.
        :type dx: float
        :param dy: Voxel size step along the Y tensor axis.
        :type dy: float
        :param dz: Voxel size step along the Z tensor axis.
        :type dz: float
        :param use_2D: Enforce dimensional projection to a single plane, defaults to True.
        :type use_2D: bool
        """
        # Domain initialization clear
        ## Clear pre-existing child nodes to allow safely redefining grid tensors
        for child in list(self.domain):
            self.domain.remove(child)

        # Node coordinate assignment
        ## Structural injection of Cartesian box limit thresholds
        ET.SubElement(self.domain, "x_min").text = str(x_min)
        ET.SubElement(self.domain, "x_max").text = str(x_max)
        ET.SubElement(self.domain, "y_min").text = str(y_min)
        ET.SubElement(self.domain, "y_max").text = str(y_max)
        ET.SubElement(self.domain, "z_min").text = str(z_min)
        ET.SubElement(self.domain, "z_max").text = str(z_max)
        ET.SubElement(self.domain, "dx").text = str(dx)
        ET.SubElement(self.domain, "dy").text = str(dy)
        ET.SubElement(self.domain, "dz").text = str(dz)
        ET.SubElement(self.domain, "use_2D").text = str(use_2D).lower()
        
        # State updates
        ## Set validation tracking flag to true
        self.is_domain_initialized = True

    def add_microenvironment_substrate(self, 
                                       name: str, 
                                       diffusion_coefficient: float, 
                                       decay_rate: float, 
                                       initial_condition: float = 0.0) -> None:
        """
        Inject a chemical continuum tracking field governed by reaction-diffusion parameters.

        :param name: Unique name tag identifying the chemical substrate variable.
        :type name: str
        :param diffusion_coefficient: Substance physical spatial translation scalar metric.
        :type diffusion_coefficient: float
        :param decay_rate: Fluid continuum clearance rate metric.
        :type decay_rate: float
        :param initial_condition: Uniform basal initial concentration, defaults to 0.0.
        :type initial_condition: float
        """
        # Element structural search
        ## Locate options block inside microenvironment tree or initialize standard fallbacks
        options_node = self.microenvironment_setup.find("options")
        if options_node is None:
            options_node = ET.Element("options")
            ## Default options properties setup
            ET.SubElement(options_node, "calculate_gradients").text = "true"
            ET.SubElement(options_node, "track_internalized_substrates_in_each_agent").text = "true"
        else:
            self.microenvironment_setup.remove(options_node)

        # Variable duplication management
        ## Prevent duplicated chemical entity entries within the continuum system tree
        for var in self.microenvironment_setup.findall("variable"):
            if var.get("name") == name:
                self.microenvironment_setup.remove(var)

        # Substrate definition building
        ## Establish sequence IDs based on active count metrics
        sub_id = len(self.microenvironment_setup.findall("variable"))
        var_node = ET.SubElement(self.microenvironment_setup, "variable", {
            "name": name,
            "units": "dimensionless",
            "ID": str(sub_id)
        })

        # Physical constants encapsulation
        ## Structuring nested PDE parameter trees
        param_set = ET.SubElement(var_node, "physical_parameter_set")
        ET.SubElement(param_set, "diffusion_coefficient", {"units": "micron^2/min"}).text = str(diffusion_coefficient)
        ET.SubElement(param_set, "decay_rate", {"units": "1/min"}).text = str(decay_rate)
        ET.SubElement(var_node, "initial_condition", {"units": "mmHg"}).text = str(initial_condition)
        
        # Boundary initialization defaults
        ## Append standard fallback configurations for Dirichlet boundary trees
        ET.SubElement(var_node, "Dirichlet_boundary_condition", {"units": "mmHg", "enabled": "False"}).text = "0"

        # Tree restructuring
        ## Append options at the final terminal node index sequence position
        self.microenvironment_setup.append(options_node)


    # ----------------------------------
    # 3. Agent Archetypes and Phenotypic Blueprints
    # ----------------------------------

    def register_allowed_cell_type(self, type_name: str, type_id: int) -> None:
        """
        Explicitly pre-register a cell functional lineage to validate configuration consistency.

        :param type_name: Unique identification string label for the cell lineage.
        :type type_name: str
        :param type_id: Unique integer index assigned to the lineage matrix.
        :type type_id: int
        :raises ValueError: If the type name or ID violates uniqueness constraints.
        """
        # Cross validation operations
        ## Check uniqueness tracking properties across existing registries
        if type_name in self.registered_cell_types:
            raise ValueError(f"Cell type name '{type_name}' has already been registered.")
        if type_id in self.registered_cell_ids:
            raise ValueError(f"Cell type ID '{type_id}' has already been registered.")

        # Registry updates
        ## Save markers to local structural tracking sets
        self.registered_cell_types[type_name] = type_id
        self.registered_cell_ids.add(type_id)

        # Base node setup
        ## Initialize empty archetype element container structures under cell_definitions
        cell_def = ET.SubElement(self.cell_definitions, "cell_definition", {
            "name": type_name,
            "ID": str(type_id)
        })
        # Structural initialization
        ## Build base container placeholders for modular phenotypic data injections
        ET.SubElement(cell_def, "phenotype")
        ET.SubElement(cell_def, "custom_data")