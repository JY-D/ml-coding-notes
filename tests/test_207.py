import importlib.util
import sys
from pathlib import Path

import pytest

# Load the solution module dynamically
solution_path = (
    Path(__file__).parent.parent
    / "problems"
    / "207-course-schedule"
    / "course_schedule_solution.py"
)
spec = importlib.util.spec_from_file_location("course_schedule_solution", solution_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load module from {solution_path}")

solution = importlib.util.module_from_spec(spec)
sys.modules["course_schedule_solution"] = solution
spec.loader.exec_module(solution)

canFinish = solution.canFinish


class TestCourseSchedule:
    def test_example_1_possible(self):
        """Basic case: 2 courses with simple dependency"""
        assert canFinish(2, [[1, 0]])

    def test_example_2_cycle(self):
        """Basic cycle: mutual dependency"""
        assert not canFinish(2, [[1, 0], [0, 1]])

    def test_multiple_prerequisites(self):
        """Course with multiple prerequisites"""
        assert canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]])

    def test_complex_cycle(self):
        """Cycle in larger graph"""
        assert not canFinish(4, [[1, 0], [2, 1], [3, 2], [1, 3]])

    def test_no_prerequisites(self):
        """All courses independent"""
        assert canFinish(3, [])

    def test_single_course(self):
        """Edge case: only one course"""
        assert canFinish(1, [])

    def test_long_chain(self):
        """Linear dependency chain"""
        assert canFinish(5, [[1, 0], [2, 1], [3, 2], [4, 3]])

    def test_disconnected_components(self):
        """Multiple independent chains"""
        assert canFinish(6, [[1, 0], [2, 1], [4, 3], [5, 4]])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
