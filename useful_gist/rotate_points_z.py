import math
import numpy as np
import numpy.typing as npt


def rotate_points_z_python(points: list[list[float]], theta: float) -> list[list[float]]:
    """
    Rotates 3D points around Z-axis using pure Python.
    Time Complexity: O(N)

    Args:
        points: List of [x, y, z] coordinates.
        theta: Rotation angle in radians.
    """
    rotated_points = []

    # Optimization: Pre-compute trig values outside the loop
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    for point in points:
        x, y, z = point

        # Apply Rotation Matrix for Z-axis
        # x' = x*cos - y*sin
        # y' = x*sin + y*cos
        x_r = x * cos_t - y * sin_t
        y_r = x * sin_t + y * cos_t

        rotated_points.append([x_r, y_r, z])

    return rotated_points


def rotate_points_z_numpy(points: npt.NDArray[np.float64], theta: float) -> npt.NDArray[np.float64]:
    """
    Rotates 3D points around Z-axis using Numpy Vectorization.
    Time Complexity: O(1) (with respect to Python interpreter overhead)

    Args:
        points: (N, 3) numpy array.
        theta: Rotation angle in radians.
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # Construct Rotation Matrix (3, 3)
    # [ cos, -sin, 0]
    # [ sin,  cos, 0]
    # [   0,    0, 1]
    R = np.array([[cos_t, -sin_t, 0], [sin_t, cos_t, 0], [0, 0, 1]])

    # Matrix Multiplication
    # points shape: (N, 3)
    # R shape: (3, 3)
    # Result: (N, 3) -> points @ R.T  OR  (R @ points.T).T
    # Using @ (matmul) automatically handles the dimensions if we align them correctly.
    # Standard convention: Rotated = Original @ R.T
    return points @ R.T
