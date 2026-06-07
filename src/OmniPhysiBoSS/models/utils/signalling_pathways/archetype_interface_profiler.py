# =============================================================================
# Archetype Interface Profiler Component Implementation
# =============================================================================

import anndata
import mudata as mu
import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional
from ...base import ModelComponent


class ArchetypeInterfaceProfiler(ModelComponent):
    """
    Component responsible for isolating significant ligand and receptor interfaces
    per cell type archetype by intersecting spatial communication scores with expression data.
    """

    def __init__(self) -> None:
        """
        Constructor method initialization.
        """
        # Internal parameter and registry allocation
        ## Initialize dictionaries tracking identified interfaces across cellular categories
        self.cell_type_interfaces: Dict[str, Dict[str, List[str]]] = {}
        self.liana_results: Optional[anndata.AnnData] = None
        self.deconvoluted_counts: Optional[pd.DataFrame] = None

    def extract_from_data(
        self, 
        source_data: mu.MuData, 
        liana_uns_key: str = "liana_res"
    ) -> None:
        """
        Parse multimodal structures using automatic modality discovery constraints.

        :param source_data: High-dimensional pre-harmonized MuData container asset.
        :type source_data: mu.MuData
        :param liana_uns_key: Target key under .uns where LIANA AnnData is stored, defaults to "liana_res".
        :type liana_uns_key: str
        :raises ValueError: If the required mandatory 'rna' layer is missing from the container.
        """
        # Dynamic modality scanning phase
        ## Inspect container keys to verify execution constraints
        available_modalities = list(source_data.mod.keys())
        
        ## Enforce that the primary transcription axis exists as a mandatory requirement
        if "rna" not in available_modalities:
            raise ValueError("Mandatory error: Required core modality 'rna' missing from MuData.")

        # Extract underlying data structures
        ## Access the primary transcription tracking registry
        rna_adata = source_data["rna"]

        if liana_uns_key not in source_data.uns and liana_uns_key not in rna_adata.uns:
            raise KeyError(f"Spatial results token '{liana_uns_key}' not found in MuData or rna registries.")

        # Resolve exact registry positioning for the bivariate AnnData object
        if liana_uns_key in source_data.uns:
            self.liana_results = source_data.uns[liana_uns_key]
        else:
            self.liana_results = rna_adata.uns[liana_uns_key]
        
        # Handle supplementary cell type deconvolution layer mapping if present
        if "ct" in available_modalities:
            ct_adata = source_data["ct"]
            if isinstance(ct_adata.X, np.ndarray):
                self.deconvoluted_counts = pd.DataFrame(
                    ct_adata.X, 
                    index=ct_adata.obs_names, 
                    columns=ct_adata.var_names
                )
            else:
                self.deconvoluted_counts = pd.DataFrame(
                    ct_adata.X.toarray(), 
                    index=ct_adata.obs_names, 
                    columns=ct_adata.var_names
                )
            print(f"[✓] ArchetypeInterfaceProfiler: Automatically aligned 'ct' layer. Cells: {self.deconvoluted_counts.shape[0]}.")
        else:
            self.deconvoluted_counts = None
            print("[!] Warning: Modality 'ct' missing. Slicing unmapped global targets.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize isolated cellular interfaces into a standard dictionary framework.

        :return: Hierarchical dictionary containing cell-type specific ligands and receptors.
        :rtype: Dict[str, Any]
        """
        return {
            "cell_type_interfaces": self.cell_type_interfaces
        }

    def __call__(
        self, 
        top_n_interactions: int = 30, 
        min_prop: float = 0.10,
        min_pvalue: float = 0.05,
        ligand_column: str = "ligand",
        receptor_column: str = "receptor"
    ) -> Dict[str, Any]:
        """
        Execute the step-by-step filtering workflow to extract top interfaces per cell type.

        :param top_n_interactions: Number of high-confidence spatial rows to consider, defaults to 30.
        :type top_n_interactions: int
        :param min_prop: Minimum expression breadth ratio for entity filtering, defaults to 0.10.
        :type min_prop: float
        :param min_pvalue: Upper boundary alpha threshold for permutation tests significance, defaults to 0.05.
        :type min_pvalue: float
        :param ligand_column: Header index key tracking ligands in LIANA .var dataframe, defaults to "ligand".
        :type ligand_column: str
        :param receptor_column: Header index key tracking receptors in LIANA .var dataframe, defaults to "receptor".
        :type receptor_column: str
        :return: Serialized dictionary mapping cell archetypes to their critical boundary elements.
        :rtype: Dict[str, Any]
        """
        # Clear historic state configurations
        self.cell_type_interfaces = {}

        # Boundary validation check
        if self.liana_results is None:
            print("[!] Critical: No data cached. Execute extract_from_data before computation loops.")
            return self.to_dict()

        # Isolate metadata dataframe from cached AnnData workspace
        liana_var_df = self.liana_results.var

        # Statistical significance validation phase (Permutation tests verification)
        ## Check if permutation testing was executed by looking for target p-value columns
        target_p_col = None
        if "pvals_adj" in liana_var_df.columns:
            target_p_col = "pvals_adj"
        elif "pvals" in liana_var_df.columns:
            target_p_col = "pvals"

        ## Hard abort constraint: if no permutation test metrics exist, raise ValueError and prevent execution
        if target_p_col == None:
            raise ValueError(
                "Execution Aborted: Permutation significance testing data missing in LIANA object. "
                "Ensure 'n_perms' parameter was explicitly defined and calculated within the bivariate pipeline."
            )

        # Filtering statistically significant rows
        ## Slice array to contain only pairs within the trusted confidence threshold bounds
        print(f"[-] Slicing significant vectors using permutation metric '{target_p_col}' <= {min_pvalue}...")
        significant_liana = liana_var_df[liana_var_df[target_p_col] <= min_pvalue]

        # Isolate and sort the highest-ranking spatial communication vectors
        print(f"[-] Filtering top {top_n_interactions} spatially active interaction pairs from significant rows...")
        if "mean" in significant_liana.columns:
            sorted_liana = significant_liana.sort_values(by="mean", ascending=False)
        else:
            sorted_liana = significant_liana
            
        top_interactions = sorted_liana.head(top_n_interactions)

        # Fallback handling for cases where deconvolution counts are missing
        if self.deconvoluted_counts is None:
            ## Return unmapped global top interactions vectors under placeholder category
            self.cell_type_interfaces["global_unmapped"] = {
                "ligands": sorted(top_interactions[ligand_column].dropna().unique().tolist()),
                "receptors": sorted(top_interactions[receptor_column].dropna().unique().tolist())
            }
            print("[✓] Finished mapping under fallback global placeholder array.")
            return self.to_dict()

        # Cell archetype cross-referencing loop
        cell_types = self.deconvoluted_counts.columns.tolist()

        for cell_type in cell_types:
            self.cell_type_interfaces[cell_type] = {
                "ligands": [],
                "receptors": []
            }

            for _, row in top_interactions.iterrows():
                # Extract structural node keys
                ligand_node = str(row[ligand_column])
                receptor_node = str(row[receptor_column])

                # Check ligand presence constraints
                if "ligand_props" in row and float(row["ligand_props"]) >= min_prop:
                    if ligand_node not in self.cell_type_interfaces[cell_type]["ligands"]:
                        self.cell_type_interfaces[cell_type]["ligands"].append(ligand_node)

                # Check receptor presence constraints
                if "receptor_props" in row and float(row["receptor_props"]) >= min_prop:
                    if receptor_node not in self.cell_type_interfaces[cell_type]["receptors"]:
                        self.cell_type_interfaces[cell_type]["receptors"].append(receptor_node)

            print(f"    -> Aligned Archetype '{cell_type}': Isolated {len(self.cell_type_interfaces[cell_type]['ligands'])} ligands, "
                  f"{len(self.cell_type_interfaces[cell_type]['receptors'])} receptors.")

        print("[✓] Interface isolation completed successfully across all distinct categories.")
        return self.to_dict()