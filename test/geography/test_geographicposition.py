import pytest
import math

from yggdrasil.geography.geographic_position import GeographicPosition
from yggdrasil.earth.earth_model import  wgs84


def test_geographic_position_initialization():
    """
    Test the initialization of the GeographicPosition class.
    """
    earth_model = wgs84()
    geo_pos = GeographicPosition(
        latitude=math.radians(52.2296756),
        longitude=math.radians(21.0122287),
        altitude=100.0,
        earth_model=earth_model
    )
    assert geo_pos.latitude == math.radians(52.2296756)
    assert geo_pos.longitude == math.radians(21.0122287)
    assert geo_pos.altitude == 100.0
    assert geo_pos.earth_model == earth_model

    with pytest.raises(TypeError):
        GeographicPosition(
            latitude="not a float",
            longitude=math.radians(21.0122287),
            altitude=100.0,
            earth_model=earth_model
        )

def test_geographic_position_str_and_repr():
    """
    Test the string and representation methods of the GeographicPosition class.
    """
    earth_model = wgs84()
    geo_pos = GeographicPosition(
        latitude=math.radians(52.2296756),
        longitude=math.radians(21.0122287),
        altitude=100.0,
        earth_model=earth_model
    )
    assert str(geo_pos) == (
        f"GeographicPosition(latitude={math.radians(52.2296756)}, "
        f"longitude={math.radians(21.0122287)}, altitude={100.0})"
    )
    assert repr(geo_pos) == (
        f"GeographicPosition(latitude={math.radians(52.2296756)}, "
        f"longitude={math.radians(21.0122287)}, altitude={100.0})"
    )


def test_geographic_position_equality():
    """
    Test the equality comparison of the GeographicPosition class.
    """
    earth_model = wgs84()
    geo_pos1 = GeographicPosition(
        latitude=math.radians(52.2296756),
        longitude=math.radians(21.0122287),
        altitude=100.0,
        earth_model=earth_model
    )
    geo_pos2 = GeographicPosition(
        latitude=math.radians(52.2296756),
        longitude=math.radians(21.0122287),
        altitude=100.0,
        earth_model=earth_model
    )
    geo_pos3 = GeographicPosition(
        latitude=math.radians(40.712776),
        longitude=math.radians(-74.005974),
        altitude=10.0,
        earth_model=earth_model
    )

    assert geo_pos1 == geo_pos2
    assert geo_pos1 != geo_pos3

    with pytest.raises(ValueError):
        geo_pos1 == "not a geographic position"


def test_geographic_position_isclose():
    """
    Test the isclose method of the GeographicPosition class.
    """
    earth_model = wgs84()
    geo_pos1 = GeographicPosition(
        latitude=math.radians(52.2296756),
        longitude=math.radians(21.0122287),
        altitude=100.0,
        earth_model=earth_model
    )
    geo_pos2 = GeographicPosition(
        latitude=math.radians(52.2296756 + 1e-10),
        longitude=math.radians(21.0122287 + 1e-10),
        altitude=100.0 + 1e-10,
        earth_model=earth_model
    )
    
    assert geo_pos1.isclose(geo_pos2, rel_tol=1e-9)

    geo_pos3 = GeographicPosition(
        latitude=math.radians(40.712776),
        longitude=math.radians(-74.005974),
        altitude=10.0,
        earth_model=earth_model
    )

    assert not geo_pos1.isclose(geo_pos3, rel_tol=1e-9)

