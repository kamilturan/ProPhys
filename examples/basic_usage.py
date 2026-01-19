"""
Example usage of the ProPhys Python API.
"""

from prophys import ProteinAnalyzer, validate_sequence
import json


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Create analyzer with a protein sequence
    sequence = "MKTIIALSYIFCLVFA"
    analyzer = ProteinAnalyzer(sequence)
    
    # Get individual properties
    print(f"Sequence: {analyzer.sequence}")
    print(f"Length: {analyzer.length} amino acids")
    print(f"Molecular Weight: {analyzer.molecular_weight()} Da")
    print(f"Isoelectric Point: {analyzer.isoelectric_point()}")
    print(f"GRAVY: {analyzer.gravy()}")
    print(f"Aromaticity: {analyzer.aromaticity()}")
    print(f"Instability Index: {analyzer.instability_index()}")
    print(f"Charge at pH 7: {analyzer.charge_at_ph7()}")
    print()


def example_amino_acid_composition():
    """Amino acid composition example."""
    print("=" * 60)
    print("Example 2: Amino Acid Composition")
    print("=" * 60)
    
    analyzer = ProteinAnalyzer("AAACCCDDDEEE")
    composition = analyzer.amino_acid_composition()
    
    # Print only non-zero compositions
    print("Amino acid percentages:")
    for aa, percent in sorted(composition.items()):
        if percent > 0:
            print(f"  {aa}: {percent:.1f}%")
    print()


def example_window_analysis():
    """Window analysis example."""
    print("=" * 60)
    print("Example 3: Window Analysis")
    print("=" * 60)
    
    sequence = "MKTIIALSYIFCLVFAGGGSSSKKK"
    analyzer = ProteinAnalyzer(sequence)
    
    # Perform window analysis with window size 7
    windows = analyzer.window_analysis(window_size=7)
    
    print(f"Analyzing sequence: {sequence}")
    print(f"Window size: 7")
    print(f"Number of windows: {len(windows)}")
    print()
    print("First 5 windows:")
    for window in windows[:5]:
        print(f"  Position {window['position']}: {window['window']}")
        print(f"    Hydrophobicity: {window['hydrophobicity']}")
        print(f"    Aromaticity: {window['aromaticity']}")
        print(f"    Charge: {window['charge']}")
    print()


def example_json_output():
    """JSON output example."""
    print("=" * 60)
    print("Example 4: JSON Output")
    print("=" * 60)
    
    analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")
    
    # Get analysis as JSON string
    json_output = analyzer.to_json(indent=2)
    print("Complete analysis as JSON:")
    print(json_output[:500] + "...")
    print()
    
    # Parse back to dict
    data = json.loads(json_output)
    print(f"Parsed data - Molecular Weight: {data['molecular_weight']} Da")
    print()


def example_validation():
    """Sequence validation example."""
    print("=" * 60)
    print("Example 5: Sequence Validation")
    print("=" * 60)
    
    # Valid sequence
    is_valid, error = validate_sequence("ACDEFG")
    print(f"'ACDEFG' is valid: {is_valid}")
    
    # Invalid sequence
    is_valid, error = validate_sequence("ACDEFGXYZ")
    print(f"'ACDEFGXYZ' is valid: {is_valid}")
    print(f"Error: {error}")
    
    # Using with analyzer
    try:
        analyzer = ProteinAnalyzer("INVALID123")
    except ValueError as e:
        print(f"ValueError caught: {e}")
    print()


def example_comparison():
    """Compare two protein sequences."""
    print("=" * 60)
    print("Example 6: Comparing Two Sequences")
    print("=" * 60)
    
    # Hydrophobic sequence (lots of I, L, V, F)
    hydrophobic = "IIIIILLLLVVVVFFFF"
    analyzer1 = ProteinAnalyzer(hydrophobic)
    
    # Hydrophilic sequence (lots of K, D, E, R)
    hydrophilic = "KKKKDDDDEEEERRRRR"
    analyzer2 = ProteinAnalyzer(hydrophilic)
    
    print(f"Hydrophobic sequence: {hydrophobic}")
    print(f"  GRAVY: {analyzer1.gravy()}")
    print(f"  Charge at pH 7: {analyzer1.charge_at_ph7()}")
    print()
    
    print(f"Hydrophilic sequence: {hydrophilic}")
    print(f"  GRAVY: {analyzer2.gravy()}")
    print(f"  Charge at pH 7: {analyzer2.charge_at_ph7()}")
    print()


def main():
    """Run all examples."""
    example_basic_usage()
    example_amino_acid_composition()
    example_window_analysis()
    example_json_output()
    example_validation()
    example_comparison()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
