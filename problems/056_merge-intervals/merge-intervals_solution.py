def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merges overlapping intervals.
    Style: Functional (No Class)
    Time Complexity: O(N log N)
    Space Complexity: O(N) (for output)
    """
    merged = []

    if len(intervals) == 1:
        return intervals

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for _i, itv in enumerate(intervals, start=1):
        if itv[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], itv[1])

        else:
            merged.append(itv)

    return merged
