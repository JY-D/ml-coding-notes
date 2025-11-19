# Open the Lock (LC 752) — Notes

**Core idea:** Unweighted shortest path on an implicit graph of size 10^4 (states `"0000" ~ "9999"`). Each state has up to 8 neighbors (turn one wheel +1/-1, ring-wrapped). Use **BFS** with a `deque`. Use **sets** for `dead` and `seen` to get O(1) membership.

## Why BFS here
- All edges have the same cost (1 move) → **first time** we pop/see a state is its **shortest distance**.
- We do **layered expansion**: distance 0 → 1 → 2 → ...; as soon as we reach `target`, that layer count is the answer.

## State & neighbors
- State: 4-char string `"d0d1d2d3"`.
- For each index `i ∈ {0..3}` and `delta ∈ {+1, -1}`:
  - `nd = (int(cur[i]) + delta) % 10`  // ring wrap (9→0, 0→9)
  - `nxt = cur[:i] + str(nd) + cur[i+1:]`

## Data structures
- `dead: set[str]` — O(1) dead-end check.
- `seen: set[str]` — **mark at enqueue time** to avoid duplicate enqueues.
- `deque` — `popleft()` is O(1), unlike `list.pop(0)`.

## Early exits / edges
- If `"0000" in dead` → return `-1`.
- If `target == "0000"` → return `0`.
- Skip enqueue if `nxt in dead or nxt in seen`.

## Two equivalent step-count styles
1) Carry `(state, steps)` in the queue.
2) Level-by-level: loop `for _ in range(len(q))` then `steps += 1` after finishing the level.

## Why set over list
- `x in set` and `set.add(x)` are average **O(1)**; with `list` it's O(n). With up to 10k states and heavy membership checks, `set` is the standard choice.

## Common pitfalls
- Using `list.pop(0)` (O(n)) instead of `deque.popleft()`.
- Marking visited only when popped (can lead to multiple enqueues) — **prefer "mark at enqueue"**.
- Trying to "jump" two digits at once (e.g., `0200 → 0202` in one step) — **illegal**; one move changes only one wheel by ±1.
- Forgetting ring wrap with `% 10`.
- Not handling start-in-dead or target-is-start cases.

## Complexity
- States ≤ 10^4, each generates ≤ 8 neighbors.
- Time: O(States + Edges) ≈ O(10^4).
- Space: O(States) for `seen` + queue in the worst case.
