"""Earth Ellipsoid Model."""

import math
from typing import Literal
import attrs

__all__ = ['EllipsoidModel', 'earth_ellipsoid_model',"DEFAULT_EARTH_ELLIPSOID_MODEL"]

@attrs.define(slots=True)
class EllipsoidModel():
    """
    Object representing the earth ellipsoid.

    Attributes:
        name (str): The name of the ellipsoid.
        semiMajorAxis (float): The semi-major axis of the ellipsoid.
        flattening (float): The flattening of the ellipsoid.
        j2 (float): The J2 coefficient of the ellipsoid.
        earth_rotation_rate (float): The Earth rotation rate.
    """
    name: str = attrs.field(
        metadata={'description': 'The name of the ellipsoid'},
        validator=attrs.validators.instance_of(str),
        )
    semi_major_axis: float = attrs.field(
        metadata={'description': 'The semi-major axis of the ellipsoid'},
        validator=attrs.validators.instance_of(float),
        )
    flattening: float = attrs.field(
        metadata={'description': 'The flattening of the ellipsoid'},
        validator=attrs.validators.instance_of(float),
        )
    j2: float = attrs.field(
        metadata={'description': 'The J2 coefficient of the ellipsoid'},
        validator=attrs.validators.instance_of(float),
        )

# ----------------------------- DUNDER_METHODS ----------------------------- #
    def __eq__(self, value: object) -> bool:
        """
        Checks if the current EllipsoidModel instance is equal to another EllipsoidModel instance.

        Args:
            value: The EllipsoidModel instance to compare with.

        Returns:
            bool: True if the two EllipsoidModel instances are equal, False otherwise.

        Raises:
            ValueError: If the input value is not an EllipsoidModel instance.
        """

        if not isinstance(value, EllipsoidModel):
            raise ValueError("Cannot compare EllipsoidModel with non-EllipsoidModel object.")
        return (
            self.name == value.name
            and self.semi_major_axis == value.semi_major_axis
            and self.flattening == value.flattening
            and self.j2 == value.j2
        )

# --------------------------- PROPERTIES --------------------------- #
    @property
    def a(self) -> float:
        """semi major axis value of the ellispoid in meters

        Returns:
            float: semi major axis value of the ellispoid in meters
        """
        return self.semi_major_axis

    @property
    def f(self) -> float:
        """flattening of the ellispoid

        Returns:
            float: flattening of the ellispoid (SI)
        """
        return self.flattening

    @property
    def b(self) -> float:
        """Semi minor acis of the ellispoid in meters

        Returns:
            float: Semi minor acis of the ellispoid in meters
        """
        return (1-self.f)*self.a

    @property
    def e(self) -> float:
        """Excentricity of the ellispoid

        Returns:
            float: Excentricity of the ellispoid (SI)
        """
        return math.sqrt((self.a**2-self.b**2)/self.a**2)

    @property
    def mean_radius(self) -> float:
        """Mean radius of the ellispoid

        Returns:
            float: Mean radius of the ellispoid (SI)
        """
        return (2*self.a+self.b)/3


def wgs84() -> EllipsoidModel:
    """WGS84 ellipsoid model.

    Returns:
        EllipsoidModel: WGS84 ellipsoid model.
    """
    return EllipsoidModel(
        name="WGS84",
        semi_major_axis=6378137.0,
        flattening=1/298.257223563,
        j2=1.08263e-3,
    )

def spherical_earth() -> EllipsoidModel:
    """Spherical Earth ellipsoid model.

    Returns:
        EllipsoidModel: Spherical Earth ellipsoid model.
    """
    return EllipsoidModel(
        name="Spherical Earth",
        semi_major_axis=6371127.0,
        flattening=0.0,
        j2=0.0,
    )

AVAILABLE_ELLIPSOIDS = {
    "WGS84": EllipsoidModel(
        name="WGS84",
        semi_major_axis=6378137.0,
        flattening=1/298.257223563,
        j2=1.08263e-3,
    ),
    "Spherical Earth": EllipsoidModel(
        name="Spherical Earth",
        semi_major_axis=6371127.0,
        flattening=0.0,
        j2=0.0,
    )
}

DEFAULT_EARTH_ELLIPSOID_MODEL = "WGS84"

def earth_ellipsoid_model(
    name: Literal["WGS84", "Spherical Earth"] = DEFAULT_EARTH_ELLIPSOID_MODEL
    ) -> EllipsoidModel:
    """
    Returns the ellipsoid model for the Earth.

    Parameters:
        name (Literal["WGS84", "Spherical Earth"], optional): The name of the ellipsoid model.
            Defaults to "WGS84".

    Returns:
        EllipsoidModel: The ellipsoid model for the Earth.

    Raises:
        KeyError: If the specified ellipsoid model name is not available.

    """
    try:
        return AVAILABLE_ELLIPSOIDS[name]
    except KeyError as e:
        available_keys = ", ".join(AVAILABLE_ELLIPSOIDS.keys())
        raise KeyError(
            f"'{name}' is not a valid ellipsoid model name."
            f" Available names are: ({available_keys})") from e
