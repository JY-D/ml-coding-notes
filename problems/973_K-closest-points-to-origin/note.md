# K Closest Points to Origin (LeetCode 973)

## 1. Problem Definition
Given an array of points where `points[i] = [xi, yi]` and an integer `k`, return the `k` closest points to the origin `(0, 0)`.
* **Metric:** Euclidean Distance $\sqrt{x^2 + y^2}$. (Squared distance $x^2 + y^2$ is sufficient for comparison).

## 2. Approaches

### A. Global Sort / Min Heap (The "Offline" Approach)
* **Logic:** Calculate distance for ALL $N$ points, put them in a list/heap, and sort them.
* **Time:** $O(N \log N)$ (Sorting) or $O(N + K \log N)$ (Heapify + Pop).
* **Space:** $O(N)$ (Must hold all points in memory).
* **Verdict:** Good for small datasets.

### B. Max Heap of Size K (The "Streaming" Approach)
* **Logic:** We only care about the $K$ smallest distances.
    * We maintain a container of size $K$.
    * To ensure we have the *smallest* $K$, we need to know which one is the *largest* inside our container, so we can kick it out when a better (smaller) one comes along.
    * Structure: **Max Heap**.
* **Python Implementation:** Python's `heapq` is a Min Heap. To make it behave like a Max Heap, we store **negative distances**.
    * Small distance (e.g., 5) $\to$ Becomes -5.
    * Large distance (e.g., 100) $\to$ Becomes -100.
    * In a Min Heap, -100 is smaller than -5, so -100 floats to the top.
    * Actually, wait... 
    * **Correction:** * We want to keep SMALL distances.
        * We want to EVICT the LARGEST distance among the K.
        * In a Min Heap of *negative* numbers: 
            * Distances: 5, 10, 100.
            * Negatives: -5, -10, -100.
            * Smallest is -100. `heap[0]` will be -100.
            * This corresponds to distance 100 (The largest).
            * Perfect! `heap[0]` gives us the "worst" point to evict.
* **Time:** $O(N \log K)$. (Much faster when $K \ll N$).
* **Space:** $O(K)$. (Memory efficient).
* **Verdict:** **Best for Big Data / Perception Streams.**

## 3. Applications in ADAS
* **Lidar Processing:** Keep only the closest 100 points for heavy processing.
* **Active Learning:** Select top K "least confident" samples for human labeling.