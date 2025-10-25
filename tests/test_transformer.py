import pytest
from order_pipeline.transformer import Transformer

def test_to_float_with_numeric_values():
    transformer = Transformer([])
    assert transformer._to_float(5) == 5.0
    assert transformer._to_float(12.3) == 12.3
def test_to_float_with_string_values():
    transformer = Transformer([])
    assert transformer._to_float("$10.50") == 10.5
    assert transformer._to_float("  $1,200  ") == 1200.0
def test_to_float_with_invalid_string():
    transformer = Transformer([])
    assert transformer._to_float("abc") == 0.0
    assert transformer._to_float(None) == 0.0
def test_transform_converts_fields_correctly():
    raw_orders = [
        {
            "quantity": "2",
            "price": "$5.50",
            "total": "$11.00",
            "payment_status": " Paid "
        }
    ]

    transformer = Transformer(raw_orders)
    cleaned = transformer.transform()


    assert len(cleaned) == 1
    order = cleaned[0]

    # Check float conversions
    assert order["quantity"] == 2.0
    assert order["price"] == 5.5
    assert order["total"] == 11.0

    # Payment status should be normalized
    assert order["payment_status"] == "paid"

def test_rename_column_changes_keys():
    orders = [{"item_name": "Laptop"}]
    transformer = Transformer(orders)
    transformer.rename_column("item_name", "item")

    assert "item" in transformer.orders[0]
    assert "item_name" not in transformer.orders[0]
    assert transformer.orders[0]["item"] == "Laptop"
def test_get_data_returns_current_orders(capsys):
    orders = [{"price": "$20", "quantity": "2", "total": "$40", "payment_status": "Paid"}]
    transformer = Transformer(orders)
    transformer.transform()

    # Test get_data
    data = transformer.get_data()
    assert isinstance(data, list)
    assert len(data) == 1

    # Test show_preview (should print first row)
    transformer.show_preview()
    captured = capsys.readouterr()
    assert "--- Showing first" in captured.out
