import json
import os

class Reader:
    """Reads order data from a JSON file."""

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        if not self.filepath.endswith(".json"):
            raise ValueError("Unsupported file format. Expected a .json file.")

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        with open(self.filepath, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format.")

        if not data or not isinstance(data, list):
            raise ValueError("JSON file must contain a list of records.")

        return data
