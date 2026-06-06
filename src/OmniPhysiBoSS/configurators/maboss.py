from pathlib import Path
from typing import Dict, Union, Any

class MaBoSSModelConfigurator:
    """
    Configures validated MaBoSS network topology (.bnd) and configuration (.cfg)
    files based on signaling pathway definitions with strict syntactic checks.
    """

    # Valid global parameters and their expected types according to MaBoSS documentation
    VALID_ENGINE_PARAMS = {
        "sample_count": int,
        "max_time": (int, float),
        "time_tick": float,
        "discrete_time": int,
        "use_physrandgen": bool,
        "seed_pseudorandom": int,
        "display_traj": bool,
        "thread_count": int,
        "statdist_traj_count": int,
        "statdist_cluster_threshold": float
    }

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.nodes = {}
        self.engine_parameters = {}
        self.global_variables = {}

    @property
    def valid_engine_params(self):
        return self.VALID_ENGINE_PARAMS.copy()

    def _validate_and_translate_logic(self, logic_expression: str) -> str:
        """
        Validates the logic expression and translates word operators to MaBoSS tokens.
        """
        # Dictionary mapping for allowed words to MaBoSS symbols
        translation = {
            " AND ": " & ",
            " OR ": " | ",
            "NOT ": " ! "
        }
        
        translated = logic_expression
        for word, token in translation.items():
            translated = translated.replace(word, token)
            
        # Strict validation of allowed characters in MaBoSS logic expressions
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_()&|!@$? \t\n.:><=+-*/,")
        invalid_chars = set(translated) - allowed_chars
        if invalid_chars:
            raise ValueError(f"Unsupported characters or operators found in logic expression: {invalid_chars}")
            
        return translated

    def add_node(self, 
                 node_name: str, 
                 logic_expression: str, 
                 istate: Union[bool, float] = 0.5, 
                 is_internal: bool = False,
                 rate_up: str = "1.0", 
                 rate_down: str = "1.0") -> None:
        """
        Add a boolean node with its transition rule, kinetic rates, and properties.
        """
        # Handler 
        ## Validate istate range
        if isinstance(istate, bool):
            istate_val = 1.0 if istate else 0.0
        elif isinstance(istate, (int, float)):
            if not (0.0 <= istate <= 1.0):
                raise ValueError(f"istate for node {node_name} must be within [0, 1] interval. Got: {istate}")
            istate_val = float(istate)
        else:
            raise TypeError(f"Invalid type for istate: {type(istate)}")

        validated_logic = self._validate_and_translate_logic(logic_expression)
        validated_rate_up = self._validate_and_translate_logic(rate_up)
        validated_rate_down = self._validate_and_translate_logic(rate_down)

        self.nodes[node_name] = {
            "logic": validated_logic,
            "istate": istate_val,
            "is_internal": is_internal,
            "rate_up": validated_rate_up,
            "rate_down": validated_rate_down
        }

    def set_engine_parameter(self, param_name: str, value: Any) -> None:
        """
        Set and validate global simulation configurations for the MaBoSS engine.
        """
        if param_name not in self.VALID_ENGINE_PARAMS:
            raise KeyError(f"Parameter '{param_name}' is not a valid MaBoSS engine configuration option.")
            
        expected_type = self.VALID_ENGINE_PARAMS[param_name]
        if not isinstance(value, expected_type):
            raise TypeError(f"Parameter '{param_name}' must be of type {expected_type}. Got {type(value)}")
            
        self.engine_parameters[param_name] = value

    def set_global_variable(self, var_name: str, value: Union[bool, float, int]) -> None:
        """
        Set global variables (prefixed with $) used inside rate equations.
        """
        if not var_name.startswith("$"):
            raise ValueError(f"Global variables in MaBoSS must begin with '$'. Got: {var_name}")
            
        if isinstance(value, bool):
            self.global_variables[var_name] = "TRUE" if value else "FALSE"
        else:
            self.global_variables[var_name] = str(value)

    def write_model(self, output_dir: str = ".") -> None:
        """
        Generate both validated .bnd and .cfg files on the file system.
        """
        # Parameters
        ## Paths 
        base_path = Path(output_dir) / self.model_name
        bnd_path = base_path.with_suffix(".bnd")
        cfg_path = base_path.with_suffix(".cfg")

        # Files generation
        ## Generation of the structural .bnd file
        with open(bnd_path, "w", encoding="utf-8") as bnd_file:
            for node, data in self.nodes.items():
                bnd_file.write(f"Node {node} {{\n")
                bnd_file.write(f"    logic = {data['logic']};\n")
                bnd_file.write(f"    rate_up = {data['rate_up']};\n")
                bnd_file.write(f"    rate_down = {data['rate_down']};\n")
                bnd_file.write("}\n\n")

        ## Generation of the configuration .cfg file
        with open(cfg_path, "w", encoding="utf-8") as cfg_file:
            ### Write global variables ($Variables) first
            for var, val in self.global_variables.items():
                cfg_file.write(f"{var} = {val};\n")
            cfg_file.write("\n")
            
            ### Write initial states and internal flags for nodes
            for node, data in self.nodes.items():
                cfg_file.write(f"[{node}].istate = {data['istate']};\n")
                if data['is_internal']:
                    cfg_file.write(f"{node}.is_internal = TRUE;\n")
            
            cfg_file.write("\n")
            ### Write validated engine parameters
            for param, val in self.engine_parameters.items():
                if isinstance(val, bool):
                    val_str = "TRUE" if val else "FALSE"
                else:
                    val_str = str(val)
                cfg_file.write(f"{param} = {val_str};\n")

        print(f"Successfully saved MaBoSS model files:\n - {bnd_path.absolute()}\n - {cfg_path.absolute()}")