from collections import defaultdict, deque


def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # create graph: adj, indegree
    adj: dict[int, list[int]] = defaultdict(list)
    indegree: list[int] = [0] * numCourses

    for a, b in prerequisites:
        adj[b].append(a)  # b → a
        indegree[a] += 1

    # Step 2: find all source
    q: deque[int] = deque()
    for i in range(numCourses):
        if indegree[i] == 0:
            q.append(i)

    # Step 3: BFS
    visited_count = 0
    while q:
        course = q.popleft()
        visited_count += 1

        for c in adj[course]:
            indegree[c] -= 1
            if indegree[c] == 0:
                q.append(c)

    # Step 4
    return visited_count == numCourses
