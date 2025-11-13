# Rotting Oranges

You are given an `m x n` `grid` where each cell can have one of three values:

* 0 representing an empty cell,
* 1 representing a fresh orange, or
* 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Example 1:
![alt text](image.png)

>Input: `grid = [[2,1,1],[1,1,0],[0,1,1]]`
Output: 4

Example 2:

>Input: `grid = [[2,1,1],[0,1,1],[1,0,1]]`
Output: -1
**Explanation**: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

Constraints:

* `m == grid.length`
* `n == grid[i].length`
* `1 <= m, n <= 10`
* `grid[i][j]` is 0, 1, or 2.

## Why this matters for ML/Robotics interviews

* Models classic multi-source BFS (epidemic/contagion spread), which parallels signal/heat diffusion, queue-based schedulers, and wavefront expansion used in grid planning/perception.

* Reinforces careful handling of levels/time, visited marking, and blocked cells—skills that directly transfer to sensor fusion grids, occupancy maps, and flood-fill style segmentation.

## Notes:
### Key ideas

* Initialize with all rotten sources: scan once, push every 2 into queue at time 0 (multi-source). Count fresh simultaneously.

* Early exits:

    * fresh == 0 → 0 (already done).

    * fresh > 0 and no initial 2 → -1 (no source to spread).

* BFS with time: either track level by level (size-based) or enqueue (r, c, t) and update `minutes = max(minutes, t+1)` when rotting neighbors.

* Visited rule: when a fresh cell becomes rotten, update `grid[nr][nc] = 2` immediately and `fresh -= 1` to avoid re-enqueue.

* Neighbors: 4-connected only.

* Answer: after BFS, if fresh == 0, return minutes; else -1.

* Complexity: O(mn) time, O(mn) space in worst case.

### Common pitfalls

* Mixing up rows/cols (use `m = len(grid)`, `n = len(grid[0]`), loop `for r in range(m): for c in range(n)` and neighbors `nr = r + dr, nc = c + dc`

* Popping once per direction instead of once per node (correct is: `r,c,t = q.popleft()` then iterate directions).

* Wrong bounds check (`0 <= nr < m` and `0 <= nc < n`, not `<= m/<= n`).

* Forgetting to mark as rotten immediately → duplicate enqueues, wrong timing.