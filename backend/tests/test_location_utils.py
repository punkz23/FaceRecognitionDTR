
from app.core.location_utils import calculate_distance
import pytest

def test_calculate_distance_same_point():
    """Test that distance between same points is 0."""
    lat, lon = 14.5995, 120.9842
    assert calculate_distance(lat, lon, lat, lon) == 0

def test_calculate_distance_known_points():
    """Test distance between two known points."""
    # Point A: Manila (14.5995, 120.9842)
    # Point B: Quezon City (approx 14.6760, 121.0437)
    # Distance is roughly 9.1 km
    dist = calculate_distance(14.5995, 120.9842, 14.6760, 121.0437)
    assert 9000 < dist < 9500 # Distance in meters

def test_calculate_distance_within_radius():
    """Test distance within a small radius."""
    # Approx 50 meters apart
    dist = calculate_distance(14.5995, 120.9842, 14.5996, 120.9845)
    assert dist < 100
