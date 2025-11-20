import subprocess
import sys
from pathlib import Path

import pytest

# Solution path
solution_path = Path(__file__).parent.parent / "problems" / "waabi-scenario-eval" / "scenario_eval_solution.py"


def run_solution(input_data: str) -> str:
    """Run the solution with given input and return output."""
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


class TestScenarioEval:
    def test_case_1_basic(self):
        """Basic test: multiple scenarios, no anomalies"""
        input_data = """5
1,1000,normal,10,10,18.5
2,1001,low_light,9,10,22.1
3,1002,normal,10,10,19.2
4,1003,low_light,8,10,25.3
5,1004,motion_blur,7,10,28.5"""

        expected = """=== Per-Scenario Statistics ===
low_light: count=2, avg_time=23.70ms, accuracy=0.85, worst_case=25.30ms, p95=25.30ms
motion_blur: count=1, avg_time=28.50ms, accuracy=0.70, worst_case=28.50ms, p95=28.50ms
normal: count=2, avg_time=18.85ms, accuracy=1.00, worst_case=19.20ms, p95=19.20ms

=== Anomalies ===
None detected

=== Top-3 Hard Cases (lowest accuracy) ===
Frame 5: accuracy=0.70, scenario=motion_blur
Frame 4: accuracy=0.80, scenario=low_light
Frame 2: accuracy=0.90, scenario=low_light"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_2_single_scenario(self):
        """Single scenario, no anomalies"""
        input_data = """3
1,1000,normal,10,10,18.0
2,1001,normal,10,10,19.0
3,1002,normal,10,10,20.0"""

        expected = """=== Per-Scenario Statistics ===
normal: count=3, avg_time=19.00ms, accuracy=1.00, worst_case=20.00ms, p95=20.00ms

=== Anomalies ===
None detected

=== Top-3 Hard Cases (lowest accuracy) ===
Frame 1: accuracy=1.00, scenario=normal
Frame 2: accuracy=1.00, scenario=normal
Frame 3: accuracy=1.00, scenario=normal"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_3_with_anomaly(self):
        """Test with anomaly window (3 consecutive frames > 25ms)"""
        input_data = """6
1,1000,normal,10,10,20.0
2,1001,normal,10,10,26.0
3,1002,normal,10,10,27.0
4,1003,low_light,8,10,28.0
5,1004,normal,10,10,19.0
6,1005,normal,10,10,21.0"""

        expected = """=== Per-Scenario Statistics ===
low_light: count=1, avg_time=28.00ms, accuracy=0.80, worst_case=28.00ms, p95=28.00ms
normal: count=5, avg_time=22.60ms, accuracy=1.00, worst_case=27.00ms, p95=27.00ms

=== Anomalies ===
Window: frames 2-4, avg_time=27.00ms, scenarios=[low_light, normal]

=== Top-3 Hard Cases (lowest accuracy) ===
Frame 4: accuracy=0.80, scenario=low_light
Frame 1: accuracy=1.00, scenario=normal
Frame 2: accuracy=1.00, scenario=normal"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_4_edge_gt_zero(self):
        """Edge case: gt = 0 (should handle gracefully)"""
        input_data = """2
1,1000,normal,5,0,18.0
2,1001,normal,10,10,19.0"""

        output = run_solution(input_data)
        assert "accuracy=1.00" in output  # gt=0 should default to 1.0

    def test_case_5_p95_calculation(self):
        """Test P95 calculation with >5 frames"""
        input_data = """10
1,1000,normal,10,10,18.0
2,1001,normal,10,10,19.0
3,1002,normal,10,10,20.0
4,1003,normal,10,10,21.0
5,1004,normal,10,10,22.0
6,1005,normal,10,10,23.0
7,1006,normal,10,10,24.0
8,1007,normal,10,10,25.0
9,1008,normal,10,10,26.0
10,1009,normal,10,10,30.0"""

        output = run_solution(input_data)
        # P95 index = int(0.95 * 10) = 9
        # sorted_times[9] = 30.0
        assert "p95=30.00ms" in output

    def test_case_6_multiple_anomalies(self):
        """Test multiple anomaly windows"""
        input_data = """10
1,1000,normal,10,10,20.0
2,1001,normal,10,10,26.0
3,1002,normal,10,10,27.0
4,1003,normal,10,10,28.0
5,1004,normal,10,10,19.0
6,1005,normal,10,10,29.0
7,1006,normal,10,10,30.0
8,1007,normal,10,10,31.0
9,1008,normal,10,10,18.0
10,1009,normal,10,10,20.0"""

        output = run_solution(input_data)
        assert "Window: frames 2-4" in output
        assert "Window: frames 6-8" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
