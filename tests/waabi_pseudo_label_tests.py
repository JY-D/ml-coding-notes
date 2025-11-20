import subprocess
import sys
from pathlib import Path

import pytest

solution_path = (
    Path(__file__).parent.parent / "problems" / "waabi-pseudo-label" / "pseudo_label_solution.py"
)


def run_solution(input_data: str) -> str:
    """Run solution with given input and return output."""
    result = subprocess.run(
        [sys.executable, str(solution_path)],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Solution failed: {result.stderr}")
    return result.stdout.strip()


class TestPseudoLabel:
    def test_case_1_basic(self) -> None:
        """Basic test with mixed confidence levels"""
        input_data = """5
img_001,0.92,truck,False
img_002,0.55,car,False
img_003,0.88,truck,True
img_004,0.45,car,False
img_005,0.78,truck,False"""

        expected = """=== Routing Summary ===
HIGH (>= 0.8): 2 images (40.0%)
  - Auto-accept for training: ['img_001', 'img_003']
MID (0.5 - 0.8): 2 images (40.0%)
  - Send to vendor QA: ['img_002', 'img_005']
LOW (< 0.5): 1 images (20.0%)
  - Discard: ['img_004']

=== Per-Label Statistics ===
car: count=2, avg_confidence=0.50, HIGH=0.0%, MID=50.0%, LOW=50.0%
truck: count=3, avg_confidence=0.86, HIGH=66.7%, MID=33.3%, LOW=0.0%

=== Ground Truth Validation ===
HIGH confidence samples with GT: 1
Accuracy: 100.0% (1/1 correct)"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_2_all_high(self) -> None:
        """All samples are high confidence"""
        input_data = """3
img_001,0.95,truck,True
img_002,0.88,car,True
img_003,0.92,truck,False"""

        expected = """=== Routing Summary ===
HIGH (>= 0.8): 3 images (100.0%)
  - Auto-accept for training: ['img_001', 'img_002', 'img_003']
MID (0.5 - 0.8): 0 images (0.0%)
  - Send to vendor QA: []
LOW (< 0.5): 0 images (0.0%)
  - Discard: []

=== Per-Label Statistics ===
car: count=1, avg_confidence=0.88, HIGH=100.0%, MID=0.0%, LOW=0.0%
truck: count=2, avg_confidence=0.94, HIGH=100.0%, MID=0.0%, LOW=0.0%

=== Ground Truth Validation ===
HIGH confidence samples with GT: 2
Accuracy: 100.0% (2/2 correct)"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_3_all_low(self) -> None:
        """All samples are low confidence"""
        input_data = """2
img_001,0.35,truck,False
img_002,0.42,car,False"""

        expected = """=== Routing Summary ===
HIGH (>= 0.8): 0 images (0.0%)
  - Auto-accept for training: []
MID (0.5 - 0.8): 0 images (0.0%)
  - Send to vendor QA: []
LOW (< 0.5): 2 images (100.0%)
  - Discard: ['img_001', 'img_002']

=== Per-Label Statistics ===
car: count=1, avg_confidence=0.42, HIGH=0.0%, MID=0.0%, LOW=100.0%
truck: count=1, avg_confidence=0.35, HIGH=0.0%, MID=0.0%, LOW=100.0%

=== Ground Truth Validation ===
HIGH confidence samples with GT: 0
No HIGH confidence samples with GT available"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_4_no_gt(self) -> None:
        """No ground truth available"""
        input_data = """3
img_001,0.92,truck,False
img_002,0.88,car,False
img_003,0.85,truck,False"""

        output = run_solution(input_data)
        assert "HIGH confidence samples with GT: 0" in output
        assert "No HIGH confidence samples with GT available" in output

    def test_case_5_boundary(self) -> None:
        """Test boundary values (exactly 0.8 and 0.5)"""
        input_data = """4
img_001,0.80,truck,False
img_002,0.50,car,False
img_003,0.79,truck,False
img_004,0.49,car,False"""

        output = run_solution(input_data)
        # 0.80 should be HIGH
        assert "'img_001'" in output.split("Auto-accept")[1].split("\n")[0]
        # 0.50 should be MID
        assert "'img_002'" in output.split("vendor QA")[1].split("\n")[0]
        # 0.79 should be MID
        assert "'img_003'" in output.split("vendor QA")[1].split("\n")[0]
        # 0.49 should be LOW
        assert "'img_004'" in output.split("Discard")[1].split("\n")[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
