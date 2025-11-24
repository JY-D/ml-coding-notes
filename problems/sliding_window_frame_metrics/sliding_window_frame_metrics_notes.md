# Sliding Window Frame Metrics

## Problem Overview

**Source**: Custom problem inspired by real-time frame monitoring  
**Difficulty**: Medium  
**Topics**: Sliding Window, Statistical Analysis, Array

### Background Story

Building a frame-time monitoring system for autonomous driving perception pipeline. The system captures frames at 30 FPS from multiple cameras and needs to detect performance anomalies using sliding window statistics.

### Real-world Application

- **Frame Time Tracking**: Monitor P50/P95 frame processing times
- **Jitter Detection**: Identify temporal instability in frame rates
- **Performance Regression**: Detect when model updates cause slowdowns
- **Alerting System**: Real-time anomaly detection for production systems

---

## Problem Statement

**Input**:
- Array `frame_times`: Processing time for each frame (in ms)
- Window size `k`: Number of consecutive frames to analyze
- Threshold `max_avg_time`: Maximum acceptable average (in ms)

**Task**:
Find all sliding windows of size `k` where the average frame time exceeds threshold.

**Output**:
- Number of anomalous windows
- For each anomaly: `(start_index, end_index, avg_time)`

**Extension (5b)**:
Given multiple window sizes, report anomalies for each.

---

## Solution Approach

### Key Insight

**Naive approach (O(N*K)):**
```python
for i in range(n - k + 1):
    window_avg = sum(frame_times[i:i+k]) / k  # O(K) each time
```

**Optimized approach (O(N)):**
```python
# Calculate first window once
win_sum = sum(frame_times[:k])  # O(K) once

# Slide window incrementally
for i in range(1, n - k + 1):
    win_sum += frame_times[i+k-1] - frame_times[i-1]  # O(1)
    win_avg = win_sum / k
```

### Algorithm Steps

```
1. Initialize window sum for first k frames
2. Check if first window average > threshold
3. For each subsequent position:
   a. Update sum: add new frame, remove old frame
   b. Calculate average
   c. Check threshold
   d. Record anomaly if exceeded
4. Output results
```

---

## Complexity Analysis

**Time Complexity**: 
- Single window size: `O(N)` where N = number of frames
- Multiple window sizes (5b): `O(N * M)` where M = number of window sizes

**Space Complexity**: 
- `O(1)` for single window size
- `O(A)` where A = total anomalies found

**Why O(N)?**
- Each frame is visited exactly twice:
  1. Once when entering the window
  2. Once when leaving the window
- Window sum update is O(1), not O(K)

---

## Key Patterns & Techniques

### 1. **Incremental Sum Update**
```python
# Instead of recalculating entire sum
win_sum = sum(frame_times[i:i+k])  # O(K)

# Update incrementally
win_sum += new_frame - old_frame  # O(1)
```

### 2. **Window Indexing**
```python
# Window starting at position i
# has frames [i, i+1, ..., i+k-1]

start = i
end = i + k - 1

# When sliding from position i to i+1:
old_frame = frame_times[i]      # leaving window
new_frame = frame_times[i+k]    # entering window
```

### 3. **Multiple Window Sizes (5b)**
```python
# Outer loop: window sizes
for k in ks:
    # Inner loop: sliding window
    for i in range(n - k + 1):
        # ...
```

---

## Edge Cases & Gotchas

### 1. **First Window**
```python
# Don't forget to check the first window!
win_sum = sum(frame_times[:k])
win_avg = win_sum / k
if win_avg > threshold:
    record_anomaly(0, k-1, win_avg)

# Then slide
for i in range(1, n - k + 1):
    # ...
```

### 2. **Boundary Condition**
```python
# > threshold, not >=
if win_avg > max_avg_time:  # ✓
if win_avg >= max_avg_time:  # ✗ (unless specified)
```

### 3. **Float Precision**
```python
# Use float for threshold and average
max_avg_time = float(input())  # not int()
win_avg = win_sum / k  # float division
```

### 4. **Window Size = Array Length**
```python
# Only 1 possible window
if k == n:
    # Only check the entire array
```

---

## Why This Problem Matters for Waabi

### Direct Alignment with Job Description

**From Waabi JD**:
- ✅ "Implement metrics and tags" → Frame time metrics
- ✅ "Enable discovery of interesting scenarios" → Anomaly detection
- ✅ "Data processing pipelines" → Real-time monitoring

### Connection to Your Resume

**Your Qualcomm Experience**:
> "Implemented P50/P95 frame time tracking and jitter detection for temporal stability"

This problem is literally what you did:
- Monitor frame processing times
- Detect anomalies in sliding windows
- Track statistical metrics over time

### Technical Skills Demonstrated

1. **Sliding Window Optimization**: O(N*K) → O(N)
2. **Statistical Analysis**: Average, threshold detection
3. **Real-time Processing**: Incremental updates
4. **Multi-metric Tracking**: Multiple window sizes

