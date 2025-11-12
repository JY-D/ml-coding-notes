import copy
import importlib.util
import pathlib
from importlib.machinery import ModuleSpec
from types import ModuleType

import pytest


def load_solution_module(slug: str) -> ModuleType:
    """Load problems/{slug}/solution.py as a module (file-based import)."""
    root = pathlib.Path(__file__).resolve().parents[1]
    sol_path = root / "problems" / slug / "solution.py"
    assert sol_path.exists(), f"solution.py not found: {sol_path}"
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(f"solutions.{slug}", sol_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for {sol_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def flood():
    mod = load_solution_module("0733-flood-fill")
    assert hasattr(mod, "Solution"), "Solution class not found"
    return mod.Solution()


@pytest.mark.parametrize(
    "image,sr,sc,color,expected",
    [
        # basic example from LC
        (
            [[1, 1, 1], [1, 1, 0], [1, 0, 1]],
            1,
            1,
            2,
            [[2, 2, 2], [2, 2, 0], [2, 0, 1]],
        ),
        # new color equals start color -> no-op
        (
            [[0, 0, 0], [0, 0, 0]],
            0,
            0,
            0,
            [[0, 0, 0], [0, 0, 0]],
        ),
        # single cell
        (
            [[5]],
            0,
            0,
            7,
            [[7]],
        ),
        # not-connected same values elsewhere should remain unchanged
        (
            [[1, 1, 0, 1], [1, 0, 0, 1], [0, 0, 1, 1]],
            0,
            0,
            9,
            [[9, 9, 0, 1], [9, 0, 0, 1], [0, 0, 1, 1]],
        ),
        # narrow zig-zag corridor
        (
            [[1, 0, 1, 0, 1], [1, 1, 0, 1, 0], [0, 1, 1, 0, 1]],
            0,
            0,
            3,
            [[3, 0, 1, 0, 1], [3, 3, 0, 1, 0], [0, 3, 3, 0, 1]],
        ),
    ],
    ids=[
        "lc-basic",
        "no-op-same-color",
        "single-cell",
        "disconnected-same-values",
        "zigzag-corridor",
    ],
)
def test_flood_fill_correctness(flood, image, sr, sc, color, expected):
    """Functional correctness tests for flood fill."""
    inp = copy.deepcopy(image)  # keep original intact
    out = flood.floodFill(inp, sr, sc, color)
    assert out == expected
