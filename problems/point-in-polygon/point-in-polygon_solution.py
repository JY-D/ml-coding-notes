def is_point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]

    for i in range(n + 1):
        # Handle wrap-around: p2 is current, p1 is previous
        p2x, p2y = polygon[i % n]

        # 1. Check if point's Y is within the edge's Y range
        # Use (p1y > y) != (p2y > y) to handle vertices safely
        # This ensures we don't double count if the ray passes exactly through a vertex
        if (y > min(p1y, p2y)) and (y <= max(p1y, p2y)):

            # 2. Check if the point is to the LEFT of the edge
            if x <= max(p1x, p2x):

                # 3. Calculate exact intersection X
                # (p1x, p1y) is start, (p2x, p2y) is end
                if p1y != p2y:  # Avoid division by zero (horizontal line)
                    x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                    # 4. Ray Casting Condition
                    # If our point is to the left of the intersection, the ray crosses it.
                    if p1x == p2x or x <= x_inters:
                        inside = not inside

        # Move to next edge
        p1x, p1y = p2x, p2y

    return inside
