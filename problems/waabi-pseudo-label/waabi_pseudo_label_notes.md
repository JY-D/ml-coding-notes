# Pseudo-label Routing Pipeline

## Problem Summary
Given teacher model predictions with confidence scores, route pseudo-labels into three categories based on thresholds:
- HIGH (≥0.8): Auto-accept for training
- MID (0.5-0.8): Send to vendor QA
- LOW (<0.5): Discard

Compute routing statistics, per-label statistics, and validate against ground truth.

---

## Solution Approach

### Task 1: Routing and Counting (Simple Grouping)

**Core Idea**: Iterate through predictions once, categorize by confidence threshold.

#### Data Structure
```python
high_conf: list[str] = []  # Image IDs with score >= 0.8
mid_conf: list[str] = []   # Image IDs with 0.5 <= score < 0.8
low_conf: list[str] = []   # Image IDs with score < 0.5
```

#### Algorithm
```python
for each prediction:
    if score >= 0.8:
        high_conf.append(image_id)
    elif score >= 0.5:
        mid_conf.append(image_id)
    else:
        low_conf.append(image_id)

# Compute percentages
total = len(high_conf) + len(mid_conf) + len(low_conf)
high_pct = len(high_conf) / total * 100
```

**Complexity**: O(N) time, O(N) space

---

### Task 2: Per-Label Statistics (Nested Grouping)

**Core Idea**: Group by `teacher_label`, track scores and routing counts per label.

#### Data Structure
```python
label_stats = defaultdict(lambda: {
    "scores": [],    # List of all scores for this label
    "HIGH": 0,       # Count routed to HIGH
    "MID": 0,        # Count routed to MID
    "LOW": 0         # Count routed to LOW
})
```

#### Algorithm
```python
for each prediction:
    label = teacher_label
    label_stats[label]["scores"].append(score)
    
    if score >= 0.8:
        label_stats[label]["HIGH"] += 1
    elif score >= 0.5:
        label_stats[label]["MID"] += 1
    else:
        label_stats[label]["LOW"] += 1

# Compute per-label statistics
for label in sorted(label_stats.keys()):
    scores = label_stats[label]["scores"]
    avg_confidence = sum(scores) / len(scores)
    high_pct = label_stats[label]["HIGH"] / len(scores) * 100
    # ... same for MID and LOW
```

**Complexity**: O(N + M log M) where M = unique labels (for sorting)

---

### Task 3: Ground Truth Validation (Filtering)

**Core Idea**: Count HIGH confidence samples that have GT available.

#### Algorithm
```python
gt_cnt = 0           # Total samples with GT
hc_w_gt_cnt = 0      # HIGH confidence samples with GT

for each prediction:
    if gt_available:
        gt_cnt += 1
        if score >= 0.8:
            hc_w_gt_cnt += 1

# Compute accuracy (assume all correct for simplicity)
if hc_w_gt_cnt > 0:
    accuracy = hc_w_gt_cnt / gt_cnt * 100
```

**Note**: In real scenarios, you'd compare `teacher_label` with actual GT labels. This problem assumes all HIGH confidence predictions with GT are correct.

**Complexity**: O(N) (done in same loop as Task 1)

---

## Key Takeaways

### Confidence-based Routing Pattern
This is a **fundamental ML pipeline pattern**:
1. **Automatic acceptance** for high-confidence predictions (saves labeling cost)
2. **Human-in-the-loop** for mid-confidence (quality control)
3. **Discard** low-confidence (noise reduction)

**Real-world usage**:
- Waabi's auto-labeling pipeline
- Active learning systems
- Weak supervision frameworks

### DefaultDict with Lambda
```python
label_stats = defaultdict(lambda: {"scores": [], "HIGH": 0, "MID": 0, "LOW": 0})
```

**Alternative without lambda**:
```python
def default_stats():
    return {"scores": [], "HIGH": 0, "MID": 0, "LOW": 0}

label_stats = defaultdict(default_stats)
```

**Or manual check**:
```python
if label not in label_stats:
    label_stats[label] = {"scores": [], "HIGH": 0, "MID": 0, "LOW": 0}
```

### String to Boolean Conversion
```python
gt_available = parts[3] == "True"  # Explicit comparison
```

**Common mistake**:
```python
if parts[3]:  # WRONG! "False" string is truthy
```

---

## Common Pitfalls

### Task 1
- ❌ Forgetting to convert `score` to float: `float(parts[1])`
- ❌ Wrong percentage calculation: Should be `count/total*100`, not `count*100/total`
- ❌ Missing leading spaces in output: `"  - Auto-accept"` (2 spaces)

### Task 2
- ❌ Not sorting labels alphabetically: `sorted(label_stats.keys())`
- ❌ Trying to unpack dict items incorrectly: Use `label, stats = item`, not `label, s, h, m, l`
- ❌ Division by zero: If a label has 0 samples (shouldn't happen in valid input)

### Task 3
- ❌ String comparison: `parts[3] == "True"`, not `parts[3]`
- ❌ Wrong accuracy calculation: Should be `hc_w_gt_cnt / gt_cnt`, not `hc_w_gt_cnt / hc_w_gt_cnt`

---

## Real-World Applications

This problem directly mirrors:

### 1. Teacher-Student Pseudo-labeling (Your Qualcomm Work)
```
Teacher model → Confidence scores → Routing:
- HIGH: Auto-add to training set
- MID: Vendor QA review
- LOW: Discard

Result: 70% reduction in manual labeling
```

### 2. Active Learning
Select samples for human annotation based on model uncertainty (mid-confidence = high uncertainty).

### 3. Data Quality Control
Track per-class confidence distribution to identify:
- Classes with consistently low confidence → need more training data
- Classes with high confidence but low GT accuracy → model bias

---

## Complexity Summary

| Task | Time | Space |
|------|------|-------|
| Task 1 | O(N) | O(N) |
| Task 2 | O(N + M log M) | O(N) |
| Task 3 | O(N) | O(1) |
| **Overall** | **O(N + M log M)** | **O(N)** |

Where N = number of predictions, M = unique labels (typically M << N).

---

## Interview Tips

### If asked "How would you optimize this?"
- Current solution is already optimal (single pass, O(N))
- Only optimization: If labels are pre-sorted in input, skip sorting (but unlikely)

### If asked "How would you handle streaming data?"
- Replace lists with rolling statistics (running mean instead of storing all scores)
- Use approximate percentiles (e.g., t-digest) instead of exact percentages

### If asked "How would you scale this to millions of samples?"
- Distribute by label (each worker handles subset of labels)
- Use MapReduce: Map = routing, Reduce = aggregation
- Store intermediate results in database instead of memory

---

## Relation to Your Resume

**Direct mapping to Qualcomm work**:
- **Confidence-based routing** → Your pseudo-label pipeline's core logic
- **Per-label statistics** → Your slice-based evaluation (per-scenario metrics)
- **GT validation** → Your QA verification process

**Interview talking points**:
- "I implemented exactly this pattern at Qualcomm for 3D hand pose pseudo-labels"
- "We routed mid-confidence samples to vendor QA, reducing manual labeling by 70%"
- "Per-label stats helped identify which scenarios (low-light, motion blur) needed more data"
