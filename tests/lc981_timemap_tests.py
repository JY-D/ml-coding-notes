import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "problems" / "lc981-timemap"))

from timemap_solution import TimeMap


class TestTimeMap:
    def test_example_1(self) -> None:
        """LeetCode Example 1"""
        tm = TimeMap()
        tm.set("foo", "bar", 1)
        assert tm.get("foo", 1) == "bar"
        assert tm.get("foo", 3) == "bar"
        tm.set("foo", "bar2", 4)
        assert tm.get("foo", 4) == "bar2"
        assert tm.get("foo", 5) == "bar2"

    def test_empty_key(self) -> None:
        """Get non-existent key returns empty string"""
        tm = TimeMap()
        assert tm.get("nonexistent", 1) == ""

    def test_timestamp_too_early(self) -> None:
        """Get timestamp before any set returns empty string"""
        tm = TimeMap()
        tm.set("foo", "bar", 10)
        assert tm.get("foo", 5) == ""
        assert tm.get("foo", 9) == ""

    def test_exact_timestamp_match(self) -> None:
        """Get exact timestamp returns correct value"""
        tm = TimeMap()
        tm.set("foo", "bar", 1)
        tm.set("foo", "bar2", 3)
        tm.set("foo", "bar3", 5)
        assert tm.get("foo", 1) == "bar"
        assert tm.get("foo", 3) == "bar2"
        assert tm.get("foo", 5) == "bar3"

    def test_between_timestamps(self) -> None:
        """Get timestamp between two sets returns earlier value"""
        tm = TimeMap()
        tm.set("foo", "bar", 1)
        tm.set("foo", "bar2", 5)
        assert tm.get("foo", 2) == "bar"
        assert tm.get("foo", 3) == "bar"
        assert tm.get("foo", 4) == "bar"

    def test_multiple_keys(self) -> None:
        """Multiple keys work independently"""
        tm = TimeMap()
        tm.set("foo", "bar", 1)
        tm.set("baz", "qux", 2)
        assert tm.get("foo", 1) == "bar"
        assert tm.get("baz", 2) == "qux"
        assert tm.get("foo", 2) == "bar"
        assert tm.get("baz", 1) == ""

    def test_many_timestamps(self) -> None:
        """Performance test with many timestamps"""
        tm = TimeMap()
        for i in range(1, 101):
            tm.set("foo", f"val{i}", i)

        assert tm.get("foo", 1) == "val1"
        assert tm.get("foo", 50) == "val50"
        assert tm.get("foo", 100) == "val100"
        assert tm.get("foo", 75) == "val75"
        assert tm.get("foo", 101) == "val100"

    def test_edge_case_single_entry(self) -> None:
        """Edge case with single entry"""
        tm = TimeMap()
        tm.set("foo", "bar", 1)
        assert tm.get("foo", 0) == ""
        assert tm.get("foo", 1) == "bar"
        assert tm.get("foo", 2) == "bar"

    def test_large_timestamps(self) -> None:
        """Test with large timestamp values"""
        tm = TimeMap()
        tm.set("foo", "bar", 1_000_000)
        tm.set("foo", "bar2", 10_000_000)
        assert tm.get("foo", 999_999) == ""
        assert tm.get("foo", 1_000_000) == "bar"
        assert tm.get("foo", 5_000_000) == "bar"
        assert tm.get("foo", 10_000_000) == "bar2"
        assert tm.get("foo", 10_000_001) == "bar2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
