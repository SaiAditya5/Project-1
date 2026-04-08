import json
from typing import List, Dict, Any


class SwaggerParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_data = self._load_file()

    def _load_file(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading Swagger file: {str(e)}")

    def extract_endpoints(self) -> List[Dict[str, Any]]:
        paths = self.raw_data.get("paths", {})
        endpoints = []

        for path, methods in paths.items():
            for method, details in methods.items():
                endpoint_data = {
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary", ""),
                    "parameters": self._extract_parameters(details),
                    "request_body": self._extract_request_body(details),
                    "responses": self._extract_responses(details)
                }
                endpoints.append(endpoint_data)

        return endpoints

    def _extract_parameters(self, details: Dict) -> List[Dict]:
        params = details.get("parameters", [])
        extracted = []

        for param in params:
            extracted.append({
                "name": param.get("name"),
                "in": param.get("in"),
                "required": param.get("required", False),
                "type": param.get("schema", {}).get("type", "unknown")
            })

        return extracted

    def _extract_request_body(self, details: Dict) -> Dict:
        body = details.get("requestBody", {})
        content = body.get("content", {})

        return {
            "required": body.get("required", False),
            "content_types": list(content.keys())
        }

    def _extract_responses(self, details: Dict) -> Dict:
        responses = details.get("responses", {})
        return {
            code: resp.get("description", "")
            for code, resp in responses.items()
        }