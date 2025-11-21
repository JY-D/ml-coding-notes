# Multi-Source Confidence Propagation

## Problem Overview

**Source**: Custom problem inspired by Waabi's LabelFormer paper  
**Difficulty**: Medium-Hard  
**Topics**: BFS, Priority Queue, Greedy, Graph

### Background Story

Building an auto-labeling propagation system for autonomous driving datasets. Given a 2D grid of pixels where some have high-confidence labels (from human annotation or teacher model), propagate these labels to neighboring unlabeled pixels based on feature similarity.

### Real-world Application

- **Waabi LabelFormer**: Propagates high-confidence predictions to unlabeled regions using learned feature similarity
- **Semi-supervised Learning**: Leverage small amount of labeled data to label similar unlabeled data
- **Image Segmentation**: Expand labeled regions to similar neighboring pixels

---

## Problem Statement

**Input**:
- H x W grid where each cell contains:
  - `label`: Current label (0 = unlabeled, 1-K = labeled classes)
  - `confidence`: Confidence score (0.0 - 1.0)
  - `features`: Feature vector (3D for this problem)
- List of seed pixels (high-confidence labeled pixels)
- Similarity threshold for propagation

**Task**:
Propagate labels from seed pixels to unlabeled neighbors following these rules:
1. Always propagate from **higher confidence** pixels first (priority queue)
2. Only propagate if feature similarity >= threshold
3. New pixel confidence = source_confidence × similarity_score
4. Use cosine similarity for feature comparison

**Output**:
- Number of pixels that received labels
- Final grid state showing (label, confidence) for each pixel

---

## Solution Approach

### Key Insight

This is **NOT standard BFS** - it's **Priority Queue + Greedy** because:
- Standard BFS: Process by distance from source (FIFO)
- This problem: Process by confidence score (priority)

**Why?** Higher confidence pixels should propagate first, regardless of distance from seed.

### Algorithm Steps

```
1. Initialize max heap with all seed pixels (ordered by confidence)
2. While heap is not empty:
   a. Pop pixel with highest confidence
   b. Mark as visited
   c. For each of 4 neighbors:
      - Skip if out of bounds
      - Skip if already labeled
      - Skip if already visited
      - Calculate cosine similarity
      - If similarity >= threshold:
        * Assign label to neighbor
        * Calculate new confidence = current_conf × similarity
        * Push neighbor to heap
3. Output propagation count and final grid
```

### Data Structures

```python
# Max heap (simulated with negative values in min heap)
pq: list[tuple[float, int, int]] = []
heapq.heappush(pq, (-confidence, row, col))

# 2D visited array
visited: list[list[bool]] = [[False] * W for _ in range(H)]

# Grid of dicts
grid: list[list[dict]] = [
    [{'label': 0, 'confidence': 0.0, 'features': [f1, f2, f3]}, ...]
]
```

---

## Complexity Analysis

**Time Complexity**: `O((V + E) log V)`
- V = H × W (number of pixels)
- E = at most 4V (each pixel has up to 4 neighbors)
- Each heap operation: O(log V)
- Total: O((V + 4V) log V) = O(V log V)

**Space Complexity**: `O(V)`
- Visited array: O(H × W) = O(V)
- Priority queue: O(V) in worst case (all pixels get propagated)
- Grid: O(V) - already given in input

---

## Key Patterns & Techniques

### 1. **Multi-Source BFS with Priority Queue**
```python
# Add ALL seed pixels to heap initially
for r, c in seed_pixels:
    heapq.heappush(pq, (-grid[r][c]['confidence'], r, c))
```

### 2. **Max Heap Simulation**
```python
# Python's heapq is min heap
# Use negative values to simulate max heap
heapq.heappush(pq, (-confidence, r, c))
neg_conf, r, c = heapq.heappop(pq)
conf = -neg_conf  # Convert back
```

### 3. **Cosine Similarity**
```python
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0
```

### 4. **Visited Pattern**
```python
# Mark visited AFTER popping (not when pushing)
if visited[r][c]:
    continue
visited[r][c] = True
```

**Why not mark when pushing?**
- A pixel might be pushed multiple times from different neighbors
- We only want to process it once (when it reaches highest priority)

---

## Edge Cases & Gotchas

### 1. **Negative Cosine Similarity**
- Features can be opposite (similarity < 0)
- Solution: `new_conf = max(0.0, conf * sim)`

### 2. **Multiple Seeds Competing**
- Two seeds might want to label the same pixel
- Solution: First one wins (checked via `neighbor['label'] != 0`)

### 3. **Zero-norm Features**
- Division by zero in cosine similarity
- Solution: Return 0.0 if either norm is 0

### 4. **Single Pixel Grid**
- No neighbors to propagate to
- Solution: Naturally handled (no valid neighbors in loop)

### 5. **Already Visited Check**
```python
# IMPORTANT: Check neighbor's visited status
if visited[nr][nc]:
    continue  # Don't re-propagate
```

---

