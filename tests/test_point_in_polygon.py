import importlib.util
import sys
from pathlib import Path

import pytest

# --- PATH SETUP ---
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "point-in-polygon" / "point-in-polygon_solution.py"


def load_solution_function(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Solution file not found at: {path}")
    spec = importlib.util.spec_from_file_location("pip_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pip_solution"] = module
    spec.loader.exec_module(module)
    return module.is_point_in_polygon


is_point_in_polygon = load_solution_function(SOLUTION_PATH)


class TestPointInPolygon:
    def test_square(self):
        # 10x10 square at origin
        poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert is_point_in_polygon((5, 5), poly) is True  # Inside
        assert is_point_in_polygon((15, 5), poly) is False  # Outside Right
        assert is_point_in_polygon((-5, 5), poly) is False  # Outside Left
        assert is_point_in_polygon((5, 15), poly) is False  # Outside Top

    def test_triangle(self):
        # Triangle (0,0) -> (10,0) -> (5,10)
        poly = [(0, 0), (10, 0), (5, 10)]
        assert is_point_in_polygon((5, 5), poly) is True
        assert is_point_in_polygon((5, 9), poly) is True
        assert is_point_in_polygon((5, 11), poly) is False

    def test_concave_shape(self):
        # "L" shape or "Pacman" mouth
        # (0,0) -> (10,0) -> (10,10) -> (0,10) -> (0,5) -> (5,5) -> (5,0) ... wait, simpler L
        poly = [(0, 0), (10, 0), (10, 2), (2, 2), (2, 10), (0, 10)]
        assert is_point_in_polygon((1, 1), poly) is True  # Inside base
        assert is_point_in_polygon((5, 5), poly) is False  # In the empty space of L


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
