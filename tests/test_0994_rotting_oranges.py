# comments in code should always be written in English
import copy
import importlib.util
import pathlib
from importlib.machinery import ModuleSpec
from types import ModuleType

import pytest


def _find_problem_folder() -> pathlib.Path:
    """Find the Rotting Oranges problem folder under problems/.
    We match *994-rotting-oranges to tolerate 4-digit prefixes like 0994.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    problems = root / "problems"
    candidates = sorted(problems.glob("*994-rotting-oranges"))
    assert candidates, "Could not find a folder matching '*994-rotting-oranges' under problems/"
    return candidates[0]


def _load_solution_module(folder: pathlib.Path) -> ModuleType:
    """Load the first *_solution.py under the given folder as a module."""
    sol_candidates = sorted(folder.glob("*_solution.py"))
    assert sol_candidates, f"No *_solution.py found under {folder}"
    sol_path = sol_candidates[0]
    module_name = f"solutions.{folder.name}"
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(
        module_name,
        sol_path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for {sol_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def rotten():
    folder = _find_problem_folder()
    mod = _load_solution_module(folder)
    assert hasattr(mod, "Solution"), "Solution class not found"
    return mod.Solution()


@pytest.mark.parametrize(
    "grid,expected",
    [
        # classic example -> 4
        ([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4),
        # already done -> 0
        ([[0, 2]], 0),
        # no rotten, fresh exists -> -1
        ([[1, 1, 1]], -1),
        # single cell rotten -> 0
        ([[2]], 0),
        # blocked by zeros -> -1
        ([[2, 0, 1]], -1),
        # true multi-source -> 4
        ([[2, 1, 1], [0, 1, 1], [2, 0, 1]], 4),
    ],
    ids=[
        "classic-4",
        "done-0",
        "fresh-no-source--1",
        "single-rotten-0",
        "blocked--1",
        "multi-source-4",
    ],
)
def test_rotting_oranges_correctness(rotten, grid, expected):
    """Functional correctness tests for Rotting Oranges (LC 994)."""
    g = copy.deepcopy(grid)
    # Accept either function or method styles
    if hasattr(rotten, "orangesRotting"):
        got = rotten.orangesRotting(g)
    elif hasattr(rotten, "solve"):
        got = rotten.solve(g)
    else:
        raise AttributeError("Expected method 'orangesRotting' or 'solve' on Solution")
    assert got == expected
