# Greedy Data Association (Tracking)

## 1. Problem Definition
In Multi-Object Tracking (MOT), we need to associate "Tracks" (objects from previous frames) with "Detections" (objects in current frame).
* **Input:** `iou_matrix`: $(N, M)$ Numpy array. Rows = Tracks, Cols = Detections.
* **Output:** List of matched pairs `[(track_id, det_id), ...]`.
* **Constraint:** One-to-One matching. A track can only match one detection, and vice versa.

## 2. The Logic: Global Greedy Strategy
We cannot simply loop through tracks and pick the best detection for each, because multiple tracks might compete for the same detection ("One-to-Many" conflict).

**Correct Algorithm:**
1.  Find the **Global Maximum** IoU in the entire matrix.
2.  If this IoU < threshold, stop.
3.  Record the match.
4.  **Mask out** the corresponding Row and Column (Set to -1). This is like dropping a **"Cross Bomb"** 💣 on the matrix index, ensuring neither the Track nor the Detection can be used again.
5.  Repeat.

## 3. Implementation Details

### A. Finding the Index (`argmax` + `unravel_index`)
`numpy.argmax()` returns the index of the maximum value in a **flattened** (1D) array. We need to convert it back to `(row, col)`.

Example: $2 \times 3$ Matrix
$$
\begin{bmatrix}
0.1 & 0.5 & 0.2 \\
\mathbf{0.9} & 0.3 & 0.4
\end{bmatrix}
$$

1.  `iou.argmax()` $\rightarrow$ Flat index `3` (value 0.9).
2.  `np.unravel_index(3, (2,3))` $\rightarrow$ Returns `(1, 0)`.
    * Row: $3 // 3 = 1$
    * Col: $3 \% 3 = 0$

### B. The "Cross Bomb" Masking
To enforce the 1-to-1 constraint without complex logic checks:

```python
# Match found at (t_idx, d_idx)
iou[t_idx, :] = -1  # Disable this Track (Row)
iou[:, d_idx] = -1  # Disable this Detection (Col)