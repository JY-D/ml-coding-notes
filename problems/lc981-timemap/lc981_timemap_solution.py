import bisect
from collections import defaultdict


class TimeMap:
    """Time-based key-value store with O(log N) retrieval.

    Supports:
    - set(key, value, timestamp): Store value at timestamp
    - get(key, timestamp): Retrieve value at largest timestamp <= target
    """

    def __init__(self) -> None:
        # key -> [(timestamp, value), ...]
        # Maintains sorted order by timestamp (strictly increasing)
        self.store: dict[str, list[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """Store value at timestamp.

        Time: O(1) amortized
        Space: O(1)
        """
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """Retrieve value at largest timestamp <= target.

        Time: O(log N) where N = number of timestamps for this key
        Space: O(1)

        Returns:
            Value at largest timestamp <= target, or "" if not found
        """
        items = self.store[key]

        if not items:
            return ""

        # Binary search for rightmost position <= timestamp
        # Use chr(127) to ensure we insert AFTER any existing timestamp
        # This handles the case where timestamp exactly matches an entry
        pos = bisect.bisect_right(items, (timestamp, chr(127)))

        if pos == 0:
            # All timestamps are greater than target
            return ""
        else:
            # Return value at previous position (largest <= timestamp)
            return items[pos - 1][1]


# Example usage (LeetCode test format)
if __name__ == "__main__":
    obj = TimeMap()
    obj.set("foo", "bar", 1)
    print(obj.get("foo", 1))  # "bar"
    print(obj.get("foo", 3))  # "bar"
    obj.set("foo", "bar2", 4)
    print(obj.get("foo", 4))  # "bar2"
    print(obj.get("foo", 5))  # "bar2"
