# Hard Sample Mining (Active Learning)

## 1. Problem Definition
In Autonomous Driving, data is abundant (petabytes of logs), but human labeling is expensive. We cannot label everything.
We need an algorithm to intelligently select the **"Most Informative"** samples (frames) to send to human annotators.

* **Goal:** Select $K$ samples that the model is struggling with (Hard Examples) and prioritize rare classes (Long-tail).
* **Context:** Used in Data Engine pipelines to iteratively improve model performance.

## 2. Core Strategies
This implementation combines two Active Learning strategies:

### A. Uncertainty Sampling (Hardness)
We define a "Hard Sample" as a case where the model is **Overconfident but Wrong**.
* **Condition:** Confidence $> 0.7$ AND IoU $< 0.5$.
* **Scoring:** $Score \propto Confidence \times (1 - IoU)$.
    * If model is 99% confident but IoU is 0.1, this is a **Critical Error** (High score).

### B. Diversity Sampling (Inverse Frequency)
Driving datasets are heavily imbalanced (mostly cars, few cyclists).
* **Method:** Calculate class frequency $N_c$.
* **Weight:** $W_c = \frac{1}{N_c}$.
* Rare classes get significantly higher weights, ensuring the selected batch isn't just 100 missed cars.

## 3. Implementation Details (Numpy Vectorization)
* **Batch IoU:** Computed using vectorized `np.maximum` and `np.minimum` operations for $O(1)$ efficiency (relative to Python loops).
* **Boolean Masking:** Used to efficiently filter candidates (`mask = is_confident & is_wrong`).
* **Argpartition/Argsort:** Used to retrieve the Top-K indices without sorting the entire array (if optimized) or simple sorting for clarity.

### **Q1: "Why multiply by (1 - IoU) instead of just using IoU?"**
**Answer:**

(1 - IoU) converts IoU into an "error magnitude":
- IoU = 0.9 (good) → (1 - 0.9) = 0.1 (low error)
- IoU = 0.1 (bad)  → (1 - 0.1) = 0.9 (high error)

We want to prioritize high error, so we maximize (1 - IoU).

### **Q3: "Can you optimize this for 10M samples?"**

For 10M samples, could use:
1. np.argpartition instead of argsort (O(N))
2. Process in batches if memory limited
3. Use GPU (CuPy) for vectorized ops