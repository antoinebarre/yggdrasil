"""UNIT TEST FOR GEOGRAPHIC ROTATIONS"""


# import module
import pytest
import numpy as np

from yggdrasil.geography.rotation_matrix import (dcm_eci2ecef, dcm_ecef2ned,
                                               dcm_ecef2enu, angle2dcm,
                                               )
from yggdrasil.math import Matrix, Vector



ABSOLUTE_TOLERANCE = 1e-12
RELATIVE_TOLERANCE = 1e-6
NB_DECIMAL = 8
NB_OBJ = 100


def test_ECI2ECEF() -> None:
    """Test Cases for the function DCM_ECI2ECEF
    """

    # assert when dt=0
    assert dcm_eci2ecef(0.).is_close(Matrix.identity(),tol=ABSOLUTE_TOLERANCE),f"Error: dcm_eci2ecef(0.).Got :\n{dcm_eci2ecef(0.)}"


    # TODO : complete the test cases
    # see https://github.com/geospace-code/pymap3d/blob/main/src/pymap3d/tests/test_eci.py


class TestDCMEcef2Ned:
    def test_dcm_ecef2ned_equator(self):
        # Test case for a point on the equator
        lat = 0.0
        lon = 0.0
        expected_dcm = Matrix.from_list([
            [0,0 , 1],
            [0, 1, 0],
            [-1, 0, 0]
        ])
        result = dcm_ecef2ned(lat, lon)

        np.testing.assert_array_almost_equal(result, expected_dcm, decimal=6)

    def test_dcm_ecef2ned_pole(self):
        # Test case for a point on the North Pole
        lat = np.deg2rad(90.0)
        lon = 0.0
        expected_dcm = Matrix.from_list([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, -1]
        ])
        result = dcm_ecef2ned(lat, lon)
        np.testing.assert_array_almost_equal(result, expected_dcm, decimal=6)

    def test_dcm_ecef2ned_random(self):
        # Test case for a random point
        
        # example from mathworks : https://fr.mathworks.com/help/aerotbx/ug/dcmecef2ned.html
        lat = np.deg2rad(45.0)
        lon = np.deg2rad(-122.0)
        expected_dcm = Matrix.from_list([
            [0.3747, 0.5997, 0.7071],
            [0.8480, -0.5299, 0],
            [0.3747, 0.5997, -0.7071]
        ])
        result = dcm_ecef2ned(lat, lon)
        np.testing.assert_array_almost_equal(result, expected_dcm, decimal=4)



class TestECEF2ENU():
    """cf. https://github.com/skulumani/astro/blob/a707ad017f061ef2d465d797b348081dc2bd09bd/astro/tests/test_transform.py"""

    def test_equator_prime_meridian(self):
        latgd = 0.
        lon = 0.
        dcm_ecef2enu_expected = Matrix.from_list([[0, 0, 1],
                                          [1, 0, 0],
                                          [0, 1, 0]]).transpose()
        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_allclose(dcm,
                                   dcm_ecef2enu_expected,
                                   atol=ABSOLUTE_TOLERANCE,
                                   rtol=RELATIVE_TOLERANCE)

    def test_pole_prime_meridian(self):
        latgd = np.pi/2
        lon = 0.
        dcm_ecef2enu_expected = Matrix.from_list([[0, 1, 0],
                                          [-1, 0, 0],
                                          [0, 0, 1]])
        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_array_almost_equal(dcm, dcm_ecef2enu_expected)

    def test_so3(self):
        latgd = np.random.uniform(-np.pi/2, np.pi/2)
        lon = np.random.uniform(-np.pi, np.pi)

        dcm = dcm_ecef2enu(latgd, lon)
        np.testing.assert_allclose(np.linalg.det(dcm), 1)
        np.testing.assert_array_almost_equal(
            dcm.transpose() @ dcm,
            np.eye(3, 3))

    def test_ecef2enu_1(self):
        """ see https://github.com/spacecraft-design-lab-2019/GNC/blob/40455d0324e01691db1c2ce13d2d41b5c5dcaaf7/util_funcs/test/test_frame_conversions.py"""
        lat = 0.
        lon = np.pi / 6
        test_vec = Vector(*[1., 0., 0.])
        R_pred = Matrix.from_list([[-1/2, np.sqrt(3)/2, 0.],
                          [0, 0, 1],
                          [np.sqrt(3)/2, 1/2, 0]])
        test_rot_vec = Vector(*[-1/2, 0, np.sqrt(3)/2])
        np.testing.assert_allclose(dcm_ecef2enu(lat, lon),
                                   R_pred,
                                   atol=1e-6)  # Python test
        np.testing.assert_allclose(dcm_ecef2enu(lat, lon) @ test_vec,
                                   test_rot_vec,
                                   atol=1e-6)  # checking rotations


