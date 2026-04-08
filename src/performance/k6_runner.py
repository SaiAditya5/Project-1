import subprocess
import tempfile


class K6Runner:

    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url

    def generate_script(self, endpoints):
        script = f"""
import http from 'k6/http';
import {{ sleep }} from 'k6';

export default function () {{
"""

        for ep in endpoints:
            method, path = ep.split(" ", 1)
            url = self.base_url + path.replace("{id}", "1")

            if method == "GET":
                script += f'  http.get("{url}");\n'
            elif method == "POST":
                script += f'  http.post("{url}", JSON.stringify({{name: "test"}}));\n'

        script += """
  sleep(1);
}
"""
        return script

    def run_test(self, endpoints):
        script_content = self.generate_script(endpoints)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as f:
            f.write(script_content.encode("utf-8"))
            file_path = f.name

        result = subprocess.run(
            ["C:\\Program Files\\k6\\k6.exe", "run", file_path],
            capture_output=True,
            text=True
        )

        return result.stdout