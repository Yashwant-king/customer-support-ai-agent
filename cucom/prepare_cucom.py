import json
from pathlib import Path


BASE_DIR = Path(__file__).parent

INPUT_FILE = BASE_DIR / "merged.jsonl"
OUTPUT_FILE = BASE_DIR / "support_eval.jsonl"


def normalize_role(role: str) -> str:
    role = role.strip().lower()

    if role == "user":
        return "user"

    if role == "agent":
        return "assistant"

    raise ValueError(f"Unknown role: {role}")


def main():

    conversations = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            conversation = json.loads(line)

            turns = []

            for turn in conversation["turns"]:

                turns.append({
                    "role": normalize_role(turn["role"]),
                    "content": turn["content"].strip()
                })

            conversations.append({
                "id": conversation["id"],
                "turns": turns
            })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for conversation in conversations:

            file.write(
                json.dumps(
                    conversation,
                    ensure_ascii=False
                ) + "\n"
            )

    print(f"Input conversations: {len(conversations):,}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()