
import math
import attrs

from ..earth import EllipsoidModel,wgs84
from .position import Position

@attrs.define(slots=True)
class GeographicPosition:
    """
    Represents a geographic position with latitude, longitude, altitude, and an ellipsoid model.

    Attributes:
        latitude (float): The latitude in radians.
        longitude (float): The longitude in radians.
        altitude (float): The altitude in radians.
        earth_model (EllipsoidModel): The ellipsoid model.

    Methods:
        from_position(X_ECEF, ellipsoid=wgs84()): Converts a position in Earth-Centered
        Earth-Fixed (ECEF) coordinates to geographic coordinates.

    References:
        - Bowring, B.R. (1976). "Transformation from spatial to geographical coordinates".
        Survey Review. 23 (181): 323–327.
        - See more details at: https://github.com/kvenkman/ecef2lla/blob/master/ecef2lla.py
    """

    latitude: float = attrs.field(
        metadata={'description': 'The latitude in radians'},
        validator=attrs.validators.instance_of(float),
        kw_only=True,
        )
    longitude: float = attrs.field(
        metadata={'description': 'The longitude in radians'},
        validator=attrs.validators.instance_of(float),
        kw_only=True,
        )
    altitude: float = attrs.field(
        metadata={'description': 'The altitude in radians'},
        validator=attrs.validators.instance_of(float),
        kw_only=True,
        )
    earth_model: EllipsoidModel = attrs.field(
        metadata={'description': 'The ellipsoid model'},
        validator=attrs.validators.instance_of(EllipsoidModel),
        kw_only=True,
        )

# ----------------------------- DUNDER METHODS ----------------------------- #
    def __str__(self):
        return (
            f"GeographicPosition(latitude={self.latitude},"
            f" longitude={self.longitude}"
            f", altitude={self.altitude})")

    def __repr__(self):
        return (
            f"GeographicPosition(latitude={self.latitude},"
            f" longitude={self.longitude}"
            f", altitude={self.altitude})")

    def __eq__(self, value: 'GeographicPosition') -> bool:
        if not isinstance(value, GeographicPosition):
            raise ValueError(
                "Cannot compare GeographicPosition with non-GeographicPosition object.")
        return (
            self.latitude == value.latitude
            and self.longitude == value.longitude
            and self.altitude == value.altitude
            and self.earth_model == value.earth_model
        )

# ------------------------------- OPERATIONS ------------------------------- #

    def isclose(self, value: 'GeographicPosition', rel_tol: float = 1e-9) -> bool:
        """
        Checks if the current GeographicPosition object is close to another
        GeographicPosition object.

        Args:
            value (GeographicPosition): The other GeographicPosition object to compare with.
            rel_tol (float, optional): The relative tolerance used for the comparison.
              Defaults to 1e-9.

        Returns:
            bool: True if the positions are close, False otherwise.

        Raises:
            ValueError: If the value parameter is not a GeographicPosition object.

        """
        if not isinstance(value, GeographicPosition):
            raise ValueError(
                "Cannot compare GeographicPosition with non-GeographicPosition object.")
        return (
            math.isclose(self.latitude, value.latitude, rel_tol=rel_tol)
            and math.isclose(self.longitude, value.longitude, rel_tol=rel_tol)
            and math.isclose(self.altitude, value.altitude, rel_tol=rel_tol)
            and self.earth_model == value.earth_model
        )
