from src.services.orchestrator import TestOrchestrator
from src.performance.k6_runner import K6Runner

orchestrator = TestOrchestrator("data/sample_swagger.json")
results = orchestrator.run()

endpoints = [suite["endpoint"] for suite in results]

k6 = K6Runner()
output = k6.run_test(endpoints)

print(output)