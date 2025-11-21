"""
Problem: Multi-Source Confidence Propagation (BFS + Priority Queue)

Background:
Auto-labeling propagation system for Waabi's autonomous driving dataset.
Propagate high-confidence labels to neighboring unlabeled pixels based on
feature similarity (inspired by LabelFormer paper).

Time Complexity: O((V + E) log V) where V = H*W pixels, E = edges
Space Complexity: O(V) for visited array and priority queue

Key Patterns:
- Multi-source BFS with priority queue
- Max heap (simulated with negative values in min heap)
- Cosine similarity for feature matching
- Greedy propagation (highest confidence first)
"""

import heapq
import math
from typing import Any


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Calculate cosine similarity between two feature vectors.

    Args:
        vec_a: First feature vector
        vec_b: Second feature vector

    Returns:
        Cosine similarity in range [-1, 1]
        Returns 0.0 if either vector has zero norm
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b, strict=True))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def solve() -> None:
    """
    Main solution function for confidence propagation.

    Algorithm:
    1. Initialize priority queue with all seed pixels
    2. Pop highest confidence pixel
    3. Propagate to unlabeled neighbors if similarity >= threshold
    4. New confidence = current_conf * similarity
    5. Repeat until queue is empty
    """
    # ============ Input Parsing ============
    # Read grid dimensions
    h, w = map(int, input().split())

    # Build grid: 2D array of dicts
    grid: list[list[dict[str, Any]]] = []
    for _ in range(h):
        # Read entire row as floats
        row_data = list(map(float, input().split()))
        row: list[dict[str, Any]] = []

        # Each cell has 5 values: label, conf, f1, f2, f3
        for i in range(0, len(row_data), 5):
            cell = {
                "label": int(row_data[i]),
                "confidence": row_data[i + 1],
                "features": [row_data[i + 2], row_data[i + 3], row_data[i + 4]],
            }
            row.append(cell)

        grid.append(row)

    # Read seed pixels
    n = int(input())
    seed_pixels: list[tuple[int, int]] = []
    for _ in range(n):
        r, c = map(int, input().split())
        seed_pixels.append((r, c))

    # Read similarity threshold
    similarity_threshold = float(input())

    # ============ Algorithm ============
    # Initialize visited array
    visited = [[False] * w for _ in range(h)]
    pq: list[tuple[float, int, int]] = []  # Priority queue (max heap)

    # Add all seed pixels to heap
    for r, c in seed_pixels:
        conf = grid[r][c]["confidence"]
        # Python heapq is min heap, use negative to simulate max heap
        heapq.heappush(pq, (-conf, r, c))

    propagated_count = 0

    # Main loop: process pixels by decreasing confidence
    while pq:
        neg_conf, r, c = heapq.heappop(pq)
        conf = -neg_conf  # Convert back to positive

        # Skip if already processed
        if visited[r][c]:
            continue

        visited[r][c] = True

        current_label = grid[r][c]["label"]
        current_features = grid[r][c]["features"]

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            # Boundary check
            if not (0 <= nr < h and 0 <= nc < w):
                continue

            neighbor = grid[nr][nc]

            # Only propagate to unlabeled neighbors
            if neighbor["label"] != 0:
                continue

            # Skip if already propagated
            if visited[nr][nc]:
                continue

            # Calculate feature similarity
            sim = cosine_similarity(current_features, neighbor["features"])

            # Check similarity threshold
            if sim < similarity_threshold:
                continue

            # Propagate label!
            new_conf = max(0.0, conf * sim)  # Ensure non-negative
            neighbor["label"] = current_label
            neighbor["confidence"] = new_conf
            propagated_count += 1

            heapq.heappush(pq, (-new_conf, nr, nc))

    # ============ Output ============
    print(propagated_count)

    for r in range(h):
        row_output = []
        for c in range(w):
            label = grid[r][c]["label"]
            conf_val = grid[r][c]["confidence"]
            row_output.append(f"({label}, {conf_val:.2f})")
        print(" ".join(row_output))


if __name__ == "__main__":
    solve()
