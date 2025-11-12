# problems/0733-flood-fill/solution.py
from collections import deque


class Solution:
    def floodFill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
        m, n = len(image), len(image[0])
        start = image[sr][sc]
        if start == color:
            return image

        q = deque([(sr, sc)])
        image[sr][sc] = color  # visited
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == start:
                    image[nr][nc] = color
                    q.append((nr, nc))
        return image


if __name__ == "__main__":
    # simple test case
    img = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
    sol = Solution()
    out = sol.floodFill([row[:] for row in img], 1, 1, 2)
    print(out)
