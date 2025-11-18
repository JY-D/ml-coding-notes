"""
Two LRU cache implementations:

1) OrderedDict-based (short and idiomatic if allowed by the interviewer)
   - move_to_end(key, last=True): mark as most-recent
   - popitem(last=False): evict least-recent (leftmost)

2) Hand-rolled doubly-linked list + dict (O(1) get/put by design)
   - Required when standard-library sugar is not allowed.
"""

from __future__ import annotations
from collections import OrderedDict
from typing import Dict, Optional


# -------------------------------
# 1) LRU via OrderedDict
# -------------------------------


class LRUCacheOD:
    """LRU using OrderedDict; get/put are O(1)."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.cap = capacity
        self.od: "OrderedDict[int, int]" = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key, last=True)  # mark as most-recent
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od[key] = value
            self.od.move_to_end(key, last=True)
        else:
            self.od[key] = value
        if len(self.od) > self.cap:
            # evict least-recent (leftmost)
            self.od.popitem(last=False)


# -------------------------------
# 2) LRU via dict + doubly-linked list
# -------------------------------


class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int, val: int) -> None:
        self.key = key
        self.val = val
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCacheDLL:
    """
    LRU using a hash map (key -> node) and a doubly linked list:
    - head ... tail (sentinels)
    - Most-recent is right after head; least-recent is right before tail.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._map: Dict[int, _Node] = {}

        # Sentinels to remove edge cases on empty/full manipulations
        self._head = _Node(0, 0)  # most-recent side
        self._tail = _Node(0, 0)  # least-recent side
        self._head.next = self._tail
        self._tail.prev = self._head

    # ---- internal helpers (all O(1)) ----
    def _remove(self, node: _Node) -> None:
        """Detach node from the list in O(1)."""
        prev, nxt = node.prev, node.next
        assert prev is not None and nxt is not None
        prev.next = nxt
        nxt.prev = prev
        node.prev = None
        node.next = None

    def _push_front(self, node: _Node) -> None:
        """Insert node right after head (mark as most-recent) in O(1)."""
        first = self._head.next
        assert first is not None
        node.prev = self._head
        node.next = first
        self._head.next = node
        first.prev = node

    def _pop_back(self) -> _Node:
        """Pop and return the least-recent node (before tail) in O(1)."""
        lru = self._tail.prev
        assert lru is not None
        if lru is self._head:
            raise IndexError("pop_back on empty list")
        prev = lru.prev
        assert prev is not None
        prev.next = self._tail
        self._tail.prev = prev
        lru.prev = None
        lru.next = None
        return lru

    # ---- public API (O(1) time) ----
    def get(self, key: int) -> int:
        node = self._map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self._map.get(key)
        if node is not None:
            node.val = value
            self._remove(node)
            self._push_front(node)
            return

        node = _Node(key, value)
        self._map[key] = node
        self._push_front(node)
        if len(self._map) > self._cap:
            lru = self._pop_back()
            del self._map[lru.key]


# -------------------------------
# Tiny smoke tests (shared)
# -------------------------------


def _run_lru_smoke_test(cache_cls) -> None:
    """
    Shared sanity test: validates external semantics.
    """
    lru = cache_cls(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1  # 1 becomes most-recent
    lru.put(3, 3)  # evicts key 2
    assert lru.get(2) == -1
    lru.put(4, 4)  # evicts key 1
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4


if __name__ == "__main__":
    _run_lru_smoke_test(LRUCacheOD)
    _run_lru_smoke_test(LRUCacheDLL)
