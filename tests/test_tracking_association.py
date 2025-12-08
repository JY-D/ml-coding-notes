import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

# --- 1. PATH SETUP ---
# Adjust path to where your solution file is located
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "tracking_association" / "tracking_association_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def load_solution_function(path: Path):
    """
    Dynamically loads the greedy_match function.
    """
    spec = importlib.util.spec_from_file_location("tracking_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["tracking_solution"] = module
    spec.loader.exec_module(module)
    return module.greedy_match


# Load the function
greedy_match = load_solution_function(SOLUTION_PATH)


class TestTrackingAssociation:
    def test_basic_match(self) -> None:
        """
        Simple case: 2 Tracks, 2 Detections.
        T0 matches D1 (0.8)
        T1 matches D0 (0.7)
        """
        iou_matrix = np.array([[0.1, 0.8], [0.7, 0.2]])  # T0  # T1
        # Expected: T0->D1 (first), then T1->D0
        expected = [(0, 1), (1, 0)]
        # Sort output to ignore order
        assert sorted(greedy_match(iou_matrix, threshold=0.3)) == sorted(expected)

    def test_conflict_one_to_one(self) -> None:
        """
        Conflict case: Both T0 and T1 want D0.
        T0 -> D0 (0.9) - Winner
        T1 -> D0 (0.8) - Loser (should look for D1)
        """
        iou_matrix = np.array(
            [[0.9, 0.1], [0.8, 0.5]]  # T0 loves D0  # T1 also loves D0, but T0 takes it. T1 takes D1 (0.5)
        )

        matches = greedy_match(iou_matrix, threshold=0.3)
        # T0 should take D0 because 0.9 > 0.8
        assert (0, 0) in matches
        # T1 should take D1 because D0 is gone
        assert (1, 1) in matches
        assert len(matches) == 2

    def test_threshold_filtering(self) -> None:
        """
        Test that low IoU matches are ignored.
        """
        iou_matrix = np.array([[0.9, 0.1], [0.1, 0.2]])  # T0 -> D0  # T1 -> D1 (0.2 is below threshold 0.3)

        matches = greedy_match(iou_matrix, threshold=0.3)
        assert matches == [(0, 0)]  # Only one valid match

    def test_uneven_matrix_more_detections(self) -> None:
        """
        1 Track, 3 Detections.
        """
        iou_matrix = np.array([[0.2, 0.9, 0.5]])
        matches = greedy_match(iou_matrix)
        assert matches == [(0, 1)]  # T0 matches D1 (0.9)

    def test_uneven_matrix_more_tracks(self) -> None:
        """
        3 Tracks, 1 Detection.
        """
        iou_matrix = np.array([[0.4], [0.9], [0.5]])  # T1 is the winner
        matches = greedy_match(iou_matrix)
        assert matches == [(1, 0)]

    def test_empty_input(self) -> None:
        """Edge case: Empty matrix (0 tracks or 0 detections)."""
        # 0 Tracks, 2 Detections
        iou_matrix = np.array([]).reshape(0, 2)
        assert greedy_match(iou_matrix) == []

        # 2 Tracks, 0 Detections
        iou_matrix_2 = np.array([]).reshape(2, 0)
        assert greedy_match(iou_matrix_2) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
