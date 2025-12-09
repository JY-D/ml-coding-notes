"""
NumPy Essentials for ML/CV Interviews
Author: Joey Tung
"""

import numpy as np

# === ARRAY CREATION ===
np.array([1, 2, 3])
np.zeros((3, 4))  # 3x4 matrix of zeros
np.ones((2, 3))
np.random.rand(5)  # Uniform [0, 1)
np.random.randn(5)  # Normal distribution

# === INDEXING & FILTERING ===
arr[arr > 0.5]  # Boolean mask
arr[2:5]  # Slice
arr[[0, 2, 4]]  # Fancy indexing

# === STATISTICS ===
np.mean(arr)
np.std(arr)
np.percentile(arr, 95)  # 95th percentile
np.max(arr), np.min(arr)

# === ARGMAX/ARGMIN ===
np.argmax(arr)  # Index of max value
np.argmin(arr)  # Index of min value
np.argsort(arr)  # Indices that would sort array

# === VECTORIZED OPS ===
arr * 2  # Element-wise multiply
arr + other_arr  # Element-wise add
np.sqrt(arr)  # Element-wise sqrt
np.clip(arr, 0, 1)  # Clip values to [0, 1]

# === USEFUL TRICKS ===
np.where(arr > 0.5, 1, 0)  # Ternary: if > 0.5 then 1 else 0
np.sum(arr > 0.5)  # Count elements > 0.5
np.unique(arr, return_counts=True)  # Unique values + counts
