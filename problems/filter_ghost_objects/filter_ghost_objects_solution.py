def filter_ghost_objects(detections: list[tuple[float, float, float]], max_speed: float) -> list[bool]:
    """
    Filters out detections that violate physical speed constraints.

    Args:
        detections: List of (timestamp, x, y). Sorted by time.
        max_speed: Maximum allowed speed (m/s).

    Returns:
        List of booleans: True if valid, False if ghost/noise.
    """
    if not detections:
        return []

    # Stack to keep track of last VALID measurement
    # We only compare against valid frames to avoid "chain reaction" errors
    valid_detections: list[tuple[float, float, float]] = []
    results: list[bool] = []

    for t, x, y in detections:
        # 1. First frame logic (Always accept initialization)
        if not valid_detections:
            valid_detections.append((t, x, y))
            results.append(True)
            continue

        # 2. Compare with LAST VALID frame
        prev_t, prev_x, prev_y = valid_detections[-1]

        dt = t - prev_t
        # Avoid ZeroDivisionError if timestamps are identical
        if dt == 0:
            dt = 1e-6

        dist = ((x - prev_x) ** 2 + (y - prev_y) ** 2) ** 0.5
        v = dist / dt

        # 3. Check speed limit
        if v <= max_speed:
            results.append(True)
            valid_detections.append((t, x, y))
        else:
            results.append(False)

    return results
