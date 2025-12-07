# Bounding Box IoU & Vectorization

## 1\. Problem Definition

Calculate the **Intersection over Union (IoU)** between bounding boxes.

  * **Scalar Version:** Calculate IoU between 1 box and 1 box.
  * **Vectorized Version:** Calculate **Pairwise IoU** between `N` prediction boxes and `M` ground truth boxes. This is essential for evaluating mAP or performing NMS (Non-Maximum Suppression) efficiently.

## 2\. The Math (Scalar)

Given two boxes $A$ and $B$:

$$
\text{IoU} = \frac{\text{Area}(A \cap B)}{\text{Area}(A \cup B)} = \frac{\text{Area}(A \cap B)}{\text{Area}(A) + \text{Area}(B) - \text{Area}(A \cap B)}
$$

-----

## 3\. Vectorization & Broadcasting (The "Magic")

The goal is to compute an $(N, M)$ matrix without using nested `for` loops. We achieve this using **Numpy Broadcasting**.

### The Setup

  * `boxes_a`: Shape `(N, 4)`  (e.g., Predictions)
  * `boxes_b`: Shape `(M, 4)`  (e.g., Ground Truths)

We cannot compare them directly because dimensions $N$ and $M$ mismatch. We need to expand them into a 3D grid $(N, M, 4)$.

### Step-by-Step Broadcasting

#### 1\. Insert Dimensions (The `None` or `np.newaxis` trick)

We manipulate the shapes to align axes for broadcasting.

  * **`boxes_a[:, None, :]`**

      * Original: `(N, 4)`
      * New Shape: **`(N, 1, 4)`**
      * *Concept:* We insert a "dummy" dimension in the middle. Think of this as stacking $N$ boxes vertically, leaving the horizontal dimension empty for $B$.

  * **`boxes_b[None, :, :]`**

      * Original: `(M, 4)`
      * New Shape: **`(1, M, 4)`**
      * *Concept:* We insert a "dummy" dimension at the front. Think of this as laying out $M$ boxes horizontally.

#### 2\. The Expansion (Implicit Copying)

When we perform an operation (like `np.maximum`) between these two reshaped arrays, Numpy automatically **replicates** the data along the dimension with size `1` to match the other array.

```text
Operation: np.maximum(A, B)

Array A: (N, 1, 4)  ---> Stretches dim 1 to M ---> Becomes (N, M, 4)
Array B: (1, M, 4)  ---> Stretches dim 0 to N ---> Becomes (N, M, 4)
--------------------------------------------------------------------
Result:  (N, M, 4)
```

#### 3\. Visualizing the Grid

Imagine $N=3$ and $M=2$. The result is a grid where every cell `(i, j)` contains the comparison result between $BoxA_i$ and $BoxB_j$.

```text
          B1        B2
      +---------+---------+
  A1  | (A1,B1) | (A1,B2) |
      +---------+---------+
  A2  | (A2,B1) | (A2,B2) |
      +---------+---------+
  A3  | (A3,B1) | (A3,B2) |
      +---------+---------+
      
Result Shape: (3, 2, ...)
```

### Code Explanation

```python
# 1. Intersection Top-Left (x1, y1)
# We want the MAX of the x1s and y1s
# (N, 1, 2) vs (1, M, 2) -> (N, M, 2)
lt = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])

# 2. Intersection Bottom-Right (x2, y2)
# We want the MIN of the x2s and y2s
# (N, 1, 2) vs (1, M, 2) -> (N, M, 2)
rb = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])

# 3. Intersection Width & Height
# rb - lt gives us [width, height]
# We must clip at 0 because if boxes don't overlap, min(x2) - max(x1) will be negative.
wh = np.clip(rb - lt, a_min=0, a_max=None)

# 4. Intersection Area
# Multiply width * height.
# wh is (N, M, 2). wh[:, :, 0] is width, wh[:, :, 1] is height.
# Result shape: (N, M)
inter = wh[:, :, 0] * wh[:, :, 1]
```

-----

## 4\. Implementation Details

### Handling 1D Inputs (Safety Check)

If a user passes a single box `[x, y, x, y]` (Shape `(4,)`), simple slicing like `[:, 2]` will fail or behave unexpectedly. We force it to be 2D.

```python
if boxes_a.ndim == 1:
    boxes_a = boxes_a[np.newaxis, :] # Shape becomes (1, 4)
```

### Zero Division Protection

Always add a small epsilon (`1e-6`) to the denominator.

```python
iou = inter / (union + 1e-6)
```

## 5\. Summary Code Snippet

```python
def calculate_iou_vectorized(boxes_a, boxes_b):
    # boxes_a: (N, 4), boxes_b: (M, 4)
    
    # 1. Compute Areas (N,) and (M,)
    area_a = (boxes_a[:, 2] - boxes_a[:, 0]) * (boxes_a[:, 3] - boxes_a[:, 1])
    area_b = (boxes_b[:, 2] - boxes_b[:, 0]) * (boxes_b[:, 3] - boxes_b[:, 1])
    
    # 2. Broadcasting for Intersection (N, M)
    # Expand dims to create grid
    lt = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])
    rb = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])
    
    wh = np.clip(rb - lt, a_min=0, a_max=None)
    inter = wh[:, :, 0] * wh[:, :, 1]
    
    # 3. Compute Union (N, M)
    # Broadcast areas: (N, 1) + (1, M) - (N, M)
    union = area_a[:, None] + area_b[None, :] - inter
    
    return inter / (union + 1e-6)
```