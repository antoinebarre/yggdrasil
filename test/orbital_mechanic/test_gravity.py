import unittest
from yggdrasil.constants import GRAVITATIONAL_CONSTANT
from yggdrasil.orbital_mechanic import gravitational_force

class TestGravitationalForce(unittest.TestCase):

    def test_normal_case(self):
        mass1 = 5.972e24  # Mass of the Earth in kg
        mass2 = 7.348e22  # Mass of the Moon in kg
        distance = 3.844e8  # Distance between Earth and Moon in meters
        expected_force = GRAVITATIONAL_CONSTANT * mass1 * mass2 / distance**2
        self.assertAlmostEqual(gravitational_force(mass1, mass2, distance), expected_force, places=10)

    def test_small_values(self):
        mass1 = 1.0  # in kg
        mass2 = 1.0  # in kg
        distance = 1.0  # in meters
        expected_force = GRAVITATIONAL_CONSTANT * mass1 * mass2 / distance**2
        self.assertAlmostEqual(gravitational_force(mass1, mass2, distance), expected_force, places=10)

    def test_large_values(self):
        mass1 = 1e30  # in kg
        mass2 = 1e30  # in kg
        distance = 1e10  # in meters
        expected_force = GRAVITATIONAL_CONSTANT * mass1 * mass2 / distance**2
        self.assertAlmostEqual(gravitational_force(mass1, mass2, distance), expected_force, places=10)

    def test_zero_mass(self):
        mass1 = 0.0  # in kg
        mass2 = 1.0  # in kg
        distance = 1.0  # in meters
        expected_force = 0.0
        self.assertEqual(gravitational_force(mass1, mass2, distance), expected_force)

    def test_zero_distance(self):
        mass1 = 1.0  # in kg
        mass2 = 1.0  # in kg
        distance = 0.0  # in meters
        with self.assertRaises(ValueError):
            gravitational_force(mass1, mass2, distance)

    def test_negative_distance(self):
        mass1 = 1.0  # in kg
        mass2 = 1.0  # in kg
        distance = -1.0  # in meters
        with self.assertRaises(ValueError):
            gravitational_force(mass1, mass2, distance)

    def test_invalid_mass_type(self):
        mass1 = "not a number"
        mass2 = 1.0  # in kg
        distance = 1.0  # in meters
        with self.assertRaises(TypeError):
            gravitational_force(mass1, mass2, distance)

    def test_invalid_distance_type(self):
        mass1 = 1.0  # in kg
        mass2 = 1.0  # in kg
        distance = "not a number"
        with self.assertRaises(TypeError):
            gravitational_force(mass1, mass2, distance)

if __name__ == '__main__':
    unittest.main()
