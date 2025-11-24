"""
Problem: Sliding Window Frame Metrics

Background:
Frame-time monitoring system for autonomous driving perception pipeline.
Detect performance anomalies using sliding window statistics.

Time Complexity: O(N * M) where N = frames, M = number of window sizes
Space Complexity: O(N * M) for storing anomalies

Key Patterns:
- Sliding window with sum tracking
- Multiple window sizes (5b variant)
- Statistical threshold detection
"""

import sys
from collections import defaultdict


def solve() -> None:
    """
    Main solution function for frame metrics anomaly detection.

    Algorithm:
    1. For each window size k:
       a. Initialize window sum for first k frames
       b. Check if average exceeds threshold
       c. Slide window and update sum incrementally
       d. Record anomalous windows
    2. Output results for each window size
    """
    # ============ Input Parsing ============
    input_data = sys.stdin.read().strip().split("\n")

    n = int(input_data[0])  # Number of frames
    frame_times = list(map(float, input_data[1].split()))  # Frame times in ms
    ks = list(map(int, input_data[2].split()))  # Window sizes
    max_avg_time = float(input_data[3])  # Threshold in ms

    # ============ Algorithm ============
    anomaly: dict[int, list[list[float]]] = defaultdict(list)

    # Process each window size
    for k in ks:
        # Initialize first window
        win_sum = sum(frame_times[:k])

        # Check first window
        win_avg = win_sum / k
        if win_avg > max_avg_time:
            anomaly[k].append([0, k - 1, win_avg])

        # Slide window through remaining frames
        for i in range(1, n - k + 1):
            # Update window sum incrementally: O(1)
            win_sum += frame_times[i + k - 1] - frame_times[i - 1]
            win_avg = win_sum / k

            if win_avg > max_avg_time:
                anomaly[k].append([i, i + k - 1, win_avg])

    # ============ Output ============
    for k in ks:
        print(f"Window size {k}: {len(anomaly[k])} anomalies")


if __name__ == "__main__":
    solve()
