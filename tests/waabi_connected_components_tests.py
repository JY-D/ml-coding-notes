import subprocess
import sys
from pathlib import Path

import pytest

solution_path = (
    Path(__file__).parent.parent
    / "problems"
    / "waabi-connected-components"
    / "connected_components_solution.py"
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


class TestConnectedComponents:
    def test_case_1_basic(self) -> None:
        """Basic test with two components"""
        input_data = """4 5
1 1 0 0 0
1 0 0 1 1
0 0 0 1 0
0 0 1 1 0"""

        expected = """=== Connected Components ===
Total components: 2

Component 1: size=3
  Cells: [(0, 0), (0, 1), (1, 0)]

Component 2: size=5
  Cells: [(1, 3), (1, 4), (2, 3), (3, 2), (3, 3)]"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_2_single_pixels(self) -> None:
        """Five disconnected single-pixel components"""
        input_data = """3 3
1 0 1
0 1 0
1 0 1"""

        expected = """=== Connected Components ===
Total components: 5

Component 1: size=1
  Cells: [(0, 0)]

Component 2: size=1
  Cells: [(0, 2)]

Component 3: size=1
  Cells: [(1, 1)]

Component 4: size=1
  Cells: [(2, 0)]

Component 5: size=1
  Cells: [(2, 2)]"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_3_all_connected(self) -> None:
        """All cells connected as one component"""
        input_data = """3 3
1 1 1
1 1 1
1 1 1"""

        output = run_solution(input_data)
        assert "Total components: 1" in output
        assert "Component 1: size=9" in output

    def test_case_4_no_components(self) -> None:
        """All background (no components)"""
        input_data = """2 2
0 0
0 0"""

        expected = """=== Connected Components ===
Total components: 0"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_5_single_cell(self) -> None:
        """Single cell grid with land"""
        input_data = """1 1
1"""

        output = run_solution(input_data)
        assert "Total components: 1" in output
        assert "Component 1: size=1" in output
        assert "Cells: [(0, 0)]" in output

    def test_case_6_single_cell_background(self) -> None:
        """Single cell grid with background"""
        input_data = """1 1
0"""

        expected = """=== Connected Components ===
Total components: 0"""

        output = run_solution(input_data)
        assert output == expected

    def test_case_7_snake_pattern(self) -> None:
        """Snake-like connected component"""
        input_data = """4 4
1 1 1 0
0 0 1 0
0 1 1 0
0 1 0 0"""

        output = run_solution(input_data)
        assert "Total components: 1" in output
        assert "Component 1: size=7" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
