import os
import json
import pytest
from order_pipeline.pipeline import OrderPipeline

@pytest.fixture
def sample_orders(tmp_path):
    """Create a temporary JSON file with sample data for the full pipeline."""
    sample_data = [
        {"order_id": 1, "timestamp": "2025-10-25", "item": "Book", "quantity": 2, "price": "$10", "payment_status": "paid", "total": "$20"},
        {"order_id": 2, "timestamp": "2025-10-25", "item": "Pen", "quantity": 0, "price": "$1", "payment_status": "pending", "total": "$0"},
        {"order_id": 3, "timestamp": "2025-10-25", "item": "", "quantity": 1, "price": "$5", "payment_status": "paid", "total": "$5"}
    ]
    file_path = tmp_path / "orders.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f)
    return file_path


def test_full_order_pipeline(tmp_path, sample_orders):
    """Integration test for the full pipeline — ensures all steps work together."""
    output_file = tmp_path / "cleaned_orders.csv"

    # Instantiate and run the pipeline
    pipeline = OrderPipeline(input_file=sample_orders, output_file=output_file)
    pipeline.run()

    # Verify output file creation
    assert os.path.exists(output_file), "Output CSV file was not created."

    # Verify that exported CSV is not empty
    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) > 1, "Exported CSV should contain data rows."

    # Quick content sanity check
    header = lines[0].strip().split(",")
    assert "order_id" in header
    assert "total" in header
