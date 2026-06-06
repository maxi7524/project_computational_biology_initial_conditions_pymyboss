"""
OmniPhysiBoSS/wrappers/_utils/log_monitor.py
---
This sub-module encapsulates line-by-line log analysis state routines to strip out verbose terminal dumps and stream summarized runtime parameters and milestones.
"""

import sys
from pathlib import Path

# Execution and log streaming sanitization layer
## Monitoring state evaluator class
class PhysiBoSSLogMonitor:
    """
    Parses and sanitizes real-time standard output from the compiled C++ PhysiBoSS executable.
    """

    def __init__(self) -> None:
        """
        Initialize monitoring boolean trackers.
        """
        # Stateful block parameters tracking flags
        self._in_mesh_info = False
        self._mesh_buffer = []

    def process_line(self, line: str) -> None:
        """
        Evaluates a single raw line of output and streams formatted telemetry milestones.

        :param line: The raw standard output line string from the running binary.
        :type line: str
        :return: None
        """
        cleaned = line.strip()
        if not cleaned:
            return

        # Mesh architecture structural parsing block
        ## Capture entry bounds of structural system description matrices
        if "Mesh information:" in cleaned:
            self._in_mesh_info = True
            print("\n[SYSTEM INFRASTRUCTURE] Extracting Cartesian mesh domain layout...")
            return

        if self._in_mesh_info:
            ### Evaluate block exit parameters if mesh information sections close
            if "Densities:" in cleaned or "WARNING" in cleaned or "Setting" in cleaned:
                self._in_mesh_info = False
                print("----------------------------------------------------------------------")
                for mesh_item in self._mesh_buffer:
                    print(f"  {mesh_item}")
                print("----------------------------------------------------------------------")
                self._mesh_buffer = []
            else:
                ### Buffer continuous spatial dimension text entries
                self._mesh_buffer.append(cleaned)
                return

        # RNG random seed tracking evaluations
        ## Capture duplicate setting warnings without breaking pipeline execution loops
        if "WARNING: Setting the random seed again." in cleaned:
            print("[RNG WARNING] Duplicate random seed variable found in user parameters. Reconfiguring standard options layout.")
            return
        if "Setting up RNG with seed" in cleaned:
            print(f"[RNG CONFIGURATION] Successfully {cleaned.lower()}")
            return

        # Pre-processing structural execution checks
        ## Track cell cycle and agent types definitions staging routines
        if "Pre-processing type" in cleaned:
            type_info = cleaned.split("named")[-1].strip()
            print(f"⚙️ [PRE-PROCESSING] Initializing structural cell properties for lineage: '{type_info}'")
            return
        if "Processing" in cleaned and "..." in cleaned:
            completed_type = cleaned.replace("Processing", "").replace("...", "").strip()
            print(f"✅ [PRE-PROCESSING] Completed pipeline setup configuration for: '{completed_type}'")
            return

        # Cataloging runtime parameter block categorizations
        ## Suppress specific numeric details while emphasizing parameter registration matrices
        if "User parameters in XML" in cleaned:
            print("[PARAMETER INITIALIZATION] Registering configuration matrices...")
            return
        if "parameters::" in cleaned:
            print(f" -> Cataloged parameters context profile: {cleaned}")
            return
        if "Signals:" in cleaned:
            print("[METRICS REGISTRATION] Mapping biochemical intracellular signal tracking vectors...")
            return
        if "Behaviors:" in cleaned:
            print("[METRICS REGISTRATION] Mapping agent multicellular behavior execution vectors...")
            return

        # Spatial element loading sequences
        ## Verify position and coordinate loading blocks without flooding terminal interfaces
        if "Loading cells from" in cleaned:
            print("📁 [CELL COHORT SYSTEM] Loading explicit initialization file spatial coordinates...")
            return
        if "Creating" in cleaned and "at" in cleaned:
            ### Silence individual spatial agent instantiation loops to keep stdout logs scannable
            return

        # Multi-scale execution telemetry outputs
        ## Stream simulation step boundaries directly into terminal outputs
        if "current simulated time:" in cleaned:
            print(f"\n⏱️ [SIMULATION METRIC] {cleaned}")
            sys.stdout.flush()
            return
        if "total agents:" in cleaned:
            print(f"👥 [SIMULATION POPULATION] {cleaned}")
            sys.stdout.flush()
            return
        if "Total simulation runtime:" in cleaned:
            print("\n🎉 [PROCESS COMPLETED] Simulation environment sequence finished successfully.")
            return