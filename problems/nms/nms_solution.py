import numpy as np
import numpy.typing as npt


def nms(boxes: npt.NDArray[np.float64], scores: npt.NDArray[np.float64], iou_threshold: float = 0.5) -> list[int]:
    """
    Apply Non-Maximum Suppression (NMS) to avoid detecting the same object multiple times.
    Args:
        boxes: (N, 4) numpy array with format [x1, y1, x2, y2]
        scores: (N, ) numpy array of confidence scores
        iou_threshold: Float threshold for suppressing overlapping boxes
    Returns:
        keep: List of indices to keep
    """
    # If no boxes, return empty list immediately
    if len(boxes) == 0:
        return []

    # Initialize the list of picked indices
    keep = []

    # Extract coordinates for faster access
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Calculate areas of all boxes
    areas = (x2 - x1) * (y2 - y1)

    # Sort the scores in descending order and get the indices
    order = scores.argsort()[::-1]

    while order.size > 0:
        # 1. Pick the index with the highest score
        i = order[0]
        keep.append(i)

        # 2. Compute IoU between the picked box (i) and the rest of the boxes (order[1:])
        # Note: We use order[1:] because we want to compare with remaining boxes

        # Calculate intersection coordinates
        # compute current most confidence box with others, xx1: max(x1[i], x1[others])
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        # Calculate intersection width and height
        # Use np.maximum(0.0, ...) to handle cases with no overlap
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)

        inter = w * h

        # Calculate IoU
        # Union = Area[i] + Area[others] - Intersection
        ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)

        # 3. Filter out boxes with IoU greater than threshold
        # We want to keep boxes where IoU <= threshold
        inds = np.where(ovr <= iou_threshold)[0]  # [0]: getting array in tuple(array(),)

        # 4. Update the order list
        # CRITICAL: Since inds corresponds to order[1:], we need to add 1 to map back to original indices in 'order'
        order = order[inds + 1]

    return keep
