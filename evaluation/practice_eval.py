import json
from langsmith import Client
from dotenv import load_dotenv

load_dotenv()
client = Client()

DATASET_NAME = "huraeee"

# Reuse the dataset if it exists, otherwise create it
if client.has_dataset(dataset_name=DATASET_NAME):
    dataset = client.read_dataset(dataset_name=DATASET_NAME)
else:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for customer support LangGraph agent",
    )

examples = []
with open("evaluation/eval_dataset.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        examples.append({
            "inputs": {"query": record["query"]},
            "outputs": {
                "expected_risk": record["expected_risk"],
                "expected_functions": record.get("expected_functions", []),
            },
            "metadata": {"id": record["id"]},
        })

client.create_examples(dataset_id=dataset.id, examples=examples)

print("Dataset:", dataset.name)
print("Dataset ID:", dataset.id)
print("Total examples:", len(examples))