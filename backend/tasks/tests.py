from django.test import TestCase
from datetime import date, timedelta

from .scoring import compute_scores, detect_cycles


class ScoringTests(TestCase):

    def test_urgency_affects_score(self):
        """
        Task with closer due date should have higher score.
        """

        tasks = [
            {
                "id": "1",
                "title": "Task A",
                "due_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "estimated_hours": 5,
                "importance": 5,
                "dependencies": []
            },
            {
                "id": "2",
                "title": "Task B",
                "due_date": (date.today() + timedelta(days=20)).strftime("%Y-%m-%d"),
                "estimated_hours": 5,
                "importance": 5,
                "dependencies": []
            }
        ]

        result = compute_scores(tasks)
        scores = {t["id"]: t["score"] for t in result["tasks"]}

        self.assertGreater(scores["1"], scores["2"])



    def test_effort_quick_wins(self):
        """
        Lower estimated_hours should produce higher score.
        """

        tasks = [
            {
                "id": "1",
                "title": "Quick",
                "due_date": None,
                "estimated_hours": 1,
                "importance": 5,
                "dependencies": []
            },
            {
                "id": "2",
                "title": "Long",
                "due_date": None,
                "estimated_hours": 20,
                "importance": 5,
                "dependencies": []
            }
        ]

        result = compute_scores(tasks)
        scores = {t["id"]: t["score"] for t in result["tasks"]}

        self.assertGreater(scores["1"], scores["2"])



    def test_circular_dependency_detection(self):
        """
        Should detect A -> B -> C -> A cycle.
        """

        tasks = [
            {"id": "1", "title": "A", "due_date": None, "estimated_hours": 3, "importance": 5, "dependencies": ["2"]},
            {"id": "2", "title": "B", "due_date": None, "estimated_hours": 3, "importance": 5, "dependencies": ["3"]},
            {"id": "3", "title": "C", "due_date": None, "estimated_hours": 3, "importance": 5, "dependencies": ["1"]},
        ]

        has_cycle, cycles = detect_cycles(tasks)

        self.assertTrue(has_cycle)
        self.assertTrue(len(cycles) > 0)
