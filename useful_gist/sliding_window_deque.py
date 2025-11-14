from collections import deque
from typing import Deque

def sliding_max(nums: list[int], k: int) -> list[int]:
    """Monotonic deque template: store indices; pop from back while smaller."""
    dq: Deque[int] = deque()
    out: list[int] = []
    for i, x in enumerate(nums):
        # 1) maintain decreasing deque
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        # 2) remove out-of-window head
        if dq[0] <= i - k:
            dq.popleft()
        # 3) record answer when window ready
        if i + 1 >= k:
            out.append(nums[dq[0]])
    return out
