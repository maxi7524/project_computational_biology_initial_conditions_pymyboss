# Heading 1 (Broad context / Top-level block / Script section)
# Robust functional metadata enrichment engine with direct database ontology cross-references.

import os
from typing import Dict, Any, List, Set
import pandas as pd
import mudata as mu
import pronto

from ...utils.logger import get_custom_logger


logger = get_custom_logger(__name__)

class CellTypeMetadataEnricher:
    """
    Processes flattened biological lineage registries to discover linked Gene Ontology 
    terms by anchoring lookups directly on verified unique cellontology_id keys.
    """

    def _normalize_cell_name(self, name: str) -> str:
        """
        Normalize cell type strings to maximize singular-form OBO matching hits.

        :param name: Raw cell name string.
        :type name: str
        :return: Normalized cell name string.
        :rtype: str
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Text canonicalization transformation workflows
        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Strip plural trailing characters and lower-case tokens
        
        norm = name.lower().strip()
        norm = norm.replace("cells", "").replace("cell", "").strip()
        if norm == "nk":
            return "natural killer"
        return norm

    def enrich_metadata_dataframe(
        self, 
        mdata: mu.MuData, 
        flat_lineage_registry: Dict[str, Any], 
        cl_ontology_path: str = 'resources/databases/go-basic.obo',
        uns_output_key: str = "cell_types_metadata_df"
    ) -> None:
        """
        Query the Gene Ontology structure by mapping the explicit cellontology_id 
        to discover linked GO terms, injecting the resulting dataframe into mdata.uns.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param flat_lineage_registry: Streamlined extraction dictionary containing flattened cluster annotations.
        :type flat_lineage_registry: Dict[str, Any]
        :param cl_ontology_path: Filesystem trajectory pointing to the target go-basic.obo file.
        :type cl_ontology_path: str
        :param uns_output_key: Objective matrix identifier key within the mdata.uns dictionary.
        :type uns_output_key: str
        :raises KeyError: If the mandatory 'rna' modality sub-container is missing.
        :raises FileNotFoundError: If the specified ontology path cannot be resolved or parsed.
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural data schema validation and ontology ingestion
        
        logger.info("Starting structural Gene Ontology parsing via pronto interface.")
        
        if 'rna' not in mdata.mod:
            logger.error("Enrichment workflow aborted. Modality layer 'rna' missing from path context.", exc_info=True) 
            raise KeyError("Missing 'rna' modality container inside MuData object.")

        if not os.path.exists(cl_ontology_path):
            logger.error("Target ontology file missing at path: %s", cl_ontology_path, exc_info=True) 
            raise FileNotFoundError(f"Ontology file tracking reference not found: {cl_ontology_path}")

        ## Load and parse the structured OBO graph layout safely
        
        logger.debug("Loading ontology graph definitions from source trajectory: %s", cl_ontology_path)
        cl_ontology = pronto.Ontology(cl_ontology_path)
        logger.info("Ontology loaded successfully. Total terms parsed: %d", len(cl_ontology))
        
        dataframe_records: List[Dict[str, Any]] = []

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Iterate over flattened entries to perform exact ontology term transformations
        for cluster_id, attributes in flat_lineage_registry.items():
            cell_type_name = str(attributes["cell_type_name"])
            cell_count = int(attributes["cell_count"])
            explicit_cl_id = str(attributes["cellontology_id"])
            meta_context = attributes.get("metadata_context", {})
            confidence_score = float(attributes.get("confidence_score", 1.0))
            
            matched_cl_id = explicit_cl_id if explicit_cl_id != "NaN" else "CL:UNKNOWN"
            matched_definition = "No ontology definition available."
            associated_go_terms: Set[str] = set()

            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Scan entire Gene Ontology database to isolate terms linked to target cellontology_id
            if explicit_cl_id and explicit_cl_id not in ["NaN", "CL:UNKNOWN"]:
                logger.info("Cluster %s: Scanning GO structures for explicit cellontology_id: %s", str(cluster_id), explicit_cl_id)
                
                for term in cl_ontology.terms():
                    is_linked = False
                    
                    # Inspect cross-references for the target Cell Ontology identifier
                    
                    if term.xrefs:
                        for xref in term.xrefs:
                            if explicit_cl_id in xref.id:
                                is_linked = True
                                break
                                
                    # Inspect relationship blocks for mapped graph connections
                    
                    if not is_linked and term.relationships:
                        for rel, related_terms in term.relationships.items():
                            for rel_term in related_terms:
                                if rel_term.id == explicit_cl_id:
                                    is_linked = True
                                    break
                            if is_linked:
                                break
                                
                    if is_linked and "GO:" in term.id:
                        associated_go_terms.add(term.id)

            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Execute fallback string normalization query if no direct GO relationships are found
            if not associated_go_terms:
                query = self._normalize_cell_name(cell_type_name)
                logger.debug("Executing name fallback string matching for query: %s", query)
                
                for term in cl_ontology.terms():
                    if not term.name:
                        continue
                    
                    term_name_norm = term.name.lower().replace("cell", "").strip() 
                    is_match = (query == term_name_norm) or (query in term_name_norm and len(query) > 3) 

                    if is_match and "GO:" in term.id:
                        associated_go_terms.add(term.id)
                        if term.definition:
                            matched_definition = str(term.definition) 

            go_terms_payload = ",".join(sorted(list(associated_go_terms))) if associated_go_terms else "None" 
            
            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Compile full context parameters from both CellMarker 2.0 layers and pronto records
            record = {
                "cluster_id": str(cluster_id),
                "cell_type_name": cell_type_name,
                "cell_count": cell_count,
                "cell_ontology_id": matched_cl_id,
                "uberon_ontology_id": str(meta_context.get("uberonontology_id", "NaN")), 
                "tissue_class": str(meta_context.get("tissue_class", "NaN")), 
                "tissue_type": str(meta_context.get("tissue_type", "NaN")), 
                "cancer_type": str(meta_context.get("cancer_type", "NaN")), 
                "marker_source": str(meta_context.get("marker_source", "NaN")), 
                "pmid": str(meta_context.get("pmid", "NaN")), 
                "ontology_definition": matched_definition,
                "associated_go_annotations": go_terms_payload,
                "source_database": "CellMarker2.0_Direct_Ontology_Resolution",
                "confidence_score": confidence_score
            }
            dataframe_records.append(record)

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Construct the target pandas dataframe and link to multi-modal object space
        
        metadata_df = pd.DataFrame(dataframe_records)
        metadata_df.set_index("cluster_id", inplace=True)

        if not isinstance(mdata.uns, dict):
            mdata.uns = dict(mdata.uns) 

        mdata.uns[uns_output_key] = metadata_df
        mdata.update() 
        logger.info("Metadata registration payload injected into mdata.uns['%s'] slot completed.", uns_output_key) 