
import math
from beartype import beartype
import numpy as np
from .position import Position
from .geographic_position import GeographicPosition
from ..earth import EllipsoidModel, wgs84

@beartype
def LLA2ECEF(  #pylint: disable=invalid-name
    LLA : GeographicPosition) -> Position:  #pylint: disable=invalid-name
    """
    Creates a Position object from latitude, longitude, and altitude.

    Args:
        LLA (GeographicPosition): The geographic position object.

    Returns:
        Position: The Position object.
    """
    # constante
    a = LLA.earth_model.a
    e2 = LLA.earth_model.e**2

    # transofrmation algorithm
    sinlat = np.sin(LLA.latitude)
    coslat = np.cos(LLA.latitude)

    N = a / np.sqrt(1 - e2 * sinlat**2)

    # Calculate ECEF position
    X = (N + LLA.altitude) * coslat * np.cos(LLA.longitude)
    Y = (N + LLA.altitude) * coslat * np.sin(LLA.longitude)
    Z = (N*(1 - e2) + LLA.altitude) * sinlat

    return Position(X, Y, Z)


@beartype
def ECEF2LLA(
    X_ECEF: Position, #pylint: disable=invalid-name
    ellipsoid: EllipsoidModel = wgs84()
) -> 'GeographicPosition':
    """
    Converts a position in Earth-Centered Earth-Fixed (ECEF) coordinates to
    geographic coordinates.

    Args:
        X_ECEF (Position): The position in ECEF coordinates.
        ellipsoid (EllipsoidModel, optional): The ellipsoid model to use for
        the conversion. Defaults to WGS84.

    Returns:
        GeographicPosition: The position in geographic coordinates (latitude,
        longitude, altitude).

    Raises:
        None

    References:
        - Bowring, B.R. (1976). "Transformation from spatial to geographical coordinates".
        Survey Review. 23 (181): 323–327.
        - See more details at: https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
    """

    # constante
    a = ellipsoid.a
    b = ellipsoid.b
    f = ellipsoid.f
    e = ellipsoid.e
    e2 = e**2       # Square of first eccentricity
    ep2 = e2 / (1 - e2)    # Square of second eccentricity

    # Longitude
    longitude = math.atan2(X_ECEF.y, X_ECEF.x)

    # Distance from Z-axis
    D = math.hypot(X_ECEF.x, X_ECEF.y)

    # Bowring's formula for initial parametric
    # (beta) and geodetic (phi) latitudes
    beta = math.atan2(X_ECEF.z, (1 - f) * D)
    phi = math.atan2(X_ECEF.z + b * ep2 * math.sin(beta)**3,
                        D - a * e2 * math.cos(beta)**3)

    # Fixed-point iteration with Bowring's formula
    # (typically converges within two or three iterations)
    beta_new = math.atan2((1 - f)*math.sin(phi), math.cos(phi))
    count = 0

    while beta != beta_new and count < 1000:

        beta = beta_new
        phi = math.atan2(X_ECEF.z + b * ep2 * math.sin(beta)**3,
                            D - a * e2 * math.cos(beta)**3)
        beta_new = math.atan2((1 - f)*math.sin(phi),
                                math.cos(phi))
        count += 1

    # Calculate ellipsoidal height from the final value for latitude
    sinphi = math.sin(phi)
    N = a / math.sqrt(1 - e2 * sinphi**2)
    altitude = D * math.cos(phi) + (X_ECEF.z + e2 * N * sinphi) * sinphi - N

    latitude = phi

    # voir https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
    return GeographicPosition(
        latitude=latitude,
        longitude=longitude,
        altitude=altitude,
        earth_model=ellipsoid)
