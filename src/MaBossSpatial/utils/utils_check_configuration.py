import numpy as np
import anndata
from typing import Any, List

def generate_config_report(
    adata: anndata.AnnData, 
    liana_key: str, 
    manager: Any, 
    spatial_env: Any, 
    time_estimator: Any,
    show_all_examples: bool = False
) -> None:
    """
    Analyzes and prints a structured configuration report evaluating data-model compatibility.

    Checks for naming convention discrepancies, active spatial connections from LIANA+,
    structural time delays mapped for signaling pathways, and critical input node availability.

    :param adata: The main AnnData object containing spatial expression.
    :type adata: anndata.AnnData
    :param liana_key: Key under ``adata.uns`` where LIANA+ results are kept.
    :type liana_key: str
    :param manager: Active instance of the MaBoSS manager.
    :type manager: src.MaBossSpatial.maboss_module.model_manager.MaBossManager
    :param spatial_env: Active instance of the spatial environment.
    :type spatial_env: src.MaBossSpatial.spatial_module.environment.SpatialEnvironment
    :param time_estimator: Active instance of the time lag calculator.
    :type time_estimator: src.MaBossSpatial.simulation.time_lag.TimeLagEstimator
    :param show_all_examples: If True, prints all mapped elements without truncation. Defaults to False.
    :type show_all_examples: bool
    :return: None
    """
    print("=" * 80)
    print("                    SPATIAL BOOLEAN PIPELINE CONFIGURATION REPORT")
    print("=" * 80)

    # 1. Evaluate Nomenclature and Organism Compatibility
    model_nodes = manager.all_nodes
    input_nodes = getattr(manager, "input_nodes", [])
    
    matched_genes = [node for node in model_nodes if node in adata.var_names]
    matched_inputs = [node for node in input_nodes if node in adata.var_names]
    missing_inputs = [node for node in input_nodes if node not in adata.var_names]

    # Heuristic to detect dataset organism naming convention
    sample_genes = [g for g in list(adata.var_names[:100]) if g.isalpha()]
    data_is_mouse = any(g.istitle() and not g.isupper() for g in sample_genes) if sample_genes else False
    model_is_human = any(n.isupper() for n in model_nodes if n.isalpha())

    print("\n[ COMPATIBILITY ALERT ]")
    print("-" * 80)
    if data_is_mouse and model_is_human:
        print("⚠️  Warning: Nomenclature Mismatch Detected!")
        print("    -> Intracellular Model Organism : HUMAN (Detected via UPPERCASE nodes)")
        print("    -> Spatial Expression Dataset   : MOUSE (Detected via Sentence-Case genes)")
        print("    -> Impact: Continuous mapping fields will register 0.0 unless matching case rules are added.")
    else:
        print("✅  Success: Intracellular model and Spatial dataset nomenclatures appear aligned.")

    # 2. Model Topology & Mapping Status
    print("\n--- 1. MODEL TOPOLOGY & MAPPING STATUS ---")
    print(f"    Total Managed Network Nodes: {len(model_nodes)}")
    print(f"    Directly Mapped Gene Overlaps (Total): {len(matched_genes)}")
    
    if matched_genes:
        display_genes = matched_genes if show_all_examples else matched_genes[:5]
        for gene in display_genes:
            target_var = adata.var_names[adata.var_names == gene][0]
            print(f"\t- {gene:<10} -> Mapped to adata.var_names['{target_var}']")
        if not show_all_examples and len(matched_genes) > 5:
            print(f"\t... and {len(matched_genes) - 5} more genes.")
    else:
        print("    ⚠️  No precise node-to-gene name mapping detected. Check capitalizations.")

    # 3. Critical Input Nodes Validation
    print("\n--- 1b. CRITICAL INPUT NODES VALIDATION ---")
    print(f"    Total Required Input Nodes : {len(input_nodes)}")
    print(f"    Overlapping Input Nodes     : {len(matched_inputs)} / {len(input_nodes)}")
    
    if len(input_nodes) > 0:
        if len(missing_inputs) == 0:
            print("    ✅  Success: All required model input nodes are present in adata.var_names.")
        else:
            print("    ⚠️  WARNING: Missing Critical Input Nodes! The model will not function correctly without them.")
            print(f"    Missing Inputs ({len(missing_inputs)}):")
            display_missing = missing_inputs if show_all_examples else missing_inputs[:5]
            for mis in display_missing:
                print(f"\t- {mis:<10} -> NOT found in adata.var_names")
            if not show_all_examples and len(missing_inputs) > 5:
                print(f"\t... and {len(missing_inputs) - 5} more missing input nodes.")
            
        if matched_inputs:
            print("    Mapped Input Examples:")
            display_inputs = matched_inputs if show_all_examples else matched_inputs[:5]
            for inp in display_inputs:
                target_var = adata.var_names[adata.var_names == inp][0]
                print(f"\t- {inp:<10} -> Mapped to adata.var_names['{target_var}'] (CRITICAL INPUT)")
            if not show_all_examples and len(matched_inputs) > 5:
                print(f"\t... and {len(matched_inputs) - 5} more input nodes.")
    else:
        print("    ℹ️  No specific input nodes defined or detected in the manager topology.")

    # 4. Spatial and Communication Graph Metrics
    print("\n--- 2. SPATIAL & COMMUNICATION LAYER ---")
    connectivity_key = spatial_env.connectivity_key
    
    expected_key = (
        connectivity_key 
        if connectivity_key.endswith("_connectivities") 
        else f"{connectivity_key}_connectivities"
    )
    
    if expected_key in adata.obsp:
        conn_matrix = adata.obsp[expected_key]
        total_edges = conn_matrix.count_nonzero() if hasattr(conn_matrix, "count_nonzero") else np.count_nonzero(conn_matrix)
        print(f"    ✅  Success: Spatial Adjacency Graph '{expected_key}' is computed and verified.")
        print(f"    ✅  Active Spatial Edges      : {total_edges} connections resolved in tissue grid.")
    else:
        print(f"    ℹ️  LIANA+ Adjacency Graph '{expected_key}' not computed yet. Evaluated lazily at runtime.")

    # 5. Temporal and Time-Lag Configuration
    print("\n--- 3. TEMPORAL & TIME-LAG CONFIGURATION ---")
    if time_estimator:
        print(f"    ✅  Signaling Delay Strategy  : {time_estimator.strategy}")
        
        # Check if lags are already computed or if we can preview them from liana data
        lags_dict = getattr(time_estimator, "intracellular_lags", None)
        
        # Dry-run preview if report is called before pipeline execution
        if (not lags_dict or len(lags_dict) == 0) and liana_key in adata.uns:
            try:
                liana_df = adata.uns[liana_key]
                if 'receptor_complex' in liana_df.columns:
                    active_receptors = liana_df['receptor_complex'].unique().tolist()
                    # Safe temporary calculation for preview purposes
                    time_estimator.calculate_intracellular_lags(
                        network_nodes=model_nodes, 
                        active_receptors=active_receptors
                    )
                    lags_dict = getattr(time_estimator, "intracellular_lags", {})
            except Exception:
                lags_dict = None

        if lags_dict:
            print("    Resolved Signaling Receptor Delays:")
            lags_items = list(lags_dict.items())
            display_lags = lags_items if show_all_examples else lags_items[:6]
            
            for rec, lag in display_lags:
                custom_lags = getattr(time_estimator, "custom_lags", {})
                origin = "[USER OVERRIDE]" if custom_lags and rec in custom_lags else "[DYNAMIC HEURISTIC]"
                print(f"\t- {rec:<12} -> Total Intracellular Lag: {lag:<5} min {origin}")
            
            if not show_all_examples and len(lags_items) > 6:
                print(f"\t... and {len(lags_items) - 6} more receptors.")
        else:
            print("    ℹ️  Time delay vectors are uncomputed. Delays will be mapped on pipeline invocation.")
    else:
        print("    ℹ️  TimeLagEstimator is not initialized in the pipeline setup.")
        
    print("\n" + "=" * 80)