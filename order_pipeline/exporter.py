import json

# exporter.py
import csv

class Exporter:
    """Exports cleaned data and summary results to a CSV file."""

    def __init__(self, data, output_file):
        self.data = data
        self.output_file = output_file

    def export(self):
        """Writes the cleaned orders to a CSV file."""
        if not self.data:
            print("No data to export.")
            return

        fieldnames = self.data[0].keys()

        with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

        print(f"✅ Exported {len(self.data)} records to {self.output_file}")

