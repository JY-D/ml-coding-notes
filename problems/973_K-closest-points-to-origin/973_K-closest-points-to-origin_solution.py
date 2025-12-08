import heapq


def k_closest_min_heap(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Approach 1: Min Heap (Global Sort).
    Time: O(N log N)
    Space: O(N)
    """
    min_heap: list[tuple[int, int, int]] = []

    for x, y in points:
        # Squared distance is sufficient for comparison (avoids sqrt cost)
        dist = x**2 + y**2
        heapq.heappush(min_heap, (dist, x, y))

    results = []
    for _ in range(k):
        _, x, y = heapq.heappop(min_heap)
        results.append([x, y])

    return results


def k_closest_streaming(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Approach 2: Max Heap of size K (Streaming).
    Time: O(N log K) - Efficient for massive N.
    Space: O(K) - Memory efficient.

    Python Trick: Use negative distance to simulate Max Heap with heapq.
    """
    # Max Heap (simulated) storing (-distance, x, y)
    max_heap: list[tuple[int, int, int]] = []

    for x, y in points:
        dist = x**2 + y**2
        # Use negative distance so the "Largest" distance becomes the "Smallest" value
        # and sits at the top of the Min Heap (heap[0]).
        neg_dist = -dist

        if len(max_heap) < k:
            heapq.heappush(max_heap, (neg_dist, x, y))
        else:
            # Check if current point is closer than the furthest point in the heap.
            # max_heap[0][0] is the largest distance (as a negative number).
            # Example: Heap has dist 10 (stored -10). New point dist 5 (stored -5).
            # -5 > -10. So new point is "larger" in heap terms (closer in reality).
            if neg_dist > max_heap[0][0]:
                # Replace the root (worst point) with the new point
                heapq.heapreplace(max_heap, (neg_dist, x, y))

    # Extract points (Order doesn't strictly matter, but usually asked to return list)
    return [[x, y] for (_, x, y) in max_heap]
