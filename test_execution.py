import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.services.orchestrator import TestOrchestrator
from src.core.test_executor import TestExecutor

# Step 1: Generate tests
orchestrator = TestOrchestrator("data/sample_swagger.json")
suites = orchestrator.run()

# Step 2: Execute tests
executor = TestExecutor()

for suite in suites:
    print(f"\nRunning tests for {suite['endpoint']}")

    results = executor.run_test_suite(suite)

    for r in results:
        print(r)