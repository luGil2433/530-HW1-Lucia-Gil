# pylint: disable=import-error, redefined-outer-name
"""Unit tests for the GPS distance calculator module using pytest."""

import pytest
from gps_distance import (
    clean_input,
    parse_degrees_to_decimal,
    validate_coordinates,
    calculate_haversine_distance,
    find_closest_points,
    get_coordinates_from_user
)

@pytest.fixture
def test_coordinates():
    """Fixture providing sets of coordinates for testing."""
    return {
        'new_york': (40.7128, -74.0060),
        'los_angeles': (34.0522, -118.2437),
        'boston': (42.3601, -71.0589),
        'chicago': (41.8781, -87.6298),
        'london': (51.5074, -0.1278),
        'paris': (48.8566, 2.3522)
    }

@pytest.mark.parametrize("input_str,expected", [
    ("42°30'10\"", "423010"),
    ("42 30 10", "423010"),
    ("42°30'10\"", "423010"),
    ("42 ° 30 ' 10 \"", "423010"),
])
def test_clean_input(input_str, expected):
    """Test input string cleaning function."""
    assert clean_input(input_str) == expected

@pytest.mark.parametrize("input_str,expected", [
    ("423010", 42.50277777777778),  # 42°30'10"
    ("401500", 40.25),              # 40°15'00"
    ("900000", 90.0),               # 90°00'00"
])
def test_parse_degrees_to_decimal(input_str, expected):
    """Test conversion from degrees format to decimal."""
    assert pytest.approx(parse_degrees_to_decimal(input_str), rel=1e-8) == expected

@pytest.mark.parametrize("lat,lon", [
    (0, 0),
    (90, 180),
    (-90, -180),
    (45.5, -120.5),
])
def test_validate_coordinates_valid(lat, lon):
    """Test valid coordinate validation."""
    validate_coordinates(lat, lon)  # Should not raise any exception

@pytest.mark.parametrize("lat,lon", [
    (91, 0),     # Invalid latitude
    (-91, 0),    # Invalid latitude
    (0, 181),    # Invalid longitude
    (0, -181),   # Invalid longitude
])
def test_validate_coordinates_invalid(lat, lon):
    """Test invalid coordinate validation."""
    with pytest.raises(ValueError):
        validate_coordinates(lat, lon)

@pytest.mark.parametrize("point1,point2,expected,tolerance", [
    # New York to Los Angeles (approximate)
    ((40.7128, -74.0060), (34.0522, -118.2437), 3935.75, 50),
    # London to Paris (approximate)
    ((51.5074, -0.1278), (48.8566, 2.3522), 343.47, 5),
    # Same point (should be 0)
    ((42.3601, -71.0589), (42.3601, -71.0589), 0, 0.1),
    # Antipodes (should be ~20,000 km)
    ((0, 0), (0, 180), 20015.09, 100),
])
def test_calculate_haversine_distance(point1, point2, expected, tolerance):
    """Test distance calculation between two points."""
    lat1, lon1 = point1
    lat2, lon2 = point2
    distance = calculate_haversine_distance(lat1, lon1, lat2, lon2)
    assert abs(distance - expected) <= tolerance

def test_find_closest_points(test_coordinates):
    """Test finding closest points between two sets."""
    set1 = [test_coordinates['new_york']]
    set2 = [
        test_coordinates['los_angeles'],
        test_coordinates['boston'],
        test_coordinates['chicago']
    ]
    matches = find_closest_points(set1, set2)
    assert len(matches) == 1
    assert matches[0][2] == test_coordinates['boston']

def test_get_coordinates_decimal_format(monkeypatch):
    """Test coordinate input in decimal format."""
    inputs = iter([
        "1",  # Choose decimal format
        "40.7128,-74.0060",  # New York coordinates
        "no"   # Don't add more coordinates
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    coordinates = get_coordinates_from_user("Enter coordinates: ")
    assert len(coordinates) == 1
    assert pytest.approx(coordinates[0][0], rel=1e-4) == 40.7128
    assert pytest.approx(coordinates[0][1], rel=1e-4) == -74.0060

def test_get_coordinates_multiple_inputs(monkeypatch):
    """Test entering multiple coordinates."""
    inputs = iter([
        "1",  # Choose decimal format
        "40.7128,-74.0060; 34.0522,-118.2437",  # New York and LA coordinates
        "no"   # Don't add more coordinates
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    coordinates = get_coordinates_from_user("Enter coordinates: ")
    assert len(coordinates) == 2
    assert pytest.approx(coordinates[0][0], rel=1e-4) == 40.7128
    assert pytest.approx(coordinates[1][0], rel=1e-4) == 34.0522

def test_get_coordinates_invalid_input(monkeypatch):
    """Test handling of invalid coordinate input."""
    inputs = iter([
        "1",  # Choose decimal format
        "invalid",  # Invalid input
        "40.7128,-74.0060",  # Valid input
        "no"   # Don't add more coordinates
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    coordinates = get_coordinates_from_user("Enter coordinates: ")
    assert len(coordinates) == 1
    assert pytest.approx(coordinates[0][0], rel=1e-4) == 40.7128
