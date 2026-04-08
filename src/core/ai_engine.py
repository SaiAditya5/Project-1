import os
from typing import Dict, List, Any


class AIEngine:
    def __init__(self, model: str = "gpt-4.1"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    # ---------------------------
    # PROMPT BUILDER
    # ---------------------------
    def build_prompt(self, endpoint: Dict[str, Any]) -> str:
        param_text = self._format_parameters(endpoint.get("parameters", []))
        response_text = self._format_responses(endpoint.get("responses", {}))

        prompt = f"""
You are a senior QA automation engineer.

Analyze the API endpoint and generate comprehensive test scenarios.

### Endpoint Details:
- Path: {endpoint['path']}
- Method: {endpoint['method']}
- Summary: {endpoint['summary']}

### Parameters:
{param_text}

### Request Body:
{endpoint.get('request_body', {})}

### Responses:
{response_text}

### Instructions:
Generate structured test cases in the following categories:
1. Positive Scenarios
2. Negative Scenarios
3. Edge Cases
4. Security Tests

Return output in clean bullet points.
"""
        return prompt.strip()

    # ---------------------------
    # FORMAT HELPERS
    # ---------------------------
    def _format_parameters(self, params: List[Dict]) -> str:
        if not params:
            return "No parameters"

        lines = []
        for p in params:
            lines.append(
                f"- {p['name']} ({p['in']} | {p['type']} | required={p['required']})"
            )
        return "\n".join(lines)

    def _format_responses(self, responses: Dict) -> str:
        lines = []
        for code, desc in responses.items():
            lines.append(f"- {code}: {desc}")
        return "\n".join(lines)

    # ---------------------------
    # MAIN GENERATION FUNCTION
    # ---------------------------
    def generate_test_cases(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self.build_prompt(endpoint)

        print("\n[DEBUG] Generated Prompt:\n", prompt[:300], "...")

        # If API key exists → real AI call
        if self.api_key:
            return self._call_openai(prompt)

        # Else → fallback mock (still dynamic)
        return self._mock_response(endpoint)

    # ---------------------------
    # OPENAI CALL (OPTIONAL)
    # ---------------------------
    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a QA expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return {
                "source": "openai",
                "content": response.choices[0].message.content
            }

        except Exception as e:
            return {
                "source": "error",
                "content": str(e)
            }

    # ---------------------------
    # SMART MOCK (IMPORTANT)
    # ---------------------------
    def _mock_response(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        method = endpoint["method"]
        path = endpoint["path"]
        params = endpoint.get("parameters", [])

        return {
            "source": "mock",
            "content": f"""
### Positive Scenarios
- Valid {method} request to {path} returns 200 OK
- All required parameters provided correctly

### Negative Scenarios
- Missing required parameters → 400 Bad Request
- Invalid data types in parameters

### Edge Cases
- Extremely large input values
- Empty payload handling

### Security Tests
- Unauthorized access → 401
- Injection attempts in parameters
"""
        }