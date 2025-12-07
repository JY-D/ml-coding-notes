import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "bbox_IoU" / "bbox_IoU_solution.py"


# --- 2. DYNAMIC IMPORT HELPER ---
def import_solution_module(path: Path):
    """
    Dynamically load the solution module from a file path.
    This mimics the 'subprocess' isolation but runs in-process for testing functions.
    """
    spec = importlib.util.spec_from_file_location("bbox_IoU_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load solution from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["bbox_IoU_solution"] = module
    spec.loader.exec_module(module)
    return module


# Load the module
sol = import_solution_module(SOLUTION_PATH)


class TestBboxIoU:
    def test_case_1_no_overlap(self) -> None:
        """Basic test case with disjoint boxes"""
        box1 = [0.0, 0.0, 10.0, 10.0]
        box2 = [20.0, 20.0, 30.0, 30.0]
        # 呼叫動態載入的 module function
        assert sol.calculate_iou(box1, box2) == 0.0

    def test_case_2_full_overlap(self) -> None:
        """Test exact overlap"""
        box1 = [10.0, 10.0, 50.0, 50.0]
        box2 = [10.0, 10.0, 50.0, 50.0]
        assert sol.calculate_iou(box1, box2) == pytest.approx(1.0, abs=1e-6)

    def test_case_3_partial_overlap(self) -> None:
        """Standard intersection case"""
        # Intersection: 5*5=25, Union: 100+100-25=175
        box1 = [0.0, 0.0, 10.0, 10.0]
        box2 = [5.0, 5.0, 15.0, 15.0]
        expected_iou = 25.0 / 175.0
        assert sol.calculate_iou(box1, box2) == pytest.approx(expected_iou, abs=1e-6)

    def test_case_4_vectorized_shapes(self) -> None:
        """Verify vectorized implementation against scalar loop"""
        np.random.seed(42)
        N, M = 10, 5

        # Generate random valid boxes
        boxes_a = np.random.randint(0, 50, size=(N, 4)).astype(float)
        boxes_b = np.random.randint(0, 50, size=(M, 4)).astype(float)

        # Ensure valid box coordinates (x2 > x1, y2 > y1)
        boxes_a[:, 2] += boxes_a[:, 0] + 1.0
        boxes_a[:, 3] += boxes_a[:, 1] + 1.0
        boxes_b[:, 2] += boxes_b[:, 0] + 1.0
        boxes_b[:, 3] += boxes_b[:, 1] + 1.0

        # Call vectorized function
        iou_matrix = sol.calculate_iou_vectorized(boxes_a, boxes_b)

        assert iou_matrix.shape == (N, M)

        # Spot check correctness
        for i in range(N):
            for j in range(M):
                scalar_val = sol.calculate_iou(boxes_a[i], boxes_b[j])
                assert iou_matrix[i, j] == pytest.approx(scalar_val, abs=1e-6)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
