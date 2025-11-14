## Shortest Path in Binary Matrix (LC 1091) — 8-direction BFS

**Problem.**  
Given an `n x n` binary grid where `0` = free and `1` = blocked, find the length of the shortest path
from `(0,0)` to `(n-1,n-1)` moving in **8 directions** (including diagonals). Return `-1` if no path
exists. Path length counts **cells visited** (includes start and end).

**Why BFS works (no priorities needed).**  
All steps have equal cost (unweighted grid), so BFS explores cells in **increasing distance layers**.
The first time we reach the target, that distance is **optimal**. The order of trying directions only
changes *which* shortest path is found, not the distance.

**Core template (distance-in-queue).**
- Early exits:
  - If `grid[0][0] == 1` or `grid[n-1][n-1] == 1` → `-1`.
  - If `n == 1` and `grid[0][0] == 0` → `1`.
- Initialize queue with `(0, 0, 1)` and mark the start as visited (e.g., set `grid[0][0] = 1`).
- 8-neighborhood: `(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)`.
- **Visited at enqueue**: when a neighbor is valid (`0`) and in-bounds, mark it visited immediately
  (set to `1`) and push with `dist + 1`. If it is `(n-1, n-1)`, return `dist + 1` on the spot.

**Common pitfalls.**
- Mixing up row/col when computing neighbors.
- Marking visited **after** popping instead of **at enqueue**, causing duplicate enqueues.
- Forgetting diagonal moves (there are 8 directions).
- Returning number of **moves** instead of **cells**; the start distance should begin at `1`.

**Complexities.**
- Time `O(n^2)`, Space `O(n^2)` in the worst case.

**Sanity tests.**
- `[[0]] → 1`, `[[1]] → -1`.
- `[[0,1],[1,0]] → 2` (diagonal directly).
- `[[0,0],[0,1]] → -1` (destination blocked).
- A detour case to ensure BFS explores layers correctly.
