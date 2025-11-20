# comments in code should always be written in English
import copy
import importlib.util
import pathlib
from importlib.machinery import ModuleSpec
from types import ModuleType

import pytest


def _find_problem_folder() -> pathlib.Path:
    """Find the problem folder under problems/ matching *1091-shortest-path-in-binary-matrix."""
    repo = pathlib.Path(__file__).resolve().parents[1]
    problems = repo / "problems"
    candidates = sorted(problems.glob("*1091-shortest-path-in-binary-matrix"))
    assert candidates, "Could not find a folder matching '*1091-shortest-path-in-binary-matrix' under problems/"
    return candidates[0]


def _load_solution_module(folder: pathlib.Path) -> ModuleType:
    """Load the first *_solution.py under the given folder as a module."""
    sol_candidates = sorted(folder.glob("*_solution.py"))
    assert sol_candidates, f"No *_solution.py found under {folder}"
    sol_path = sol_candidates[0]
    mod_name = f"solutions.{folder.name}"
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(mod_name, sol_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for {sol_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def spbm():
    folder = _find_problem_folder()
    mod = _load_solution_module(folder)
    assert hasattr(mod, "Solution"), "Solution class not found"
    return mod.Solution()


@pytest.mark.parametrize(
    "grid,expected",
    [
        # 1x1 open -> 1
        ([[0]], 1),
        # 1x1 blocked -> -1
        ([[1]], -1),
        # simple 2x2 diagonal -> 2
        ([[0, 1], [1, 0]], 2),
        # blocked destination -> -1
        ([[0, 0], [0, 1]], -1),
        # small detour with diagonals allowed
        (
            [
                [0, 1, 0],
                [0, 0, 0],
                [1, 1, 0],
            ],
            3,
        ),
        # fully blocked start -> -1
        (
            [
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ],
            -1,
        ),
    ],
    ids=[
        "1x1-open",
        "1x1-blocked",
        "diag-2",
        "blocked-dst",
        "detour-3",
        "blocked-start",
    ],
)
def test_shortest_path_binary_matrix(spbm, grid, expected):
    """Functional tests for LC 1091 (Shortest Path in Binary Matrix)."""
    g = copy.deepcopy(grid)
    if hasattr(spbm, "shortestPathBinaryMatrix"):
        got = spbm.shortestPathBinaryMatrix(g)
    elif hasattr(spbm, "solve"):
        got = spbm.solve(g)
    else:
        raise AttributeError("Expected method 'shortestPathBinaryMatrix' or 'solve' on Solution")
    assert got == expected
