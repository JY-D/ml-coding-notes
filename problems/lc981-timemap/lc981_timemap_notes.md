# 981. Time-based Key-Value Store

## Problem Summary
Design a time-based key-value store that:
- `set(key, value, timestamp)`: Stores the key with value at given timestamp
- `get(key, timestamp)`: Returns value at largest timestamp ≤ target, or "" if not found

**Constraints**:
- All timestamps are strictly increasing for each key
- Multiple calls to `set` for same key will have increasing timestamps

---

## Solution Approach: Binary Search on Sorted List

### Core Insight
Since timestamps are **strictly increasing**, the list of `(timestamp, value)` pairs for each key is **already sorted**. This enables O(log N) binary search for retrieval.

---

## Data Structure

```python
self.store = defaultdict(list)  # key -> [(timestamp, value), ...]
```

**Why list of tuples?**
- Tuples are immutable and hashable
- Naturally sorted by first element (timestamp)
- Single append operation maintains order

**Alternative (don't use)**:
```python
# ❌ Separate lists - harder to keep in sync
{"values": [...], "timestamps": [...]}
```

---

## Algorithm

### Set Operation
```python
def set(self, key: str, value: str, timestamp: int) -> None:
    self.store[key].append((timestamp, value))
```

**Complexity**: O(1) amortized

---

### Get Operation (The Tricky Part)

#### Goal
Find largest timestamp ≤ target

#### Approach: Binary Search with `bisect_right`
```python
def get(self, key: str, timestamp: int) -> str:
    items = self.store[key]
    
    if not items:
        return ""
    
    # Binary search for rightmost position <= timestamp
    pos = bisect.bisect_right(items, (timestamp, chr(127)))
    
    if pos == 0:
        return ""  # All timestamps > target
    else:
        return items[pos - 1][1]
```

**Complexity**: O(log N) where N = number of timestamps for this key

---

## Critical Detail: Why `chr(127)` Not `""`?

### The Problem

When `timestamp` **exactly matches** an entry, tuple comparison rules matter:

```python
items = [(1, "bar")]
timestamp = 1

# ❌ Using empty string
pos = bisect.bisect_right(items, (1, ""))
# Compares: (1, "") vs (1, "bar")
# Result: "" < "bar" → inserts LEFT of (1, "bar")
# pos = 0 → returns "" (WRONG!)

# ✅ Using chr(127)
pos = bisect.bisect_right(items, (1, chr(127)))
# Compares: (1, chr(127)) vs (1, "bar")
# Result: chr(127) > "bar" → inserts RIGHT of (1, "bar")
# pos = 1 → items[0] = (1, "bar") (CORRECT!)
```

### Tuple Comparison Rules

Python compares tuples element-by-element:
```python
(1, "a") < (2, "b")  # True (compare first: 1 < 2)
(2, "a") < (2, "b")  # True (first equal, compare second: "a" < "b")
(2, "c") < (2, "b")  # False ("c" > "b")
```

### Why `chr(127)`?

**`chr(127)` is the largest standard ASCII character (DEL).**

This ensures `(timestamp, chr(127))` is always **greater than or equal to** any `(timestamp, value)` pair, forcing `bisect_right` to insert **after** all matching timestamps.

**Alternatives (all work)**:
```python
chr(127)     # ✅ Standard choice
chr(255)     # ✅ Extended ASCII
"~" * 1000   # ✅ Works but ugly
```

---

## Memory Trick

### Mnemonic: "bisect_RIGHT + chr(max)"

```
bisect_RIGHT
    ↓
Want to insert on the RIGHT of matching elements
    ↓
Need MAXIMUM string value
    ↓
chr(127)
```

### Visual Example

```
items = [(1, "a"), (3, "b"), (5, "c")]
target = 3

bisect_right with (3, ""):
  [(1,"a"), (3,"b"), (5,"c")]
            ↑ Insert here (pos=1)
  Because "" < "b"

bisect_right with (3, chr(127)):
  [(1,"a"), (3,"b"), (5,"c")]
                   ↑ Insert here (pos=2)
  Because chr(127) > "b"

We want pos=2 → items[1] = (3, "b") ✅
```

---

## Why Not `bisect_left`?

### `bisect_left` vs `bisect_right`

```python
items = [(1, "a"), (3, "b"), (5, "c")]
timestamp = 4 (not in list)

# bisect_left
pos = bisect.bisect_left(items, (4, chr(127)))  # pos = 2
return items[pos][1]  # items[2] = (5, "c") ❌ WRONG (5 > 4)

# bisect_right
pos = bisect.bisect_right(items, (4, chr(127)))  # pos = 2
return items[pos - 1][1]  # items[1] = (3, "b") ✅ CORRECT (3 < 4)
```

**`bisect_right` + `pos - 1` always gives the correct "largest ≤ target".**

---

## Common Pitfalls

### 1. Using Empty String
```python
# ❌ Fails when timestamp exactly matches
pos = bisect.bisect_right(items, (timestamp, ""))
```

### 2. Forgetting `pos == 0` Check
```python
# ❌ Index out of bounds when all timestamps > target
return items[pos - 1][1]  # pos=0 → items[-1] (wrong!)
```

### 3. Not Understanding Tuple Comparison
```python
# ❌ Thinking only timestamp matters
# But second element affects insertion position!
```

### 4. Using Linear Search
```python
# ❌ O(N) instead of O(log N)
for ts, val in items:
    if ts <= timestamp:
        result = val
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| `__init__` | O(1) | O(1) |
| `set` | O(1) amortized | O(1) per call |
| `get` | O(log N) | O(1) |

Where N = number of timestamps for a given key.

**Total Space**: O(T) where T = total number of `set` calls across all keys.

---

## Why This Problem Matters

### Real-World Applications

1. **Time-series Databases** (e.g., InfluxDB, Prometheus)
   - Store metrics at timestamps
   - Query "what was the value at time T?"

2. **Version Control Systems** (e.g., Git)
   - Each commit has a timestamp
   - "Show me the code as of date X"

3. **ML Model Versioning**
   - Track model performance over time
   - Retrieve best model before timestamp T

4. **Financial Data** (Stock prices, exchange rates)
   - Historical price lookups
   - "What was BTC price at 3:47 PM?"

### Connection to Your Work

**Qualcomm Metrics Tracking**:
- Track inference time / accuracy over time
- Query: "What was the P95 frame time on Oct 15?"
- Same pattern: time-indexed data retrieval

**Waabi Auto-labeling**:
- Track teacher model confidence scores over time
- Query: "What was average confidence for low-light at timestamp T?"

---

## Alternative Solutions

### Approach 1: Linear Search (Naive)
```python
def get(self, key, timestamp):
    for ts, val in reversed(self.store[key]):
        if ts <= timestamp:
            return val
    return ""
```
**Complexity**: O(N) per query ❌

### Approach 2: Binary Search (Our Solution)
**Complexity**: O(log N) per query ✅

### Approach 3: Segment Tree / Fenwick Tree
- Overkill for this problem
- Useful if you need range queries (min/max/sum over timestamp range)

---

## Interview Tips

### If Asked: "How would you optimize further?"

**Answer**:
- Current solution is already optimal: O(log N) per query
- Only micro-optimization: Cache last query result if queries are often repetitive

### If Asked: "What if timestamps are NOT strictly increasing?"

**Answer**:
- Need to sort after each `set`: O(N log N) per set
- Or use `insort` from `bisect`: O(N) per set
- Better: Enforce timestamps in API contract

### If Asked: "How would you handle deletions?"

**Answer**:
- Mark as deleted (tombstone) instead of removing
- Or rebuild list periodically (garbage collection)
- Trade-off: space vs time

---

## Key Takeaway for Interviews

**When you see:**
- "Strictly increasing" timestamps/IDs
- "Find largest/smallest value ≤/≥ target"

**Think: Binary Search (`bisect`)**

**Remember**: `bisect_right` + `chr(127)` for "largest ≤ target"

---

## Practice Problem

Try solving without looking:
1. Implement `TimeMap` from scratch
2. Add test: `get` with timestamp before any `set`
3. Add test: `get` with exact timestamp match
4. Verify complexity is O(log N)

Once you can do this, you've mastered the pattern! 🎯
