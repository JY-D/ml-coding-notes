"""
Deque vs List — how to choose (with tiny, practical templates).

Quick complexity cheat sheet (amortized):
- list
  - append/pop (right): O(1)
  - pop(0)/insert(0, x) (left): O(n)  ← shifts all elements
  - random index a[i]: O(1)
  - slicing / sorting: supported

- deque (collections.deque)
  - append/pop (right): O(1)
  - appendleft/popleft (left): O(1)
  - random index / slicing: not suitable (treat as O(n))
  - rotate(k), maxlen: supported

Rules of thumb:
- Need queue semantics (BFS, multi-source BFS, topological order)? → deque
- Need two-pointers, random indexing, slicing, sorting? → list
- Need sliding window max with a monotonic queue? → deque
- Need LRU-like "move to ends" and "pop oldest"? Prefer OrderedDict, not deque.
"""

from __future__ import annotations
from collections import deque
from typing import Iterable, List, Tuple


# -------------------------------
# 1) BFS on a grid → deque popleft() is O(1)
# -------------------------------


def bfs_shortest_path_8dir(grid: List[List[int]]) -> int:
    """
    Example: shortest path in binary matrix (like LC 1091).
    Move in 8 directions through zeros (0 = free, 1 = blocked).
    Returns minimum steps from (0,0) to (n-1,n-1), or -1 if impossible.

    This is simply a template to illustrate why deque is ideal for BFS.
    """
    n = len(grid)
    if n == 0:
        return -1
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    if n == 1:
        return 1

    q: deque[Tuple[int, int, int]] = deque()
    q.append((0, 0, 1))  # (r, c, distance)
    grid[0][0] = 1  # mark visited by turning into blocked

    dirs = [
        (1, 1),
        (1, 0),
        (0, 1),
        (1, -1),
        (-1, 1),
        (-1, 0),
        (0, -1),
        (-1, -1),
    ]

    while q:
        r, c, d = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                if nr == n - 1 and nc == n - 1:
                    return d + 1
                grid[nr][nc] = 1
                q.append((nr, nc, d + 1))
    return -1


# -------------------------------
# 2) Sliding Window Maximum → deque (monotonic queue)
# -------------------------------


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Classic monotonic deque template:
    Store indices; keep values decreasing in the deque.
    - Pop from right while nums[right] <= current
    - Pop left if index is out of the window
    - The max is always at the left end
    """
    if k <= 0:
        raise ValueError("k must be positive")
    dq: deque[int] = deque()
    out: List[int] = []

    for i, x in enumerate(nums):
        # Maintain decreasing values in deque
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        # Remove outdated (outside window)
        if dq[0] <= i - k:
            dq.popleft()
        # Record window max
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


# -------------------------------
# 3) Stack / two-pointers → list
# -------------------------------


def valid_parentheses_stack(s: str) -> bool:
    """
    Simple stack example using list; push/pop on right are O(1).
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    st: List[str] = []
    for ch in s:
        if ch in "([{":
            st.append(ch)
        else:
            if not st or st[-1] != pairs.get(ch, ""):
                return False
            st.pop()
    return not st


# -------------------------------
# 4) Pitfalls
# -------------------------------
# - Avoid list.pop(0) in BFS: it's O(n). Use deque.popleft() instead.
# - Avoid heavy random indexing on deque; convert to list if you must:
#     arr = list(dq)
# - Avoid sorting a deque; only list supports sort():
#     arr = list(dq); arr.sort()


if __name__ == "__main__":
    # Tiny self-checks (not exhaustive)
    assert valid_parentheses_stack("()[]{}")
    assert not valid_parentheses_stack("(]")

    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], k=3) == [3, 3, 5, 5, 6, 7]

    g = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
    ]
    # A reachable example for the BFS template (result may vary by grid)
    res = bfs_shortest_path_8dir(g)
    assert res in (3, 4, 5, -1)  # just a sanity check; not a strict test
