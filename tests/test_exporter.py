import os
import csv
import pytest
from order_pipeline.exporter import Exporter


class TestExporter:
    def setup_method(self):
        """Set up sample data before each test."""
        self.sample_data = [
            {"order_id": "1", "item": "Book", "quantity": 2, "price": 12.5, "total": 25.0},
            {"order_id": "2", "item": "Pen", "quantity": 5, "price": 1.5, "total": 7.5}
        ]
        self.output_file = "test_output.csv"

    def teardown_method(self):
        """Clean up after tests."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_export_creates_csv_file(self):
        """Check if export() creates the CSV file."""
        exporter = Exporter(self.sample_data, self.output_file)
        exporter.export()
        assert os.path.exists(self.output_file)

    def test_export_writes_correct_content(self):
        """Ensure CSV contains the right data."""
        exporter = Exporter(self.sample_data, self.output_file)
        exporter.export()

        with open(self.output_file, newline='', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))

        assert len(reader) == 2
        assert reader[0]["item"] == "Book"
        assert reader[1]["item"] == "Pen"

    def test_export_with_empty_data(self, capsys):
        """Handle empty data with grace
        """
        exporter = Exporter([], self.output_file)
        exporter.export()

        captured = capsys.readouterr()
        assert "No data to export." in captured.out
        assert not os.path.exists(self.output_file)
