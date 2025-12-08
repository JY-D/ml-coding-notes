import importlib.util
import sys
from pathlib import Path

import pytest

# --- PATH SETUP ---
# Note: Adjust folder name if you strictly used "937" or "973"
SOLUTION_PATH = (
    Path(__file__).parent.parent
    / "problems"
    / "973_K-closest-points-to-origin"
    / "973_K-closest-points-to-origin_solution.py"
)


# --- DYNAMIC IMPORT ---
def load_solution_module(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Solution file not found at: {path}")
    spec = importlib.util.spec_from_file_location("k_closest_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["k_closest_solution"] = module
    spec.loader.exec_module(module)
    return module


module = load_solution_module(SOLUTION_PATH)
k_closest_min_heap = module.k_closest_min_heap
k_closest_streaming = module.k_closest_streaming


class TestKClosest:
    @pytest.mark.parametrize("func", [k_closest_min_heap, k_closest_streaming])
    def test_basic_example(self, func):
        """Standard LeetCode example."""
        points = [[1, 3], [-2, 2]]
        k = 1
        # [-2, 2] dist is sqrt(8) ~ 2.82
        # [1, 3] dist is sqrt(10) ~ 3.16
        expected = [[-2, 2]]
        assert func(points, k) == expected

    @pytest.mark.parametrize("func", [k_closest_min_heap, k_closest_streaming])
    def test_k_equals_n(self, func):
        """Return all points."""
        points = [[3, 3], [5, -1], [-2, 4]]
        k = 3
        result = func(points, k)
        # Check lengths match
        assert len(result) == 3
        # Check content match (order might differ for streaming, so sort)
        assert sorted(result) == sorted(points)

    @pytest.mark.parametrize("func", [k_closest_min_heap, k_closest_streaming])
    def test_ties(self, func):
        """Points with same distance."""
        points = [[1, 1], [-1, -1], [1, -1]]  # All dist sqrt(2)
        k = 2
        result = func(points, k)
        assert len(result) == 2
        # Any 2 are valid, but logic should handle it gracefully

    @pytest.mark.parametrize("func", [k_closest_min_heap, k_closest_streaming])
    def test_empty_input(self, func):
        """Edge case: Empty list."""
        assert func([], 0) == []

    def test_streaming_logic_specifically(self):
        """Ensure streaming logic actually evicts the furthest point."""
        points = [[10, 10], [1, 1], [2, 2]]
        k = 1
        # Heap should simplify to size 1.
        # [10,10] in -> [1,1] replaces it -> [2,2] rejected (dist 8 > dist 2)
        # Wait, [2,2] is dist 8. [1,1] is dist 2.
        # Max Heap of size 1 holds the smallest distance seen so far?
        # NO. Max Heap holds the K smallest.
        # If K=1, it holds the smallest.
        # [10,10] (200) -> In. Heap: [200]
        # [1,1] (2) -> 2 < 200. Replace. Heap: [2]
        # [2,2] (8) -> 8 > 2. Ignore? NO.
        # Wait, if K=1, we want the SINGLE CLOSEST point.
        # Heap has [2]. New is 8. Since 8 is worse than 2, we ignore 8.
        # Correct.
        result = k_closest_streaming(points, k)
        assert result == [[1, 1]]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
