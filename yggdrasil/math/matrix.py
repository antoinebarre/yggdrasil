"""Pure Python implementation of a matrix class."""

from typing import Any, TypeVar, Union
import attrs
import numpy as np
from .vector import Vector

__all__ = ["Matrix"]

MV = TypeVar('MV', bound=Union['Matrix', 'Vector'])

@attrs.define(slots=True)
class Matrix:
    xx: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    xy: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    xz: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    yx: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    yy: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    yz: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    zx: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    zy: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )
    zz: float = attrs.field(
        converter=float,
        validator=attrs.validators.instance_of(float),
    )

    @staticmethod
    def from_list(data: list[list[float]]) -> "Matrix":
        """Create a matrix from a list."""
        if len(data) != 3 or any(len(row) != 3 for row in data):
            raise ValueError("Expected a 3x3 list of lists")
        flat_data = [element for row in data for element in row]
        return Matrix(*flat_data)

    @staticmethod
    def is_matrix(matrix: Any) -> bool:
        """Check if an object is a matrix."""
        return isinstance(matrix, Matrix)

    @staticmethod
    def validate_matrix(matrix: Any) -> "Matrix":
        """Validate a matrix."""
        if not Matrix.is_matrix(matrix):
            raise TypeError(f"Expected a Matrix but got {type(matrix)}")
        return matrix

    def __str__(self) -> str:
        return (
            f"3D Matrix(\n{self.xx}, {self.xy}, {self.xz},\n"
            f"{self.yx}, {self.yy}, {self.yz},\n"
            f"{self.zx}, {self.zy}, {self.zz})"
        )

    def __repr__(self) -> str:
        return (
            f"Matrix(xx={self.xx}, xy={self.xy}, xz={self.xz}, "
            f"yx={self.yx}, yy={self.yy}, yz={self.yz}, "
            f"zx={self.zx}, zy={self.zy}, zz={self.zz})"
        )

    def __array__(self) -> "np.ndarray":
        """Convert to numpy array."""
        return np.array([
            [self.xx, self.xy, self.xz],
            [self.yx, self.yy, self.yz],
            [self.zx, self.zy, self.zz],
        ])

    def __getitem__(self, indices) -> float:
        """Get item."""
        if not isinstance(indices, tuple) or len(indices) != 2:
            raise IndexError("Expected a tuple of two indices")
        i, j = indices
        return float(self.__array__()[i, j])

    def __add__(self, other: "Matrix") -> "Matrix":
        """Matrix addition."""
        Matrix.validate_matrix(other)
        return Matrix(
            xx=self.xx + other.xx, xy=self.xy + other.xy, xz=self.xz + other.xz,
            yx=self.yx + other.yx, yy=self.yy + other.yy, yz=self.yz + other.yz,
            zx=self.zx + other.zx, zy=self.zy + other.zy, zz=self.zz + other.zz,
        )

    def __sub__(self, other: "Matrix") -> "Matrix":
        """Matrix subtraction."""
        Matrix.validate_matrix(other)
        return Matrix(
            xx=self.xx - other.xx, xy=self.xy - other.xy, xz=self.xz - other.xz,
            yx=self.yx - other.yx, yy=self.yy - other.yy, yz=self.yz - other.yz,
            zx=self.zx - other.zx, zy=self.zy - other.zy, zz=self.zz - other.zz,
        )

    def __neg__(self) -> "Matrix":
        """Negate the matrix."""
        return Matrix(
            xx=-self.xx, xy=-self.xy, xz=-self.xz,
            yx=-self.yx, yy=-self.yy, yz=-self.yz,
            zx=-self.zx, zy=-self.zy, zz=-self.zz,
        )


    def transpose(self) -> "Matrix":
        """Transpose the matrix."""
        return Matrix(
            xx=self.xx, xy=self.yx, xz=self.zx,
            yx=self.xy, yy=self.yy, yz=self.zy,
            zx=self.xz, zy=self.yz, zz=self.zz,
        )

    def __mul__(self, scalar: float) -> "Matrix":
        """Scalar multiplication."""
        return Matrix(
            xx=self.xx * scalar, xy=self.xy * scalar, xz=self.xz * scalar,
            yx=self.yx * scalar, yy=self.yy * scalar, yz=self.yz * scalar,
            zx=self.zx * scalar, zy=self.zy * scalar, zz=self.zz * scalar,
        )

    @staticmethod
    def identity() -> "Matrix":
        """Identity matrix."""
        return Matrix(
            xx=1, xy=0, xz=0,
            yx=0, yy=1, yz=0,
            zx=0, zy=0, zz=1,
        )

    def __matmul__(self, other: MV) -> MV:
        """Matrix multiplication."""
        if isinstance(other, Vector):
            return Vector(
                x=self.xx * other.x + self.xy * other.y + self.xz * other.z,
                y=self.yx * other.x + self.yy * other.y + self.yz * other.z,
                z=self.zx * other.x + self.zy * other.y + self.zz * other.z) # type: ignore
        elif isinstance(other, Matrix):
            return Matrix(
                xx=self.xx * other.xx + self.xy * other.yx + self.xz * other.zx,
                xy=self.xx * other.xy + self.xy * other.yy + self.xz * other.zy,
                xz=self.xx * other.xz + self.xy * other.yz + self.xz * other.zz,
                yx=self.yx * other.xx + self.yy * other.yx + self.yz * other.zx,
                yy=self.yx * other.xy + self.yy * other.yy + self.yz * other.zy,
                yz=self.yx * other.xz + self.yy * other.yz + self.yz * other.zz,
                zx=self.zx * other.xx + self.zy * other.yx + self.zz * other.zx,
                zy=self.zx * other.xy + self.zy * other.yy + self.zz * other.zy,
                zz=self.zx * other.xz + self.zy * other.yz + self.zz * other.zz,) # type: ignore
        else:
            raise TypeError(f"Unsupported type for matrix multiplication: {type(other)}")

    def __abs__(self) -> float:
        """Matrix determinant."""
        ixx = self.yy * self.zz - self.yz * self.zy
        ixy = self.yx * self.zz - self.yz * self.zx
        ixz = self.yx * self.zy - self.yy * self.zx
        return self.xx * ixx - self.xy * ixy + self.xz * ixz

    def det(self) -> float:
        """Matrix determinant."""
        return abs(self)

    def __eq__(self, value: object) -> bool:
        """Equality check."""
        if not Matrix.is_matrix(value):
            return False
        return all(
            getattr(self, k) == getattr(value, k)
            for k in self.attributes_list())

    def is_close(self, value: object, tol: float = 1e-10) -> bool:
        """Equality check with tolerance."""
        if not Matrix.is_matrix(value):
            return False
        return all(
            np.isclose(getattr(self, k), getattr(value, k), atol=tol)
            for k in self.attributes_list())

    @staticmethod
    def attributes_list() -> list[str]:
        """List of attributes."""
        attributes = attrs.fields(Matrix)
        return [attribute.name for attribute in attributes]

    def __pow__(self, scalar: int) -> "Matrix":
        """Scalar power."""
        result = Matrix.identity()
        for _ in range(scalar):
            result = result.__matmul__(self)
        return result