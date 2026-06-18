# Heading 1 (Configuration management module)
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, List
from OmniPhysiBoSS.utils.logger import get_custom_logger

logger = get_custom_logger(__name__)


class ConfigurationManager:
    """Manages multi-scale model configuration environments by tracking execution

    directories, detecting existing PhysiCell/MaBoSS setups, and exposing a
    mapped parameter abstraction layer through the lib_loc interface.
    """

    def __init__(self, target_directory: str | Path, create_model_directory: False) -> None:
        """Initialize the manager and validate the target deployment directory.

        :param target_directory: Local file system path to the model directory.
        :type target_directory: str
        :param create_model_directory: Flag for creating folder at given location (instantiate new model)
        :type create_model_directory: bool
        :raises FileNotFoundError: If the specified directory does not exist.
        """
        # Directory state verification
        ## Convert string input to standard Path abstraction
        self.directory_path = Path(target_directory)

        ## Enforce strict directory existence checks
        ### Verify path existence and handle directory creation logic
        if not self.directory_path.exists():
            logger.error("Target configuration directory does not exist: %s", self.directory_path)
        
            #### case: user craetes new model
            if create_model_directory:
                try:
                    self.directory_path.mkdir(parents=True, exist_ok=True)
                    logger.info("Successfully created directory: %s", self.directory_path)
                except OSError as e:
                    logger.error("Failed to create directory %s: %s", self.directory_path, e, exc_info=True)
                    raise
            #### case: user wants to find model (default)
            else:
                logger.error("Configuration directory creation disabled: %s", self.directory_path)
                raise FileNotFoundError(f"Configuration directory not found: {self.directory_path}")

        # Internal state tracking
        ## Initialize structured parameter mapping storage
        self.lib_loc: Dict[str, Dict[str, Any]] = {
            #TODO - to będzie aktualizowane)
            "simulation_settings": {},
            "output_settings": {},
            "space_time": {},
            "cell_definitions": {},
            "microenvironment": {}
        }
        
        ## Track raw state files discovered inside the target path
        self.detected_xml_files: List[Path] = []
        self.detected_maboss_files: List[Path] = []

        ## Execute automatic scanning of the verified path
        self._scan_target_directory()

    # Heading 2 (Directory exploratory operations)
    def _scan_target_directory(self) -> None:
        """Scan the target directory path to automatically inventory existing

        simulation configuration assets.
        """
        # Asset search loop
        ## Iterate over all standard files in the targeted environment
        for file_entry in self.directory_path.iterdir():
            if file_entry.is_file():
                ### Categorize configuration infrastructure by file extension
                if file_entry.suffix.lower() == ".xml":
                    self.detected_xml_files.append(file_entry)
                elif file_entry.suffix.lower() in [".cfg", ".bnd"]:
                    self.detected_maboss_files.append(file_entry)

        # Execution log feedback
        ## Notify user via logging subsystem about discovered workspace state
        if self.detected_xml_files or self.detected_maboss_files:
            logger.info(
                "Existing configuration files detected in workspace. XML count: %d, MaBoSS count: %d",
                len(self.detected_xml_files),
                len(self.detected_maboss_files)
            )
        else:
            logger.info("Clean execution environment identified. No legacy configuration files present.")

    # Heading 2 (High-level serialization operations)
    def load_configuration(self, xml_filename: str) -> None:
        """Load an existing PhysiCell XML configuration file and map parameters

        into the internal lib_loc registry.

        :param xml_filename: Name of the target XML file within the workspace.
        :type xml_filename: str
        :raises FileNotFoundError: If the explicit file name cannot be resolved.
        """
        # Target path composition
        ## Resolve explicit file system path
        full_xml_path = self.directory_path / xml_filename
        if not full_xml_path.exists():
            logger.error("Requested configuration file target missing: %s", full_xml_path)
            raise FileNotFoundError(f"Configuration file target not found: {full_xml_path}")

        # Parsing execution context
        try:
            ## Parse tree structure from physical disk file
            parsed_tree = ET.parse(str(full_xml_path))
            root = parsed_tree.getroot()
            
            ## Map low-level elements into high-level abstractions
            self._map_xml_to_lib_loc(root_element=root)
            logger.info("Successfully loaded and mapped file structure from: %s", xml_filename)
        except Exception as exception_context:
            ### Capture and log internal tree structural breaks
            logger.error("Failed to parse target XML file layout: %s", full_xml_path, exc_info=True)
            raise exception_context

    def save_configuration(self, output_filename: str) -> None:
        """Compile internal lib_loc updates back into a structural PhysiCell

        XML configuration output file.

        :param output_filename: Target name for the generated output file.
        :type output_filename: str
        """
        # Reconstruction environment setup
        ## Initialize fresh empty XML root node
        root = ET.Element("PhysiCell_settings", {"version": "devel-version"})
        
        # Serialization sequence
        ## Reconstruct tree nodes systematically from internal parameter maps
        self._map_lib_loc_to_xml(root_element=root)
        
        ## Write raw tracking stream to target path destination
        output_path = self.directory_path / output_filename
        tree = ET.ElementTree(root)
        
        try:
            ## Execute physical storage operations
            tree.write(str(output_path), encoding="utf-8", xml_declaration=True)
            logger.info("Successfully synchronized model parameters to file destination: %s", output_path)
        except Exception as exception_context:
            ### Capture write failures
            logger.error("Failed to save operational state to target path: %s", output_path, exc_info=True)
            raise exception_context

    # Heading 2 (Internal translation logic)
    def _map_xml_to_lib_loc(self, root_element: ET.Element) -> None:
        """Translate native XML nodes into structured dictionary properties within

        the lib_loc dictionary abstraction layer.

        :param root_element: The root element of the source XML tree.
        :type root_element: ET.Element
        """
        # Mapping implementation placeholder
        ## Extract simulation tracking attributes
        parallel_node = root_element.find("parallel")
        if parallel_node is not None:
            ### Map thread properties to correct mapping coordinate
            threads = parallel_node.find("omp_num_threads")
            if threads is not None:
                self.lib_loc["simulation_settings"]["omp_num_threads"] = int(threads.text or 1)

    def _map_lib_loc_to_xml(self, root_element: ET.Element) -> None:
        """Translate properties back from the internal lib_loc dictionary layer

        into concrete XML sub-elements.

        :param root_element: The target root element of the output XML tree.
        :type root_element: ET.Element
        """
        # Re-assembly block creation
        ## Compile simulation settings block if values are populated
        if self.lib_loc["simulation_settings"]:
            ### Construct parallel execution trees
            parallel = ET.SubElement(root_element, "parallel")
            threads_val = self.lib_loc["simulation_settings"].get("omp_num_threads", 1)
            threads_elem = ET.SubElement(parallel, "omp_num_threads")
            threads_elem.text = str(threads_val)