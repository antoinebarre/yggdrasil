"""Tools to calculate gravitational forces."""

from yggdrasil.constants import GRAVITATIONAL_CONSTANT

__all__ = ["gravitational_force"]

def gravitational_force(
    mass1: float,
    mass2: float,
    distance: float
    ) -> float:
    """
    Calculates the gravitational force between two objects.

    Parameters:
    mass1 (float): The mass of the first object.
    mass2 (float): The mass of the second object.
    distance (float): The distance between the two objects.

    Returns:
    float: The gravitational force between the two objects.
    """
    if (
        not isinstance(mass1, (int, float))
        or not isinstance(mass2, (int, float))
        or not isinstance(distance, (int, float))):
        raise TypeError("Masses and distance must be numbers.")
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")
    return GRAVITATIONAL_CONSTANT * mass1 * mass2 / distance**2
