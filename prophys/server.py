"""
Web service scaffold for ProPhys using Flask.
"""

from flask import Flask, request, jsonify
from prophys import ProteinAnalyzer, validate_sequence


app = Flask(__name__)


@app.route("/")
def index():
    """Root endpoint with API information."""
    return jsonify({
        "service": "ProPhys - Protein Physicochemical Profiling",
        "version": "0.1.0",
        "endpoints": {
            "/analyze": "POST - Analyze a protein sequence",
            "/health": "GET - Health check"
        },
        "example": {
            "endpoint": "/analyze",
            "method": "POST",
            "body": {
                "sequence": "ACDEFGHIKLMNPQRSTVWY",
                "include_windows": False,
                "window_size": 9
            }
        }
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze a protein sequence.
    
    Expected JSON body:
    {
        "sequence": "ACDEFGHIKLMNPQRSTVWY",
        "include_windows": false,  # optional
        "window_size": 9  # optional
    }
    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Validate input
    if "sequence" not in data:
        return jsonify({"error": "Missing required field: sequence"}), 400
    
    sequence = data["sequence"]
    include_windows = data.get("include_windows", False)
    window_size = data.get("window_size", 9)
    
    # Validate sequence
    is_valid, error_msg = validate_sequence(sequence)
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    # Validate window_size
    if not isinstance(window_size, int) or window_size < 1:
        return jsonify({"error": "window_size must be a positive integer"}), 400
    
    try:
        # Perform analysis
        analyzer = ProteinAnalyzer(sequence)
        result = analyzer.analyze(include_windows=include_windows, window_size=window_size)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


def run_server(host="0.0.0.0", port=5000, debug=False):
    """
    Run the Flask development server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ProPhys Web Service")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print(f"Starting ProPhys web service on {args.host}:{args.port}")
    run_server(host=args.host, port=args.port, debug=args.debug)
