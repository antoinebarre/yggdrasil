"""
--------------   GRAVITY MODEL  --------------
"""

# PYLINT rules
# pylint: disable=C0103

# EXPORT
__all__ = [
    "gravity",
]

from ..geography.position import Position
from .earth_ellipsoid_model import EllipsoidModel, earth_ellipsoid_model
from .constants import EarthConstants


def gravity(
        position: Position,
        earth_model: EllipsoidModel = earth_ellipsoid_model()
        ) -> tuple[float,float,float]:
    """
    Calculate the gravitational acceleration vector at a given position on Earth.

    Args:
        position (Position): The position at which to calculate
            the gravitational acceleration.
        earth_model (str, optional): The Earth model to use for
            the calculation. Defaults to DEFAULT_EARTH_MODEL.

    Returns:
        list[float]: The gravitational acceleration vector [gx, gy, gz]
            in meters per second squared.

    Examples:
        >>> position = Position(x=0, y=0, z=6371000)
        >>> gravity(position)
        (-9.819649, 0.0, 0.0)
    """

    # get constant
    a = earth_model.a
    mu = EarthConstants.mu
    j2 = earth_model.j2

    # get norm of ECEF coordinate
    r = position.norm

    # Common factors in the gravity components
    common_factor = -mu / r**2
    j2_factor = 3/2 * j2 * (a/r)**2
    z_factor = (position.z/r)**2

    gx = common_factor * (1 + j2_factor * (1 - 5 * z_factor)) * position.x / r
    gy = common_factor * (1 + j2_factor * (1 - 5 * z_factor)) * position.y / r
    gz = common_factor * (1 + j2_factor * (3 - 5 * z_factor)) * position.z / r

    return (gx, gy, gz)
