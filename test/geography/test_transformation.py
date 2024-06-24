import pytest
import numpy as np
from yggdrasil.geography.geographic_position import GeographicPosition
from yggdrasil.geography.position import Position
from yggdrasil.earth.earth_ellipsoid_model import wgs84
from yggdrasil.geography.transformation import LLA2ECEF, ECEF2LLA


# Sample data
LLA4ECEF = [
    {"ECEF": [5117118.21, -1087677.05, 3638574.7],  # meter, meter, meter
     "LLA": [35., -12., 1234.]},  # lat, lon, alt (deg, deg, m)
    {"ECEF": [1193872.96, 1584322.93, -6064737.91],
     "LLA": [-72., 53., 22135.]}
]

@pytest.fixture(params=LLA4ECEF)
def lla_ecef_fixture(request):
    """
    Fixture that provides sample LLA and ECEF positions for testing.

    Args:
        request: The request object.

    Returns:
        dict: A dictionary containing the geographic_position and ecef_position.

    """
    data = request.param
    lla = data["LLA"]
    ecef = data["ECEF"]
    return {
        "geographic_position": GeographicPosition(
            latitude=np.deg2rad(lla[0]),
            longitude=np.deg2rad(lla[1]),
            altitude=lla[2],
            earth_ellispoid_model=wgs84()
        ),
        "ecef_position": Position(x=ecef[0], y=ecef[1], z=ecef[2])
    }

def test_LLA2ECEF(lla_ecef_fixture):  #pylint: disable=redefined-outer-name, invalid-name
    """
    Test the LLA2ECEF transformation function.

    Args:
        lla_ecef_fixture: The fixture providing the sample LLA and ECEF positions.

    """
    geo_pos = lla_ecef_fixture["geographic_position"]
    expected_ecef = lla_ecef_fixture["ecef_position"]

    ecef_pos = LLA2ECEF(geo_pos)

    assert isinstance(ecef_pos, Position)
    assert ecef_pos.x == pytest.approx(expected_ecef.x, rel=1e-2)
    assert ecef_pos.y == pytest.approx(expected_ecef.y, rel=1e-2)
    assert ecef_pos.z == pytest.approx(expected_ecef.z, rel=1e-2)

def test_ECEF2LLA(lla_ecef_fixture):
    """
    Test the ECEF2LLA transformation function.

    Args:
        lla_ecef_fixture: The fixture providing the sample LLA and ECEF positions.

    """
    ecef_pos = lla_ecef_fixture["ecef_position"]
    expected_geo_pos = lla_ecef_fixture["geographic_position"]

    geo_pos = ECEF2LLA(ecef_pos, wgs84())

    assert isinstance(geo_pos, GeographicPosition)
    assert geo_pos.latitude == pytest.approx(expected_geo_pos.latitude, rel=1e-6)
    assert geo_pos.longitude == pytest.approx(expected_geo_pos.longitude, rel=1e-6)
    assert geo_pos.altitude == pytest.approx(expected_geo_pos.altitude, rel=1e-1)

def test_round_trip_conversion(lla_ecef_fixture):  #pylint: disable=redefined-outer-name, invalid-name
    """
    Test the round trip conversion between LLA and ECEF positions.

    Args:
        lla_ecef_fixture: The fixture providing the sample LLA and ECEF positions.

    """
    initial_geo_pos = lla_ecef_fixture["geographic_position"]
    ecef_pos = LLA2ECEF(initial_geo_pos)
    converted_geo_pos = ECEF2LLA(ecef_pos, initial_geo_pos.earth_ellispoid_model)

    assert initial_geo_pos.isclose(converted_geo_pos, rel_tol=1e-9)
