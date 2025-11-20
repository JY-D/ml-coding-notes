import sys
from collections import defaultdict
from typing import Any


def main() -> None:
    input_data = sys.stdin.read().strip().split("\n")
    n = int(input_data[0])

    gt_cnt = 0
    hc_w_gt_cnt = 0
    high_conf: list[str] = []
    mid_conf: list[str] = []
    low_conf: list[str] = []

    label_stats: dict[str, dict[str, Any]] = defaultdict(lambda: {"scores": [], "HIGH": 0, "MID": 0, "LOW": 0})

    for i in range(1, n + 1):
        parts = input_data[i].split(",")
        image_id = parts[0]
        score = float(parts[1])
        teacher_label = parts[2]
        gt_available = parts[3] == "True"

        label_stats[teacher_label]["scores"].append(score)

        if score >= 0.8:
            high_conf.append(image_id)
            label_stats[teacher_label]["HIGH"] += 1
        elif score >= 0.5:
            mid_conf.append(image_id)
            label_stats[teacher_label]["MID"] += 1
        else:
            low_conf.append(image_id)
            label_stats[teacher_label]["LOW"] += 1

        if gt_available:
            gt_cnt += 1
            if score >= 0.8:
                hc_w_gt_cnt += 1

    total = n

    # Task 1: Routing Summary
    print("=== Routing Summary ===")
    print(f"HIGH (>= 0.8): {len(high_conf)} images " f"({len(high_conf)/total*100:.1f}%)")
    print(f"  - Auto-accept for training: {high_conf}")
    print(f"MID (0.5 - 0.8): {len(mid_conf)} images " f"({len(mid_conf)/total*100:.1f}%)")
    print(f"  - Send to vendor QA: {mid_conf}")
    print(f"LOW (< 0.5): {len(low_conf)} images ({len(low_conf)/total*100:.1f}%)")
    print(f"  - Discard: {low_conf}")

    # Task 2: Per-Label Statistics
    print("\n=== Per-Label Statistics ===")
    for label in sorted(label_stats.keys()):
        stats = label_stats[label]
        scores: list[float] = stats["scores"]
        cnt = len(scores)
        avg = sum(scores) / cnt
        cnt_h: int = stats["HIGH"]
        cnt_m: int = stats["MID"]
        cnt_l: int = stats["LOW"]
        print(
            f"{label}: count={cnt}, avg_confidence={avg:.2f}, "
            f"HIGH={cnt_h/cnt*100:.1f}%, MID={cnt_m/cnt*100:.1f}%, "
            f"LOW={cnt_l/cnt*100:.1f}%"
        )

    # Task 3: Ground Truth Validation
    print("\n=== Ground Truth Validation ===")
    print(f"HIGH confidence samples with GT: {hc_w_gt_cnt}")
    if hc_w_gt_cnt > 0:
        acc = hc_w_gt_cnt / gt_cnt * 100
        print(f"Accuracy: {acc:.1f}% ({hc_w_gt_cnt}/{gt_cnt} correct)")
    else:
        print("No HIGH confidence samples with GT available")


if __name__ == "__main__":
    main()
