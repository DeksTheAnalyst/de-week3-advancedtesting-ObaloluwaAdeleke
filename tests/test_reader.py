# tests/test_reader.py
import json
import pytest
from pathlib import Path
from order_pipeline.reader import Reader


@pytest.fixture
def sample_orders():
    """A small list of example order dictionaries used across tests."""
    return [
        {
            "order_id": "ORD001",
            "timestamp": "2025-10-19T08:00:00Z",
            "item": "Wireless Mouse",
            "quantity": 2,
            "price": "$15.99",
            "total": "$31.98",
            "payment_status": "paid"
        },
        {
            "order_id": "ORD002",
            "timestamp": "2025-10-19 08:05",
            "item": "Laptop Sleeve",
            "quantity": "1",
            "price": "12.50",
            "total": "12.50",
            "payment_status": "PAID"
        },
        {
            "order_id": "ORD003",
            "timestamp": "2025-10-19T08:10:00Z",
            "item": "",
            "quantity": 1,
            "price": "$5.00",
            "total": "$5.00",
            "payment_status": "pending"
        },
    ]


@pytest.fixture
def write_json(tmp_path):
    """Factory fixture: write `obj` to a json file under tmp_path and return filepath str.

    Usage: path = write_json(my_obj, "myfile.json")
    """
    def _write(obj, name="tmp.json"):
        p = tmp_path / name
        p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
        return str(p)
    return _write


def test_reader_reads_valid_json(sample_orders, write_json):
    # Prepare: write sample_orders to a temp json file
    filepath = write_json(sample_orders, name="valid.json")

    # Act: construct Reader with the file path and read data
    reader = Reader(filepath)
    data = reader.read()

    # Assert: we got a list with expected length and first record id
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["order_id"] == "ORD001"


def test_reader_raises_on_wrong_extension(tmp_path):
    # Prepare: create a non-json file (wrong extension)
    p = tmp_path / "data.txt"
    p.write_text("this is not json", encoding="utf-8")

    # Act / Assert: Reader should raise ValueError for unsupported extension
    reader = Reader(str(p))
    with pytest.raises(ValueError):
        reader.read()


def test_reader_raises_on_invalid_json(tmp_path):
    # Prepare: create a file with bad JSON content
    p = tmp_path / "bad.json"
    p.write_text("{ invalid json :::", encoding="utf-8")

    # Act / Assert: reading should raise ValueError for invalid JSON format
    reader = Reader(str(p))
    with pytest.raises(ValueError):
        reader.read()


def test_reader_raises_file_not_found():
    # Act / Assert: passing a path that doesn't exist should raise FileNotFoundError
    reader = Reader("this_file_does_not_exist_hopefully.json")
    with pytest.raises(FileNotFoundError):
        reader.read()
