# ProPhys

**ProPhys** is a Python toolkit + web service scaffold for protein physicochemical profiling.

Given a protein sequence (IUPAC amino-acid alphabet), ProPhys computes a rich set of sequence-level and window-level properties as clean, JSON-serializable outputs—ready for downstream analytics, feature engineering, and classical ML workflows.

## Features

- **Sequence-level properties:**
  - Amino acid composition
  - Molecular weight
  - Isoelectric point (pI)
  - GRAVY (Grand Average of Hydropathy)
  - Aromaticity
  - Instability index
  - Net charge at pH 7.0

- **Window-level analysis:**
  - Sliding window analysis for local properties
  - Configurable window size
  - Local hydrophobicity, aromaticity, and charge profiles

- **JSON-serializable output:**
  - Clean, structured data format
  - Ready for downstream processing
  - Compatible with ML pipelines

- **Web service scaffold:**
  - RESTful API using Flask
  - Easy integration with existing systems
  - Health check and analysis endpoints

- **Command-line interface:**
  - Simple CLI for quick analysis
  - Pipeline-friendly (stdin/stdout support)
  - Pretty-print option

## Installation

### From source

```bash
git clone https://github.com/kamilturan/ProPhys.git
cd ProPhys
pip install -e .
```

### Dependencies

- Python ≥ 3.8
- Flask ≥ 2.0.0

## Usage

### Python API

```python
from prophys import ProteinAnalyzer

# Create analyzer with a protein sequence
analyzer = ProteinAnalyzer("ACDEFGHIKLMNPQRSTVWY")

# Get sequence-level properties
print(f"Molecular weight: {analyzer.molecular_weight()} Da")
print(f"Isoelectric point: {analyzer.isoelectric_point()}")
print(f"GRAVY: {analyzer.gravy()}")
print(f"Aromaticity: {analyzer.aromaticity()}")

# Get complete analysis as dictionary
results = analyzer.analyze()

# Get complete analysis as JSON
json_output = analyzer.to_json(indent=2)
print(json_output)

# Include window-level analysis
results_with_windows = analyzer.analyze(include_windows=True, window_size=9)
```

### Command-line Interface

```bash
# Basic analysis
prophys ACDEFGHIKLMNPQRSTVWY

# With window analysis
prophys ACDEFGHIKLMNPQRSTVWY --windows --window-size 5

# Pretty-printed output
prophys ACDEFGHIKLMNPQRSTVWY --pretty

# Read from stdin
echo "ACDEFGHIKLMNPQRSTVWY" | prophys -

# Pipeline example
cat sequences.txt | prophys - > results.json
```

### Web Service

Start the web server:

```bash
# Using the CLI command
prophys-server --host 0.0.0.0 --port 5000

# Or using Python
python -m prophys.server --host 0.0.0.0 --port 5000
```

API endpoints:

**GET /** - Service information and usage examples

**GET /health** - Health check

**POST /analyze** - Analyze a protein sequence

Example request:

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "sequence": "ACDEFGHIKLMNPQRSTVWY",
    "include_windows": false,
    "window_size": 9
  }'
```

Example response:

```json
{
  "sequence": "ACDEFGHIKLMNPQRSTVWY",
  "length": 20,
  "molecular_weight": 2395.69,
  "isoelectric_point": 6.04,
  "gravy": -0.785,
  "aromaticity": 0.15,
  "instability_index": 10.0,
  "charge_at_ph7": -0.993,
  "amino_acid_composition": {
    "A": 5.0,
    "C": 5.0,
    ...
  }
}
```

## Output Format

ProPhys generates JSON-serializable output with the following structure:

### Sequence-level properties

```json
{
  "sequence": "ACDEFGHIKLMNPQRSTVWY",
  "length": 20,
  "molecular_weight": 2395.69,
  "isoelectric_point": 6.04,
  "gravy": -0.785,
  "aromaticity": 0.15,
  "instability_index": 10.0,
  "charge_at_ph7": -0.993,
  "amino_acid_composition": {
    "A": 5.0,
    "C": 5.0,
    "D": 5.0,
    ...
  }
}
```

### Window-level properties (optional)

When `include_windows=True`:

```json
{
  ...
  "window_analysis": [
    {
      "position": 1,
      "window": "ACDEFGHIK",
      "hydrophobicity": -1.322,
      "aromaticity": 0.111,
      "charge": -1
    },
    ...
  ]
}
```

## Development

### Setup development environment

```bash
# Clone the repository
git clone https://github.com/kamilturan/ProPhys.git
cd ProPhys

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Run tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=prophys --cov-report=html

# Run specific test file
pytest tests/test_properties.py
```

### Project Structure

```
ProPhys/
├── prophys/              # Main package
│   ├── __init__.py       # Package initialization
│   ├── constants.py      # Physicochemical constants
│   ├── validators.py     # Sequence validation
│   ├── properties.py     # Core property calculations
│   ├── cli.py            # Command-line interface
│   └── server.py         # Web service (Flask)
├── tests/                # Test suite
│   ├── test_validators.py
│   ├── test_properties.py
│   └── test_server.py
├── setup.py              # Package setup (setuptools)
├── pyproject.toml        # Package configuration (PEP 517/518)
├── requirements.txt      # Runtime dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md             # This file
```

## Physicochemical Properties

### Molecular Weight

Calculated as the sum of amino acid residue weights minus water molecules lost in peptide bond formation.

### Isoelectric Point (pI)

The pH at which the protein has no net charge. Calculated using Henderson-Hasselbalch equation with standard pKa values.

### GRAVY (Grand Average of Hydropathy)

Average hydrophobicity score using the Kyte-Doolittle scale. Positive values indicate hydrophobic proteins, negative values indicate hydrophilic proteins.

### Aromaticity

The fraction of aromatic amino acids (F, W, Y) in the sequence.

### Instability Index

Predicts protein stability. Values < 40 suggest stable proteins, values > 40 suggest unstable proteins.

### Charge at pH 7

Net charge of the protein at physiological pH (7.0).

### Window Analysis

Sliding window analysis computes local properties across the sequence, useful for identifying:
- Hydrophobic/hydrophilic regions
- Transmembrane domains
- Signal peptides
- Disordered regions

## Use Cases

- **Protein characterization** - Quick profiling of physicochemical properties
- **Feature engineering** - Generate features for ML models
- **Comparative analysis** - Compare properties across protein variants
- **Quality control** - Validate synthesized or engineered proteins
- **Drug discovery** - Screen protein candidates based on properties
- **Bioinformatics pipelines** - Integrate with existing workflows

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use ProPhys in your research, please cite:

```
ProPhys: A Python toolkit for protein physicochemical profiling
https://github.com/kamilturan/ProPhys
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.