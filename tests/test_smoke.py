import importlib.util
import pathlib
from importlib.machinery import ModuleSpec
from types import ModuleType


def _load_by_path(path: pathlib.Path, mod_name: str) -> ModuleType:
    """Load a Python module from a file path with explicit None checks for mypy."""
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_import_all_solutions():
    for path in pathlib.Path("problems").rglob("solution.py"):
        _ = _load_by_path(path, f"solutions.{path.parent.name}")
