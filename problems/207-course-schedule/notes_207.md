# 207. Course Schedule

## Problem Summary
Given `numCourses` and a list of `prerequisites` where `prerequisites[i] = [ai, bi]` indicates you must take course `bi` before course `ai`, determine if it's possible to finish all courses.

## Solution Approach: Kahn's Algorithm (Topological Sort)

### Core Idea
This is a **cycle detection problem in a directed graph**. If there's a cycle, some courses will have circular dependencies and cannot be completed.

Kahn's Algorithm uses **BFS with indegree tracking**:
1. Build adjacency list and indegree array
2. Start from all sources (courses with indegree 0)
3. Process each course and reduce indegree of neighbors
4. If all courses are processed → no cycle → return True

### Step-by-Step Logic

#### Step 1: Build Graph
```python
adj: dict[int, list[int]] = defaultdict(list)
indegree: list[int] = [0] * numCourses

for a, b in prerequisites:
    adj[b].append(a)  # b → a (b unlocks a)
    indegree[a] += 1  # a has one more prerequisite
```
- `adj[b]` stores all courses that can be unlocked after completing course `b`
- `indegree[a]` counts how many prerequisites course `a` has

#### Step 2: Find All Sources
```python
q = deque()
for i in range(numCourses):
    if indegree[i] == 0:
        q.append(i)
```
- Sources are courses with no prerequisites (indegree = 0)
- These can be taken immediately

#### Step 3: BFS Processing
```python
visited_count = 0
while q:
    course = q.popleft()
    visited_count += 1
    
    for c in adj[course]:
        indegree[c] -= 1  # Remove edge: course → c
        if indegree[c] == 0:
            q.append(c)  # c becomes a new source
```
- Process each source course
- For each neighbor `c`, reduce its indegree (simulate "removing the edge")
- If `c`'s indegree becomes 0, it's now a source → add to queue

#### Step 4: Check Result
```python
return visited_count == numCourses
```
- If all courses are processed → no cycle → True
- If some courses remain unprocessed → cycle exists → False

## Complexity Analysis
- **Time**: O(V + E) where V = numCourses, E = len(prerequisites)
  - Build graph: O(E)
  - BFS: Visit each node once O(V), check each edge once O(E)
- **Space**: O(V + E)
  - Adjacency list: O(E)
  - Indegree array: O(V)
  - Queue: O(V) worst case

## Key Takeaways
- **Indegree tracking** is the key to detect when a course becomes available
- **Only add to queue when indegree becomes 0** (all prerequisites met)
- **defaultdict(list)** handles missing keys gracefully, no need for `is not None` checks
- This pattern applies to any DAG scheduling problem (ML pipelines, task dependencies, etc.)

## Common Pitfalls
- ❌ Adding neighbors to queue immediately without checking indegree
- ❌ Forgetting to count visited courses for cycle detection
- ❌ Using `>=` instead of `==` in final check (though both work, `==` is more precise)
- ❌ Confusing edge direction: `[a, b]` means b → a, not a → b

## Related Problems
- **210. Course Schedule II**: Return the actual ordering (just collect courses in BFS order)
- **DFS Alternative**: Use 3-color marking (white/gray/black) to detect cycles recursively