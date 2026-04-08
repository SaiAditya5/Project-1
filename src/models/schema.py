from typing import List, Dict


class TestCase:
    def __init__(self, test_id: str, title: str, category: str, steps: List[str], expected: str):
        self.test_id = test_id
        self.title = title
        self.category = category
        self.steps = steps
        self.expected = expected

    def to_dict(self) -> Dict:
        return {
            "test_id": self.test_id,
            "title": self.title,
            "category": self.category,
            "steps": self.steps,
            "expected": self.expected
        }


class TestSuite:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.test_cases: List[TestCase] = []

    def add_test_case(self, test_case: TestCase):
        self.test_cases.append(test_case)

    def to_dict(self):
        return {
            "endpoint": self.endpoint,
            "total_tests": len(self.test_cases),
            "test_cases": [tc.to_dict() for tc in self.test_cases]
        }