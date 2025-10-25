# validator.py
import json

class Validator:
    """Validates order data for completeness and correctness."""

    def __init__(self, orders):
        # Store incoming data
        self.orders = orders

        # Prepare lists for results
        self.valid_rows = []
        self.invalid_rows = []

    def _is_positive_number(self, value):
        """Checks if value is a positive number."""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    def validate(self):
        """Main validation process. Checks required fields and value correctness."""
        required_fields = ["order_id", "timestamp", "item", "quantity", "price", "payment_status", "total"]

        for order in self.orders:
            # Skip non-dictionary data
            if not isinstance(order, dict):
                self.invalid_rows.append(order)
                continue

            # Check missing required fields
            if not all(field in order and order[field] not in [None, ""] for field in required_fields):
                self.invalid_rows.append(order)
                continue

            # Check numeric fields
            if not self._is_positive_number(order["quantity"]):
                self.invalid_rows.append(order)
                continue

            # Price and total must contain a "$"
            if "$" not in str(order["price"]):
                self.invalid_rows.append(order)
                continue

            if "$" not in str(order["total"]):
                self.invalid_rows.append(order)
                continue

            # Passed all checks 
            self.valid_rows.append(order)


