import pytest
from math import isclose

from yggdrasil.earth.earth_ellipsoid_model import EllipsoidModel, wgs84, spherical_earth, earth_ellipsoid_model

# Test data for parameterized tests
ellipsoid_model_data = [
    ("TestModel", 6378137.0, 1/298.257223563, 1.08263e-3),
    ("AnotherModel", 6371000.0, 1/300.0, 1.1e-3),
]

@pytest.mark.parametrize("name, semi_major_axis, flattening, j2", ellipsoid_model_data)
def test_initialization(name, semi_major_axis, flattening, j2):
    """
    Test the initialization of the EllipsoidModel class.

    Args:
        name (str): The name of the ellipsoid model.
        semi_major_axis (float): The semi-major axis of the ellipsoid.
        flattening (float): The flattening of the ellipsoid.
        j2 (float): The J2 coefficient of the ellipsoid.

    Returns:
        None
    """
    model = EllipsoidModel(
        name=name,
        semi_major_axis=semi_major_axis,
        flattening=flattening,
        j2=j2,
    )
    assert model.name == name
    assert model.semi_major_axis == semi_major_axis
    assert model.flattening == flattening
    assert model.j2 == j2


@pytest.mark.parametrize("name, semi_major_axis, flattening, j2", [
    (123, "6378137.0", "1/298.257223563", "1.08263e-3")
])
def test_initialization_invalid(name, semi_major_axis, flattening, j2):
    """
    Test the initialization of the EllipsoidModel class with invalid arguments.

    Args:
        name (int): The name of the ellipsoid model (invalid type).
        semi_major_axis (str): The semi-major axis of the ellipsoid (invalid type).
        flattening (str): The flattening of the ellipsoid (invalid type).
        j2 (str): The J2 coefficient of the ellipsoid (invalid type).

    Returns:
        None
    """
    with pytest.raises(TypeError):
        EllipsoidModel(
            name=name,
            semi_major_axis=semi_major_axis,
            flattening=flattening,
            j2=j2,
        )

@pytest.mark.parametrize("model, expected_b, expected_e, expected_mean_radius", [
    (EllipsoidModel("TestModel", 6378137.0, 1/298.257223563, 1.08263e-3), 6356752.314245179, 0.0818191908426215, 6371008.771415059),
    (EllipsoidModel("SphericalModel", 6371000.0, 0.0, 0.0), 6371000.0, 0.0, 6371000.0),
])
def test_properties(model, expected_b, expected_e, expected_mean_radius):
    """
    Test the properties of the EllipsoidModel class.

    Args:
        model (EllipsoidModel): The ellipsoid model to test.
        expected_b (float): The expected value of the minor axis.
        expected_e (float): The expected value of the eccentricity.
        expected_mean_radius (float): The expected value of the mean radius.

    Returns:
        None
    """
    assert model.a == model.semi_major_axis
    assert model.f == model.flattening
    assert isclose(model.b, expected_b)
    assert isclose(model.e, expected_e)
    assert isclose(model.mean_radius, expected_mean_radius)

def test_equality():
    """
    Test the equality comparison of the EllipsoidModel class.

    Returns:
        None
    """
    model1 = EllipsoidModel("Model1", 6378137.0, 1/298.257223563, 1.08263e-3)
    model2 = EllipsoidModel("Model1", 6378137.0, 1/298.257223563, 1.08263e-3)
    model3 = EllipsoidModel("Model3", 6378138.0, 1/299.257223563, 1.08363e-3)
    assert model1 == model2
    assert model1 != model3

def test_equality_invalid():
    """
    Test the equality comparison of the EllipsoidModel class with invalid type.

    Returns:
        None
    """
    model = EllipsoidModel("Model", 6378137.0, 1/298.257223563, 1.08263e-3)
    with pytest.raises(ValueError):
        model == "InvalidType"

def test_wgs84_function():
    """
    Test the wgs84 function.

    Returns:
        None
    """
    model = wgs84()
    assert model.name == "WGS84"
    assert model.semi_major_axis == 6378137.0
    assert model.flattening == 1/298.257223563
    assert model.j2 == 1.08263e-3

def test_spherical_earth_function():
    """
    Test the spherical_earth function.

    Returns:
        None
    """
    model = spherical_earth()
    assert model.name == "Spherical Earth"
    assert model.semi_major_axis == 6371127.0
    assert model.flattening == 0.0
    assert model.j2 == 0.0

@pytest.mark.parametrize("model_name, expected_model", [
    ("WGS84", EllipsoidModel("WGS84", 6378137.0, 1/298.257223563, 1.08263e-3)),
    ("Spherical Earth", EllipsoidModel("Spherical Earth", 6371127.0, 0.0, 0.0)),
])
def test_earth_ellipsoid_model_function(model_name, expected_model):
    """
    Test the earth_ellipsoid_model function.

    Args:
        model_name (str): The name of the ellipsoid model.
        expected_model (EllipsoidModel): The expected ellipsoid model.

    Returns:
        None
    """
    model = earth_ellipsoid_model(model_name)
    assert model == expected_model

def test_earth_ellipsoid_model_invalid():
    """
    Test the earth_ellipsoid_model function with invalid model name.

    Returns:
        None
    """
    with pytest.raises(KeyError):
        earth_ellipsoid_model("InvalidModel")

