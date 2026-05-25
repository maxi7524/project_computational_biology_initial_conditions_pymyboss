# src/MaBossSpatial/utils/utils_check_configuration.py

import numpy as np
import anndata
from typing import Any, List

def generate_config_report(adata: anndata.AnnData, liana_key: str, manager: Any, 
                           spatial_env: Any, time_estimator: Any) -> None:
    """
    Analyzes and prints a structured configuration report evaluating data-model compatibility.

    Checks for naming convention discrepancies, active spatial connections from LIANA+,
    and structural time delays mapped for signaling pathways.

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
    :return: None
    """
    print("=" * 80)
    print("                    SPATIAL BOOLEAN PIPELINE CONFIGURATION REPORT")
    print("=" * 80)

    # 1. Evaluate Nomenclature and Organism Compatibility
    model_nodes = manager.all_nodes
    matched_genes = [node for node in model_nodes if node in adata.var_names]
    missing_genes = [node for node in model_nodes if node not in adata.var_names]

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
    print(f"    Directly Mapped Gene Overlaps: {len(matched_genes)}")
    if matched_genes:
        for gene in matched_genes[:5]:
            print(f"\t- {gene:<10} -> Mapped to adata.var_names")
        if len(matched_genes) > 5:
            print(f"\t... and {len(matched_genes) - 5} more genes.")
    else:
        print("    ⚠️  No precise node-to-gene name mapping detected. Check capitalizations.")

    # 3. Spatial and Communication Graph Metrics
    print("\n--- 2. SPATIAL & COMMUNICATION LAYER ---")
    conn_key = spatial_env.connectivity_key
    if conn_key in adata.obsp:
        conn_matrix = adata.obsp[conn_key]
        total_edges = conn_matrix.count_nonzero() if hasattr(conn_matrix, "count_nonzero") else np.count_nonzero(conn_matrix)
        print(f"    ✅  LIANA+ Connectivity Key   : {conn_key}")
        print(f"    ✅  Active Spatial Edges      : {total_edges} connections resolved in tissue grid.")
    else:
        print(f"    ℹ️  LIANA+ Adjacency Graph '{conn_key}' not computed yet. Evaluated lazily at runtime.")

    # 4. Temporal and Time-Lag Configuration
    print("\n--- 3. TEMPORAL & TIME-LAG CONFIGURATION ---")
    if time_estimator and time_estimator.intracellular_lags:
        print(f"    ✅  Signaling Delay Strategy  : {time_estimator.strategy}")
        print("    Resolved Signaling Receptor Delays:")
        for rec, lag in list(time_estimator.intracellular_lags.items())[:6]:
            origin = "[USER OVERRIDE]" if rec in time_estimator.custom_lags else "[DYNAMIC HEURISTIC]"
            print(f"\t- {rec:<12} -> Total Intracellular Lag: {lag:<5} min {origin}")
        if len(time_estimator.intracellular_lags) > 6:
            print(f"\t... and {len(time_estimator.intracellular_lags) - 6} more receptors.")
    else:
        print("    ℹ️  Time delay vectors are uncomputed. Delays will be mapped on pipeline invocation.")
        
    print("\n" + "=" * 80)