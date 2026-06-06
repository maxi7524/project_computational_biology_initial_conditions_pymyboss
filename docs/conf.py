import os
import sys
from pathlib import Path

# Ustawienie ścieżki źródłowej, aby Sphinx widział moduły biblioteki
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

project = "OmniPhysiBoSS"
copyright = "2026, Max Stróżyk"
author = "Max Stróżyk"
release = "0.1.0"

# Aktywacja rozszerzeń
extensions = [
    "sphinx.ext.autodoc",      # Automatyczne wyciąganie docstringów
    "sphinx.ext.napoleon",     # Obsługa formatów dokumentacji NumPy/Google/Sphinx
    "sphinx.ext.mathjax",      # Renderowanie równań matematycznych LaTeX
    "myst_parser"             # Kompilacja plików Markdown (.md)
]

# Wspierane rozszerzenia plików źródłowych
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

html_theme = "sphinx_rtd_theme"

# Konfiguracja MyST-Parser dla zaawansowanych funkcji (np. matematyka $)
myst_enable_extensions = [
    "dollarmath",              # Wsparcie dla $ inline i $$ block math
    "amsmath",
    "colon_fence"
]