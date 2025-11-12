class Solution:
    def islandPerimeter(self, grid: list[list[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        perimeter = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    perimeter += 4
                    if r + 1 < m and grid[r + 1][c] == 1:
                        perimeter -= 2
                    if c + 1 < n and grid[r][c + 1] == 1:
                        perimeter -= 2
        return perimeter
