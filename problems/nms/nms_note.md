# Non-Maximum Suppression (NMS) Notes

## 1\. Problem Definition

**Goal:** Eliminate redundant, overlapping bounding boxes and keep only the "best" box for each object.

  * **Input:**
      * `boxes`: $(N, 4)$ matrix $[x_1, y_1, x_2, y_2]$.
      * `scores`: $(N,)$ confidence scores.
      * `iou_threshold`: Float (e.g., 0.5).
  * **Output:** List of indices to keep.

## 2\. The Greedy Strategy (Logic)

NMS follows a **Greedy Algorithm** approach:

1.  **Sort** all boxes by score (High $\to$ Low).
2.  **Pick** the box with the highest score as the **Winner**. Add it to the `keep` list.
3.  **Compare** the Winner with all **remaining boxes**.
4.  **Suppress (Remove)** any remaining box that has an $\text{IoU} > \text{threshold}$ with the Winner.
5.  **Repeat** step 2-4 with the survivors until no boxes remain.

-----

## 3\. Numpy Implementation Details

### A. Sorting

We need to sort indices, not values, to track the original boxes.

```python
# argsort returns indices from Low to High, so we reverse it [::-1]
order = scores.argsort()[::-1]
```

### B. Vectorized Intersection (Broadcasting)

This is the core optimization. Instead of a `for` loop to compare the Winner against every other box, we use **Broadcasting**.

  * **Winner ($i$):** `x1[i]` is a **Scalar**.
  * **Others (`order[1:]`):** `x1[order[1:]]` is a **Vector** (size $M$).

When computing `np.maximum(scalar, vector)`, Numpy **broadcasts** the scalar to match the vector's shape.

```python
# i = order[0] (Winner)
# others = order[1:]

# One-to-Many comparison in a single step
xx1 = np.maximum(x1[i], x1[order[1:]])  # Scalar vs Vector -> Vector
yy1 = np.maximum(y1[i], y1[order[1:]])
xx2 = np.minimum(x2[i], x2[order[1:]])
yy2 = np.minimum(y2[i], y2[order[1:]])

# Calculate Intersection Area
w = np.maximum(0.0, xx2 - xx1)
h = np.maximum(0.0, yy2 - yy1)
inter = w * h  # Result is a Vector of intersection areas
```

### C. Index Mapping (The Tricky Part)

After calculating IoU (`ovr`), we filter the `order` list.

```python
# 1. Find relative indices of boxes to KEEP (IoU <= threshold)
# np.where returns a tuple (arr,), so we take [0]
inds = np.where(ovr <= iou_threshold)[0]

# 2. Update 'order' for the next iteration
# CRITICAL: 'inds' are indices relative to 'order[1:]' (the Candidates).
# We must add +1 to map them back to the original 'order'.
order = order[inds + 1]
```

**Visualizing `order = order[inds + 1]`:**

Assume `order = [10, 5, 8, 2]`.

  * **Winner:** `10` (Index 0).
  * **Candidates:** `[5, 8, 2]` (from `order[1:]`).
  * **IoU Check:**
      * Box 5: Keep (Index 0 in candidates).
      * Box 8: Suppress (Index 1 in candidates).
      * Box 2: Keep (Index 2 in candidates).
  * **`inds` (Relative):** `[0, 2]`
  * **`inds + 1` (Absolute in `order`):** `[1, 3]` -\> corresponds to `5` and `2`.
  * **New `order`:** `[5, 2]`.

-----

## 4\. Complete Code Snippet

```python
def nms(boxes, scores, iou_threshold=0.5):
    keep = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    
    order = scores.argsort()[::-1]

    while order.size > 0:
        i = order[0]
        keep.append(i)
        
        # Vectorized IoU Calculation
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        
        ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)

        # Filter indices
        inds = np.where(ovr <= iou_threshold)[0]
        order = order[inds + 1]

    return keep
```