def test_angle2dcm_ZYX():
    """unit test for angle to dcm with ZYX order

    Data Source: Example 1 generated using book GNSS Applications and Methods
            Chapter 7 library function: eul2Cbn.m (transpose of this used).
            Example 2 found in Performance, Stability, Dynamics, and Control
            of Airplanes, Second Edition (p. 355).

    """
    # Define Euler angles and expected DCMs
    checks = (
        (np.deg2rad([-83, 2.3, 13]), 6,
            Matrix.from_list([[0.121771, -0.991747, -0.040132],
                     [0.968207,  0.109785,  0.224770],
                     [-0.218509, -0.066226,  0.973585]])),
        (np.deg2rad([-10, 20, 30]), 4,
            Matrix.from_list([[0.9254,  0.3188,  0.2049],
                     [-0.1632,  0.8232, -0.5438],
                     [-0.3420,  0.4698,  0.8138]]).transpose()),
    )

    for angles, decimal, Rnav2body_expected in checks:
        yaw, pitch, roll = angles

        Rnav2body_computed = angle2dcm(yaw, pitch, roll)

        np.testing.assert_almost_equal(
            Rnav2body_expected.__array__(),
            Rnav2body_computed.__array__(),
            decimal=decimal)


# def test_angle2dcm_errorImplemented():
#     "test only ZYX feature is implemented"
#     with pytest.raises(NotImplementedError):
#         print(angle2dcm(0., 0., 0., "XYZ"))


# def test_dcm2angle_ZYX():
#     """test dcm2angle with ZYX rotation
#     """
#     # Define (expected) Euler angles and associated DCM (Rnav2body)
#     yaw, pitch, roll = np.deg2rad([-83, 2.3, 13])  # degrees

#     Rnav2body = np.array([[0.121771, -0.991747, -0.040132],
#                          [0.968207,  0.109785,  0.224770],
#                          [-0.218509, -0.066226,  0.973585]])

#     yaw_C, pitch_C, roll_C = dcm2angle(Rnav2body)

#     # Assess
#     np.testing.assert_almost_equal([yaw_C, pitch_C, roll_C],
#                                    [yaw, pitch, roll],
#                                    decimal=4)


# def test_angle2dcm_error():
#     "test only ZYX feature is implemented"
#     with pytest.raises(NotImplementedError):
#         print(dcm2angle(np.ndarray((3, 3)),
#                         rotationSequence="XYZ"))
#                         def test_dcm_ecef2ned() -> None:
#                             """Test Cases for the dcm_ecef2ned function"""

#                             # Test Case 1: Zero latitude and longitude
#                             lat = 0.0
#                             lon = 0.0
#                             expected_dcm = np.array([[0, 0, 1],
#                                                      [1, 0, 0],
#                                                      [0, 1, 0]])
#                             computed_dcm = dcm_ecef2ned(lat, lon)
#                             assert np.allclose(computed_dcm, expected_dcm), "Test Case 1 Failed"

#                             # Test Case 2: Non-zero latitude and longitude
#                             lat = np.deg2rad(45.0)
#                             lon = np.deg2rad(-30.0)
#                             expected_dcm = np.array([[0.70710678, -0.70710678, 0],
#                                                      [0.5, 0.5, -0.70710678],
#                                                      [0.5, 0.5, 0.70710678]])
#                             computed_dcm = dcm_ecef2ned(lat, lon)
#                             assert np.allclose(computed_dcm, expected_dcm), "Test Case 2 Failed"

#                             # Test Case 3: Negative latitude and longitude
#                             lat = np.deg2rad(-60.0)
#                             lon = np.deg2rad(-120.0)
#                             expected_dcm = np.array([[0.5, -0.5, -0.70710678],
#                                                      [0.8660254, 0.8660254, 0],
#                                                      [0, 0, 1]])
#                             computed_dcm = dcm_ecef2ned(lat, lon)
#                             assert np.allclose(computed_dcm, expected_dcm), "Test Case 3 Failed"

#                             # Add more test cases as needed

#                         test_dcm_ecef2ned()





        