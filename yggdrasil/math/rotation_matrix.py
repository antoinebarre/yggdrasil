"""
 Math - Basic Rotations matrix tools
"""

from beartype import beartype
import numpy as np
from scipy.spatial.transform import Rotation
from ..types import  FloatNumber

__all__ = [
    "rotx",
    "roty",
    "rotz",
]

def rotx(theta: FloatNumber) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the X-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation around
        the X-axis.
    """
    return __fundamental_rotation(np.array([1.0, 0, 0]), theta)


def roty(theta: FloatNumber) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the Y-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation around
        the Y-axis.
    """
    return __fundamental_rotation(np.array([0, 1.0, 0]), theta)


def rotz(theta: FloatNumber) -> np.ndarray:
    """Generate a rotation matrix for a rotation around the Z-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation
        around the Z-axis.
    """
    return __fundamental_rotation(np.array([0, 0, 1.0]), theta)


@beartype
def __fundamental_rotation(
        axis: np.ndarray,
        theta: FloatNumber
        ) -> np.ndarray:
    """Create a rotation matrix based on angle and axis.

    Args:
        axis (Float64Array3): The rotation axis as a 3D vector.
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix.
    """
    theta = float(theta)
    return Rotation.from_rotvec(theta * axis.reshape((3,))).as_matrix().T
