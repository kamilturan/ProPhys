"""
Tests for the web service.
"""

import pytest
import json
from prophys.server import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test index endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "service" in data
    assert "ProPhys" in data["service"]


def test_health(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_analyze_valid_sequence(client):
    """Test analyze endpoint with valid sequence."""
    response = client.post('/analyze',
                          json={"sequence": "ACDEFGHIKLMNPQRSTVWY"},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["sequence"] == "ACDEFGHIKLMNPQRSTVWY"
    assert data["length"] == 20
    assert "molecular_weight" in data


def test_analyze_with_windows(client):
    """Test analyze endpoint with window analysis."""
    response = client.post('/analyze',
                          json={
                              "sequence": "ACDEFGHIKLMNPQRSTVWY",
                              "include_windows": True,
                              "window_size": 5
                          },
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "window_analysis" in data
    assert len(data["window_analysis"]) > 0


def test_analyze_missing_sequence(client):
    """Test analyze endpoint with missing sequence."""
    response = client.post('/analyze',
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_analyze_invalid_sequence(client):
    """Test analyze endpoint with invalid sequence."""
    response = client.post('/analyze',
                          json={"sequence": "ACDEFGXYZ"},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_analyze_invalid_content_type(client):
    """Test analyze endpoint with non-JSON content."""
    response = client.post('/analyze',
                          data="not json",
                          content_type='text/plain')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_analyze_invalid_window_size(client):
    """Test analyze endpoint with invalid window size."""
    response = client.post('/analyze',
                          json={
                              "sequence": "ACDEFGHIKLMNPQRSTVWY",
                              "window_size": -5
                          },
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_not_found(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
