# Polygon Area (Shoelace Formula)

## 1. Problem Definition
Calculate the area of a simple polygon given its vertices in order (clockwise or counter-clockwise).
* **Input:** `points`: $(N, 2)$ Numpy array representing $[x, y]$ coordinates.
* **Output:** `float`: Area of the polygon.

## 2. The Math (Shoelace Formula)
The area $A$ of a polygon with vertices $(x_0, y_0), (x_1, y_1), \dots, (x_{n-1}, y_{n-1})$ is given by:

$$
A = \frac{1}{2} \left| \sum_{i=0}^{N-1} (x_i y_{i+1} - x_{i+1} y_i) \right|
$$

*Note: The indices wrap around, so when $i = N-1$, the term $(i+1)$ corresponds to index $0$.*

## 3. Vectorization Strategy
Instead of iterating through points using a loop, we can perform the operation on the entire array at once.

The challenge is the $(i+1)$ term, which requires looking at the "next" element. In Numpy, we use `np.roll`.

### Visualizing `np.roll(x, -1)`

| Index | Original `x` | `np.roll(x, -1)` | Meaning |
| :--- | :--- | :--- | :--- |
| 0 | $x_0$ | $x_1$ | Pair $x_0$ with $y_1$ |
| 1 | $x_1$ | $x_2$ | Pair $x_1$ with $y_2$ |
| ... | ... | ... | ... |
| N-1 | $x_{N-1}$ | $x_0$ | Pair $x_{N-1}$ with $y_0$ (Wrap-around) |

## 4. Implementation Code

```python
import numpy as np

def polygon_area(points: np.ndarray) -> float:
    # Extract coordinates
    x = points[:, 0]
    y = points[:, 1]
    
    # Shift arrays to align i with i+1
    x_next = np.roll(x, -1)
    y_next = np.roll(y, -1)
    
    # Vectorized calculation
    # term1: x_i * y_{i+1}
    # term2: x_{i+1} * y_i
    cross_product = (x * y_next) - (x_next * y)
    
    return 0.5 * np.abs(np.sum(cross_product))