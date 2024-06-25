""" 

This module contains unit tests for the gravity function.

"""

import numpy as np

# MODULE IMPORT
from yggdrasil.geography.geographic_position import GeographicPosition
from yggdrasil.geography.transformation import LLA2ECEF
from yggdrasil.earth.earth_ellipsoid_model import  wgs84
from yggdrasil.earth.gravity import gravity

ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6

def test_equator_WGS84():  # pylint: disable=C0103
    """
    Test the gravity function at the equator using the WGS84 ellipsoid model.

    The expected gravity vector at the equator is [-9.814197355899799, 0., 0.].

    """
    g_expected = [-9.814197355899799, 0., 0.]

    pos2test = LLA2ECEF(GeographicPosition(
        latitude=0.,
        longitude=0.,
        altitude=0.,
        earth_ellispoid_model=wgs84()))

    g_list = gravity(position=pos2test)

    np.testing.assert_allclose(
            g_list,
            g_expected,
            atol=ABSOLUTE_TOLERANCE,
            rtol=RELATIVE_TOLERANCE)

def test_NorthPole_WGS84():  # pylint: disable=C0103
    """
    Test the gravity function at the North Pole using the WGS84 ellipsoid model.

    The expected gravity vector at the North Pole is [0., 0., -9.83206684120325].

    """
    g_expected = [0., 0., -9.83206684120325]

    pos2test = LLA2ECEF(GeographicPosition(
        latitude=np.deg2rad(90),
        longitude=0.,
        altitude=0.,
        earth_ellispoid_model=wgs84()))

    g_list = gravity(
        position=pos2test
        )
    np.testing.assert_array_almost_equal(
        g_list,
        g_expected)
