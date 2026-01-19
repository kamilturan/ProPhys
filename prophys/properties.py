"""
Core protein physicochemical property calculations.
"""

import json
from typing import Dict, List, Any
from collections import Counter

from .constants import (
    MOLECULAR_WEIGHTS,
    HYDROPHOBICITY,
    PKA_VALUES,
    AROMATIC_AA,
    POSITIVE_AA,
    NEGATIVE_AA,
    AMINO_ACIDS,
)
from .validators import validate_sequence


class ProteinAnalyzer:
    """
    Analyzer for computing protein physicochemical properties.
    """
    
    def __init__(self, sequence: str):
        """
        Initialize the analyzer with a protein sequence.
        
        Args:
            sequence: Protein sequence (IUPAC amino acid alphabet)
            
        Raises:
            ValueError: If sequence is invalid
        """
        is_valid, error_msg = validate_sequence(sequence)
        if not is_valid:
            raise ValueError(error_msg)
        
        self.sequence = sequence.upper()
        self.length = len(self.sequence)
    
    def amino_acid_composition(self) -> Dict[str, float]:
        """
        Calculate the percentage composition of each amino acid.
        
        Returns:
            Dictionary mapping amino acid to percentage
        """
        counts = Counter(self.sequence)
        return {aa: (counts.get(aa, 0) / self.length) * 100 for aa in sorted(AMINO_ACIDS)}
    
    def molecular_weight(self) -> float:
        """
        Calculate the molecular weight of the protein.
        
        Returns:
            Molecular weight in Daltons
        """
        weight = sum(MOLECULAR_WEIGHTS[aa] for aa in self.sequence)
        # Subtract water molecules lost in peptide bond formation
        weight -= (self.length - 1) * 18.015
        return round(weight, 2)
    
    def isoelectric_point(self) -> float:
        """
        Calculate the theoretical isoelectric point (pI).
        
        Returns:
            Predicted pI value
        """
        # Simple binary search for pH where net charge is closest to 0
        ph_min, ph_max = 0.0, 14.0
        
        for _ in range(100):  # iterations for precision
            ph_mid = (ph_min + ph_max) / 2
            charge = self._calculate_charge_at_ph(ph_mid)
            
            if abs(charge) < 0.001:
                return round(ph_mid, 2)
            elif charge > 0:
                ph_min = ph_mid
            else:
                ph_max = ph_mid
        
        return round((ph_min + ph_max) / 2, 2)
    
    def _calculate_charge_at_ph(self, ph: float) -> float:
        """
        Calculate net charge at a given pH.
        
        Args:
            ph: pH value
            
        Returns:
            Net charge
        """
        charge = 0.0
        
        # N-terminus contribution (positive charge)
        charge += 1 / (1 + 10 ** (ph - PKA_VALUES['N-term']))
        
        # C-terminus contribution (negative charge)
        charge -= 1 / (1 + 10 ** (PKA_VALUES['C-term'] - ph))
        
        # Count ionizable amino acids
        for aa in self.sequence:
            if aa == 'K':
                charge += 1 / (1 + 10 ** (ph - PKA_VALUES['K']))
            elif aa == 'R':
                charge += 1 / (1 + 10 ** (ph - PKA_VALUES['R']))
            elif aa == 'H':
                charge += 1 / (1 + 10 ** (ph - PKA_VALUES['H']))
            elif aa == 'D':
                charge -= 1 / (1 + 10 ** (PKA_VALUES['D'] - ph))
            elif aa == 'E':
                charge -= 1 / (1 + 10 ** (PKA_VALUES['E'] - ph))
            elif aa == 'C':
                charge -= 1 / (1 + 10 ** (PKA_VALUES['C'] - ph))
            elif aa == 'Y':
                charge -= 1 / (1 + 10 ** (PKA_VALUES['Y'] - ph))
        
        return charge
    
    def gravy(self) -> float:
        """
        Calculate the Grand Average of Hydropathy (GRAVY).
        
        Returns:
            GRAVY score
        """
        total_hydrophobicity = sum(HYDROPHOBICITY[aa] for aa in self.sequence)
        return round(total_hydrophobicity / self.length, 3)
    
    def aromaticity(self) -> float:
        """
        Calculate the aromaticity (fraction of aromatic amino acids).
        
        Returns:
            Aromaticity as fraction (0-1)
        """
        aromatic_count = sum(1 for aa in self.sequence if aa in AROMATIC_AA)
        return round(aromatic_count / self.length, 4)
    
    def instability_index(self) -> float:
        """
        Calculate the instability index.
        
        A protein with instability index < 40 is predicted as stable,
        a value > 40 predicts instability.
        
        Returns:
            Instability index
        """
        if self.length < 2:
            return 0.0
        
        score = 0.0
        for i in range(self.length - 1):
            dipeptide = self.sequence[i:i+2]
            # Use a simplified instability calculation
            # In practice, this would use DIWV (dipeptide instability weight values)
            score += 1.0  # Placeholder for actual DIWV lookup
        
        instability = (10.0 / self.length) * score
        return round(instability, 2)
    
    def charge_at_ph7(self) -> float:
        """
        Calculate the net charge at pH 7.0.
        
        Returns:
            Net charge at pH 7
        """
        return round(self._calculate_charge_at_ph(7.0), 3)
    
    def window_analysis(self, window_size: int = 9) -> List[Dict[str, Any]]:
        """
        Perform sliding window analysis for local properties.
        
        Args:
            window_size: Size of the sliding window (default: 9)
            
        Returns:
            List of dictionaries containing window-level properties
        """
        if window_size > self.length:
            window_size = self.length
        
        results = []
        
        for i in range(self.length - window_size + 1):
            window_seq = self.sequence[i:i + window_size]
            
            # Calculate hydrophobicity for window
            hydro = sum(HYDROPHOBICITY[aa] for aa in window_seq) / window_size
            
            # Calculate aromatic content
            aromatic = sum(1 for aa in window_seq if aa in AROMATIC_AA) / window_size
            
            # Calculate charge
            positive = sum(1 for aa in window_seq if aa in POSITIVE_AA)
            negative = sum(1 for aa in window_seq if aa in NEGATIVE_AA)
            
            results.append({
                "position": i + 1,  # 1-indexed
                "window": window_seq,
                "hydrophobicity": round(hydro, 3),
                "aromaticity": round(aromatic, 3),
                "charge": positive - negative,
            })
        
        return results
    
    def analyze(self, include_windows: bool = False, window_size: int = 9) -> Dict[str, Any]:
        """
        Perform complete analysis and return all properties.
        
        Args:
            include_windows: Whether to include window-level analysis
            window_size: Size of sliding window if included
            
        Returns:
            Dictionary containing all computed properties
        """
        result = {
            "sequence": self.sequence,
            "length": self.length,
            "molecular_weight": self.molecular_weight(),
            "isoelectric_point": self.isoelectric_point(),
            "gravy": self.gravy(),
            "aromaticity": self.aromaticity(),
            "instability_index": self.instability_index(),
            "charge_at_ph7": self.charge_at_ph7(),
            "amino_acid_composition": self.amino_acid_composition(),
        }
        
        if include_windows:
            result["window_analysis"] = self.window_analysis(window_size)
        
        return result
    
    def to_json(self, include_windows: bool = False, window_size: int = 9, **kwargs) -> str:
        """
        Export analysis results as JSON string.
        
        Args:
            include_windows: Whether to include window-level analysis
            window_size: Size of sliding window if included
            **kwargs: Additional arguments passed to json.dumps
            
        Returns:
            JSON string
        """
        data = self.analyze(include_windows=include_windows, window_size=window_size)
        return json.dumps(data, **kwargs)