---

## Follow-up Questions (Prepare for Interview)

### Q1: "How would you track P95 instead of average?"

**Answer**:
```
For P95, we need to maintain sorted order within window:
- Use a sorted data structure (e.g., balanced BST)
- Or use approximate sketch algorithms (t-digest)
- Time: O(N log K) for exact, O(N) for approximate
```

### Q2: "What if we want real-time processing (streaming)?"

**Answer**:
```
- Use circular buffer for O(1) insertion
- Maintain running sum for O(1) average
- Publish alerts asynchronously
- Example: Kafka + Flink for stream processing
```

### Q3: "How would you handle multiple thresholds?"

**Answer**:
```
- Priority: CRITICAL > WARNING > INFO
- Check thresholds in order
- Example: >30ms critical, >25ms warning
```

### Q4: "What about memory constraints with millions of frames?"

**Answer**:
```
- Streaming aggregation: don't store all frames
- Keep only window_size recent frames in memory
- Persist anomalies to database
- Use time-based windows instead of count-based
```

---

## Related Problems

### Similar Patterns
- **643. Maximum Average Subarray I**: Fixed window average
- **1456. Maximum Vowels in Substring**: Fixed window counting
- **209. Minimum Size Subarray Sum**: Variable window with target
- **239. Sliding Window Maximum**: Window with monotonic deque

### Practice Recommendations
1. **643** → Warm up on fixed window
2. **209** → Practice variable window
3. **239** → Advanced window with extrema tracking

---

## Implementation Notes

### Python-Specific Tips

```python
# 1. Float division in Python 3
win_avg = win_sum / k  # Always returns float

# 2. List slicing for initialization
win_sum = sum(frame_times[:k])  # O(K)

# 3. Formatted output
print(f"{start} {end} {avg:.2f}")  # 2 decimal places

# 4. defaultdict for multiple window sizes
from collections import defaultdict
anomaly = defaultdict(list)  # Auto-initializes empty list
```

### Common Mistakes

```python
# ❌ Wrong: Recomputing sum every time
for i in range(n - k + 1):
    win_sum = sum(frame_times[i:i+k])  # O(K)

# ✅ Right: Incremental update
win_sum = sum(frame_times[:k])
for i in range(1, n - k + 1):
    win_sum += frame_times[i+k-1] - frame_times[i-1]  # O(1)

# ❌ Wrong: Forgetting first window
for i in range(1, n - k + 1):  # Starts at 1!

# ✅ Right: Check first, then slide
check_window(0, k-1)
for i in range(1, n - k + 1):
    # ...
```

---

## Comparison: Different Window Problems

| Problem | Window Type | Metric | Complexity |
|---------|-------------|--------|------------|
| **This (5a)** | Fixed size | Average | O(N) |
| **This (5b)** | Multiple fixed | Average | O(N*M) |
| **209** | Variable | Sum | O(N) |
| **239** | Fixed | Maximum | O(N) |
| **3** | Variable | Unique count | O(N) |

---

## Extension: Problem 5b Analysis

### Multi-Window Size Strategy

```python
# Naive: Compute each window size independently
for k in ks:
    for i in range(n - k + 1):
        # O(N) per k → O(N * M) total

# Can we do better?
# Not really, each window size needs full scan
# But we can optimize memory by streaming results
```

### Expected Behavior

```
Larger windows → Smoother averages → Fewer anomalies
Smaller windows → More sensitive → More anomalies

Example:
Window size 3: 4 anomalies  (captures short spikes)
Window size 5: 2 anomalies  (smooths out noise)
Window size 7: 1 anomaly    (only major incidents)
```

---

## Lessons Learned

1. **Sliding window is about incremental updates** - Don't recompute!
2. **Handle first window explicitly** - Easy to forget
3. **Float precision matters** - Use float for thresholds
4. **Boundary conditions** - `>` vs `>=` makes a difference
5. **Multi-metric tracking** - Same technique, different window sizes

---

## Time Spent

- **Understanding**: 5 min (problem is straightforward)
- **Design**: 5 min (recognize sliding window pattern)
- **Implementation**: 15 min (handle edge cases)
- **Testing**: 10 min (verify with examples)
- **Extension (5b)**: 10 min (add multi-window support)
- **Total**: ~45 min

**Target for interview**: 20-25 min (if you know the pattern)

---

## Interview Talking Points

When discussing this problem:

1. **Start with naive approach**:
   "First, I'd compute the average for each window by summing k elements each time..."

2. **Identify optimization**:
   "But that's O(N*K). We can optimize by maintaining a running sum and updating incrementally..."

3. **Explain correctness**:
   "This works because when we slide the window, only 2 elements change: one leaves, one enters..."

4. **Connect to experience**:
   "This is actually similar to what I did at Qualcomm with P95 frame time tracking..."

5. **Discuss trade-offs**:
   "For real-time systems, we'd use streaming aggregation to avoid storing all frames..."
