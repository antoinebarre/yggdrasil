"""Collection of types used in Yggdrasil."""

from typing import Annotated, Union
from beartype.vale import Is
import numpy as np

FloatNumber = Union[float, np.float64]

FloatInt = Union[int, np.int64]

FloatVector = Union[np.ndarray, list]


# Float64Array3 = Annotated[
#     np.ndarray,
#     Is[
#         lambda array: (
#             array.shape == (3,) and
#             np.issubdtype(array.dtype, np.float64)
#             )
#         ]
#     ]

# Vector = Annotated[
#     np.ndarray,
#     Is[lambda array: (
#         array.ndim == 1 and
#         (np.issubdtype(array.dtype, np.float64) or
#         np.issubdtype(array.dtype, np.int64))
#         )
#        ]
#         ]

# Float641DVector = Annotated[
#     np.ndarray,
#     Is[
#         lambda array: (
#             array.ndim == 1 and
#             np.issubdtype(array.dtype, np.float64)
#             )
#         ]
#     ]

# Float64Matrix_3x3 = Annotated[
#     np.ndarray,
#     Is[
#         lambda array: (
#             array.shape == (3, 3) and
#             np.issubdtype(array.dtype, np.float64)
#             )
#         ]
#     ]