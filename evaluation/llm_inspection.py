import json

# Read, one record at a time
with open("evaluation/eval_dataset.jsonl","r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        print(f"Line: {line}")
        if not line:
            continue          # skip blank lines
        record = json.loads(line)
        with open("evaluation/new_new.jsonl","a", encoding="utf-8") as new_file:
            json.dump(record, new_file)
            new_file.write("\n")
            
        # print(record)
        # print(type(record))
        

