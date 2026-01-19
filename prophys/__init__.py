"""
ProPhys - Protein Physicochemical Profiling Toolkit

A Python toolkit for computing sequence-level and window-level properties
of protein sequences using the IUPAC amino acid alphabet.
"""

__version__ = "0.1.0"

from .properties import ProteinAnalyzer
from .validators import validate_sequence

__all__ = ["ProteinAnalyzer", "validate_sequence"]
