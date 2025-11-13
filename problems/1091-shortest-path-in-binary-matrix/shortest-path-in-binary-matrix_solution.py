from collections import deque


class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        n = len(grid)

        # early return
        # gird's top left or buttom right is not 0
        if (grid[0][0] == 1) or (grid[n - 1][n - 1] == 1):
            return -1
        if n == 1:
            return 1

        q: deque[tuple[int, int, int]] = deque()  # (r, c, dist)
        q.append((0, 0, 1))
        dirs = [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]

        while q:
            r, c, dist = q.popleft()
            for dr, dc in dirs:
                nr = dr + r
                nc = dc + c

                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    if (nr == n - 1) and (nc == n - 1):
                        return dist + 1
                    grid[nr][nc] = 1
                    q.append((nr, nc, dist + 1))
        return -1
