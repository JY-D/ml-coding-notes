import sys
from collections import deque


def bfs(
    grid: list[list[int]], start_r: int, start_c: int, rows: int, cols: int
) -> list[tuple[int, int]]:
    """BFS to find all cells in one connected component.
    Modifies grid in-place by marking visited cells as 0.
    """
    q = deque([(start_r, start_c)])
    grid[start_r][start_c] = 0  # Mark as visited
    component = [(start_r, start_c)]

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # down, right, up, left

    while q:
        r, c = q.popleft()

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            # Check bounds and if it's an unvisited land cell
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 0  # Mark as visited
                q.append((nr, nc))
                component.append((nr, nc))

    return component


def main() -> None:
    input_data = sys.stdin.read().strip().split("\n")
    rows, cols = map(int, input_data[0].split())

    grid: list[list[int]] = []
    for i in range(1, rows + 1):
        row = list(map(int, input_data[i].split()))
        grid.append(row)

    components: list[list[tuple[int, int]]] = []

    # Find all connected components
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                component = bfs(grid, r, c, rows, cols)
                components.append(component)

    # Output
    print("=== Connected Components ===")
    print(f"Total components: {len(components)}")

    if len(components) == 0:
        # No components found (edge case)
        pass
    else:
        print()
        for i, component in enumerate(components, start=1):
            component_sorted = sorted(component)
            print(f"Component {i}: size={len(component)}")
            print(f"  Cells: {component_sorted}")
            if i < len(components):
                print()


if __name__ == "__main__":
    main()
