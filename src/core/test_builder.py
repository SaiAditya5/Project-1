import uuid
from typing import Dict
from src.models.schema import TestCase, TestSuite


class TestBuilder:

    def build_suite(self, endpoint: Dict, ai_output: str) -> TestSuite:
        suite = TestSuite(endpoint=f"{endpoint['method']} {endpoint['path']}")

        sections = self._split_sections(ai_output)

        for category, lines in sections.items():
            for line in lines:
                test_case = self._create_test_case(category, line)
                suite.add_test_case(test_case)

        return suite

    # ---------------------------
    # SPLIT AI OUTPUT INTO SECTIONS
    # ---------------------------
    def _split_sections(self, text: str) -> Dict:
        sections = {
            "positive": [],
            "negative": [],
            "edge": [],
            "security": []
        }

        current_section = None

        for line in text.split("\n"):
            line = line.strip()

            if "Positive" in line:
                current_section = "positive"
            elif "Negative" in line:
                current_section = "negative"
            elif "Edge" in line:
                current_section = "edge"
            elif "Security" in line:
                current_section = "security"
            elif line.startswith("-") and current_section:
                sections[current_section].append(line.replace("-", "").strip())

        return sections

    # ---------------------------
    # CREATE TEST CASE OBJECT
    # ---------------------------
    def _create_test_case(self, category: str, description: str) -> TestCase:
        test_id = f"TC-{uuid.uuid4().hex[:8].upper()}"

        return TestCase(
            test_id=test_id,
            title=description,
            category=category,
            steps=[
                "Prepare request data",
                "Send API request",
                "Capture response"
            ],
            expected="Validate response based on scenario"
        )