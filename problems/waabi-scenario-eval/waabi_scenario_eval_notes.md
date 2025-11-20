# Waabi Scenario Evaluation Pipeline

## Problem Summary
Given inference logs from an auto-labeling pipeline, compute per-scenario statistics, detect anomalies (consecutive slow frames), and identify hard cases (lowest accuracy frames).

This problem simulates **real-world ML pipeline monitoring** used in autonomous driving systems.

---

## Solution Approach

### Task 1: Per-Scenario Statistics (Grouping + Aggregation)

**Core Idea**: Group frames by scenario and compute metrics per group.

#### Data Structure
```python
frame_group_by_scen: dict[str, list[tuple[int, float, float]]]
# Key: scenario name
# Value: list of (frame_id, accuracy, time_ms)
```

#### Key Steps
1. **Parse input** and compute `accuracy = detected / gt` (handle `gt=0` edge case)
2. **Group by scenario** using `defaultdict(list)`
3. **For each scenario**, compute:
   - Count
   - Average accuracy
   - Average inference time
   - Worst case time (max)
   - **P95 time** (95th percentile):
     ```python
     if len(times) <= 5:
         p95 = max(times)
     else:
         p95 = sorted(times)[int(0.95 * len(times))]
     ```
4. **Sort scenarios alphabetically** for consistent output

#### Complexity
- Time: O(N log N) due to sorting scenarios and P95 calculation
- Space: O(N) to store all frames

---

### Task 2: Anomaly Detection (Sliding Window Pattern)

**Core Idea**: Detect consecutive sequences of ≥3 frames where `inference_time > 25ms`.

#### Algorithm: State Machine
```python
current_window = {
    "start_frame": None,
    "frames": [],
    "times": [],
    "scenarios": []
}

for each frame:
    if time_ms > 25:
        # Enter or extend anomaly window
        if start_frame is None:
            start new window
        add frame to current window
    else:
        # Exit anomaly window
        if window has ≥3 frames:
            save to anomalies list
        reset window
```

#### Key Points
- **Don't forget the last window**: After loop ends, check if current window has ≥3 frames
- **Unique scenarios**: Use `set()` to deduplicate scenarios in window
- **Average time**: Compute mean across all frames in window

#### Complexity
- Time: O(N) single pass
- Space: O(W) where W = max window size (typically small)

---

### Task 3: Top-K Hard Cases (Sorting)

**Core Idea**: Find K frames with lowest accuracy.

#### Simple Approach (Recommended for Interviews)
```python
cases = [(accuracy, frame_id, scenario) for all frames]
cases.sort(key=lambda x: x[0])  # Sort by accuracy ascending
top_k = cases[:K]
```

#### Alternative: Min Heap (For Large Data)
If N >> K (e.g., 10M frames, top-10), use heap:
```python
import heapq
heap = []  # Use negative accuracy to simulate max heap
for frame:
    if len(heap) < K:
        heapq.heappush(heap, (-accuracy, frame_id, scenario))
    elif -accuracy > heap[0][0]:
        heapq.heapreplace(heap, (-accuracy, frame_id, scenario))
```
- **Time**: O(N log K) vs O(N log N) for sorting
- **Space**: O(K) vs O(N)

**Why negative?** Python's `heapq` is min heap; negating values simulates max heap.

#### Complexity
- Sorting: O(N log N) time, O(N) space
- Heap: O(N log K) time, O(K) space

---

## Key Takeaways

### P50/P95 Concept (百分位數)
- **P50 (median)**: Typical case performance
- **P95**: Worst-case performance for 95% of frames
- **Why track P95?** Autonomous systems can't tolerate tail latency; even 5% slow frames impact safety

### Sliding Window for Consecutive Events
- Use **state machine** pattern: track current window, close when condition breaks
- Don't forget to finalize the last window after loop ends

### Sorting vs Heap Trade-off
- **Sorting**: Simple, readable, sufficient for small datasets (N < 10K)
- **Heap**: Optimal for large datasets where N >> K
- **Interview tip**: Start with sorting; mention heap optimization if asked

---

## Common Pitfalls

### Task 1
- ❌ Forgetting to sort scenarios alphabetically → output inconsistent
- ❌ Not handling `gt=0` edge case → division by zero
- ❌ P95 calculation wrong for small datasets (≤5 frames)

### Task 2
- ❌ Forgetting to check last window after loop ends
- ❌ Not deduplicating scenarios in window → wrong output format
- ❌ Off-by-one error: should be `> 25` not `>= 25`

### Task 3
- ❌ Not handling case where `len(cases) < K` → index out of bounds

---

## HackerRank-Specific Tips

### Input Parsing
```python
import sys
input_data = sys.stdin.read().strip().split('\n')
n = int(input_data[0])
for i in range(1, n + 1):
    parts = input_data[i].split(',')
```

### Output Formatting
- Use `f"{value:.2f}"` for 2 decimal places
- Match exact format: `count=X, avg_time=Y.YYms, ...`
- Alphabetical sorting for scenarios ensures consistency

### Edge Cases to Test
- Single scenario
- All frames have same accuracy (Task 3 outputs first K in order)
- `gt=0` (handle gracefully: `accuracy = 1.0`)
- Anomaly window at end of sequence
- P95 with exactly 5 frames vs >5 frames

---

## Real-World Applications

This problem directly mirrors:
1. **Slice-based evaluation** (Task 1): Group metrics by scenario to catch performance gaps
2. **Jitter detection** (Task 2): Find consecutive latency spikes that degrade user experience
3. **Hard negative mining** (Task 3): Identify failure cases for targeted data collection

These are **core ML pipeline operations** at companies like Waabi, Waymo, Tesla, Cruise.

---

## Complexity Summary

| Task | Time | Space |
|------|------|-------|
| Task 1 | O(N log N) | O(N) |
| Task 2 | O(N) | O(W) |
| Task 3 (sorting) | O(N log N) | O(N) |
| Task 3 (heap) | O(N log K) | O(K) |
| **Overall** | **O(N log N)** | **O(N)** |

For typical interview constraints (N ≤ 10^4), this is highly efficient.
