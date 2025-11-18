import copy
import importlib.util
import pathlib
import types

import pytest


def _load_solution_module() -> types.ModuleType:
    root = pathlib.Path(__file__).resolve().parents[1]
    folder = root / "problems" / "0752-open-the-lock"
    assert folder.exists(), f"Folder not found: {folder}"

    # Prefer "*_solution.py", otherwise fallback to "solution.py"
    candidates = sorted(folder.glob("*_solution.py"))
    if not candidates:
        fallback = folder / "solution.py"
        assert fallback.exists(), f"solution.py not found: {fallback}"
        candidates = [fallback]

    sol_path = candidates[0]

    spec = importlib.util.spec_from_file_location(f"solutions.{folder.name}", sol_path)
    assert spec is not None and spec.loader is not None, f"Cannot load module spec for {sol_path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def locker():
    mod = _load_solution_module()
    assert hasattr(mod, "Solution"), "Expected class `Solution` in solution module"
    obj = mod.Solution()
    # Accept either openLock or solve method
    assert hasattr(obj, "openLock") or hasattr(
        obj, "solve"
    ), "Expected method `openLock` or `solve` in Solution"
    return obj


def _run(locker, deadends, target) -> int:
    if hasattr(locker, "openLock"):
        return locker.openLock(deadends, target)
    return locker.solve(deadends, target)


@pytest.mark.parametrize(
    "deadends,target,expected",
    [
        # LeetCode sample: 6
        (["0201", "0101", "0102", "1212", "2002"], "0202", 6),
        # Target is start (0 moves)
        ([], "0000", 0),
        # Start in dead → -1
        (["0000"], "9999", -1),
        # Simple one-step move
        ([], "0001", 1),
        # Blocked straightforward path, must go around ring
        # From "0000" to "0009": can be 1 step via -1.
        (["0001"], "0009", 1),
        # Impossible because all neighbors of "0000" are dead
        (["0001", "0010", "0100", "1000", "0009", "0090", "0900", "9000"], "8888", -1),
    ],
    ids=[
        "sample-6",
        "target-is-start-0",
        "start-dead--1",
        "one-step-1",
        "ring-around-1",
        "all-neighbors-dead--1",
    ],
)
def test_open_lock(locker, deadends, target, expected):
    got = _run(locker, copy.deepcopy(deadends), target)
    assert got == expected
