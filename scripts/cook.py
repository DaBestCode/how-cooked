#!/usr/bin/env python3
"""Calculate a playful workload-pressure score from Canvas-style task data."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


LEVELS = (
    (20, "refrigerated"),
    (40, "lightly toasted"),
    (60, "air-fried"),
    (80, "well done"),
    (99, "charcoal"),
    (100, "academically cremated"),
)


def parse_time(value: str) -> datetime:
    """Parse an ISO 8601 timestamp, including the common trailing Z form."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def urgency_points(hours_until_due: float, window_hours: float = 72) -> int:
    if hours_until_due < 0:
        return 25
    if hours_until_due <= 12:
        return 20
    if hours_until_due <= 24:
        return 15
    if hours_until_due <= 48:
        return 10
    if hours_until_due <= 72:
        return 5
    if hours_until_due <= window_hours:
        return 2
    return 0


def calculate(data: dict[str, Any]) -> dict[str, Any]:
    now = parse_time(data["now"])
    window_hours = float(data.get("window_hours", 72))
    available_minutes = max(0, int(data.get("available_minutes", 0)))
    scored_tasks: list[dict[str, Any]] = []

    for raw_task in data.get("tasks", []):
        if raw_task.get("submitted", False):
            continue

        due = parse_time(raw_task["due"])
        hours_until_due = (due - now).total_seconds() / 3600
        if hours_until_due > window_hours:
            continue

        points = urgency_points(hours_until_due, window_hours)
        kind = str(raw_task.get("kind", "assignment")).lower()
        major_bonus = 5 if kind in {"exam", "project"} else 0
        scored_tasks.append(
            {
                "name": raw_task["name"],
                "course": raw_task.get("course", "Unknown course"),
                "due": raw_task["due"],
                "hours_until_due": round(hours_until_due, 1),
                "points": points + major_bonus,
            }
        )

    raw_points = sum(task["points"] for task in scored_tasks)
    availability_relief = min(20, (available_minutes // 60) * 5)
    score = max(0, min(100, raw_points - availability_relief))
    level = next(label for ceiling, label in LEVELS if score <= ceiling)

    biggest_threat = None
    if scored_tasks:
        threat = sorted(
            scored_tasks,
            key=lambda task: (-task["points"], task["hours_until_due"]),
        )[0]
        biggest_threat = {
            "name": threat["name"],
            "course": threat["course"],
            "due": threat["due"],
        }

    return {
        "score": score,
        "level": level,
        "biggest_threat": biggest_threat,
        "open_tasks_in_window": len(scored_tasks),
        "available_minutes": available_minutes,
        "calculation": {
            "deadline_points": raw_points,
            "availability_relief": availability_relief,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Workload JSON file")
    args = parser.parse_args()

    with args.input.open(encoding="utf-8") as source:
        data = json.load(source)
    print(json.dumps(calculate(data), indent=2))


if __name__ == "__main__":
    main()

