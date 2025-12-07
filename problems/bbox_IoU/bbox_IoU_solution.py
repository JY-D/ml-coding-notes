from typing import TypeAlias

import numpy as np
import numpy.typing as npt

# Define a type alias for Bounding Box (List, Tuple, or Array)
BoxType: TypeAlias = list[float] | tuple[float, float, float, float] | npt.NDArray[np.float64]  # noqa: UP040


def calculate_iou(box1: BoxType, box2: BoxType) -> float:
    """
    Calculate Intersection over Union (IoU) between two bounding boxes (Scalar version).

    Args:
        box1: [x1, y1, x2, y2]
        box2: [x1, y1, x2, y2]

    Returns:
        float: IoU value between 0.0 and 1.0
    """
    x1_a, y1_a, x2_a, y2_a = box1
    x1_b, y1_b, x2_b, y2_b = box2

    inter_x1 = max(x1_a, x1_b)
    inter_y1 = max(y1_a, y1_b)
    inter_x2 = min(x2_a, x2_b)
    inter_y2 = min(y2_a, y2_b)

    inter_w = max(0.0, inter_x2 - inter_x1)
    inter_h = max(0.0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    if inter_area == 0:
        return 0.0

    box1_area = (x2_a - x1_a) * (y2_a - y1_a)
    box2_area = (x2_b - x1_b) * (y2_b - y1_b)
    union_area = box1_area + box2_area - inter_area

    return inter_area / (union_area + 1e-6)


def calculate_iou_vectorized(
    boxes_a: npt.NDArray[np.float64], boxes_b: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    """
    Calculate Pairwise IoU Matrix between two sets of boxes using Numpy Broadcasting.

    Args:
        boxes_a: Shape (N, 4) -> [x1, y1, x2, y2]
        boxes_b: Shape (M, 4) -> [x1, y1, x2, y2]

    Returns:
        np.ndarray: Shape (N, M), IoU matrix.
    """
    boxes_a = np.array(boxes_a, dtype=np.float64)
    boxes_b = np.array(boxes_b, dtype=np.float64)

    if boxes_a.ndim == 1:
        boxes_a = boxes_a[np.newaxis, :]
    if boxes_b.ndim == 1:
        boxes_b = boxes_b[np.newaxis, :]

    area_a = (boxes_a[:, 2] - boxes_a[:, 0]) * (boxes_a[:, 3] - boxes_a[:, 1])
    area_b = (boxes_b[:, 2] - boxes_b[:, 0]) * (boxes_b[:, 3] - boxes_b[:, 1])

    lt = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])
    rb = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])

    wh = np.clip(rb - lt, a_min=0, a_max=None)
    inter_area = wh[:, :, 0] * wh[:, :, 1]

    union_area = area_a[:, None] + area_b[None, :] - inter_area

    return inter_area / (union_area + 1e-6)
