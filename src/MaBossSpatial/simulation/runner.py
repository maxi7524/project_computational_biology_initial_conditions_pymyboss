# src/simulation/runner.py

import os
import csv
import copy
import numpy as np
import pandas as pd
import anndata
from typing import Dict, List, Any, Tuple

class SimulationRunner:
    """
    Executes the piecewise, time-delayed spatial Boolean simulation loop.

    This module handles the execution phase of the pipeline. It simulates a 
    selected subset of cells over time by splitting the total duration into small 
    intervals (delta_t). At each step, it calculates time-delayed signaling inputs 
    from neighbors, updates MaBoSS transition rates, runs short stochastical 
    simulations, tracks state histories, and streams outputs to a CSV file.

    :param adata: The main AnnData object containing expression and spatial metadata.
    :type adata: anndata.AnnData
    :param spatial_env: Activated instance of the spatial environment module.
    :type spatial_env: src.spatial_module.environment.SpatialEnvironment
    :param time_estimator: Activated instance of the time lag estimation module.
    :type time_estimator: src.simulation.time_estimator.TimeLagEstimator
    :param manager: Activated instance of the MaBoSS model manager.
    :type manager: src.maboss_module.model_manager.MaBossManager
    """

    def __init__(self, adata: anndata.AnnData, spatial_env: Any, time_estimator: Any, manager: Any):
        """
        Constructor method.
        """
        self.adata = adata
        self.spatial_env = spatial_env
        self.time_estimator = time_estimator
        self.manager = manager
        
        # History buffer: maps time_step -> cell_id -> node_name -> probability_value
        self.history_buffer: Dict[float, Dict[str, Dict[str, float]]] = {}

    def _extract_node_probabilities(self, maboss_result: Any, model_nodes: List[str]) -> Dict[str, float]:
        """
        Extracts the probability of each individual node being active (state 1) 
        from the final state of a MaBoSS piecewise simulation run.

        :param maboss_result: The result object returned by a MaBoSS simulation run.
        :type maboss_result: maboss.Result
        :param model_nodes: List of all node names in the network topology.
        :type model_nodes: list of str
        :return: A dictionary mapping node names to their activation probability (0.0 to 1.0).
        :rtype: dict
        """
        node_probs = {node: 0.0 for node in model_nodes}
        try:
            # Get the probability trajectory and select the very last timepoint row
            probtraj = maboss_result.get_last_states_probtraj()
            if probtraj.empty:
                return node_probs
                
            last_row = probtraj.iloc[0]
            # MaBoSS columns represent states combined as string names (e.g., "NodeA -- NodeB")
            for state_name, state_prob in last_row.items():
                if state_name in ["Nil", "State"]: 
                    continue
                # Split the combined state string to find which individual nodes are active (1)
                active_nodes_in_state = [node.strip() for node in state_name.split("--")]
                for node in active_nodes_in_state:
                    if node in node_probs:
                        node_probs[node] += state_prob
        except Exception:
            # Fallback wrapper if probtraj structure is unavailable or mocked
            pass
        return node_probs

    def _get_historical_value(self, cell_id: str, node_name: str, target_time: float) -> float:
        """
        Looks up a node's probability for a specific cell at a delayed point in time.

        If the requested historical time is less than or equal to 0, it automatically 
        falls back to the initial state conditions established at t=0.

        :param cell_id: Barcode of the cell to query.
        :type cell_id: str
        :param node_name: Name of the gene/node to look up.
        :type node_name: str
        :param target_time: The calculated delayed time point (t - lag).
        :type target_time: float
        :return: Activation probability value (0.0 to 1.0).
        :rtype: float
        """
        if target_time <= 0:
            # Fall back to initial state baseline (t=0)
            return self.history_buffer.get(0.0, {}).get(cell_id, {}).get(node_name, 0.0)
            
        # Find the closest available discrete time step in the history buffer
        available_times = sorted(list(self.history_buffer.keys()))
        closest_time = available_times[0]
        for t in available_times:
            if t <= target_time:
                closest_time = t
            else:
                break
                
        return self.history_buffer.get(closest_time, {}).get(cell_id, {}).get(node_name, 0.0)

    def RunPiecewiseSimulation(self, simulation_set: List[str], context_set: List[str], 
                               sim_settings: Dict[str, Any], output_csv_path: str) -> None:
        """
        Executes the main iterative evaluation loop and streams rows directly to a CSV file.

        The method handles 2-hop boundary evaluation at t=0, dynamically adjusts 
        transition parameters per cell using physical connectivity weights and lag buffers, 
        and updates states sequentially.

        :param simulation_set: Core cells to actively simulate (1-hop network).
        :type simulation_set: list of str
        :param context_set: Static background context cells (2-hop network).
        :type context_set: list of str
        :param sim_settings: Parameters including 'max_time', 'delta_t', and 'sample_count'.
        :type sim_settings: dict
        :param output_csv_path: Destination path for streaming out simulation logs.
        :type output_csv_path: str
        :return: None
        """
        max_time = sim_settings.get("max_time", 60.0)
        delta_t = sim_settings.get("delta_t", 5.0)
        sample_count = sim_settings.get("sample_count", 1000)
        
        # 1. Initialize all cell models and compute global 99th percentile baselines
        cell_models = self.manager.initialize_evaluation_models(self.adata, simulation_set, context_set)
        all_tracked_cells = list(set(simulation_set) + set(context_set))
        
        # Populate history buffer at t=0 from initialized models
        self.history_buffer[0.0] = {}
        for cell_id in all_tracked_cells:
            self.history_buffer[0.0][cell_id] = {}
            # Take the probability of state 1 directly from the initial configuration
            for model_name, sim_inst in cell_models[cell_id].items():
                for node in self.manager.network_nodes[model_name]:
                    # MaBoSS internal istate structure lookup
                    istate_prob_1 = sim_inst.network.get_istate(node)[1] # Index 1 corresponds to state 1
                    self.history_buffer[0.0][cell_id][node] = istate_prob_1

        # Prepare the output CSV file and write header lines
        with open(output_csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Cell_ID", "Time", "Model", "Node", "Probability"])
            
            # Write out initial state profiles (t=0)
            for cell_id in simulation_set:
                for model_name in cell_models[cell_id].keys():
                    for node in self.manager.network_nodes[model_name]:
                        prob = self.history_buffer[0.0][cell_id][node]
                        writer.writerow([cell_id, 0.0, model_name, node, prob])

        # 2. Main Time Stepping Loop
        current_time = delta_t
        connectivities = self.adata.obsp[self.spatial_env.connectivity_key]
        cell_names = self.adata.obs_names.tolist()
        cell_to_idx = {cell: i for i, cell in enumerate(cell_names)}

        while current_time <= max_time:
            print(f"Simulating time step t = {current_time} min...")
            self.history_buffer[current_time] = {}
            
            # Temporary dict to store newly computed cell states for this step before saving to disk
            current_step_results: Dict[str, Dict[str, Dict[str, float]]] = {}

            # Iterate only over the active simulation set (1-hop cells)
            for cell_id in simulation_set:
                current_step_results[cell_id] = {}
                idx_i = cell_to_idx[cell_id]
                
                # Fetch row of spatial connectivities from LIANA+ output
                spatial_row = connectivities[idx_i].toarray().flatten() if hasattr(connectivities, "toarray") else connectivities[idx_i]
                neighbor_indices = np.where(spatial_row > 0)[0]

                for model_name, sim_instance in cell_models[cell_id].items():
                    # Set short-term piecewise execution time window bounds for MaBoSS
                    sim_instance.update_parameters(max_time=delta_t, sample_count=sample_count)
                    
                    # Update parameters/rates based on spatial neighbor histories and lags
                    for node in self.manager.network_nodes[model_name]:
                        # Check if this node is configured to receive external ligand signal inputs
                        if node in self.time_estimator.intracellular_lags:
                            integrated_signal = 0.0
                            
                            for idx_j in neighbor_indices:
                                neighbor_id = cell_names[idx_j]
                                w_ij = spatial_row[idx_j] # Physical decay weight computed by LIANA+
                                
                                # Fetch physical distance from matrix to calculate extracellular delay
                                distance = self.spatial_env.distance_matrix[idx_i, idx_j] if hasattr(self.spatial_env, "distance_matrix") else 10.0
                                total_lag = self.time_estimator.get_total_lag(node, distance)
                                
                                # Look up what the neighbor's signaling output state was at (current_time - total_lag)
                                historical_ligand_activity = self._get_historical_value(neighbor_id, node, current_time - total_lag)
                                integrated_signal += w_ij * historical_ligand_activity
                            
                            # Map the integrated signal onto the transition rate parameter inside MaBoSS
                            sim_instance.param[f"${node}_up"] = integrated_signal

                    # Run stochastical simulation step for this cell
                    res = sim_instance.run()
                    
                    # Extract node probabilities from the trajectory outcome
                    updated_probs = self._extract_node_probabilities(res, self.manager.network_nodes[model_name])
                    current_step_results[cell_id][model_name] = updated_probs
                    
                    # Update initial states (istate) of the model instance to act as the starting point for the NEXT step
                    for node, prob in updated_probs.items():
                        sim_instance.network.set_istate(node, [1.0 - prob, prob])

            # 3. Store results for this time point in the history buffer and stream straight to CSV
            with open(output_csv_path, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                for cell_id in simulation_set:
                    self.history_buffer[current_time][cell_id] = {}
                    for model_name, nodes_data in current_step_results[cell_id].items():
                        for node, prob in nodes_data.items():
                            # Save to memory buffer for future lag lookups
                            self.history_buffer[current_time][cell_id][node] = prob
                            # Stream to disk immediately
                            writer.writerow([cell_id, current_time, model_name, node, prob])
                            
            # Clean up old history buffers that are further back than the maximum possible lag to optimize memory
            # TODO: Implement memory buffer pruning logic if running very large grids
            
            current_time += delta_t
        print(f"Piecewise simulation complete. All outputs saved to '{output_csv_path}'.")