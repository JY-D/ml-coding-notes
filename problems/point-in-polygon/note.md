# Point in Polygon (Ray Casting Algorithm)

## 1. Problem Definition
Given a point $(x, y)$ and a polygon defined by a list of vertices $[(x_1, y_1), (x_2, y_2), ...]$, determine if the point is strictly inside the polygon.

* **Context:** Used in HD Maps to check if a vehicle is inside a specific lane, parking spot, or intersection.
* **Difficulty:** Medium-Hard (Requires Geometric Math).

## 2. Core Algorithm: Ray Casting (Even-Odd Rule)
Imagine shooting a horizontal ray from the point towards the right ($+x$ direction).
* Count how many times this ray intersects with the polygon's edges.
* **Odd Intersections:** The point is **Inside**.
* **Even Intersections:** The point is **Outside**.

### ASCII Visualization

**Scenario A: Point is Inside**
The ray hits the wall ONCE to get out.
```text
       / \
      /   \
     /  *--\----------> Ray (1 intersection)
    /_______\
```

Scenario B: Point is Outside (Left) The ray hits the wall ONCE to enter, and ONCE to exit. (1 + 1 = 2).

```text
*--------\---------/---------> Ray (2 intersections)
           \       /
            \_____/
```

## 3. The Math: Intersection Calculation
Why can't we just use x < max(p1.x, p2.x)?Because for slanted lines, the point might be within the X-range but still to the right of the line.

We need the Exact Intersection Point ($x_{inters}$)Using the property of similar triangles (slope formula):$$\frac{x_{inters} - x_1}{x_2 - x_1} = \frac{y - y_1}{y_2 - y_1}$$Solving for $x_{inters}$:$$x_{inters} = x_1 + (y - y_1) \times \frac{x_2 - x_1}{y_2 - y_1}$$

## 4. Implementation Details (Handling Edge Cases)
1. Horizontal Lines: (p2y - p1y) == 0. The formula would divide by zero.
* Solution: The condition min_y < y <= max_y implicitly handles this. Horizontal lines are parallel to the ray and are usually ignored (or handled as boundary cases).
2. Vertices: If the ray passes exactly through a vertex, we might double count (once for the edge ending there, once for the edge starting there).
* Solution: Use strict inequality > for one side and inclusive <= for the other (e.g., p1y > y vs p2y <= y). This ensures a vertex is counted by only one of the connected edges.
3. Wrap-around: The last point must connect to the first.
* Solution: Use polygon[i % n] in the loop.

## 5. Time Complexity
Time: $O(N)$ where $N$ is the number of vertices. We iterate through every edge exactly once.

Space: $O(1)$. No extra data structures needed.