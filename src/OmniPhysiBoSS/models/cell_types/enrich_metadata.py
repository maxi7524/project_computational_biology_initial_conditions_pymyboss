# Heading 1 (Broad context / Top-level block / Script section)
# Quantitative functional metadata enrichment and ontologized gene parameter mining engine.

import os
from typing import Dict, Any, List, Set
import pandas as pd
import mudata as mu
import pronto

from ...utils.logger import get_custom_logger

logger = get_custom_logger(__name__)

class CellTypeMetadataEnricher:
    """
    Processes discrete lineage registries to extract functional annotations, 
    resolve Cell Ontology terms using pronto, and compile unified parameter frames.
    """

    def enrich_metadata_dataframe(
        self, 
        mdata: mu.MuData, 
        lineage_registry: Dict[str, Any], 
        cl_ontology_path: str,
        uns_output_key: str = "cell_types_metadata_df"
    ) -> None:
        """
        Query structural Cell Ontologies to extract absolute CL identifiers and 
        associated GO terms, injecting the resulting dataframe into mdata.uns.

        :param mdata: Integrated multi-modal omics storage asset.
        :type mdata: mu.MuData
        :param lineage_registry: Structured extraction dictionary derived from cell type strategies.
        :type lineage_registry: Dict[str, Any]
        :param cl_ontology_path: Filesystem trajectory or remote URL pointing to the target cl.obo file.
        :type cl_ontology_path: str
        :param uns_output_key: Objective matrix identifier key within the mdata.uns dictionary.
        :type uns_output_key: str
        :raises KeyError: If the mandatory 'rna' modality sub-container is missing.
        :raises FileNotFoundError: If the specified ontology path cannot be resolved or parsed.
        """
        # Heading 1 (Broad context / Top-level block / Script section)
        # Structural data schema validation and ontology ingestion
        logger.info("Starting structural Cell Ontology parsing via pronto interface.")
        
        if 'rna' not in mdata.mod:
            logger.error("Enrichment workflow aborted. Modality layer 'rna' missing from path context.", exc_info=True)
            raise KeyError("Missing 'rna' modality container inside MuData object.")

        if not cl_ontology_path.startswith("http") and not os.path.exists(cl_ontology_path):
            logger.error("Target OBO ontology file missing at designated tracker path: %s", cl_ontology_path, exc_info=True)
            raise FileNotFoundError(f"Ontology file tracking reference not found: {cl_ontology_path}")

        ## Load and parse the structured OBO graph layout safely
        logger.debug("Loading ontology graph definitions from source trajectory: %s", cl_ontology_path)
        cl_ontology = pronto.Ontology(cl_ontology_path)
        
        dataframe_records: List[Dict[str, Any]] = []

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Iterate over registry entries to perform term matching transformations
        for cluster_id, attributes in lineage_registry.items():
            ref_data = attributes["database_reference"]
            cell_type_name = str(ref_data["identifier"])
            cell_count = int(attributes["cell_count"])
            
            logger.info("Mining ontological structures for identified cell type label: %s", cell_type_name)

            # Execution fallback constants allocation
            matched_cl_id = "CL:UNKNOWN"
            matched_definition = "No ontology definition available."
            associated_go_terms: Set[str] = set()

            ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
            ## Scan parsed ontology terms to match the target string label
            cleaned_query = cell_type_name.lower().strip()
            
            for term in cl_ontology.terms():
                if not term.name:
                    continue
                    
                ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
                ### Inspect both main terminology handles and nested synonym strings
                is_match = False
                if term.name.lower() == cleaned_query:
                    is_match = True
                elif term.synonyms:
                    for synonym in term.synonyms:
                        if synonym.description and synonym.description.lower() == cleaned_query:
                            is_match = True
                            break

                if is_match:
                    ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
                    ### Isolate identification trackers and definition properties on match
                    matched_cl_id = term.id
                    if term.definition:
                        matched_definition = str(term.definition)

                    # Extract cross-references explicitly pointing to Gene Ontology blocks
                    if term.xrefs:
                        for xref in term.xrefs:
                            if xref.id.startswith("GO:"):
                                associated_go_terms.add(xref.id)

                    # Interrogate graph relationships to harvest functional GO predicates
                    if term.relationships:
                        for rel_type, related_terms in term.relationships.items():
                            for rel_term in related_terms:
                                if rel_term.id.startswith("GO:"):
                                    associated_go_terms.add(rel_term.id)
                    break

            ### Heading 3 (Deep sub-step / Conditional branch / Granular execution detail)
            ### Format the compiled terms into a flat string sequence for storage
            go_terms_payload = ",".join(sorted(list(associated_go_terms)))
            logger.debug("Cluster %s mapped to identifier %s with %d linked GO terms.", str(cluster_id), matched_cl_id, len(associated_go_terms))

            # Append the completed data record to the dataframe array
            record = {
                "cluster_id": str(cluster_id),
                "cell_type_name": cell_type_name,
                "cell_count": cell_count,
                "cell_ontology_id": matched_cl_id,
                "ontology_definition": matched_definition,
                "associated_go_annotations": go_terms_payload,
                "source_database": str(ref_data["source"]),
                "confidence_score": float(ref_data.get("confidence_score", 1.0))
            }
            dataframe_records.append(record)

        ## Heading 2 (Specific operation / Sub-step inside a loop or function / Secondary logic)
        ## Construct the target pandas dataframe and link it to root dictionary metadata slots
        logger.info("Compiling and structuring cell types metadata dataframe array layers.")
        metadata_df = pd.DataFrame(dataframe_records)
        metadata_df.set_index("cluster_id", inplace=True)

        if not isinstance(mdata.uns, dict):
            mdata.uns = dict(mdata.uns)

        mdata.uns[uns_output_key] = metadata_df
        mdata.update()
        logger.info("Successfully synchronized enriched metadata under mdata.uns['%s'] key.", uns_output_key)