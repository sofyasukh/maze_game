import json
import os

def load_records():
    if not os.path.exists("records.json"):
        return {}
    with open("records.json", "r") as f:
        return json.load(f)

def save_record(level, time):
    records = load_records()
    records[level] = min(records.get(level, float('inf')), time)
    with open("records.json", "w") as f:
        json.dump(records, f)