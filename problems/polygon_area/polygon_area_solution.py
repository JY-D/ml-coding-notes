import numpy as np


def polygon_area(points: np.ndarray) -> float:
    # Extract coordinates
    x = points[:, 0]
    y = points[:, 1]

    # Shift arrays to align i with i+1
    x_next = np.roll(x, -1)
    y_next = np.roll(y, -1)

    # Vectorized calculation
    # term1: x_i * y_{i+1}
    # term2: x_{i+1} * y_i
    cross_product = (x * y_next) - (x_next * y)

    return 0.5 * np.abs(np.sum(cross_product))
