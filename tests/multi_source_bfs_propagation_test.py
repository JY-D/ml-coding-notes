"""
Test cases for Multi-Source Confidence Propagation problem.
"""

import io
import sys
from pathlib import Path

import pytest

# Add problems directory to path to import solution
# tests/multi_source_bfs_propagation_test.py needs to import from problems/multi_source_bfs_propagation/solution.py
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "problems" / "multi_source_bfs_propagation"))
# Import will be done in fixtures to avoid import errors during collection


@pytest.fixture
def solution_module():
    """Import solution module."""
    from multi_source_bfs_propagation_solution import solve

    return solve


def run_solution(input_str: str, solution_func) -> str:
    """Helper to run solution with given input and capture output."""
    # Redirect stdin and stdout
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


def test_case_1_single_seed_high_threshold(solution_module):
    """
    Test Case 1: Single seed pixel with high similarity threshold (0.8).

    Grid: 3x3
    Seed: (1,1) with label=1, conf=0.9
    Threshold: 0.8

    Expected: 6 pixels propagated (corners fail similarity check)
    """
    input_str = """3 3
0 0.0 1.0 0.0 0.0    0 0.0 0.8 0.1 0.1    0 0.0 0.5 0.5 0.0
0 0.0 0.9 0.1 0.0    1 0.9 1.0 0.0 0.0    0 0.0 0.7 0.3 0.0
0 0.0 0.6 0.4 0.0    0 0.0 0.9 0.1 0.0    0 0.0 0.4 0.6 0.0
1
1 1
0.8"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    # Check propagated count
    assert lines[0] == "8", f"Expected 8 propagations, got {lines[0]}"

    # Check that center remains labeled
    assert "(1, 0.90)" in lines[2], "Center seed should maintain label and confidence"

    # Check that all cells got labeled (similarity threshold allows it)
    # All cells should have label=1
    for i in range(1, 4):
        assert lines[i].startswith("(1,"), f"Row {i-1} should all have label=1"


def test_case_2_multiple_seeds(solution_module):
    """
    Test Case 2: Multiple seed pixels with different labels.

    Grid: 4x4
    Seeds: (0,0) label=1, (0,3) label=2, (3,0) label=3
    Threshold: 0.85

    Expected: Each seed propagates to similar neighbors
    Higher confidence seeds propagate first
    """
    input_str = """4 4
1 0.95 1.0 0.0 0.0    0 0.0 0.9 0.1 0.0    0 0.0 0.5 0.5 0.0    2 0.90 0.0 1.0 0.0
0 0.0 0.95 0.05 0.0   0 0.0 0.8 0.2 0.0    0 0.0 0.3 0.7 0.0    0 0.0 0.1 0.9 0.0
0 0.0 0.9 0.1 0.0     0 0.0 0.7 0.3 0.0    0 0.0 0.2 0.8 0.0    0 0.0 0.0 1.0 0.0
3 0.88 0.5 0.0 0.5    0 0.0 0.6 0.1 0.3    0 0.0 0.4 0.2 0.4    0 0.0 0.1 0.3 0.6
3
0 0
0 3
3 0
0.85"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    propagated_count = int(lines[0])

    # Should propagate to at least some neighbors
    assert propagated_count > 0, "Should propagate to some neighbors"

    # Check that original seeds maintain their labels
    assert "(1, 0.95)" in lines[1], "Seed at (0,0) should keep label=1"
    assert "(2, 0.90)" in lines[1], "Seed at (0,3) should keep label=2"
    assert "(3, 0.88)" in lines[4], "Seed at (3,0) should keep label=3"


def test_case_3_low_threshold_full_propagation(solution_module):
    """
    Test Case 3: Very low threshold (0.0) - almost everything propagates.

    Grid: 2x2
    Seed: (0,0) with label=1
    Threshold: 0.0

    Expected: All unlabeled neighbors get propagated
    """
    input_str = """2 2
1 0.9 1.0 0.0 0.0    0 0.0 0.0 1.0 0.0
0 0.0 0.0 0.0 1.0    0 0.0 -1.0 0.0 0.0
1
0 0
0.0"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    propagated_count = int(lines[0])

    # Should propagate to all 3 unlabeled cells
    assert propagated_count == 3, f"Expected 3 propagations, got {propagated_count}"

    # Check that all cells have label=1
    for line in lines[1:]:
        assert line.startswith("(1,"), f"All cells should have label=1, got {line}"


def test_case_4_no_propagation_high_threshold(solution_module):
    """
    Test Case 4: Very high threshold (0.99) - no propagation possible.

    Grid: 2x2 with dissimilar features
    Seed: (0,0)
    Threshold: 0.99

    Expected: 0 propagations
    """
    input_str = """2 2
1 0.9 1.0 0.0 0.0    0 0.0 0.0 1.0 0.0
0 0.0 0.0 0.0 1.0    0 0.0 0.5 0.5 0.0
1
0 0
0.99"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    propagated_count = int(lines[0])

    # No propagation should happen (features too dissimilar)
    assert propagated_count == 0, f"Expected 0 propagations, got {propagated_count}"


def test_case_5_single_pixel_grid(solution_module):
    """
    Test Case 5: Edge case - 1x1 grid (no neighbors to propagate).

    Expected: 0 propagations
    """
    input_str = """1 1
1 0.9 1.0 0.0 0.0
1
0 0
0.5"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    propagated_count = int(lines[0])

    # No neighbors to propagate to
    assert propagated_count == 0, f"Expected 0 propagations, got {propagated_count}"

    # Original seed should remain
    assert "(1, 0.90)" in lines[1], "Seed should maintain its label and confidence"


def test_case_6_linear_propagation(solution_module):
    """
    Test Case 6: Linear chain propagation (1D-like in 2D grid).

    Grid: 1x5 (single row)
    Seed: leftmost cell
    Threshold: 0.9 (high similarity required)

    Expected: Propagates along the chain
    """
    input_str = """1 5
1 0.9 1.0 0.0 0.0    0 0.0 0.95 0.05 0.0    0 0.0 0.9 0.1 0.0    0 0.0 0.85 0.15 0.0    0 0.0 0.8 0.2 0.0
1
0 0
0.9"""

    output = run_solution(input_str, solution_module)
    lines = output.strip().split("\n")

    propagated_count = int(lines[0])

    # Should propagate along the chain (at least to immediate neighbors)
    assert propagated_count >= 1, "Should propagate to at least one neighbor"


def test_cosine_similarity_function():
    """Test the cosine_similarity helper function directly."""
    from multi_source_bfs_propagation_solution import cosine_similarity

    # Test identical vectors
    assert abs(cosine_similarity([1.0, 0.0, 0.0], [1.0, 0.0, 0.0]) - 1.0) < 1e-6

    # Test orthogonal vectors
    assert abs(cosine_similarity([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])) < 1e-6

    # Test opposite vectors
    assert abs(cosine_similarity([1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]) - (-1.0)) < 1e-6

    # Test zero vector (should return 0.0)
    assert cosine_similarity([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]) == 0.0
    assert cosine_similarity([1.0, 0.0, 0.0], [0.0, 0.0, 0.0]) == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
