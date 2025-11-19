from collections import deque


class Solution:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0

        seen = {"0000"}  # set: O(1) membership
        q = deque([("0000", 0)])  # BFS deque = [("start"), steps]

        while q:
            cur, d = q.popleft()
            if cur == target:
                return d
            for i in range(4):
                digit = int(cur[i])
                for delta in (1, -1):
                    nd = (digit + delta) % 10
                    nxt = cur[:i] + str(nd) + cur[i + 1 :]
                    if nxt not in dead and nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, d + 1))
        return -1
