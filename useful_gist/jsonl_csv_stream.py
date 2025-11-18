from collections import Counter, defaultdict
import json
import csv
import gzip
import sys


def stream_jsonl(path: str):
    """Yield one JSON object per line."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            # Each line is a JSON object
            obj = json.loads(line)
            yield obj


def stream_csv(path: str):
    """Yield dict rows from a CSV file."""
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row  # row is a dict: {header: value}


def stream_gzip_jsonl(path: str):
    """Yield JSON objects from a .gz JSONL file."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


for line in sys.stdin:  # e.g., cat data.jsonl | python script.py
    # process line
    pass


def update_metrics(acc, y_true: int, y_pred: int, tags: list[str]):
    """Update per-tag TP/FP/FN counts."""
    for t in tags:
        m = acc[t]
        if y_pred == 1 and y_true == 1:
            m["tp"] += 1
        elif y_pred == 1 and y_true == 0:
            m["fp"] += 1
        elif y_pred == 0 and y_true == 1:
            m["fn"] += 1


def finalize(acc):
    """Compute precision/recall/F1 per tag."""
    out = {}
    for tag, m in acc.items():
        tp, fp, fn = m["tp"], m["fp"], m["fn"]
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        out[tag] = {"precision": prec, "recall": rec, "f1": f1}
    return out


def stream_jsonl_metrics(path: str):
    """Stream a JSONL of {y, yhat, tags: []} and aggregate metrics."""
    from collections import defaultdict

    acc = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # skip malformed line
                continue
            update_metrics(acc, obj["y"], obj["yhat"], obj.get("tags", []))
    return finalize(acc)
