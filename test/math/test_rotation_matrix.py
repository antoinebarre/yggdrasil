# import module
import pytest
import numpy as np
from yggdrasil.math.rotation_matrix import rotx, roty, rotz
from yggdrasil.math.vector import Vector

ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6
NB_OBJ = 100



def test_rotx_error():
    """Check appropriate behavior with wrong inputs"""
    with pytest.raises(Exception):
        rotx("a") # type: ignore
    with pytest.raises(Exception):
        rotx([1, 2]) # type: ignore


@pytest.mark.parametrize("angle", np.random.uniform(low=-6 * np.pi, high=6 * np.pi, size=NB_OBJ))
def test_rotx_determinant(angle):
    """The function rotx shall have a determinant equal to 1"""
    det = np.linalg.det(rotx(angle))
    message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [current: {det}]"
    assert det == pytest.approx(1.0, abs=ABSOLUTE_TOLERANCE, rel=RELATIVE_TOLERANCE), message


@pytest.mark.parametrize("angle, vector, expected", [
    (90, Vector(10, 0, 0), Vector(10, 0, 0)),
    (90, Vector(0, 9, 0), Vector(0, 0, -9)),
    (90, Vector(0, 0, 4), Vector(0, 4, 0)),
    (180, Vector(0, 3, 0), Vector(0, -3, 0)),
    (270, Vector(0, 3, 0), Vector(0, 0, 3)),
])
def test_rotx_behaviour(angle, vector, expected):
    X = rotx(np.deg2rad(angle)) @ vector
    assert X.is_close(expected, tol=ABSOLUTE_TOLERANCE), f"Expected {expected} but got {X}"


@pytest.mark.parametrize("angle", np.random.uniform(low=-6 * np.pi, high=6 * np.pi, size=NB_OBJ))
def test_roty_determinant(angle):
    """The function roty shall have a determinant equal to 1"""
    det = np.linalg.det(roty(angle))
    message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [current: {det}]"
    assert det == pytest.approx(1.0, abs=ABSOLUTE_TOLERANCE, rel=RELATIVE_TOLERANCE), message


@pytest.mark.parametrize("angle, vector, expected", [
    (90, Vector(0, 10, 0), Vector(0, 10, 0)),
    (90, Vector(4, 0, 0), Vector(0, 0, 4)),
    (90, Vector(0, 0, 4), Vector(-4, 0, 0)),
    (180, Vector(3, 0, 0), Vector(-3, 0, 0)),
    (270, Vector(3, 0, 0), Vector(0, 0, -3)),
])
def test_roty_behaviour(angle, vector, expected):
    X = roty(np.deg2rad(angle)) @ vector
    assert X.is_close(expected, tol=ABSOLUTE_TOLERANCE), f"Expected {expected} but got {X}"


def test_roty_error():
    """Check appropriate behavior with wrong inputs"""
    with pytest.raises(Exception):
        roty("a") # type: ignore

    with pytest.raises(Exception):
        roty([1, 2]) # type: ignore


@pytest.mark.parametrize("angle", np.random.uniform(low=-6 * np.pi, high=6 * np.pi, size=NB_OBJ))
def test_rotz_determinant(angle):
    """The function rotz shall have a determinant equal to 1"""
    det = np.linalg.det(rotz(angle))
    message = f"For an angle of the determinant of a rotation matrix shall be equal to 1.0 [current: {det}]"
    assert det == pytest.approx(1.0, abs=ABSOLUTE_TOLERANCE, rel=RELATIVE_TOLERANCE), message


@pytest.mark.parametrize("angle, vector, expected", [
    (90, Vector(0, 0, 10), Vector(0, 0, 10)),
    (90, Vector(4, 0, 0), Vector(0, -4, 0)),
    (90, Vector(0, 4, 0), Vector(4, 0, 0)),
    (180, Vector(3, 0, 0), Vector(-3, 0, 0)),
    (270, Vector(3, 0, 0), Vector(0, 3, 0)),
])
def test_rotz_behaviour(angle, vector, expected):
    X = rotz(np.deg2rad(angle)) @ vector
    assert X.is_close(expected, tol=ABSOLUTE_TOLERANCE), f"Expected {expected} but got {X}"


def test_rotz_error():
    """Check appropriate behavior with wrong inputs"""
    with pytest.raises(Exception):
        rotz("a") # type: ignore
    with pytest.raises(Exception):
        rotz([1, 2]) # type: ignore

#---------------- TOOLS ----------------
def compare_column_vector(X: Vector, X_expected: Vector, tol: float = ABSOLUTE_TOLERANCE):
    """
    Compare two column vectors and assert if they are not close within a given tolerance.

    Parameters:
        X (Vector): The actual column vector.
        X_expected (Vector): The expected column vector.
        tol (float, optional): The tolerance value. Defaults to ABSOLUTE_TOLERANCE.

    Raises:
        AssertionError: If the actual column vector is not close to the expected column vector.

    """
    assert X.is_close(X_expected, tol=tol), f"Expected {X_expected} but got {X}"

def apply_rotx(angle: float, X0: Vector) -> Vector:
    """Apply rotation around x-axis"""
    return rotx(np.deg2rad(angle)) @ X0

def apply_roty(angle: float, X0: Vector) -> Vector:
    """Apply rotation around y-axis"""
    return roty(np.deg2rad(angle)) @ X0

def apply_rotz(angle: float, X0: Vector) -> Vector:
    """Apply rotation around z-axis"""
    return rotz(np.deg2rad(angle)) @ X0
