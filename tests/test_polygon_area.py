import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

# --- 1. PATH SETUP ---
# Path to the solution file
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "polygon_area" / "polygon_area_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def load_solution_function(path: Path):
    """
    Dynamically loads the function from a file path.
    """
    spec = importlib.util.spec_from_file_location("polygon_area_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["polygon_area_solution"] = module
    spec.loader.exec_module(module)
    return module.polygon_area


# Load the function directly
polygon_area = load_solution_function(SOLUTION_PATH)


class TestPolygonArea:
    def test_square(self) -> None:
        """Test a simple 10x10 square."""
        points = np.array([[0, 0], [10, 0], [10, 10], [0, 10]], dtype=float)
        # Area = 10 * 10 = 100
        assert polygon_area(points) == pytest.approx(100.0, abs=1e-6)

    def test_triangle(self) -> None:
        """Test a right-angled triangle."""
        # Base 10, Height 5. Area = 0.5 * 10 * 5 = 25
        points = np.array([[0, 0], [10, 0], [0, 5]], dtype=float)
        assert polygon_area(points) == pytest.approx(25.0, abs=1e-6)

    def test_rectangle_shifted(self) -> None:
        """Test a rectangle not starting at (0,0)."""
        # Width 3, Height 4. Area = 12
        points = np.array([[1, 1], [4, 1], [4, 5], [1, 5]], dtype=float)
        assert polygon_area(points) == pytest.approx(12.0, abs=1e-6)

    def test_order_independence(self) -> None:
        """Test that clockwise and counter-clockwise give the same area (abs value)."""
        # Counter-Clockwise
        pts_ccw = np.array([[0, 0], [10, 0], [0, 10]], dtype=float)
        # Clockwise
        pts_cw = np.array([[0, 0], [0, 10], [10, 0]], dtype=float)

        area_ccw = polygon_area(pts_ccw)
        area_cw = polygon_area(pts_cw)

        assert area_ccw == pytest.approx(50.0, abs=1e-6)
        assert area_cw == pytest.approx(50.0, abs=1e-6)

    def test_not_enough_points(self) -> None:
        """Edge case: Less than 3 points cannot form a polygon."""
        points = np.array([[0, 0], [10, 10]], dtype=float)
        assert polygon_area(points) == 0.0

    def test_hexagon(self) -> None:
        """Test a regular shape roughly."""
        # Simple irregular hexagon
        # Split into two squares:
        # Square 1: (0,0) to (2,2) -> Area 4
        # Square 2: (2,0) to (4,2) -> Area 4
        # Total Area 8
        points = np.array([[0, 0], [4, 0], [4, 2], [0, 2]], dtype=float)
        assert polygon_area(points) == pytest.approx(8.0, abs=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
