import json
from datetime import datetime
from typing import List


def save_as_json(data: List, file_path: str = None):
    file_path = file_path or f"outputs/test_cases_{_timestamp()}.json"
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def save_as_readable(data: List, file_path: str = None):
    file_path = file_path or f"outputs/test_cases_{_timestamp()}.txt"

    with open(file_path, "w") as f:
        for suite in data:
            f.write(f"\n=== {suite['endpoint']} ===\n")

            for tc in suite["test_cases"]:
                f.write(f"\n[{tc['test_id']}] {tc['title']}\n")
                f.write(f"Category: {tc['category']}\n")
                f.write(f"Expected: {tc['expected']}\n")


def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
