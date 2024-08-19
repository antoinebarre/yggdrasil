"""
 Math - Basic Rotations matrix tools
"""

import numpy as np
from .matrix import Matrix

__all__ = [
    "rotx",
    "roty",
    "rotz",
]

def rotx(theta: float) -> Matrix:
    """Generate a rotation matrix for a rotation around the X-axis.

    Args:
        theta (float, np.float64): Angle in radians for the rotation.

    Returns:
        np.ndarray: 3x3 rotation matrix representing the rotation around
        the X-axis.
    """
    c, s = np.cos(theta), np.sin(theta)
    return Matrix(
        xx=1.0, xy=0.0, xz=0.0,
        yx=0.0, yy=c, yz=s,
        zx=0.0, zy=-s, zz=c
    )

def roty(theta: float) -> Matrix:
    """Generate a rotation matrix for a rotation around the Y-axis.

    Args:
        theta (float): Angle in radians for the rotation.

    Returns:
        Matrix: 3x3 rotation matrix representing the rotation around
        the Y-axis.
    """
    c, s = np.cos(theta), np.sin(theta)
    return Matrix(
        xx=c, xy=0.0, xz=-s,
        yx=0.0, yy=1.0, yz=0.0,
        zx=s, zy=0.0, zz=c
    )

def rotz(theta: float) -> Matrix:
    """Generate a rotation matrix for a rotation around the Z-axis.

    Args:
        theta (float): Angle in radians for the rotation.

    Returns:
        Matrix: 3x3 rotation matrix representing the rotation
        around the Z-axis.
    """
    c, s = np.cos(theta), np.sin(theta)
    return Matrix(
        xx=c, xy=s, xz=0.0,
        yx=-s, yy=c, yz=0.0,
        zx=0.0, zy=0.0, zz=1.0
   )
