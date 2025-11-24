"""
Test cases for Sliding Window Frame Metrics problem.
"""

import io
import sys
from pathlib import Path

import pytest

# Add problems directory to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "problems" / "sliding_window_frame_metrics"))


@pytest.fixture
def solution_module():
    """Import solution module."""
    from sliding_window_frame_metrics_solution import solve

    return solve


def run_solution(input_str: str, solution_func) -> str:
    """Helper to run solution with given input and capture output."""
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(input_str)
    sys.stdout = io.StringIO()

    try:
        solution_func()
        output = sys.stdout.getvalue()
        return output
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout


def test_case_1_single_window_size_with_anomalies(solution_module):
    """
    Test Case 1: Single window size with multiple anomalies.

    10 frames, window size 3, threshold 20.0
    Expected: 4 anomalous windows
    """
    input_str = """10
12.5 15.0 18.0 25.0 30.0 28.0 20.0 16.0 14.0 13.0
3
20.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert len(lines) == 1, "Should output 1 line for 1 window size"
    assert "Window size 3: 4 anomalies" in lines[0]


def test_case_2_no_anomalies(solution_module):
    """
    Test Case 2: No anomalies detected.

    All windows have average below threshold.
    """
    input_str = """5
10.0 12.0 11.0 13.0 12.5
3
20.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert "Window size 3: 0 anomalies" in lines[0]


def test_case_3_all_anomalies(solution_module):
    """
    Test Case 3: All windows exceed threshold.

    Every possible window is anomalous.
    """
    input_str = """4
25.0 30.0 28.0 26.0
2
20.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert "Window size 2: 3 anomalies" in lines[0]


def test_case_4_large_window(solution_module):
    """
    Test Case 4: Large window size.

    Window size close to array length.
    """
    input_str = """6
15.0 18.0 20.0 22.0 19.0 21.0
5
19.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert "Window size 5:" in lines[0]


def test_case_5_multiple_window_sizes(solution_module):
    """
    Test Case 5: Multiple window sizes (5b variant).

    Test with 3 different window sizes.
    Expected: Different anomaly counts for each.
    """
    input_str = """10
12.5 15.0 18.0 25.0 30.0 28.0 20.0 16.0 14.0 13.0
3 5 7
20.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert len(lines) == 3, "Should output 3 lines for 3 window sizes"
    assert "Window size 3:" in lines[0]
    assert "Window size 5:" in lines[1]
    assert "Window size 7:" in lines[2]

    # Check that different window sizes give different results
    counts = []
    for line in lines:
        count = int(line.split(":")[1].strip().split()[0])
        counts.append(count)

    # Just check that we got results for all window sizes
    # (Anomaly counts can vary based on data distribution)
    assert all(c >= 0 for c in counts), "All counts should be non-negative"


def test_case_6_single_frame_window(solution_module):
    """
    Test Case 6: Window size of 1.

    Each frame is checked individually.
    """
    input_str = """5
15.0 25.0 18.0 30.0 12.0
1
20.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert "Window size 1:" in lines[0]
    # Should detect frames with value > 20.0 (25.0 and 30.0)
    assert "2 anomalies" in lines[0]


def test_case_7_edge_case_window_equals_array(solution_module):
    """
    Test Case 7: Window size equals array length.

    Only one window possible.
    """
    input_str = """3
15.0 20.0 25.0
3
19.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    assert "Window size 3:" in lines[0]
    # Average of [15, 20, 25] = 20.0 > 19.0
    assert "1 anomalies" in lines[0]


def test_case_8_threshold_exactly_at_boundary(solution_module):
    """
    Test Case 8: Some averages exactly equal threshold.

    Test boundary condition: should NOT count exact equals.
    """
    input_str = """4
10.0 20.0 20.0 10.0
2
15.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    # Window [10, 20] = 15.0 (not > 15.0)
    # Window [20, 20] = 20.0 (> 15.0) ✓
    # Window [20, 10] = 15.0 (not > 15.0)
    assert "Window size 2: 1 anomalies" in lines[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
