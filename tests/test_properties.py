"""
Tests for protein property calculations.
"""

import pytest
import json
from prophys import ProteinAnalyzer


def test_protein_analyzer_initialization():
    """Test ProteinAnalyzer initialization."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    assert analyzer.sequence == "ACDEFGHIKLMNPQRSTVWY"
    assert analyzer.length == 20


def test_protein_analyzer_case_insensitive():
    """Test that analyzer handles lowercase input."""
    analyzer = ProteinAnalyzer("acdefghiklmnpqrstvwy")
    assert analyzer.sequence == "ACDEFGHIKLMNPQRSTVWY"


def test_protein_analyzer_invalid_sequence():
    """Test that invalid sequences raise ValueError."""
    with pytest.raises(ValueError):
        ProteinAnalyzer("ACDEFGXYZ")
    
    with pytest.raises(ValueError):
        ProteinAnalyzer("")


def test_amino_acid_composition():
    """Test amino acid composition calculation."""
    analyzer = ProteinAnalyzer("AAACC")
    composition = analyzer.amino_acid_composition()
    
    assert composition['A'] == 60.0  # 3 out of 5
    assert composition['C'] == 40.0  # 2 out of 5
    assert composition['D'] == 0.0


def test_molecular_weight():
    """Test molecular weight calculation."""
    # Simple test with glycine (smallest)
    analyzer = ProteinAnalyzer("GG")
    mw = analyzer.molecular_weight()
    # 2 * 75.07 - 18.015 (water from peptide bond)
    expected = 2 * 75.07 - 18.015
    assert abs(mw - expected) < 0.1


def test_gravy():
    """Test GRAVY calculation."""
    analyzer = ProteinAnalyzer("IIIII")  # Isoleucine is very hydrophobic (4.5)
    gravy = analyzer.gravy()
    assert gravy == 4.5
    
    analyzer = ProteinAnalyzer("KKKKK")  # Lysine is hydrophilic (-3.9)
    gravy = analyzer.gravy()
    assert gravy == -3.9


def test_aromaticity():
    """Test aromaticity calculation."""
    # All aromatic (F, W, Y)
    analyzer = ProteinAnalyzer("FFWWY")
    aromaticity = analyzer.aromaticity()
    assert aromaticity == 1.0
    
    # No aromatic
    analyzer = ProteinAnalyzer("AAAAA")
    aromaticity = analyzer.aromaticity()
    assert aromaticity == 0.0
    
    # Half aromatic
    analyzer = ProteinAnalyzer("FFAAA")
    aromaticity = analyzer.aromaticity()
    assert aromaticity == 0.4


def test_charge_at_ph7():
    """Test charge calculation at pH 7."""
    # Lysine-rich (positive)
    analyzer = ProteinAnalyzer("KKKKKAAAAA")
    charge = analyzer.charge_at_ph7()
    assert charge > 0
    
    # Aspartate-rich (negative)
    analyzer = ProteinAnalyzer("DDDDDAAAAA")
    charge = analyzer.charge_at_ph7()
    assert charge < 0


def test_isoelectric_point():
    """Test isoelectric point calculation."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    pi = analyzer.isoelectric_point()
    assert 0 < pi < 14


def test_window_analysis():
    """Test window analysis."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    windows = analyzer.window_analysis(window_size=5)
    
    # Should have length - window_size + 1 windows
    assert len(windows) == 20 - 5 + 1
    
    # Check first window
    first_window = windows[0]
    assert first_window["position"] == 1
    assert first_window["window"] == "ACDEF"
    assert "hydrophobicity" in first_window
    assert "aromaticity" in first_window
    assert "charge" in first_window


def test_window_analysis_size_exceeds_length():
    """Test window analysis when window size exceeds sequence length."""
    analyzer = ProteinAnalyzer("ACDEF")
    windows = analyzer.window_analysis(window_size=10)
    
    # Should return one window with the entire sequence
    assert len(windows) == 1
    assert windows[0]["window"] == "ACDEF"


def test_analyze_without_windows():
    """Test complete analysis without windows."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    result = analyzer.analyze(include_windows=False)
    
    assert "sequence" in result
    assert "length" in result
    assert "molecular_weight" in result
    assert "isoelectric_point" in result
    assert "gravy" in result
    assert "aromaticity" in result
    assert "instability_index" in result
    assert "charge_at_ph7" in result
    assert "amino_acid_composition" in result
    assert "window_analysis" not in result


def test_analyze_with_windows():
    """Test complete analysis with windows."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    result = analyzer.analyze(include_windows=True, window_size=5)
    
    assert "window_analysis" in result
    assert len(result["window_analysis"]) > 0


def test_to_json():
    """Test JSON serialization."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    json_str = analyzer.to_json()
    
    # Should be valid JSON
    data = json.loads(json_str)
    assert data["sequence"] == "ACDEFGHIKLMNPQRSTVWY"
    assert data["length"] == 20


def test_to_json_with_windows():
    """Test JSON serialization with windows."""
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    json_str = analyzer.to_json(include_windows=True, window_size=5)
    
    data = json.loads(json_str)
    assert "window_analysis" in data
    assert len(data["window_analysis"]) > 0


def test_to_json_pretty():
    """Test pretty-printed JSON."""
    analyzer = ProteinAnalyzer("ACDEF")
    json_str = analyzer.to_json(indent=2)
    
    # Pretty-printed JSON should have newlines
    assert "\n" in json_str
    
    # Should still be valid JSON
    data = json.loads(json_str)
    assert data["sequence"] == "ACDEF"
