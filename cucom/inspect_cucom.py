import json
from pathlib import Path
from collections import Counter


FILE_PATH = Path(__file__).parent / "merged.jsonl"


def main():

    conversations = []

    with open(FILE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                conversations.append(json.loads(line))

    print("\n========== CuCom Dataset ==========\n")

    print(f"Total conversations: {len(conversations):,}")

    # -------------------------
    # Roles
    # -------------------------

    roles = Counter()

    for conversation in conversations:
        for turn in conversation.get("turns", []):
            roles[turn.get("role")] += 1

    print("\nRoles:")
    for role, count in roles.items():
        print(f"  {role}: {count:,}")

    # -------------------------
    # Number of turns
    # -------------------------

    turn_counts = [
        len(conversation.get("turns", []))
        for conversation in conversations
    ]

    if turn_counts:
        print("\nTurns per conversation:")
        print(f"  Minimum: {min(turn_counts)}")
        print(f"  Maximum: {max(turn_counts)}")
        print(f"  Average: {sum(turn_counts) / len(turn_counts):.2f}")

    # -------------------------
    # First conversation
    # -------------------------

    print("\nFirst conversation:")

    first = conversations[0]

    print(f"ID: {first.get('id')}")

    for turn in first.get("turns", []):
        print(f"\n{turn.get('role').upper()}:")
        print(turn.get("content"))

    print("\n===================================\n")


if __name__ == "__main__":
    main()