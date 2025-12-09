# Machine Learning — Coding Notes

Practice repo for algorithm/data-structure problems with a focus on **robotic perception / ML/AI/DL interviews**.  
Each problem lives in its own folder under `problems/` and ships with a minimal `_solution.py` plus optional notes/tests.

---

## Quick start (Python 3.12, arm64)

```bash
# 1) Create a venv (arm64 Python 3.12)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dev tools
pip install -U pip
pip install -r requirements.txt

# 3) (Optional) Enable git hooks
pre-commit install
pre-commit run --all-files
```

**VS Code**: select interpreter at `.venv/bin/python`.

---

## Repository layout

```
problems/
  0733-flood-fill/
    0733-flood-fill_solution.py  #your solution (importable by CI smoke test)
    NOTES.md            # (optional) reasoning, pitfalls, variants
  0200-number-of-islands/
    0200-number-of-islands_solution.py
tests/
  test_repo_smoke.py    # imports every problems/**/solution.py
  test_0733_flood_fill.py  # example of functional tests
scripts/
  new_problem.py        # (optional) scaffold helper, if you use it
pyproject.toml          # ruff/black/mypy config
requirements.txt        # dev dependencies (pytest/ruff/black/mypy/pre-commit)
```

---

## Add a new problem

Create a folder `problems/<id>-<kebab-title>/`, and inside it:
* NOTES.md (optional)
* **<snake_title>_solution.py** ← unique, mypy-friendly

**Minimal `solution.py` skeleton:**
```python
from typing import List

class Solution:
    def solve(self, *args, **kwargs):
        """Implement your solution."""
        pass

if __name__ == "__main__":
    # quick local sanity check (not part of CI)
    print("OK")
```

> CI only requires `*_solution.py` to be **importable**. You can keep LeetCode-style `class Solution` and method names.

---

## Testing

Run all tests:
```bash
pytest -q
```

Example per-problem test lives in `tests/test_0733_flood_fill.py` and loads modules by **file path** (so problem folders can keep IDs and hyphens).

---

## Lint & format & type-check

- **Ruff** (linter + import sort):  
  ```bash
  ruff check . --fix
  ```
- **Black** (formatter):  
  ```bash
  black .
  ```
- **mypy** (type checker):  
  ```bash
  mypy .
  ```

Notes:
- We **exclude** `problems/**/<name>_solution.py` from mypy to avoid duplicate-module issues (mypy can’t derive a valid package name from `kebab-case` + numeric folders). See `pyproject.toml`.
- In pre-commit, mypy runs with `pass_filenames: false` and an explicit `--exclude` to guarantee the same behavior.

---

## Git hooks (pre-commit)

Installed via:
```bash
pre-commit install
pre-commit run --all-files
```

The hook runs Ruff (with `--fix`), Black (check), and mypy (project-wide).  
Adjust `.pre-commit-config.yaml` if you want mypy only in CI.

---

## Commit style

Small, focused commits with clear scopes:
```
feat(0733): add BFS one-phase implementation
test(0733): add edge cases (no-op color, zigzag corridor)
docs(0733): record pitfalls & complexity
chore(ci): add mypy + ruff + black steps
```

---

## CI

Typical steps:
```yaml
- run: pip install -r requirements.txt
- run: ruff check .
- run: black --check .
- run: mypy .
- run: pytest -q
```

---

## FAQ

**Why `test_repo_smoke.py`?**  
It’s a **smoke test**: fast health-check that every `<name>_solution.py` is importable (catches syntax/path issues early).  
Behavioral correctness goes in per-problem tests.

**Why exclude `solution.py` from mypy?**  
Problem folders like `problems/0463-island-perimeter` are not valid Python package names (digits + `-`). mypy collapses them to the same top-level module name `solution`, causing duplicate-module errors. We keep LeetCode-friendly filenames and avoid fighting the package layout.

---

## Troubleshooting

- **mypy still scans solutions in pre-commit**  
  Ensure the mypy hook has `pass_filenames: false` and `--exclude=^problems/.+/solution\.py$`. Run `pre-commit clean` then `pre-commit run --all-files -v` and verify the printed mypy command includes those args.

- **Using the wrong Python**  
  Check:
  ```bash
  python3 -c "import platform, sys; print(platform.machine(), sys.version)"
  ```
  Expect `arm64 3.12.x`. Recreate the venv if needed.
