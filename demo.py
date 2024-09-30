"""This module provides a Runge-Kutta 4th order solver for solving ordinary
differential equations (ODEs).

Classes:
- ODEOutput: Represents the output of the ODE solver, including time points, state vectors,
 extracted values, and metadata.
- ODESolver: Implements the Runge-Kutta 4th order integration method for solving ODEs.

Functions:
- RK4: Performs a single step of the Runge-Kutta 4th order integration method."""

from typing import Callable, TypeVar
from dataclasses import dataclass, field
from enum import StrEnum, auto
import numpy as np
from numpy.typing import NDArray
import attrs

VectorType = TypeVar('VectorType', bound=NDArray[np.float_])

def rk4(
    tc: float,
    xc: VectorType,
    dt: float,
    func: Callable[[float, VectorType], VectorType]
) -> VectorType:  # Updated return type hint to be consistent with input
    """
    Runge-Kutta 4th order method for solving ordinary differential equations.

    Parameters:
        tc (float): The current time.
        xc (VectorType): The current state vector.
        dt (float): The time step size.
        func (Callable[[float, VectorType], VectorType]): The function that defines
            the system of differential equations.

    Returns:
        VectorType: The updated state vector after one time step.
    """
    k1 = dt * func(tc, xc)
    k2 = dt * func(tc + dt / 2, VectorType(xc + k1 / 2))
    k3 = dt * func(tc + dt / 2, xc + k2 / 2)
    k4 = dt * func(tc + dt, xc + k3)
    return xc + (k1 + 2 * k2 + 2 * k3 + k4) / 6

@dataclass(slots=True)
class ODEOutput:
    """
    Represents the output of an ODE solver.

    Attributes:
        t_values (np.ndarray): An array of time points.
        y_values (np.ndarray): A 2D array of state vectors.
        z_values (np.ndarray): A 2D array of extracted values.
        metadata (dict): Additional metadata.

    Raises:
        NotImplementedError: Addition of ODEOutput objects is not supported.
    """
    t_values: np.ndarray = field(metadata={'description': 'An array of time points'})
    y_values: np.ndarray = field(metadata={'description': 'A 2D array of state vectors'})
    z_values: np.ndarray = field(
        default_factory=np.array, # type: ignore
        metadata={'description': 'A 2D array of extracted value'})
    metadata: dict = field(
        default_factory=dict,
        metadata={'description': 'Additional metadata'})

    def __add__(self, other):
        raise NotImplementedError("Addition of ODEOutput objects is not supported.")
    #TODO: Add a method to merge two ODEOutput objects


class ODEStatus(StrEnum):
    """
    An enumeration class representing the status of the ODE solver.

    Attributes:
    - SUCCESS: The solver successfully completed the integration.
    - STOPPED: The solver stopped due to a stop condition.
    - ERROR: An error occurred during the integration.
    """
    SUCCESS = auto()
    STOPPED = auto()
    ERROR = auto()


def default_callable(*args, **kwargs): # pylint: disable=unused-argument
    """
    This is a default callable function.

    Parameters:
    - args: Variable length argument list.
    - kwargs: Arbitrary keyword arguments.

    Returns:
    - An empty NumPy array.

    """
    return np.array([])

def default_check_callable(*args, **kwargs): # pylint: disable=unused-argument
    """
    This function is a default implementation of a check callable.

    Parameters:
    - *args: Variable length argument list.
    - **kwargs: Arbitrary keyword arguments.

    Returns:
    - bool: False.

    """
    return False

