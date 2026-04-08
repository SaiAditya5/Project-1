from typing import Dict, List
from playwright.sync_api import sync_playwright


class TestExecutor:

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url

    # ---------------------------
    # RUN FULL SUITE
    # ---------------------------
    def run_test_suite(self, suite: Dict) -> List[Dict]:
        results = []

        with sync_playwright() as p:
            request_context = p.request.new_context()

            for test_case in suite["test_cases"]:
                result = self._execute_test(
                    request_context,
                    suite["endpoint"],
                    test_case
                )
                results.append(result)

        return results

    # ---------------------------
    # EXECUTE SINGLE TEST
    # ---------------------------
    def _execute_test(self, request_context, endpoint: str, test_case: Dict) -> Dict:
        try:
            method, path = endpoint.split(" ", 1)

            url = self._build_url(path)
            payload = self._build_payload(test_case)

            print(f"[EXEC] {method} {url} | Test: {test_case['test_id']}")

            response = self._send_request(
                request_context,
                method,
                url,
                payload
            )

            is_valid = self._validate_response(response)

            return {
                "test_id": test_case["test_id"],
                "status": "PASS" if is_valid else "FAIL",
                "status_code": response.status
            }

        except Exception as e:
            return {
                "test_id": test_case["test_id"],
                "status": "ERROR",
                "error": str(e)
            }

    # ---------------------------
    # BUILD URL
    # ---------------------------
    def _build_url(self, path: str) -> str:
        if "{id}" in path:
            path = path.replace("{id}", "1")

        return self.base_url + path

    # ---------------------------
    # BUILD PAYLOAD
    # ---------------------------
    def _build_payload(self, test_case: Dict) -> Dict:
        if "invalid" in test_case["title"].lower():
            return {"invalid_field": None}

        return {
            "name": "test_user",
            "email": "test@example.com"
        }

    # ---------------------------
    # SEND REQUEST
    # ---------------------------
    def _send_request(self, request_context, method: str, url: str, payload: Dict):
        method = method.upper()

        if method == "GET":
            return request_context.get(url)

        elif method == "POST":
            return request_context.post(url, data=payload)

        elif method == "PUT":
            return request_context.put(url, data=payload)

        elif method == "DELETE":
            return request_context.delete(url)

        else:
            raise Exception(f"Unsupported method: {method}")

    # ---------------------------
    # VALIDATION (CLEAN VERSION)
    # ---------------------------
    def _validate_response(self, response) -> bool:
        try:
            # Status check
            if response.status not in [200, 201, 204]:
                return False

            # Try parsing JSON
            try:
                body = response.json()
            except Exception:
                return True  # Non-JSON but OK status

            # Validate structure
            if isinstance(body, dict):
                return True

            elif isinstance(body, list):
                return len(body) > 0

            return True

        except Exception as e:
            print(f"[VALIDATION ERROR] {str(e)}")
            return False