# useful_gist/heapq_topk.py
# Comments in code should always be written in English.

from __future__ import annotations

from collections import Counter
import heapq
from typing import Iterable, Iterator, List, Tuple, Dict, Any
import pdb


def top_k_numbers(nums: Iterable[int], k: int) -> List[int]:
    """
    Return the top-k largest numbers from a stream/iterable in descending order.
    Uses a fixed-size min-heap of size k.

    Time:
        - Main loop: O(n log k)  (one heap op per element)
        - Final sort of k elements: O(k log k)
        => Overall: O(n log k) + O(k log k)

    Space: O(k)
    """
    if k <= 0:
        return []

    heap: List[int] = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)  # O(log k) worst-case; amortized ok
        else:
            # Keep only the k largest: replace the smallest if x is larger
            if x > heap[0]:
                heapq.heapreplace(heap, x)  # O(log k)

    # Sort the k candidates in descending order for presentation
    return sorted(heap, reverse=True)


def kth_largest_number(nums: Iterable[int], k: int) -> int:
    """
    Return the k-th largest number from an iterable.
    Uses a fixed-size min-heap of size k.

    If the iterable has fewer than k elements, raises ValueError.

    Time: O(n log k)
    Space: O(k)
    """
    if k <= 0:
        raise ValueError("k must be positive")

    heap: List[int] = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)  # sift up, compare with parent node O(logn)
        else:
            if x > heap[0]:
                heapq.heapreplace(heap, x)  # sift down, swap with smaller child node. (won't swap with sibling)

    if len(heap) < k:
        raise ValueError("not enough elements for k-th largest")

    # The heap root is the k-th largest
    return heap[0]


def top_k_from_counts(counts: Dict[Any, int], k: int) -> List[Tuple[int, Any]]:
    """
    Given a dict mapping item -> count, return top-k (count, item) pairs
    sorted by count descending.

    Example:
        counts = {"a": 3, "b": 7, "c": 5}
        top_k_from_counts(counts, 2) -> [(7, "b"), (5, "c")]

    Time:
        - Iterate items: O(n log k)
        - Sort the k results: O(k log k)
    Space: O(k)
    """
    if k <= 0:
        return []

    heap: List[Tuple[int, Any]] = []  # (count, item)
    for item, cnt in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (cnt, item))
        else:
            if cnt > heap[0][0]:
                heapq.heapreplace(heap, (cnt, item))

    # Sort by count descending; stable on ties
    return sorted(heap, key=lambda p: p[0], reverse=True)


def top_k_nlargest_builtin(nums: Iterable[int], k: int) -> List[int]:
    """
    Convenience wrapper using heapq.nlargest (internally O(n log k)).
    Returns descending order. Equivalent to top_k_numbers for numbers.
    """
    return heapq.nlargest(k, nums)


# ----------------------------
# Mini self-check (optional) |
# ----------------------------
if __name__ == "__main__":
    # Basic sanity checks; in real projects prefer pytest unit tests.

    data = [7, 2, 9, 1, 3, 12, 4]
    assert top_k_numbers(data, 3) == [12, 9, 7]
    assert kth_largest_number(data, 3) == 7
    assert top_k_nlargest_builtin(data, 3) == [12, 9, 7]

    cnt = Counter(["a", "b", "a", "c", "b", "b", "d", "a", "b"])  # a:3, b:4, c:1, d:1
    assert top_k_from_counts(cnt, 2) == [(4, "b"), (3, "a")]

    # Edge cases
    assert top_k_numbers([], 3) == []
    try:
        _ = kth_largest_number([1, 2], 3)
        raise AssertionError("Expected ValueError for insufficient elements")
    except ValueError:
        pass

    print("All self-checks passed.")


# Top-K：min-heap remains size k, new val > heap
# Kth largest：heap[0] is Kth largest
# time complexity：O(n log k)

# Why dont use list.sort()
# O(n log n)
