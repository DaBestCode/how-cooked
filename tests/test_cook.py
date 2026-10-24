import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "cook.py"
SPEC = importlib.util.spec_from_file_location("cook", MODULE_PATH)
cook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(cook)


class CookScoreTests(unittest.TestCase):
    def test_scores_pressure_and_ignores_submitted_or_late_window_tasks(self):
        result = cook.calculate(
            {
                "now": "2026-10-24T12:00:00-07:00",
                "window_hours": 72,
                "available_minutes": 60,
                "tasks": [
                    {
                        "name": "Overdue lab",
                        "course": "BIO 181",
                        "due": "2026-10-24T10:00:00-07:00",
                        "kind": "assignment",
                    },
                    {
                        "name": "Midterm",
                        "course": "MAT 266",
                        "due": "2026-10-25T00:00:00-07:00",
                        "kind": "exam",
                    },
                    {
                        "name": "Submitted essay",
                        "course": "ENG 102",
                        "due": "2026-10-24T18:00:00-07:00",
                        "submitted": True,
                    },
                    {
                        "name": "Future project",
                        "course": "CSE 310",
                        "due": "2026-10-30T18:00:00-07:00",
                        "kind": "project",
                    },
                ],
            }
        )

        self.assertEqual(result["score"], 45)
        self.assertEqual(result["level"], "air-fried")
        self.assertEqual(result["open_tasks_in_window"], 2)
        self.assertEqual(result["biggest_threat"]["name"], "Overdue lab")

    def test_clamps_score_at_zero(self):
        result = cook.calculate(
            {
                "now": "2026-10-24T12:00:00-07:00",
                "available_minutes": 600,
                "tasks": [],
            }
        )

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["level"], "refrigerated")
        self.assertIsNone(result["biggest_threat"])

    def test_clamps_score_at_one_hundred(self):
        tasks = [
            {
                "name": f"Overdue task {number}",
                "course": "CHAOS 101",
                "due": "2026-10-23T12:00:00-07:00",
            }
            for number in range(5)
        ]
        result = cook.calculate(
            {
                "now": "2026-10-24T12:00:00-07:00",
                "available_minutes": 0,
                "tasks": tasks,
            }
        )

        self.assertEqual(result["score"], 100)
        self.assertEqual(result["level"], "academically cremated")

    def test_weekly_request_counts_work_after_seventy_two_hours(self):
        result = cook.calculate(
            {
                "now": "2026-10-24T12:00:00-07:00",
                "window_hours": 168,
                "available_minutes": 0,
                "tasks": [
                    {
                        "name": "Friday reflection",
                        "course": "ENG 102",
                        "due": "2026-10-29T12:00:00-07:00",
                    }
                ],
            }
        )

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["open_tasks_in_window"], 1)


if __name__ == "__main__":
    unittest.main()

