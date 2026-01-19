"""
Tests for validation utilities.
"""

import pytest
from prophys.validators import validate_sequence


def test_validate_valid_sequence():
    """Test validation of valid sequences."""
    is_valid, error = validate_sequence("ACDEFGHIKLMNPQRSTVWY")
    assert is_valid
    assert error == ""
    
    is_valid, error = validate_sequence("acdefghiklmnpqrstvwy")
    assert is_valid
    assert error == ""


def test_validate_empty_sequence():
    """Test validation of empty sequence."""
    is_valid, error = validate_sequence("")
    assert not is_valid
    assert "empty" in error.lower()


def test_validate_invalid_characters():
    """Test validation with invalid characters."""
    is_valid, error = validate_sequence("ACDEFGHIKLMNPQRSTVWYBXZ")
    assert not is_valid
    assert "invalid" in error.lower()
    assert "B" in error or "X" in error or "Z" in error


def test_validate_non_string():
    """Test validation with non-string input."""
    is_valid, error = validate_sequence(123)
    assert not is_valid
    assert "string" in error.lower()
