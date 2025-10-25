from order_pipeline.validator import Validator

def test_valid_data_passes():
    orders = [
        {
            "order_id": "001",
            "timestamp": "2024-10-20T12:00:00",
            "item": "Laptop",
            "quantity": 2,
            "price": "$1000",
            "payment_status": "Paid",
            "total": "$2000",
        }
    ]

    validator = Validator(orders)
    validator.validate()

    assert len(validator.valid_rows) == 1
    assert len(validator.invalid_rows) == 0

def test_missing_required_fields():
    orders = [
        {
            "order_id": "002",
            "timestamp": "2024-10-20T12:30:00",
            # "item" is missing
            "quantity": 1,
            "price": "$500",
            "payment_status": "Paid",
            "total": "$500",
        }
    ]

    validator = Validator(orders)
    validator.validate()

    assert len(validator.valid_rows) == 0
    assert len(validator.invalid_rows) == 1

def test_invalid_numeric_fields():
    orders = [
        {
            "order_id": "003",
            "timestamp": "2024-10-20T13:00:00",
            "item": "Phone",
            "quantity": "abc",  # not numeric
            "price": "$300",
            "payment_status": "Paid",
            "total": "$300",
        },
        {
            "order_id": "004",
            "timestamp": "2024-10-20T13:30:00",
            "item": "Mouse",
            "quantity": -5,  # negative number
            "price": "$20",
            "payment_status": "Paid",
            "total": "$100",
        },
    ]
    validator = Validator(orders)
    validator.validate()
    assert len(validator.valid_rows) == 0
    assert len(validator.invalid_rows) == 2


def test_missing_currency_symbol():
    orders = [
        {
            "order_id": "005",
            "timestamp": "2024-10-20T14:00:00",
            "item": "Keyboard",
            "quantity": 1,
            "price": "300",  # missing "$"
            "payment_status": "Paid",
            "total": "$300",
        },
        {
            "order_id": "006",
            "timestamp": "2024-10-20T14:30:00",
            "item": "Monitor",
            "quantity": 2,
            "price": "$150",
            "payment_status": "Paid",
            "total": "300",  # missing "$"
        },
    ]
    validator = Validator(orders)
    validator.validate()
    assert len(validator.valid_rows) == 0
    assert len(validator.invalid_rows) == 2


def test_non_dict_input():
    orders = [
        ["not", "a", "dict"],
        "invalid_string",
        123,
        None,
    ]
    validator = Validator(orders)
    validator.validate()
    assert len(validator.valid_rows) == 0
    assert len(validator.invalid_rows) == 4


def test_mixed_valid_and_invalid():
    orders = [
        {
            "order_id": "007",
            "timestamp": "2024-10-20T15:00:00",
            "item": "Tablet",
            "quantity": 1,
            "price": "$200",
            "payment_status": "Paid",
            "total": "$200",
        },
        {
            "order_id": "008",
            "timestamp": "2024-10-20T15:30:00",
            "item": "",
            "quantity": 3,
            "price": "$50",
            "payment_status": "Paid",
            "total": "$150",
        },
    ]
    validator = Validator(orders)
    validator.validate()
    assert len(validator.valid_rows) == 1
    assert len(validator.invalid_rows) == 1