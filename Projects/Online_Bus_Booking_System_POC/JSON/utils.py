import json
import os

def load_json_file(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=3)
