# =============================================================================
# OmniPath Database Management Component Implementation
# =============================================================================

import mudata as mu
import pandas as pd
import liana as li
from typing import Any, Dict, Optional
from ...base import ModelComponent


# TODO it treats all ligand -> receptor as activatros !!! 

class InteractionTypeIdentifier(ModelComponent):
    """
    Component responsible for fetching, filtering, and structural formatting
    of signed directed intracellular interaction networks from OmniPath.
    """

    def __init__(self) -> None:
        """
        Constructor method initialization.
        """
        # Internal parameter and registry allocation
        ## Initialize dataframe containers tracking formal signed edgelists
        self.raw_resource: Optional[pd.DataFrame] = None
        self.signed_edgelist: Optional[pd.DataFrame] = None

    def extract_from_data(
        self, 
        source_data: mu.MuData, 
        resource_name: str = "consensus"
    ) -> None:
        """
        Query the LIANA database registry to pull raw intracellular networks.

        :param source_data: High-dimensional multi-modal container asset.
        :type source_data: mu.MuData
        :param resource_name: Target registry identifier (use 'consensus' for pathways), defaults to "consensus".
        :type resource_name: str
        """
        # Database query phase
        ## Fetch unified consensus dataframe containing regulatory records
        print(f"[-] InteractionTypeIdentifier: Fetching intracellular pathway network '{resource_name}'...")
        self.raw_resource = li.rs.select_resource(resource_name=resource_name)
        print(f"[✓] InteractionTypeIdentifier: Successfully cached {self.raw_resource.shape[0]} raw database entries.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize processed signed interactions into a standard dictionary tree.

        :return: Hierarchical dictionary containing the compiled signed edge data.
        :rtype: Dict[str, Any]
        """
        return {
            "signed_edgelist": self.signed_edgelist.to_dict(orient="records") if self.signed_edgelist is not None else []
        }

    def __call__(
        self, 
        source_column: str = "ligand",
        target_column: str = "receptor"
    ) -> Dict[str, Any]:
        """
        Execute transition rules to convert biological records to a signed mathematical graph.

        :param source_column: Header index key tracking source entities, defaults to "ligand".
        :type source_column: str
        :param target_column: Header index key tracking target entities, defaults to "receptor".
        :type target_column: str
        :return: Serialized dictionary payload tracking formalized network edges.
        :rtype: Dict[str, Any]
        """
        # Boundary validation check
        if self.raw_resource is None:
            print("[!] Critical: No database entries cached. Execute extract_from_data first.")
            return self.to_dict()

        # Structural compilation phase
        print("[-] Reconstructing raw interaction records into signed directed graph topologies...")
        processing_df = self.raw_resource.copy()

        # Fallback column nomenclature resolution
        if source_column not in processing_df.columns or target_column not in processing_df.columns:
            source_column = "source" if "source" in processing_df.columns else source_column
            target_column = "target" if "target" in processing_df.columns else target_column

        # Mathematical sign conversion loop
        processing_df["sign"] = 0

        # Parse activation and inhibition tracking flags from OmniPath structure
        if "is_stimulation" in processing_df.columns and "is_inhibition" in processing_df.columns:
            print("[-] Decoupling causal mechanisms from 'is_stimulation' and 'is_inhibition' fields...")
            
            ### Set stimulation events to positive unity constants
            stimulation_mask = (processing_df["is_stimulation"] == 1) & (processing_df["is_inhibition"] == 0)
            processing_df.loc[stimulation_mask, "sign"] = 1
            
            ### Set inhibition events to negative unity constants
            inhibition_mask = (processing_df["is_stimulation"] == 0) & (processing_df["is_inhibition"] == 1)
            processing_df.loc[inhibition_mask, "sign"] = -1
        else:
            print("[!] Warning: Missing signaling flags. Enforcing default activation signs.")
            processing_df["sign"] = 1

        # Causal network filtering step
        ## Drop ambiguous, unsigned, or conflicting rows
        filtered_df = processing_df[processing_df["sign"] != 0].copy()

        # Final structural matrix compilation
        self.signed_edgelist = filtered_df[[source_column, target_column, "sign"]].dropna()
        self.signed_edgelist.columns = ["source", "target", "sign"]
        
        ## Deduplicate rows to prevent parallel constraint injection faults
        self.signed_edgelist = self.signed_edgelist.drop_duplicates().reset_index(drop=True)

        print(f"[✓] Completed sign conversion. Retained {self.signed_edgelist.shape[0]} signed directed edges.")
        return self.to_dict()