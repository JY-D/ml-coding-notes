import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

# --- 1. PATH SETUP ---
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "nms" / "nms_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def load_solution_function(path: Path):
    spec = importlib.util.spec_from_file_location("nms_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["nms_solution"] = module
    spec.loader.exec_module(module)
    return module.nms


nms = load_solution_function(SOLUTION_PATH)


class TestNMS:
    def test_basic_suppression(self) -> None:
        """
        Three boxes:
        Box 0: (10, 10, 50, 50), Score 0.9  <-- Highest, Keep
        Box 1: (10, 10, 48, 48), Score 0.8  <-- High IoU with Box 0, Suppress
        Box 2: (100, 100, 150, 150), Score 0.7 <-- No overlap, Keep
        """
        boxes = np.array([[10.0, 10.0, 50.0, 50.0], [10.0, 10.0, 48.0, 48.0], [100.0, 100.0, 150.0, 150.0]])
        scores = np.array([0.9, 0.8, 0.7])
        threshold = 0.5

        # Should keep index 0 and 2
        # Index 1 should be suppressed because it overlaps heavily with index 0
        keep = nms(boxes, scores, iou_threshold=threshold)

        # Sort output to compare easily (though NMS usually returns high-score first)
        assert sorted(keep) == [0, 2]

    def test_perfect_overlap(self) -> None:
        """Identical boxes, should only keep the highest score"""
        boxes = np.array([[10, 10, 50, 50], [10, 10, 50, 50], [10, 10, 50, 50]]).astype(float)
        scores = np.array([0.5, 0.9, 0.7])  # Index 1 is winner

        keep = nms(boxes, scores, iou_threshold=0.5)

        assert keep == [1]

    def test_empty_input(self) -> None:
        """Edge case: No boxes"""
        boxes = np.array([])
        scores = np.array([])

        keep = nms(boxes, scores)
        assert keep == []

    def test_threshold_logic(self) -> None:
        """Test strict vs loose threshold"""
        # Two boxes with IoU approx 0.6
        # Box 1: 100 area
        # Box 2: overlap 60 area
        # Intersection 60, Union 140 -> IoU ~ 0.42

        boxes = np.array(
            [[0, 0, 10, 10], [0, 0, 10, 6]]  # Area 100  # Area 60, fully inside Box 1. IoU = 60/100 = 0.6
        ).astype(float)
        scores = np.array([0.9, 0.8])

        # If threshold is 0.7 (loose), both should be kept (0.6 < 0.7)
        keep_loose = nms(boxes, scores, iou_threshold=0.7)
        assert sorted(keep_loose) == [0, 1]

        # If threshold is 0.5 (strict), Box 1 should be suppressed (0.6 > 0.5)
        keep_strict = nms(boxes, scores, iou_threshold=0.5)
        assert keep_strict == [0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
