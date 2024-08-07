"""
firefly - geographic rotation matrix
"""

# PYLINT rules
# pylint: disable=C0103

# EXPORT
__all__ = [
    "dcm_eci2ecef",
    "dcm_ecef2enu",
    "dcm_ecef2ned",
    "dcm2angle",
    "angle2dcm",
]

# IMPORT
from typing import Union
from beartype import beartype
import numpy as np

from ..earth import EarthConstants
from ..math import rotx, roty, rotz, Matrix
from ..utils.argument_validation.float import (
    validate_positive_float,
    validate_float)


def dcm_eci2ecef(
        dt: float,
        earth_rotation_rate: float = EarthConstants.earth_rotation_rate
        ) -> Matrix:
    """Provide the Direct Cosine Matrix to convert Earth-centered inertial
     (ECI) to Earth-centered Earth-fixed (ECEF) coordinates

    - The x-axis points towards the vernal equinox (First Point of Aries ♈).
    - The y-axis points 90 degrees to the east of the x-axis in the equatorial
        plane.
    - The z-axis points northward along the Earth rotation axis.

    Args:
        dt (float): time in second since the user defined the Earth Center
        Inertial (ECI) frame. This value shall be positive (>=0)
        earth_rotation_rate (float, optional): Earth rotation rate in rad/s.
         Defaults to EarthConstants.earth_rotation_rate (WGS-84).

    Returns:
        Matrix: rotational matrix [3x3] to transform a vector in ECI in
        the ECEF frame
    """

    # voir https://github.com/NavPy/NavPy/blob/master/navpy/core/navpy.py

    rot_angle = validate_positive_float(earth_rotation_rate * dt)

    return rotz(rot_angle)



def dcm_ecef2ned(
        latitude: float,
        longitude: float
        ) -> Matrix:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth
    Fixed) to NED (North Earth Down) to transform a vector defined in ECEF
    to NED frame

    Args:
        latitude (float): latitude of the geographical
          point in radians
        longitude (float): longitude of the geographical
          point in radians

    Returns:
        Matrix: Direct Cosinus Matrix from ECEF to NED
    """
    lat = validate_float(latitude)
    long = validate_float(longitude)

    return  roty(-np.pi/2) @ (roty(-lat) @ rotz(long))


def dcm_ecef2enu(
        latitude: float,
        longitude: float
        ) -> Matrix:
    """Calculate the rotational matrix from the ECEF (Earth Centered Earth
     Fixed) to ENU (East North Up) to transform a vector defined in ECEF to
     ENU frame

    Args:
        latitude (float): latitude of the geographical
          point in radians
        longitude (float): longitude of the geographical
          point in radians

    Reference:
        https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates

    Returns:
        Matrix: Direct Cosinus Matrix from ECEF to ENU
    """
    lat = validate_float(latitude)
    long = validate_float(longitude)

    return (
        rotx(np.pi / 2) @ (rotz(np.pi / 2) @ (roty(-lat) @ rotz(long)))
    )


def angle2dcm(rotAngle1: float,
              rotAngle2: float,
              rotAngle3: float,
              rotationSequence: str = 'ZYX'
              ) -> Matrix:
    """This function converts Euler Angle into Direction Cosine Matrix (DCM).
    Args:
        rotAngle1 (float, np.float64): first angle of roation in radians
            (e.g. yaw for 'ZYX')
        rotAngle2 (float, np.float64): second angle of roation in radians
            (e.g. pitch for 'ZYX')
        rotAngle3 (float, np.float64): third angle of roation in radians
            (e.g. roll for 'ZYX')
        rotationSequence (str, optional): sequence of rotations.
            Defaults to 'ZYX'.

    Returns:
        np.ndarray: direction cosine matrix associated to the rotation angles
    """

    # validate the input
    validate_float(rotAngle1)
    validate_float(rotAngle2)
    validate_float(rotAngle3)

    if rotationSequence.upper() == "ZYX":
        return rotx(rotAngle3) @ roty(rotAngle2) @ rotz(rotAngle1)
    msg = (f"Rotation sequence {rotationSequence.upper()}"
           " is not implemented.")
    raise NotImplementedError(msg)


def dcm2angle(
        dcm: Matrix,
        rotationSequence: str = 'ZYX'
        ) -> tuple[float, float, float]:
    """This function converts a Direction Cosine Matrix (DCM) into the three
    rotation angles.

    Notes:
    The returned rotAngle1 and 3 will be between   +/- 180 deg (+/- pi rad).
    In contrast, rotAngle2 will be in the interval +/- 90 deg (+/- pi/2 rad).
    In the 'ZYX' or '321' aerospace sequence, that means the pitch angle
    returned will always be inside the closed interval +/- 90 deg
    (+/- pi/2 rad).
    Applications where pitch angles near or larger than 90 degrees
    in magnitude are expected should used alternate attitude parameterizations
    like quaternions.

    Args:
        dcm (Matrix): direction cosine matrix associated
            to the rotation angles
        rotationSequence (str, optional): sequence of rotations.
            Defaults to 'ZYX'.

    Returns:
        rotAngle1 (float): first angle of roation in radians
            (e.g. yaw for 'ZYX')
        rotAngle2 (float): second angle of roation in radians
            (e.g. pitch for 'ZYX')
        rotAngle3 (float): third angle of roation in radians
            (e.g. roll for 'ZYX')
    """

    # validate the input
    Matrix.validate_matrix(dcm)


    if rotationSequence.upper() == "ZYX":
        rotAngle1 = np.arctan2(dcm[0, 1], dcm[0, 0])   # Yaw
        rotAngle2 = -np.arcsin(dcm[0, 2])  # Pitch
        rotAngle3 = np.arctan2(dcm[1, 2], dcm[2, 2])  # Roll

        return rotAngle1, rotAngle2, rotAngle3
    #TODO : implement test based on Mathworks test
    else:
        msg = (f"Rotation sequence {rotationSequence.upper()}"
               " is not implemented.")
        raise NotImplementedError(msg)