## Comparison: BFS vs Dijkstra vs This Problem

| Feature | BFS | Dijkstra | This Problem |
|---------|-----|----------|--------------|
| **Data Structure** | Queue (deque) | Min Heap | Max Heap (negated) |
| **Order** | FIFO | Shortest distance | Highest confidence |
| **Edge Weights** | Unweighted | Non-negative | Confidence × similarity |
| **Guarantee** | Shortest path (hops) | Shortest path (weight) | Highest confidence first |

---

## Test Cases Breakdown

### Test Case 1: Single Seed, High Threshold
- **Threshold**: 0.8 (strict)
- **Expected**: Only very similar neighbors get labeled
- **Learning**: Some corners fail similarity check

### Test Case 2: Multiple Seeds
- **Seeds**: 3 different labels
- **Expected**: Each seed propagates to its neighborhood
- **Learning**: Higher confidence seeds propagate first

### Test Case 3: Zero Threshold
- **Threshold**: 0.0 (accept everything)
- **Expected**: All unlabeled pixels get labeled
- **Learning**: Even opposite features can propagate (but conf → 0)

### Test Case 4: Very High Threshold
- **Threshold**: 0.99 (nearly identical required)
- **Expected**: No propagation
- **Learning**: Threshold acts as quality gate

---

## Why This Problem Matters for Waabi

### Direct Alignment with Job Description

**From Waabi JD**:
- ✅ "Work with large datasets from various sources" → Grid processing
- ✅ "Implement metrics and tags" → Confidence tracking
- ✅ "Enable discovery of interesting scenarios" → Propagation logic
- ✅ "Data processing pipelines" → Multi-stage propagation

### Technical Skills Demonstrated

1. **Graph Algorithms**: BFS variant with priority queue
2. **Data Structures**: Efficient use of heap, dict, 2D arrays
3. **ML Concepts**: Confidence propagation, feature similarity
4. **Python Proficiency**: Type hints, clean code structure

### Connection to LabelFormer Paper

> "Our method propagates high-confidence predictions to unlabeled regions using learned feature similarity"

This problem is a simplified implementation of their core algorithm.

---

## Follow-up Questions (Prepare for Interview)

### Q1: "How would you optimize this for very large grids?"

**Answer**:
- Use sparse representation (only store labeled pixels)
- Implement spatial indexing (k-d tree for neighbor search)
- Parallelize: Each seed can propagate independently initially
- Early stopping: Stop if confidence drops below threshold

### Q2: "What if features are high-dimensional (e.g., 512D)?"

**Answer**:
- Cosine similarity still works (vectorized with NumPy)
- Consider approximate nearest neighbor search (FAISS)
- Dimensionality reduction (PCA) if memory is concern

### Q3: "How would you handle video sequences (temporal data)?"

**Answer**:
- Extend to 3D grid (H × W × T)
- Add temporal consistency constraint
- Use optical flow to guide propagation
- Implement sliding window for online processing

### Q4: "What if we want bidirectional propagation?"

**Answer**:
- Run forward pass (high → low confidence)
- Run backward pass (refine based on neighbors)
- Iterate until convergence
- Similar to belief propagation in CRF

---

## Related LeetCode Problems

### Similar Patterns
- **994. Rotting Oranges**: Multi-source BFS (but no priority)
- **1091. Shortest Path in Binary Matrix**: BFS with obstacles
- **743. Network Delay Time**: Single-source Dijkstra
- **847. Shortest Path Visiting All Nodes**: BFS with state

### Practice Recommendations
1. **994** → Warm up on multi-source BFS
2. **743** → Practice heap-based graph traversal
3. **1293** → BFS with constraints (similar to threshold)

---

## Implementation Notes

### Python-Specific Tricks

```python
# 1. Tuple unpacking in heap
neg_conf, r, c = heapq.heappop(pq)

# 2. Dictionary update in-place
neighbor['label'] = current_label
neighbor['confidence'] = new_conf

# 3. List comprehension for 2D array
visited = [[False] * W for _ in range(H)]

# 4. Formatted output with f-string
row_output.append(f"({label}, {conf:.2f})")
```

### Type Hints Best Practices

```python
from typing import Any

grid: list[list[dict[str, Any]]] = []
pq: list[tuple[float, int, int]] = []
seed_pixels: list[tuple[int, int]] = []
```

---

## Lessons Learned

1. **Not all "spreading" problems are BFS** - consider priority-based approaches
2. **Visited tracking is subtle** - mark after popping, not when pushing
3. **Feature similarity is domain-specific** - cosine works for normalized features
4. **Edge cases matter** - zero norms, negative similarities, boundary checks
5. **Type hints help** - especially with complex nested structures

---

## Time Spent

- **Understanding**: 10 min (reading problem + examples)
- **Design**: 10 min (choosing data structures)
- **Implementation**: 40 min (coding + debugging)
- **Testing**: 30 min (test cases + edge cases)
- **Total**: ~1.5 hours

**Target for interview**: 30 min (with practice)
