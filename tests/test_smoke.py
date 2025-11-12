import importlib.util
import pathlib

def test_import_all_solutions():
    for path in pathlib.Path("problems").rglob("solution.py"):
        mod_name = f"solutions.{path.parent.name}"
        spec = importlib.util.spec_from_file_location(mod_name, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
