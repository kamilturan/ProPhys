"""
Command-line interface for ProPhys.
"""

import argparse
import json
import sys

from prophys import ProteinAnalyzer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ProPhys - Protein Physicochemical Profiling Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prophys ACDEFGHIKLMNPQRSTVWY
  prophys ACDEFGHIKLMNPQRSTVWY --windows --window-size 5
  prophys ACDEFGHIKLMNPQRSTVWY --pretty
  echo "ACDEFGHIKLMNPQRSTVWY" | prophys -
        """
    )
    
    parser.add_argument(
        "sequence",
        help="Protein sequence (IUPAC amino acid alphabet) or '-' to read from stdin"
    )
    
    parser.add_argument(
        "-w", "--windows",
        action="store_true",
        help="Include window-level analysis"
    )
    
    parser.add_argument(
        "-s", "--window-size",
        type=int,
        default=9,
        help="Size of sliding window for window analysis (default: 9)"
    )
    
    parser.add_argument(
        "-p", "--pretty",
        action="store_true",
        help="Pretty-print JSON output"
    )
    
    args = parser.parse_args()
    
    # Read sequence
    if args.sequence == "-":
        sequence = sys.stdin.read().strip()
    else:
        sequence = args.sequence
    
    try:
        # Create analyzer and perform analysis
        analyzer = ProteinAnalyzer(sequence)
        
        # Get results
        json_kwargs = {}
        if args.pretty:
            json_kwargs = {"indent": 2, "sort_keys": True}
        
        result_json = analyzer.to_json(
            include_windows=args.windows,
            window_size=args.window_size,
            **json_kwargs
        )
        
        print(result_json)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
