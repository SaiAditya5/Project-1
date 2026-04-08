from src.services.orchestrator import TestOrchestrator
from src.utils.formatter import save_as_json, save_as_readable

orchestrator = TestOrchestrator("data/sample_swagger.json")

results = orchestrator.run()

save_as_json(results)
save_as_readable(results)

print("\n✅ Test cases generated and saved!")