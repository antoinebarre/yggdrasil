"""Collection of constants used in the Earth model."""

from dataclasses import dataclass

__all__ = ['EarthConstants']

@dataclass
class EarthConstants:
    """
    A class that defines constants related to Earth.

    Attributes:
        mu (float): The gravitational parameter of Earth. (m^3/s^2)
        earth_rotation_rate (float): The Earth rotation rate. (rad/s)
    """
    mu: float = 3.986004418e14 # m^3/s^2 gravitational parameter of Earth
    earth_rotation_rate : float =7.292115e-5 # rad/s Earth rotation rate