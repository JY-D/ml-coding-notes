import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

# --- PATH SETUP ---
# Adjust folder name if needed
SOLUTION_PATH = Path(__file__).parent.parent / "problems" / "hard-sample-mining" / "hard-sample-mining_solution.py"


def load_solution_function(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Solution file not found at: {path}")
    spec = importlib.util.spec_from_file_location("mining_solution", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["mining_solution"] = module
    spec.loader.exec_module(module)
    return module.mine_hard_samples


mine_hard_samples = load_solution_function(SOLUTION_PATH)


class TestHardSampleMining:
    def test_basic_mining(self):
        """
        Scenario: 3 samples.
        0. Perfect prediction (IoU=1.0, Conf=0.9) -> Easy
        1. Wrong prediction (IoU=0.0, Conf=0.9) -> HARD (Should be picked)
        2. Low confidence (Conf=0.1) -> Ignored
        """
        predictions = np.array(
            [[0, 0, 10, 10], [0, 0, 10, 10], [0, 0, 10, 10]]  # Perfect  # Wrong (GT is different)  # Low conf
        )
        ground_truth = np.array(
            [[0, 0, 10, 10], [20, 20, 30, 30], [20, 20, 30, 30]]  # Matches idx 0  # No overlap with idx 1
        )
        confidences = np.array([0.9, 0.9, 0.1])
        classes = np.array([0, 0, 0])

        indices = mine_hard_samples(predictions, ground_truth, confidences, classes, k=1)

        assert len(indices) == 1
        assert indices[0] == 1  # Index 1 is the confident failure

    def test_class_imbalance(self):
        """
        Scenario:
        - Class 0 (Car): Very common, 100 samples. One hard failure.
        - Class 1 (Bike): Rare, 1 sample. One hard failure.

        Both have same failure severity (Conf=0.9, IoU=0).
        But Class 1 should be ranked higher due to inverse frequency weight.
        """
        # Create 100 samples
        N = 100
        predictions = np.zeros((N, 4))
        ground_truth = np.ones((N, 4)) * 100  # No overlap (IoU=0)
        confidences = np.ones(N) * 0.9  # All confident

        # 99 cars (Class 0), 1 bike (Class 1) at the end
        classes = np.zeros(N, dtype=int)
        classes[-1] = 1

        # We want top 1 sample. It should be the bike (index 99).
        indices = mine_hard_samples(predictions, ground_truth, confidences, classes, k=1)

        assert indices[0] == 99

    def test_no_hard_samples(self):
        """
        Scenario: All predictions are perfect. Should return based on 'score'
        but since mask is 0, score is 0. Argsort is stable or implementation dependent,
        but logic should not crash.
        """
        predictions = np.array([[0, 0, 10, 10]])
        ground_truth = np.array([[0, 0, 10, 10]])
        confidences = np.array([0.9])
        classes = np.array([0])

        # Everything is correct (IoU=1.0), so is_wrong=False.
        indices = mine_hard_samples(predictions, ground_truth, confidences, classes, k=1)
        assert len(indices) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
