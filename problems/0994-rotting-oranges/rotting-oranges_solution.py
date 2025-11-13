from collections import deque


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        q: deque[tuple[int, int, int]] = deque()  # (r, c, t)
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        m = len(grid)
        n = len(grid[0])
        fresh = 0

        # find all rotten orange first, send [x, y, t] into q
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c, 0))  # multi-source, time=0
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0
        if fresh > 0 and not q:
            return -1

        # BFS
        minutes = 0
        while q:
            r, c, t = q.popleft()
            for dr, dc in dirs:  # [(1, 0), (-1, 0), (0, 1), (0, -1)]
                nr = dr + r
                nc = dc + c

                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc, t + 1))
                    minutes = max(minutes, t + 1)
                    # nothing to add if it's already rotten or empty

        return minutes if fresh == 0 else -1
