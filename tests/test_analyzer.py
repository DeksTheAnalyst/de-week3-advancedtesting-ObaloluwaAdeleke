# tests/test_analyzer.py
import pytest
from order_pipeline.analyzer import Analyzer

@pytest.fixture
def sample_orders():
    return [
        {"total": 50.0, "payment_status": "paid"},
        {"total": 100.0, "payment_status": "pending"},
        {"total": 25.5, "payment_status": "paid"},
        {"total": 75.0, "payment_status": "refunded"},
    ]

def test_total_orders(sample_orders):
    analyzer = Analyzer(sample_orders)
    assert analyzer.total_orders() == 4

def test_total_sales(sample_orders):
    analyzer = Analyzer(sample_orders)
    assert analyzer.total_sales() == 250.5  # 50 + 100 + 25.5 + 75

def test_average_order_value(sample_orders):
    analyzer = Analyzer(sample_orders)
    expected_avg = round(250.5 / 4, 2)
    assert analyzer.average_order_value() == expected_avg

def test_average_order_value_empty():
    analyzer = Analyzer([])
    assert analyzer.average_order_value() == 0.0

def test_payment_status_summary(sample_orders):
    analyzer = Analyzer(sample_orders)
    result = analyzer.payment_status_summary()
    assert result == {"paid": 2, "pending": 1, "refunded": 1}

def test_compute_summary(sample_orders):
    analyzer = Analyzer(sample_orders)
    summary = analyzer.compute_summary()
    assert summary["total_orders"] == 4
    assert summary["total_sales"] == 250.5
    assert summary["average_order_value"] == 62.62
    assert summary["payment_summary"]["paid"] == 2

def test_print_report_output(sample_orders, capsys):
    analyzer = Analyzer(sample_orders)
    analyzer.print_report()
    captured = capsys.readouterr()
    assert "SALES ANALYSIS REPORT" in captured.out
    assert "Total Orders: 4" in captured.out
