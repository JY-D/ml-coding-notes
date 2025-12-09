import numpy as np

"""
Hard Sample Mining for Active Learning

Context:
You trained a perception model on 10,000 frames. Now you want to
select 100 "hardest" frames to send for human annotation to improve the model.

Definition of "hard":
- Model is confident (confidence > 0.7) but prediction is wrong (IoU < 0.5)
- Rare object classes should be prioritized (weight by inverse frequency)

Input:
- predictions: np.ndarray, shape (N, 4) - predicted boxes [x_min, y_min, x_max, y_max]
- ground_truth: np.ndarray, shape (N, 4) - ground truth boxes
- confidences: np.ndarray, shape (N,) - model confidence [0, 1]
- classes: np.ndarray, shape (N,) - object class IDs [0, 1, 2, ...]

Output:
- hard_indices: np.ndarray, shape (100,) - indices of 100 hardest samples

Example:
predictions = np.array([[10, 10, 20, 20], [30, 30, 40, 40], ...])
ground_truth = np.array([[12, 12, 22, 22], [30, 30, 40, 40], ...])
confidences = np.array([0.9, 0.6, ...])
classes = np.array([0, 1, ...])  # 0=car, 1=pedestrian, 2=bike

hard_indices = mine_hard_samples(predictions, ground_truth, confidences, classes, k=100)
# Returns: [234, 567, 891, ...] (100 indices)
"""


def mine_hard_samples(predictions, ground_truth, confidences, classes, k=100):
    """
    Find k hardest samples for active learning
    """
    # Step 1: Vectorized IoU Calculation
    # Box format: [x_min, y_min, x_max, y_max]

    # Compute areas
    area_pred = (predictions[:, 2] - predictions[:, 0]) * (predictions[:, 3] - predictions[:, 1])
    area_gt = (ground_truth[:, 2] - ground_truth[:, 0]) * (ground_truth[:, 3] - ground_truth[:, 1])

    # Intersection coordinates
    inter_x1 = np.maximum(predictions[:, 0], ground_truth[:, 0])
    inter_y1 = np.maximum(predictions[:, 1], ground_truth[:, 1])
    inter_x2 = np.minimum(predictions[:, 2], ground_truth[:, 2])
    inter_y2 = np.minimum(predictions[:, 3], ground_truth[:, 3])

    # Intersection area
    inter_w = np.maximum(0, inter_x2 - inter_x1)
    inter_h = np.maximum(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    # Union and IoU
    union_area = area_pred + area_gt - inter_area
    ious = inter_area / (union_area + 1e-6)

    # Step 2: Compute Class Weights (inverse frequency)
    counts = np.bincount(classes)  # e.g., [8000, 1500, 500] for classes [0, 1, 2]
    weights = 1.0 / (counts + 1e-6)  # Inverse frequency
    sample_weights = weights[classes]  # Map back to each sample

    # Step 3: Define "Hard" Samples
    is_confident = confidences > 0.7  # High confidence
    is_wrong = ious < 0.5  # Low IoU (wrong prediction)
    candidate_mask = is_confident & is_wrong

    # Step 4: Compute Hardness Score
    hardness = confidences * (1 - ious)  # Higher conf + lower IoU = harder
    score = sample_weights * hardness * candidate_mask

    # Step 5: Select Top-K
    hard_indices = np.argsort(-score)[:k]

    return hard_indices