@attrs.define(slots=True)
class ODESolver:
    """A class representing a solver for a system of ordinary differential equations
    (ODEs) using the Runge-Kutta 4th order method.

    Attributes:
    - time_span (tuple): The time span for the solution.
    - dt (float): The time step size.
    - x0 (np.ndarray): The initial state vector.
    - func (Callable): The system of ODEs.
    - parameter_function (Callable): The parameter function.
    - stop_condition (Callable): The stop condition function.
    - t (float): The current time in seconds.
    - x (np.ndarray): The current state vector.
    - z (np.ndarray): The current extracted value.
    - stop (bool): The stop condition.
    - integration_method (Callable): The integration method. Default is RK4.

    Methods:
    - solve(): Solves the system of ODEs using the Runge-Kutta 4th order method.
    - step(): Executes one step of the integration for a system of ODEs."""

    time_span: tuple = attrs.field(
        metadata={'description': 'The time span for the solution'},
        kw_only=True,
    )
    @time_span.validator # type: ignore
    def _validate_time_span(self, attribute, value): # type: ignore
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError(
                f"Time span {attribute.name} must be a tuple of two values (t0, t_end).")
        if not all(isinstance(t, (int, float)) for t in value):
            raise ValueError(
                f"Time span {attribute.name} values must be integers or floats.")
        if value[0] >= value[1]:
            raise ValueError(
                "Initial time must be less than the final time.")

    dt: float = attrs.field(
        metadata={'description': 'The time step size'},
        validator=[
            attrs.validators.instance_of(float),
            attrs.validators.gt(0),],
        converter=float,
    )

    x0: np.ndarray = attrs.field(
        metadata={'description': 'The initial state vector'},
        kw_only=True,
        converter=np.array,
    )
    @x0.validator # type: ignore
    def _validate_x0(self, attribute, value): # type: ignore
        if not isinstance(value, np.ndarray):
            raise TypeError((f"'{attribute.name}' must be a numpy ndarray,"
                             f" but got {type(value).__name__}."))
        if value.ndim != 1:
            raise ValueError(
                (f"'{attribute.name}' must be a one-dimensional array (vector),"
                 f" but got an array with {value.ndim} dimensions."))

    func: Callable = attrs.field(
        metadata={'description': 'The system of ODEs'},
        kw_only=True,
    )
    @func.validator # type: ignore
    def _validate_func(self, attribute, value): # type: ignore
        if not callable(value):
            raise ValueError(
                f"'{attribute.name}' must be a callable function.")

    parameter_function: Callable = attrs.field(
        metadata={'description': 'The parameter function'},
        kw_only=True,
        default=attrs.Factory(lambda: default_callable),
    )
    @parameter_function.validator # type: ignore
    def _validate_parameter_function(self, attribute, value): # type: ignore
        if value is not None and not callable(value):
            raise ValueError(
                f"'{attribute.name}' must be a callable function.")

    stop_condition: Callable = attrs.field(
        metadata={'description': 'The stop condition function'},
        kw_only=True,
        default=attrs.Factory(lambda: default_check_callable),
    )
    @stop_condition.validator # type: ignore
    def _validate_stop_condition(self, attribute, value): # type: ignore
        if value is not None and not callable(value):
            raise ValueError(
                f"'{attribute.name}' must be a callable function.")

    t : float = attrs.field(
        metadata={'description': 'The current time in seconds'},
        init=False,
        validator=attrs.validators.instance_of(float),
        converter=float,
    )

    x : np.ndarray = attrs.field(
        metadata={'description': 'The current state vector'},
        init=False,
        validator=attrs.validators.instance_of(np.ndarray),
    )

    z: np.ndarray = attrs.field(
        metadata={'description': 'The current extracted value'},
        init=False,
        converter=np.array,
        validator=attrs.validators.instance_of(np.ndarray))

    stop: bool = attrs.field(
        metadata={'description': 'The stop condition'},
        init=False,
        default=False,
        converter=bool,
        validator=attrs.validators.instance_of(bool), # type: ignore
    ) # type: ignore

    integration_method: Callable = attrs.field(
        metadata={'description': 'The integration method'},
        default=attrs.Factory(lambda: rk4),
    )
    failed: bool = attrs.field(
        metadata={'description': 'An indicator of whether the solver failed'},
        default=False,
        converter=bool,
        validator=attrs.validators.instance_of(bool), # type: ignore
    ) # type: ignore

    def __attrs_post_init__(self):
        # initialize the current time and state vector
        self.t = self.time_span[0]
        self.x = self.x0

        # validate the shape of the function output
        self._validate_func() # pylint: disable=no-value-for-parameter

        # validate the shape of the parameter function output
        self._validate_parameter_function() # pylint: disable=no-value-for-parameter

        # validate the stop condition function
        self._validate_stop_condition() # pylint: disable=no-value-for-parameter

        # initialize the current extracted value
        self.z = self.parameter_function(self.t, self.x) # type: ignore

        # check the stop condition
        self.stop = self.stop_condition(self.t, self.x) # type: ignore

    def _validate_func(self) -> None:
        try:
            test_output =self.func(self.t, self.x)
        except Exception as e:
            raise ValueError((
                f"Error when evaluating the function with :\n"
                f"- state Vector : {self.x}\n"
                f"- time value : {self.t}\n"
                f"due to : {e}")) from e

        test_output = np.array(test_output, dtype=float)
        if test_output.shape != self.x.shape:
            raise ValueError((
                f"Inconsistent shapes: function output shape {test_output.shape} "
                f"does not match initial values shape {self.x.shape}"))

    def _validate_parameter_function(self) -> None:
        try:
            self.parameter_function(self.t, self.x)
        except Exception as e:
            raise ValueError((
                f"Error when evaluating the parameter function with :\n"
                f"- state Vector : {self.x}\n"
                f"- time value : {self.t}\n"
                f"due to : {e}")) from e

    def _validate_stop_condition(self) -> None:
        try:
            value= self.stop_condition(self.t, self.x)
        except Exception as e:
            raise ValueError((
                f"Error when evaluating the stop condition function with :\n"
                f"- state Vector : {self.x}\n"
                f"- time value : {self.t}\n"
                f"due to : {e}")) from e

        if not isinstance(value, bool):
            raise ValueError((
                f"Stop condition function must return a boolean value,"
                f" but got {type(value).__name__}"))

    @property
    def t0(self):
        """
        Returns the first element of the time_span list.

        Returns:
            The first element of the time_span list.
        """
        return self.time_span[0]

    @property
    def t_end(self):
        """
        Returns the end time of the time span.

        Returns:
            int: The end time of the time span.
        """
        return self.time_span[1]

    def solve(self):
        # Number of steps
        n_steps = int((self.t_end - self.t) / self.dt)

        # init metadata
        metadata = {
            "solver": self.func.__name__,
            "time_span": self.time_span,
            "dt": self.dt,
            "n_steps": n_steps,
        }

        # Initialize arrays to store the results
        t_values = np.linspace(self.t, self.t_end, n_steps + 1)
        x_values = np.zeros((n_steps + 1, len(self.x)))
        z_values = np.zeros((n_steps + 1, self.z.size)) \
            if self.z.size > 0 else np.array([])

        # Set the initial conditions
        x_values[0] = self.x

        if self.z.size > 0:
            z_values[0] = self.z

        # Perform the Runge-Kutta integration
        for i in range(n_steps):
            try:
                self.step()
                x_values[i + 1] = self.x
                t_values[i + 1] = self.t

                if self.z.size > 0:
                    z_values[i + 1] = self.z

                if self.stop:
                    metadata["message"] = f"Stop condition met at time {self.t}."
                    metadata["status"] = ODEStatus.STOPPED
                    return ODEOutput(
                        t_values=t_values[:i + 1],
                        y_values=x_values[:i + 1],
                        z_values=z_values[:i + 1],
                        metadata=metadata)
            except Exception as e: # pylint: disable=broad-except
                metadata["status"] = ODEStatus.ERROR
                metadata["message"] = f"An error occurred at step {i + 1}: {e}"
                return ODEOutput(
                    t_values=t_values[:i + 1],
                    y_values=x_values[:i + 1],
                    z_values=z_values[:i + 1],
                    metadata=metadata)

        metadata["status"] = ODEStatus.SUCCESS
        metadata["message"] = "Integration completed successfully."
        return ODEOutput(
            t_values=t_values,
            y_values=x_values,
            z_values=z_values,
            metadata=metadata)

    def step(self) -> None:
        """
        Execute one step of the integration for a system of ODEs.

        Returns:
        - y_next: The next value of the state vector after one step.
        """

        try:
            if self.stop:
                raise ValueError("Stop condition already met.")

            if self.failed:
                raise ValueError("Solver failed.")

            x_next = self.integration_method(self.t, self.x, self.dt, self.func)

            # Update the value of x and t
            self.x = x_next
            self.t += self.dt

            # update the value of z
            self.z = self.parameter_function(self.t, self.x)

            # check the stop condition
            self.stop = self.stop_condition(self.t, self.x)
        except Exception as e:
            self.failed = True
            raise ValueError(f"An error occurred during the integration: {e}") from e

# Example usage:
def example_ode_system(t, y):
    return np.array([y[1], -y[0]])

def example_parameter_function(t, y):
    return t*3

def example_stop_condition(t, y):
    return t > 4

# Initial values for the system
initial_values = [1, 0]  # Example: y1(0) = 1, y2(0) = 0

# Initialize the solver
solver = ODESolver(
    func=example_ode_system,
    x0=initial_values,
    time_span=(0, 10),
    dt=0.1,
    parameter_function=example_parameter_function,
    stop_condition=example_stop_condition,
)

print(f"Initial state vector: y({solver.t}) = {solver.x}")

# Execute one step
solver.step()
print(f"Next state vector after one step: y({solver.t}) = {solver.x}")

# Solve the ODE over the entire time span
res = solver.solve()
print(res.t_values)
print(res.y_values)

print(res.metadata)
