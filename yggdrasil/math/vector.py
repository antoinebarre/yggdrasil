"""Library for vector operations."""

from functools import cached_property
from typing import Any, Callable
import numpy as np
import attrs

__all__ = ['Vector']

@attrs.define(slots=True)
class Vector:
    """A class for representing and manipulating 3D vectors."""

    x: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float))
    y: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float))
    z: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float))

    def __get_item__(self, index: int) -> float:
        """Get the vector component by index.

        Args:
            index (int): Index of the component (0 for x, 1 for y, 2 for z).

        Returns:
            float: The value of the component at the specified index.

        Raises:
            IndexError: If the index is not in [0, 1, 2].

        Examples:
            >>> v = Vector(1, 2, 3)
            >>> v.__get_item__(0)
            1.0
            >>> v.__get_item__(2)
            3.0
        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError(f"Index {index} out of range")

    @staticmethod
    def is_vector(other: Any) -> bool:
        """Check if an object is a Vector.

        Args:
            other (Any): The object to check.

        Returns:
            bool: True if the object is a Vector, False otherwise.

        Examples:
            >>> Vector.is_vector(Vector(1, 2, 3))
            True
            >>> Vector.is_vector([1, 2, 3])
            False
        """
        return isinstance(other, Vector)

    @staticmethod
    def validate_vector(other: Any) -> 'Vector':
        """Validate if an object is a Vector.

        Args:
            other (Any): The object to validate.

        Returns:
            Vector: The validated Vector object.

        Raises:
            TypeError: If the object is not a Vector.

        Examples:
            >>> Vector.validate_vector(Vector(1, 2, 3))
            Vector(1.0, 2.0, 3.0)
            >>> Vector.validate_vector([1, 2, 3])
            Traceback (most recent call last):
            ...
            TypeError: Cannot perform operation with <class 'list'>
        """
        if not Vector.is_vector(other):
            raise TypeError(f"Cannot perform operation with {type(other)}")
        return other

    def __len__(self) -> int:
        """Get the length of the vector (always 3).

        Returns:
            int: The length of the vector.

        Examples:
            >>> len(Vector(1, 2, 3))
            3
        """
        return 3

    def __str__(self) -> str:
        """Get the string representation of the vector.

        Returns:
            str: The string representation of the vector.

        Examples:
            >>> str(Vector(1, 2, 3))
            'Vector(1.0, 2.0, 3.0)'
        """
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        """Get the official string representation of the vector.

        Returns:
            str: The official string representation of the vector.

        Examples:
            >>> repr(Vector(1, 2, 3))
            'Vector(1.0, 2.0, 3.0)'
        """
        return str(self)

    def element_wise(self, operation: Callable[[float], float]) -> 'Vector':
        """Apply an element-wise operation to the vector.

        Args:
            operation (Callable[[float], float]): A function to apply to each
             component of the vector.

        Returns:
            Vector: A new vector with the operation applied to each component.

        Examples:
            >>> v = Vector(1, 2, 3)
            >>> v.element_wise(lambda x: x ** 2)
            Vector(1.0, 4.0, 9.0)
        """
        return Vector(
            operation(self.x),
            operation(self.y),
            operation(self.z)
        )

    def __array__(self) -> np.ndarray:
        """Convert the vector to a NumPy array.

        Returns:
            np.ndarray: The vector as a NumPy array.

        Examples:
            >>> np.array(Vector(1, 2, 3))
            array([1., 2., 3.])
        """
        return np.array([self.x, self.y, self.z])

    def __add__(self, other: 'Vector') -> 'Vector':
        """Add two vectors.

        Args:
            other (Vector): The vector to add.

        Returns:
            Vector: The result of adding the two vectors.

        Examples:
            >>> Vector(1, 2, 3) + Vector(4, 5, 6)
            Vector(5.0, 7.0, 9.0)
        """
        Vector.validate_vector(other)
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Subtract two vectors.

        Args:
            other (Vector): The vector to subtract.

        Returns:
            Vector: The result of subtracting the two vectors.

        Examples:
            >>> Vector(4, 5, 6) - Vector(1, 2, 3)
            Vector(3.0, 3.0, 3.0)
        """
        Vector.validate_vector(other)
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self) -> float:
        """Calculate the magnitude of the vector.

        Returns:
            float: The magnitude of the vector.

        Examples:
            >>> abs(Vector(3, 4, 0))
            5.0
        """
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __neg__(self) -> 'Vector':
        """Negate the vector.

        Returns:
            Vector: The negated vector.

        Examples:
            >>> -Vector(1, -2, 3)
            Vector(-1.0, 2.0, -3.0)
        """
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: float) -> 'Vector':
        """Multiply the vector by a scalar.

        Args:
            scalar (float): The scalar to multiply by.

        Returns:
            Vector: The scaled vector.

        Examples:
            >>> Vector(1, 2, 3) * 2
            Vector(2.0, 4.0, 6.0)
        """
        return self.__rmul__(scalar)

    def __rmul__(self, scalar: float) -> 'Vector':
        """Multiply the vector by a scalar (reversed operands).

        Args:
            scalar (float): The scalar to multiply by.

        Returns:
            Vector: The scaled vector.

        Examples:
            >>> 2 * Vector(1, 2, 3)
            Vector(2.0, 4.0, 6.0)
        """
        return Vector(scalar * self.x, scalar * self.y, scalar * self.z)

    def __truediv__(self, scalar: float) -> 'Vector':
        """Divide the vector by a scalar.

        Args:
            scalar (float): The scalar to divide by.

        Returns:
            Vector: The scaled vector.

        Examples:
            >>> Vector(4, 6, 8) / 2
            Vector(2.0, 3.0, 4.0)
        """
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def __matmul__(self, other: 'Vector') -> float:
        """Calculate the dot product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The dot product of the two vectors.

        Examples:
            >>> Vector(1, 2, 3) @ Vector(4, 5, 6)
            32.0
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __xor__(self, other: 'Vector') -> 'Vector':
        """Calculate the cross product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            Vector: The cross product of the two vectors.

        Examples:
            >>> Vector(1, 0, 0) ^ Vector(0, 1, 0)
            Vector(0.0, 0.0, 1.0)
        """
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __eq__(self, other: 'Vector') -> bool:
        """Check if two vectors are equal.

        Args:
            other (Vector): The other vector.

        Returns:
            bool: True if the vectors are equal, False otherwise.

        Examples:
            >>> Vector(1, 2, 3) == Vector(1, 2, 3)
            True
            >>> Vector(1, 2, 3) == Vector(4, 5, 6)
            False
        """
        Vector.validate_vector(other)
        return self.x == other.x and self.y == other.y and self.z == other.z

    def is_close(self, other: 'Vector', tol: float = 1e-9) -> bool:
        """Check if two vectors are close within a tolerance.

        Args:
            other (Vector): The other vector.
            tol (float): The tolerance.

        Returns:
            bool: True if the vectors are close, False otherwise.

        Examples:
            >>> Vector(1.0, 2.0, 3.0).is_close(Vector(1.0, 2.0, 3.000000001))
            True
            >>> Vector(1.0, 2.0, 3.0).is_close(Vector(1.0, 2.0, 3.1))
            False
        """
        Vector.validate_vector(other)
        return np.allclose(self.__array__(), other.__array__(), atol=tol)

    def is_parallel(self, other: 'Vector', tol: float = 1e-9) -> bool:
        """Check if two vectors are parallel within a tolerance.

        Args:
            other (Vector): The other vector.
            tol (float): The tolerance.

        Returns:
            bool: True if the vectors are parallel, False otherwise.

        Examples:
            >>> Vector(1, 2, 3).is_parallel(Vector(2, 4, 6))
            True
            >>> Vector(1, 2, 3).is_parallel(Vector(4, 5, 6))
            False
        """
        Vector.validate_vector(other)
        return (self ^ other).is_close(Vector(0, 0, 0), tol=tol)

    def is_orthogonal(self, other: 'Vector', tol: float = 1e-9) -> bool:
        """Check if two vectors are orthogonal within a tolerance.

        Args:
            other (Vector): The other vector.
            tol (float): The tolerance.

        Returns:
            bool: True if the vectors are orthogonal, False otherwise.

        Examples:
            >>> Vector(1, 0, 0).is_orthogonal(Vector(0, 1, 0))
            True
            >>> Vector(1, 1, 0).is_orthogonal(Vector(1, 0, 1))
            False
        """
        Vector.validate_vector(other)
        return bool(np.isclose(self @ other, 0., atol=tol))

    def dot(self, other: 'Vector') -> float:
        """Calculate the dot product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The dot product of the two vectors.

        Examples:
            >>> Vector(1, 2, 3).dot(Vector(4, 5, 6))
            32.0
        """
        return self @ other

    def cross(self, other: 'Vector') -> 'Vector':
        """Calculate the cross product of two vectors.

        Args:
            other (Vector): The other vector.

        Returns:
            Vector: The cross product of the two vectors.

        Examples:
            >>> Vector(1, 0, 0).cross(Vector(0, 1, 0))
            Vector(0.0, 0.0, 1.0)
        """
        return self ^ other

    @cached_property
    def normalized(self) -> 'Vector':
        """Get the normalized vector.

        Returns:
            Vector: The normalized vector.

        Examples:
            >>> Vector(3, 0, 0).normalized
            Vector(1.0, 0.0, 0.0)
        """
        return self / abs(self)

    def project(self, other: 'Vector') -> float:
        """Project this vector onto another vector.

        Args:
            other (Vector): The other vector.

        Returns:
            float: The projection of this vector onto the other vector.

        Examples:
            >>> Vector(1, 2, 3).project(Vector(4, 5, 6))
            3.24037034920393
        """
        return (self @ other) / abs(other)

    def norm(self) -> float:
        """Get the norm (magnitude) of the vector.

        Returns:
            float: The norm of the vector.

        Examples:
            >>> Vector(3, 4, 0).norm()
            5.0
        """
        return abs(self)

    def skew(self):
        """Get the skew-symmetric matrix of the vector.

        Raises:
            NotImplementedError: Method not implemented.

        Examples:
            >>> Vector(1, 2, 3).skew()
            Traceback (most recent call last):
            ...
            NotImplementedError: Method not implemented
        """
        raise NotImplementedError("Method not implemented")
