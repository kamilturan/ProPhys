"""
Validation utilities for protein sequences.
"""

from typing import Tuple
from .constants import AMINO_ACIDS


def validate_sequence(sequence: str) -> Tuple[bool, str]:
    """
    Validate a protein sequence against the IUPAC amino acid alphabet.
    
    Args:
        sequence: Protein sequence string
        
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    """
    if not sequence:
        return False, "Sequence cannot be empty"
    
    if not isinstance(sequence, str):
        return False, "Sequence must be a string"
    
    # Convert to uppercase for validation
    sequence_upper = sequence.upper()
    
    # Check for invalid characters
    invalid_chars = set(sequence_upper) - AMINO_ACIDS
    if invalid_chars:
        return False, f"Invalid amino acids found: {', '.join(sorted(invalid_chars))}"
    
    return True, ""
