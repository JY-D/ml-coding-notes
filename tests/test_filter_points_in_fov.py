import importlib.util
import math
import sys
from pathlib import Path

import pytest

# --- 1. PATH SETUP ---
# Adjust this path if your folder name is different
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "filter_points_in_fov" / "filter_points_in_fov_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def load_solution_function(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Solution file not found at: {path}")

    spec = importlib.util.spec_from_file_location("fov_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["fov_solution"] = module
    spec.loader.exec_module(module)
    return module.filter_points_in_fov


# Load the function
filter_points_in_fov = load_solution_function(SOLUTION_PATH)


class TestFovFilter:
    def test_basic_inside(self):
        """Standard points clearly inside the sector."""
        # Car at (0,0) facing +x. FOV=60 (Half=30). MaxDist=10.
        points = [
            [5.0, 0.0],  # Dead center
            [5.0, 1.0],  # Slightly left
            [5.0, -1.0],  # Slightly right
        ]
        results = filter_points_in_fov(points, max_distance=10.0, fov_degrees=60.0)
        assert results == [True, True, True]

    def test_distance_cutoff(self):
        """Points within angle but too far away."""
        points = [
            [10.1, 0.0],  # Just beyond 10m
            [20.0, 0.0],  # Far away
        ]
        results = filter_points_in_fov(points, max_distance=10.0, fov_degrees=60.0)
        assert results == [False, False]

    def test_angle_cutoff(self):
        """Points within distance but outside angle."""
        # FOV 60 -> +/- 30 degrees.
        # (1, 1) is 45 degrees -> Should be False
        # (0, 5) is 90 degrees -> Should be False
        points = [[1.0, 1.0], [0.0, 5.0]]
        results = filter_points_in_fov(points, max_distance=10.0, fov_degrees=60.0)
        assert results == [False, False]

    def test_behind_vehicle(self):
        """Points with negative x (Behind the car)."""
        # atan2 will return +/- pi (approx 3.14) or close to it.
        # 3.14 > 0.52 (30 deg rad), so should be False.
        points = [[-5.0, 0.0], [-1.0, 1.0]]  # Directly behind  # Behind and left
        results = filter_points_in_fov(points, max_distance=10.0, fov_degrees=60.0)
        assert results == [False, False]

    def test_boundary_conditions(self):
        """Points exactly on the boundary."""
        # Max distance boundary: [10.0, 0.0] -> True
        # Angle boundary: 30 degrees.
        # x = 10 * cos(30), y = 10 * sin(30)

        angle_rad = math.radians(30.0)
        x_edge = 5.0 * math.cos(angle_rad)
        y_edge = 5.0 * math.sin(angle_rad)

        points = [
            [10.0, 0.0],  # Exact distance limit
            [x_edge, y_edge],  # Exact +30 deg limit
            [x_edge, -y_edge],  # Exact -30 deg limit
        ]

        # Note: Floating point precision might be tricky, but logic uses <=
        results = filter_points_in_fov(points, max_distance=10.0, fov_degrees=60.0)
        assert results == [True, True, True]

    def test_empty_input(self):
        """Edge case: No points."""
        assert filter_points_in_fov([], 10.0, 60.0) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
