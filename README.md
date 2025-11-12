
# Robotic Perception — Coding Notes

Lightweight repo to track daily coding practice for ML/AI/DL & robotic perception interviews.
Keep commits small and messages meaningful. Problems are organized by LeetCode ID and title.

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Structure
```
problems/
  0733-flood-fill/
    solution.py          # your final/reference solution
    NOTES.md             # attempts, pseudocode, pitfalls, variants
  ...
templates/
  PROBLEM_NOTE_TEMPLATE.md
scripts/
  new_problem.py         # scaffold a new problem folder
  run_tests.sh
tests/
  test_smoke.py          # sanity test that imports each solution
```

## Commit convention
- `feat(0733): first BFS version`
- `refactor(0733): in-place mark to avoid visited set`
- `docs(0200): add pitfalls & edge cases`
- `test(0463): add edge/hole cases`

## CI
- GitHub Actions runs `pytest`. Add linters later if needed.
