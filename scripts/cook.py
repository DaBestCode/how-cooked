#!/usr/bin/env python3
"""Calculate playful cooked and aura scores from Canvas-style task data."""

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

AURA_LEVELS = (
    (20, "aura debt"),
    (40, "side-quest energy"),
    (60, "respectable motion"),
    (80, "campus main character"),
    (99, "generational aura"),
    (100, "mythic office-hours lore"),
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


def calculate_aura(data: dict[str, Any]) -> dict[str, Any]:
    """Score visible academic momentum without guessing grades or personality."""
    now = parse_time(data["now"])
    window_hours = float(data.get("window_hours", 168))
    planned_focus_minutes = max(0, int(data.get("planned_focus_minutes", 0)))
    tasks = data.get("tasks", [])

    submitted_ahead = 0
    overdue = 0
    last_minute = 0
    biggest_drain = None

    for task in tasks:
        due = parse_time(task["due"])
        hours_until_due = (due - now).total_seconds() / 3600
        submitted = bool(task.get("submitted", False))

        if 0 <= hours_until_due <= window_hours and submitted:
            submitted_ahead += 1
        elif hours_until_due < 0 and not submitted:
            overdue += 1
            if biggest_drain is None or hours_until_due < biggest_drain["hours_until_due"]:
                biggest_drain = {
                    "name": task["name"],
                    "course": task.get("course", "Unknown course"),
                    "due": task["due"],
                    "hours_until_due": round(hours_until_due, 1),
                }
        elif 0 <= hours_until_due <= 24 and not submitted:
            last_minute += 1
            if biggest_drain is None:
                biggest_drain = {
                    "name": task["name"],
                    "course": task.get("course", "Unknown course"),
                    "due": task["due"],
                    "hours_until_due": round(hours_until_due, 1),
                }

    submitted_bonus = min(20, submitted_ahead * 5)
    focus_bonus = min(20, (planned_focus_minutes // 60) * 5)
    clear_bonus = 10 if overdue == 0 else 0
    overdue_penalty = min(30, overdue * 10)
    last_minute_penalty = min(15, last_minute * 5)
    score = max(
        0,
        min(
            100,
            50
            + submitted_bonus
            + focus_bonus
            + clear_bonus
            - overdue_penalty
            - last_minute_penalty,
        ),
    )
    level = next(label for ceiling, label in AURA_LEVELS if score <= ceiling)

    return {
        "score": score,
        "level": level,
        "biggest_drain": biggest_drain,
        "signals": {
            "submitted_ahead": submitted_ahead,
            "planned_focus_minutes": planned_focus_minutes,
            "overdue": overdue,
            "due_within_24_hours": last_minute,
        },
        "calculation": {
            "starting_score": 50,
            "submitted_ahead_bonus": submitted_bonus,
            "planned_focus_bonus": focus_bonus,
            "no_overdue_bonus": clear_bonus,
            "overdue_penalty": overdue_penalty,
            "last_minute_penalty": last_minute_penalty,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Workload JSON file")
    parser.add_argument(
        "--mode",
        choices=("cooked", "aura"),
        default="cooked",
        help="Score to calculate (default: cooked)",
    )
    args = parser.parse_args()

    with args.input.open(encoding="utf-8") as source:
        data = json.load(source)
    calculator = calculate_aura if args.mode == "aura" else calculate
    print(json.dumps(calculator(data), indent=2))


if __name__ == "__main__":
    main()

