import importlib.util
import sys
from pathlib import Path

import pytest

# --- 1. PATH SETUP ---
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "056_merge-intervals" / "merge-intervals_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def load_solution_function(path: Path):
    """
    Dynamically loads the merge function from a file path.
    """
    spec = importlib.util.spec_from_file_location("merge_intervals_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["merge_intervals_solution"] = module
    spec.loader.exec_module(module)
    return module.merge


# Load the function directly
merge = load_solution_function(SOLUTION_PATH)


class TestMergeIntervals:
    def test_basic_overlap(self) -> None:
        """Example 1: Standard overlap case"""
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
        expected = [[1, 6], [8, 10], [15, 18]]
        assert merge(intervals) == expected

    def test_touching_intervals(self) -> None:
        """Example 2: Intervals touching at edges should merge"""
        intervals = [[1, 4], [4, 5]]
        expected = [[1, 5]]
        assert merge(intervals) == expected

    def test_unsorted_input(self) -> None:
        """Test with unsorted input to ensure internal sorting works"""
        intervals = [[1, 4], [0, 4]]
        expected = [[0, 4]]
        assert merge(intervals) == expected

    def test_nested_intervals(self) -> None:
        """One interval is completely inside another"""
        intervals = [[1, 10], [2, 6]]
        expected = [[1, 10]]
        assert merge(intervals) == expected

    def test_chain_reaction(self) -> None:
        """Multiple intervals merging into one big interval"""
        intervals = [[1, 3], [2, 4], [3, 5], [4, 6]]
        expected = [[1, 6]]
        assert merge(intervals) == expected

    def test_single_interval(self) -> None:
        """Edge case: Single interval"""
        intervals = [[1, 4]]
        expected = [[1, 4]]
        assert merge(intervals) == expected

    def test_large_gap(self) -> None:
        """No overlap at all"""
        intervals = [[1, 2], [5, 6], [10, 20]]
        expected = [[1, 2], [5, 6], [10, 20]]
        assert merge(intervals) == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
