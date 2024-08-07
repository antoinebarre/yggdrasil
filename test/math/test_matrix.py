import pytest
import numpy as np
from yggdrasil.math import Matrix, Vector


def test_matrix_initialization():
    """Test initialization of Matrix class."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert m.xx == 1.0
    assert m.xy == 2.0
    assert m.xz == 3.0
    assert m.yx == 4.0
    assert m.yy == 5.0
    assert m.yz == 6.0
    assert m.zx == 7.0
    assert m.zy == 8.0
    assert m.zz == 9.0

def test_matrix_from_list():
    """Test Matrix creation from list."""
    m = Matrix.from_list([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert m.xx == 1.0
    assert m.xy == 2.0
    assert m.xz == 3.0
    assert m.yx == 4.0
    assert m.yy == 5.0
    assert m.yz == 6.0
    assert m.zx == 7.0
    assert m.zy == 8.0
    assert m.zz == 9.0

    with pytest.raises(ValueError):
        Matrix.from_list([[1, 2], [3, 4], [5, 6]])  # Not a 3x3 list

def test_matrix_is_matrix():
    """Test the is_matrix method."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert Matrix.is_matrix(m)
    assert not Matrix.is_matrix([1, 2, 3])

def test_matrix_validate_matrix():
    """Test the validate_matrix method."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert Matrix.validate_matrix(m) == m

    with pytest.raises(TypeError):
        Matrix.validate_matrix([1, 2, 3])  # Not a Matrix

def test_matrix_get_item():
    """Test __getitem__ method."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert m[0, 0] == 1.0
    assert m[0, 1] == 2.0
    assert m[1, 0] == 4.0
    assert m[2, 2] == 9.0

    with pytest.raises(IndexError):
        _ = m[3, 0]  # Out of bounds

def test_matrix_str_repr():
    """Test __str__ and __repr__ methods."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    assert str(m) == "3D Matrix(\n1.0, 2.0, 3.0,\n4.0, 5.0, 6.0,\n7.0, 8.0, 9.0)"
    assert repr(m) == "Matrix(xx=1.0, xy=2.0, xz=3.0, yx=4.0, yy=5.0, yz=6.0, zx=7.0, zy=8.0, zz=9.0)"

def test_matrix_array():
    """Test __array__ method."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    np.testing.assert_array_equal(m.__array__(), np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

def test_matrix_addition():
    """Test matrix addition."""
    m1 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m2 = Matrix(9, 8, 7, 6, 5, 4, 3, 2, 1)
    m3 = m1 + m2
    assert m3 == Matrix(10, 10, 10, 10, 10, 10, 10, 10, 10)

def test_matrix_subtraction():
    """Test matrix subtraction."""
    m1 = Matrix(9, 8, 7, 6, 5, 4, 3, 2, 1)
    m2 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m3 = m1 - m2
    assert m3 == Matrix(8, 6, 4, 2, 0, -2, -4, -6, -8)

def test_matrix_negation():
    """Test matrix negation."""
    m = Matrix(1, -2, 3, -4, 5, -6, 7, -8, 9)
    neg_m = -m
    assert neg_m == Matrix(-1, 2, -3, 4, -5, 6, -7, 8, -9)

def test_matrix_transpose():
    """Test matrix transpose."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    mt = m.transpose()
    assert mt == Matrix(1, 4, 7, 2, 5, 8, 3, 6, 9)

def test_matrix_scalar_multiplication():
    """Test scalar multiplication."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m2 = m * 2
    assert m2 == Matrix(2, 4, 6, 8, 10, 12, 14, 16, 18)

def test_matrix_identity():
    """Test identity matrix creation."""
    identity = Matrix.identity()
    assert identity == Matrix(1, 0, 0, 0, 1, 0, 0, 0, 1)

def test_matrix_multiplication():
    """Test matrix multiplication."""
    m1 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m2 = Matrix(9, 8, 7, 6, 5, 4, 3, 2, 1)
    result = m1 @ m2
    expected = Matrix(30, 24, 18, 84, 69, 54, 138, 114, 90)
    assert result == expected

def test_matrix_vector_multiplication():
    """Test matrix-vector multiplication."""
    m = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    v = Vector(1, 2, 3)
    result = m @ v
    expected = Vector(14, 32, 50)
    assert result == expected

def test_matrix_determinant():
    """Test matrix determinant."""
    m = Matrix(1, 2, 3, 0, 1, 4, 5, 6, 0)
    det = abs(m)
    assert det == -1.0

def test_matrix_equality():
    """Test matrix equality."""
    m1 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m2 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m3 = Matrix(9, 8, 7, 6, 5, 4, 3, 2, 1)
    assert m1 == m2
    assert m1 != m3

def test_matrix_is_close():
    """Test is_close method."""
    m1 = Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9)
    m2 = Matrix(1.000000001, 2, 3, 4, 5, 6, 7, 8, 9)
    m3 = Matrix(9, 8, 7, 6, 5, 4, 3, 2, 1)
    assert m1.is_close(m2)
    assert not m1.is_close(m3)

def test_matrix_pow():
    """Test matrix power."""
    m = Matrix.identity()
    result = m ** 3
    assert result == Matrix.identity()

    m2 = Matrix(1, 2, 3, 0, 1, 4, 5, 6, 0)
    result2 = m2 ** 2
    expected2 = m2 @ m2
    assert result2 == expected2
