import sys
from collections import defaultdict
from typing import Any


def main() -> None:
    # Fast input
    input_data = sys.stdin.read().strip().split("\n")
    n = int(input_data[0])

    frame_group_by_scen: dict[str, list[tuple[int, float, float]]] = defaultdict(list)

    # Parse input and group by scenario
    for i in range(1, n + 1):
        parts = input_data[i].split(",")
        frame_id = int(parts[0])
        scenario = parts[2]
        detected = int(parts[3])
        gt = int(parts[4])
        time_ms = float(parts[5])

        accuracy = detected / gt if gt > 0 else 1.0
        frame_group_by_scen[scenario].append((frame_id, accuracy, time_ms))

    # ============================================================
    # Task 1: Per-Scenario Statistics
    # ============================================================
    print("=== Per-Scenario Statistics ===")
    for scenario in sorted(frame_group_by_scen.keys()):
        frames_data = frame_group_by_scen[scenario]
        count = len(frames_data)

        accuracies = [f[1] for f in frames_data]
        times = [f[2] for f in frames_data]

        avg_accuracy = sum(accuracies) / count
        avg_time = sum(times) / count
        worst_case_time = max(times)

        # P95 calculation
        sorted_times = sorted(times)
        if len(sorted_times) <= 5:
            p95_time = max(sorted_times)
        else:
            p95_index = int(0.95 * len(sorted_times))
            p95_time = sorted_times[p95_index]

        print(
            f"{scenario}: count={count}, avg_time={avg_time:.2f}ms, "
            f"accuracy={avg_accuracy:.2f}, worst_case={worst_case_time:.2f}ms, "
            f"p95={p95_time:.2f}ms"
        )

    # ============================================================
    # Task 2: Anomaly Detection (consecutive frames with time > 25ms)
    # ============================================================
    # Re-parse to maintain frame order
    anomalies: list[dict[str, Any]] = []
    current_frames: list[int] = []
    current_times: list[float] = []
    current_scenarios: list[str] = []
    current_start: int | None = None

    for i in range(1, n + 1):
        parts = input_data[i].split(",")
        frame_id = int(parts[0])
        scenario = parts[2]
        time_ms = float(parts[5])

        if time_ms > 25:
            if current_start is None:
                current_start = frame_id

            current_frames.append(frame_id)
            current_times.append(time_ms)
            current_scenarios.append(scenario)
        else:
            if len(current_frames) >= 3:
                anomalies.append(
                    {
                        "start": current_start,
                        "end": current_frames[-1],
                        "avg_time": sum(current_times) / len(current_times),
                        "scenarios": list(set(current_scenarios)),
                    }
                )

            current_frames = []
            current_times = []
            current_scenarios = []
            current_start = None

    # Check last window
    if len(current_frames) >= 3:
        anomalies.append(
            {
                "start": current_start,
                "end": current_frames[-1],
                "avg_time": sum(current_times) / len(current_times),
                "scenarios": list(set(current_scenarios)),
            }
        )

    print("\n=== Anomalies ===")
    if not anomalies:
        print("None detected")
    else:
        for anomaly in anomalies:
            scenarios_str = ", ".join(sorted(anomaly["scenarios"]))
            print(
                f"Window: frames {anomaly['start']}-{anomaly['end']}, avg_time={anomaly['avg_time']:.2f}ms, scenarios=[{scenarios_str}]"
            )  # noqa: E501

    # ============================================================
    # Task 3: Top-K Hard Cases (lowest accuracy)
    # ============================================================
    K = 3
    cases: list[tuple[float, int, str]] = []

    for scenario, frames_data in frame_group_by_scen.items():
        for frame_id, accuracy, _time_ms in frames_data:
            cases.append((accuracy, frame_id, scenario))

    cases.sort(key=lambda x: x[0])
    top_k = cases[:K] if len(cases) >= K else cases

    print("\n=== Top-3 Hard Cases (lowest accuracy) ===")
    for accuracy, frame_id, scenario in top_k:
        print(f"Frame {frame_id}: accuracy={accuracy:.2f}, scenario={scenario}")


if __name__ == "__main__":
    main()
