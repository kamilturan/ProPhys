"""
Example demonstrating the web service API.

This script shows how to:
1. Start the server
2. Make requests to the API
3. Process responses
"""

import requests
import json
import time
import subprocess
import sys
from multiprocessing import Process


def start_server_process():
    """Start the ProPhys server in a subprocess."""
    subprocess.Popen(
        [sys.executable, "-m", "prophys.server", "--host", "127.0.0.1", "--port", "5555"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Wait for server to start
    time.sleep(2)


def example_health_check():
    """Check server health."""
    print("=" * 60)
    print("Example 1: Health Check")
    print("=" * 60)
    
    response = requests.get("http://127.0.0.1:5555/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def example_basic_analysis():
    """Basic protein analysis via API."""
    print("=" * 60)
    print("Example 2: Basic Analysis")
    print("=" * 60)
    
    data = {
        "sequence": "MKTIIALSYIFCLVFA"
    }
    
    response = requests.post(
        "http://127.0.0.1:5555/analyze",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Request: {json.dumps(data, indent=2)}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
    print()


def example_window_analysis():
    """Analysis with window-level properties."""
    print("=" * 60)
    print("Example 3: Window Analysis")
    print("=" * 60)
    
    data = {
        "sequence": "ACDEFGHIKLMNPQRSTVWY",
        "include_windows": True,
        "window_size": 5
    }
    
    response = requests.post(
        "http://127.0.0.1:5555/analyze",
        json=data
    )
    
    result = response.json()
    print(f"Sequence: {result['sequence']}")
    print(f"Number of windows: {len(result.get('window_analysis', []))}")
    print(f"First 3 windows:")
    for window in result.get('window_analysis', [])[:3]:
        print(f"  Position {window['position']}: {window['window']}")
    print()


def example_error_handling():
    """Demonstrate error handling."""
    print("=" * 60)
    print("Example 4: Error Handling")
    print("=" * 60)
    
    # Invalid sequence
    data = {
        "sequence": "INVALID123"
    }
    
    response = requests.post(
        "http://127.0.0.1:5555/analyze",
        json=data
    )
    
    print(f"Request with invalid sequence: {data['sequence']}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def example_batch_analysis():
    """Analyze multiple sequences."""
    print("=" * 60)
    print("Example 5: Batch Analysis")
    print("=" * 60)
    
    sequences = [
        "ACDEFGHIKLMNPQRSTVWY",
        "MKTIIALSYIFCLVFA",
        "KKKKDDDDEEEERRRRR"
    ]
    
    results = []
    for seq in sequences:
        response = requests.post(
            "http://127.0.0.1:5555/analyze",
            json={"sequence": seq}
        )
        results.append(response.json())
    
    print(f"Analyzed {len(sequences)} sequences:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['sequence'][:20]}...")
        print(f"   MW: {result['molecular_weight']} Da, pI: {result['isoelectric_point']}")
    print()


def main():
    """Run all API examples."""
    print("Starting ProPhys server on port 5555...")
    start_server_process()
    
    try:
        # Wait a bit more to ensure server is ready
        time.sleep(2)
        
        # Run examples
        example_health_check()
        example_basic_analysis()
        example_window_analysis()
        example_error_handling()
        example_batch_analysis()
        
        print("=" * 60)
        print("All API examples completed!")
        print("=" * 60)
        print("\nNote: The server is still running on port 5555.")
        print("You can test it manually with curl:")
        print('  curl -X POST http://127.0.0.1:5555/analyze \\')
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"sequence": "ACDEFGHIKLMNPQRSTVWY"}\'')
        print("\nPress Ctrl+C to stop.")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure it's running.")
        sys.exit(1)


if __name__ == "__main__":
    main()
