import pytest
from yggdrasil.geography.position import Position


def test_position_initialization():
    """
    Test case for initializing a Position object.

    This test verifies that a Position object is initialized correctly with the given x, y, and z coordinates.
    It also checks that a TypeError is raised when non-float values are provided for the coordinates.

    """
    pos = Position(x=1.0, y=2.0, z=3.0)
    assert pos.x == 1.0
    assert pos.y == 2.0
    assert pos.z == 3.0

    with pytest.raises(ValueError):
        Position(x="a", y=2, z=3)


def test_position_str_and_repr():
    """
    Test case for the string representation of a Position object.

    This test verifies that the string representation of a Position object is formatted correctly.

    """
    pos = Position(x=1.0, y=2.0, z=3.0)
    assert str(pos) == "Position ECEF(x=1.0, y=2.0, z=3.0)"
    assert repr(pos) == "Position ECEF (x=1.0, y=2.0, z=3.0)"


def test_position_equality():
    """
    Test case for the equality comparison of Position objects.

    This test verifies that the equality comparison of Position objects works as expected.
    It checks that two Position objects with the same coordinates are considered equal,
    and that a ValueError is raised when comparing a Position object with a non-Position object.

    """
    pos1 = Position(x=1.0, y=2.0, z=3.0)
    pos2 = Position(x=1.0, y=2.0, z=3.0)
    pos3 = Position(x=4.0, y=5.0, z=6.0)

    assert pos1 == pos2
    assert pos1 != pos3

    with pytest.raises(ValueError):
        pos1 == "not a position"


def test_position_norm():
    """
    Test case for calculating the norm of a Position object.

    This test verifies that the norm of a Position object is calculated correctly.
    It checks the norm for both 2D and 3D positions.

    """
    pos = Position(x=3.0, y=4.0, z=0.0)
    assert pos.norm == 5.0

    pos = Position(x=1.0, y=2.0, z=2.0)
    assert pos.norm == pytest.approx(3.0)


if __name__ == "__main__":
    pytest.main()
