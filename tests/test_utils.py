# -*- coding: utf-8 -*-
"""
Tests for utility functions.
"""
import pytest
from utils.common import is_valid_email, is_valid_age, get_family_coeff

# --- Tests for is_valid_email ---

def test_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("test.name@example.co.uk") == True

def test_invalid_email():
    assert is_valid_email("test@example") == False
    assert is_valid_email("test@.com") == False
    assert is_valid_email("test@example.") == False
    assert is_valid_email("plainaddress") == False
    assert is_valid_email("@missingusername.com") == False

# --- Tests for is_valid_age ---

def test_valid_age():
    assert is_valid_age("16") == True
    assert is_valid_age("30") == True
    assert is_valid_age("100") == True

def test_invalid_age():
    assert is_valid_age("15") == False
    assert is_valid_age("101") == False
    assert is_valid_age("abc") == False
    assert is_valid_age("25.5") == False
    assert is_valid_age(None) == False

# --- Tests for get_family_coeff ---

@pytest.mark.parametrize("family_n, expected_coeff", [
    (1, 1.0),
    (2, 1.57),
    (3, 2.04),
    (4, 2.46),
    (5, 2.85),
    (6, 3.20),  # 2.85 + 0.35
    (7, 3.55),  # 2.85 + 0.35 * 2
    (0, 1.0),   # Edge case
    (-1, 1.0)  # Edge case
])
def test_family_coefficient_calculation(family_n, expected_coeff):
    assert get_family_coeff(family_n) == pytest.approx(expected_coeff, 0.001)
