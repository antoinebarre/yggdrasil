"""Position Object."""


import attrs

@attrs.define(slots=True)
class Position:
    """
    Represents a position in Earth-Centered Earth-Fixed (ECEF) coordinates.

    Attributes:
        x (float): The x-coordinate of the ECEF position.
        y (float): The y-coordinate of the ECEF position.
        z (float): The z-coordinate of the ECEF position.
    """

    x: float = attrs.field(
        metadata={'description': 'The x-coordinate of the ECEF position'},
        validator=attrs.validators.instance_of(float),
    )
    y: float = attrs.field(
        metadata={'description': 'The y-coordinate of the ECEF position'},
        validator=attrs.validators.instance_of(float),
    )
    z: float = attrs.field(
        metadata={'description': 'The z-coordinate of the ECEF position'},
        validator=attrs.validators.instance_of(float),
    )

    def __str__(self):
        return f"Position ECEF(x={self.x}, y={self.y}, z={self.z})"

    def __repr__(self):
        return f"Position ECEF (x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, value: 'Position') -> bool:
        if not isinstance(value, Position):
            raise ValueError("Cannot compare Position with non-Position object.")
        return (
            self.x == value.x
            and self.y == value.y
            and self.z == value.z
        )

    @property
    def norm(self) -> float:
        """
        Calculates the Euclidean norm of the position vector.

        Returns:
            float: The Euclidean norm of the position vector.
        """
        return (self.x**2 + self.y**2 + self.z**2)**0.5
