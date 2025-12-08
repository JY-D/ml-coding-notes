import math


def filter_points_in_fov(points: list[list[float]], max_distance: float, fov_degrees: float) -> list[bool]:
    """
    Args:
        points: List of [x, y] coordinates. (Car is at 0,0 facing +x)
        max_distance: Maximum detection range (meters).
        fov_degrees: Total Field of View in degrees (e.g., 60.0).
        Assume the FOV is centered around the +x axis.
    Returns:
        List of booleans: True if point is inside the sector, False otherwise.
    """
    results = []

    # Pre-compute threshold in radians
    # FOV is total angle, so half_angle = fov / 2
    half_fov_rad = math.radians(fov_degrees / 2)

    for x, y in points:
        dist = (x**2 + y**2) ** 0.5
        if dist > max_distance:
            results.append(False)
            continue

        angle = math.atan2(y, x)

        if abs(angle) <= half_fov_rad:
            results.append(True)
        else:
            results.append(False)

    return results
