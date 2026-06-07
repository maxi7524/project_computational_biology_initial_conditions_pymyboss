# Multi-Modal Structural Type References and Schema Blueprints

from typing import Dict, List, Any

# Global hardcoded structure schema requirements
## Maps standard functional pipeline keys to their required sub-slots
OMNI_PHYSIBOSS_SCHEMA: Dict[str, List[str]] = {
    "obs": ["cell_type", "sample_id"],
    "spatial": ["spatial_coords"],
    "uns": ["decoupleR_networks", "liana_res"]
}

# Explicit expected type signatures matching multi-scale processing steps
## Tracks string labels of class structures required by simulation boundaries
EXPECTED_TYPE_SIGNATURES: Dict[str, str] = {
    "obs": "DataFrame",
    "spatial": "ndarray",
    "uns": "dict"
}