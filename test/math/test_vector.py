import pytest
import numpy as np
from yggdrasil.math import Vector  # replace 'your_module' with the actual module name

def test_vector_initialization():
    """Test initialization of Vector class."""
    v = Vector(1, 2, 3)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

    with pytest.raises(ValueError):
        Vector('a', 2, 3) # type: ignore

    with pytest.raises(ValueError):
        Vector(1, 'b', 3) # type: ignore

    with pytest.raises(ValueError):
        Vector(1, 2, 'c') # type: ignore

def test_vector_get_item():
    """Test __get_item__ method."""
    v = Vector(1, 2, 3)
    assert v.__get_item__(0) == 1.0
    assert v.__get_item__(1) == 2.0
    assert v.__get_item__(2) == 3.0

    with pytest.raises(IndexError):
        v.__get_item__(3)

def test_vector_is_vector():
    """Test is_vector static method."""
    assert Vector.is_vector(Vector(1, 2, 3))
    assert not Vector.is_vector([1, 2, 3])

def test_vector_validate_vector():
    """Test validate_vector static method."""
    assert Vector.validate_vector(Vector(1, 2, 3)) == Vector(1, 2, 3)

    with pytest.raises(TypeError):
        Vector.validate_vector([1, 2, 3])

def test_vector_len():
    """Test __len__ method."""
    v = Vector(1, 2, 3)
    assert len(v) == 3

def test_vector_str_repr():
    """Test __str__ and __repr__ methods."""
    v = Vector(1, 2, 3)
    assert str(v) == "Vector(1.0, 2.0, 3.0)"
    assert repr(v) == "Vector(1.0, 2.0, 3.0)"

def test_vector_element_wise():
    """Test element_wise method."""
    v = Vector(1, 2, 3)
    squared = v.element_wise(lambda x: x ** 2)
    assert squared == Vector(1, 4, 9)

def test_vector_array():
    """Test __array__ method."""
    v = Vector(1, 2, 3)
    np.testing.assert_array_equal(np.array(v), np.array([1.0, 2.0, 3.0]))

def test_vector_add():
    """Test __add__ method."""
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    assert v1 + v2 == Vector(5, 7, 9)

def test_vector_sub():
    """Test __sub__ method."""
    v1 = Vector(4, 5, 6)
    v2 = Vector(1, 2, 3)
    assert v1 - v2 == Vector(3, 3, 3)

def test_vector_abs():
    """Test __abs__ method."""
    v = Vector(3, 4, 0)
    assert abs(v) == 5.0

def test_vector_neg():
    """Test __neg__ method."""
    v = Vector(1, -2, 3)
    assert -v == Vector(-1, 2, -3)

def test_vector_mul_rmul():
    """Test __mul__ and __rmul__ methods."""
    v = Vector(1, 2, 3)
    assert v * 2 == Vector(2, 4, 6)
    assert 2 * v == Vector(2, 4, 6)

def test_vector_truediv():
    """Test __truediv__ method."""
    v = Vector(4, 6, 8)
    assert v / 2 == Vector(2, 3, 4)

def test_vector_matmul():
    """Test __matmul__ method."""
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    assert v1 @ v2 == 32.0

def test_vector_xor():
    """Test __xor__ method (cross product)."""
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    assert v1 ^ v2 == Vector(0, 0, 1)

def test_vector_eq():
    """Test __eq__ method."""
    v1 = Vector(1, 2, 3)
    v2 = Vector(1, 2, 3)
    v3 = Vector(4, 5, 6)
    assert v1 == v2
    assert v1 != v3

def test_vector_is_close():
    """Test is_close method."""
    v1 = Vector(1.0, 2.0, 3.0)
    v2 = Vector(1.0, 2.0, 3.000000001)
    v3 = Vector(1.0, 2.0, 3.1)
    assert v1.is_close(v2)
    assert not v1.is_close(v3)

def test_vector_is_parallel():
    """Test is_parallel method."""
    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 4, 6)
    v3 = Vector(4, 5, 6)
    assert v1.is_parallel(v2)
    assert not v1.is_parallel(v3)

def test_vector_is_orthogonal():
    """Test is_orthogonal method."""
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = Vector(1, 1, 0)
    assert v1.is_orthogonal(v2)
    assert not v1.is_orthogonal(v3)

def test_vector_dot():
    """Test dot method."""
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    assert v1.dot(v2) == 32.0

def test_vector_cross():
    """Test cross method."""
    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    assert v1.cross(v2) == Vector(0, 0, 1)

def test_vector_normalized():
    """Test normalized property."""
    v = Vector(3, 0, 0)
    assert v.normalized == Vector(1, 0, 0)

def test_vector_project():
    """Test project method."""
    v1 = Vector(1, 7, 3)
    v2 = Vector(2, 5, 6)
    assert v1.project(v2) == 6.821910402406465

def test_vector_norm():
    """Test norm method."""
    v = Vector(3, 4, 0)
    assert v.norm() == 5.0

def test_vector_skew():
    """Test skew method."""
    v = Vector(1, 2, 3)
    with pytest.raises(NotImplementedError):
        v.skew()
