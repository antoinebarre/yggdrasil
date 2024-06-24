from typing import Tuple, TypeVar

import numpy as np


T = TypeVar("T", bound=np.generic, covariant=True)

Vector = np.ndarray[Tuple[int], np.dtype[T]]
Matrix = np.ndarray[Tuple[int, int], np.dtype[T]]
Tensor = np.ndarray[Tuple[int, ...], np.dtype[T]]

def f(v: Vector[np.complex64]) -> None:
    print(v[0])


def g(m: Matrix[np.float_]) -> None:
    print(m[0])


def h(t: Tensor[np.int32]) -> None:
    print(t.reshape((1, 4)))


f(np.array([0j+1]))  # prints (1+0j)
f(3)
g(np.array([[3.14, 0.], [1., -1.]]))  # prints [3.14 0.  ]
h(np.array([[3.14, 0.], [1., -1.]]))  # prints [[ 3.14  0.    1.   -1.  ]]