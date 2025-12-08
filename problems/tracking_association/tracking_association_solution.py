import numpy as np
import numpy.typing as npt


def greedy_match(iou_matrix: npt.NDArray[np.float64], threshold: float = 0.3) -> list[tuple[int, int]]:
    """
    Assigns tracks to detections using greedy bipartite matching based on IoU.
    """
    matches: list[tuple[int, int]] = []

    # FIX: Handle empty input edge case immediately
    if iou_matrix.size == 0:
        return matches
    # Copy to avoid modifying the input matrix
    iou = iou_matrix.copy()

    while True:
        # 1. Find the max value in the entire matrix
        max_idx_flat = iou.argmax()
        t_idx, d_idx = np.unravel_index(max_idx_flat, iou.shape)

        # 2. Check threshold
        if iou[t_idx, d_idx] < threshold:
            break

        # 3. Record match
        # FIX: Cast numpy int64 to python int to satisfy Mypy
        matches.append((int(t_idx), int(d_idx)))

        # 4. Mask out the row and column
        iou[t_idx, :] = -1.0
        iou[:, d_idx] = -1.0

    return matches


# --- Test ---
iou_mat = np.array([[0.1, 0.8, 0.0], [0.7, 0.2, 0.0]])
print(greedy_match(iou_mat))
# Output: [(0, 1), (1, 0)] (Order might vary depending on max value implementation if equal)
