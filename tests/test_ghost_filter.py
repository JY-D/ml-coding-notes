import importlib.util
import sys
from pathlib import Path

import pytest

# --- PATH SETUP ---
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "filter_ghost_objects" / "filter_ghost_objects_solution.py"


# --- DYNAMIC IMPORT ---
def load_solution_function(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Solution file not found at: {path}")

    spec = importlib.util.spec_from_file_location("ghost_solution", path)

    # 1. Explicit check for Spec (Fixes arg-type error)
    if spec is None:
        raise ImportError(f"Could not load spec from {path}")

    # 2. Explicit check for Loader (Fixes union-attr error)
    if spec.loader is None:
        raise ImportError(f"No loader found for {path}")

    # Now MyPy knows spec is definitely NOT None, and loader is NOT None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ghost_solution"] = module
    spec.loader.exec_module(module)

    return module.filter_ghost_objects


filter_ghost_objects = load_solution_function(SOLUTION_PATH)


class TestGhostFilter:
    def test_normal_movement(self):
        """Car moving at 10m/s (Limit 30). All valid."""
        detections = [
            (0.0, 0.0, 0.0),
            (0.1, 1.0, 0.0),  # dist=1, dt=0.1, v=10
            (0.2, 2.0, 0.0),  # dist=1, dt=0.1, v=10
        ]
        assert filter_ghost_objects(detections, max_speed=30.0) == [True, True, True]

    def test_ghost_glitch(self):
        """One frame jumps 100m instantly."""
        detections = [
            (0.0, 0.0, 0.0),
            (0.1, 100.0, 0.0),  # dist=100, dt=0.1, v=1000! (Ghost)
            (0.2, 2.0, 0.0),  # Should compare to Frame 0, not Frame 1.
            # dt=0.2, dist=2, v=10 (Valid)
        ]
        # Frame 1 is False. Frame 2 is True (recovered).
        assert filter_ghost_objects(detections, max_speed=30.0) == [True, False, True]

    def test_chain_of_ghosts(self):
        """Continuous noise."""
        detections = [
            (0.0, 0.0, 0.0),
            (0.1, 50.0, 0.0),  # Ghost
            (0.2, 60.0, 0.0),  # Ghost (relative to Frame 0, v=300)
            (0.3, 3.0, 0.0),  # Valid (relative to Frame 0, v=10)
        ]
        assert filter_ghost_objects(detections, max_speed=30.0) == [True, False, False, True]

    def test_duplicate_timestamp(self):
        """dt = 0 case."""
        detections = [
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),  # Same point, same time. v=0/1e-6=0. Valid.
        ]
        assert filter_ghost_objects(detections, max_speed=30.0) == [True, True]

    def test_empty(self):
        assert filter_ghost_objects([], 30.0) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
