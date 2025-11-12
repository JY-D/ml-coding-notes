
import importlib, glob

folders = glob.glob('problems/*/solution.py')
def test_import_all_solutions():
    for path in folders:
        mod = path.replace('/', '.').rstrip('.py')
        importlib.import_module(mod)
