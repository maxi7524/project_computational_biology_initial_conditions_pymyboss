# Heading 1 (Broad context / Top-level block / Script section)
# Scentralizowany system rejestracji komponentów dla pakietu OmniPhysiBoSS

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type, Callable, Any
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


class CentralRegistry:
    """
    Unified architectural registry executing strategy binding via decorators
    and forcing package discovery across computational subdomains.
    """

    def __init__(self) -> None:
        """Initialize independent state dictionaries for each mathematical domain."""
        self._cell_types_registry: Dict[str, Type[Any]] = {}
        self._networks_registry: Dict[str, Type[Any]] = {}
        self._kinetics_registry: Dict[str, Type[Any]] = {}

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Decorator methods for compilation binding
    def register_cell_type(self, name: str) -> Callable[[Type[Any]], Type[Any]]:
        """
        Register a structural cell types aggregation strategy.

        :param name: Unique identifier for the strategy.
        :type name: str
        :return: Wrapped registration target class.
        :rtype: Callable[[Type[Any]], Type[Any]]
        """
        def decorator(cls: Type[Any]) -> Type[Any]:
            self._cell_types_registry[name] = cls
            logger.debug("Registered cell type strategy: %s", name)
            return cls
        return decorator

    def register_network(self, name: str) -> Callable[[Type[Any]], Type[Any]]:
        """
        Register a logical network translation strategy.

        :param name: Unique identifier for the strategy.
        :type name: str
        :return: Wrapped registration target class.
        :rtype: Callable[[Type[Any]], Type[Any]]
        """
        def decorator(cls: Type[Any]) -> Type[Any]:
            self._networks_registry[name] = cls
            logger.debug("Registered network logic strategy: %s", name)
            return cls
        return decorator

    def register_kinetics(self, name: str) -> Callable[[Type[Any]], Type[Any]]:
        """
        Register a kinetic parameterization strategy.

        :param name: Unique identifier for the strategy.
        :type name: str
        :return: Wrapped registration target class.
        :rtype: Callable[[Type[Any]], Type[Any]]
        """
        def decorator(cls: Type[Any]) -> Type[Any]:
            self._kinetics_registry[name] = cls
            logger.debug("Registered kinetic scaling strategy: %s", name)
            return cls
        return decorator

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Resolution methods for factory generation
    def get_cell_type_strategy(self, name: str) -> Type[Any]:
        """Resolve cell type strategy class or raise KeyError."""
        if name not in self._cell_types_registry:
            ### Handle missing runtime configuration mappings
            raise KeyError(f"Cell type strategy '{name}' is not registered.")
        return self._cell_types_registry[name]

    def get_network_strategy(self, name: str) -> Type[Any]:
        """Resolve network strategy class or raise KeyError."""
        if name not in self._networks_registry:
            raise KeyError(f"Network strategy '{name}' is not registered.")
        return self._networks_registry[name]

    def get_kinetics_strategy(self, name: str) -> Type[Any]:
        """Resolve kinetic strategy class or raise KeyError."""
        if name not in self._kinetics_registry:
            raise KeyError(f"Kinetic strategy '{name}' is not registered.")
        return self._kinetics_registry[name]

    ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
    ## Package auto-discovery logic
    def discover_strategies(self, base_models_path: Union[str, Path]) -> None:
        """
        Programmatically walk through subdirectories to force execution of registration decorators.

        :param base_models_path: Absolute or relative path to the models/ domain root.
        :type base_models_path: Union[str, Path]
        """
        base_path = Path(base_models_path)
        subdomains = ["cell_types", "networks", "kinetics"]

        for domain in subdomains:
            strategies_path = base_path / domain / "strategies"
            if not strategies_path.exists():
                ### Skip uninitialized computational subdomains
                continue

            logger.info("Discovering strategies inside: %s", strategies_path)
            
            for _, module_name, _ in pkgutil.iter_modules([str(strategies_path)]):
                full_module_path = f"OmniPhysiBoSS.models.{domain}.strategies.{module_name}"
                try:
                    ### Force runtime execution of the module file to trigger the decorator
                    importlib.import_module(full_module_path)
                except Exception as e:
                    ### Log trace failures inside try-except execution contexts
                    logger.error("Failed to dynamically import module: %s", full_module_path, exc_info=True)


# Instancjonowanie globalnego, scentralizowanego rejestru dostępnego dla całego pakietu
models_registry = CentralRegistry()