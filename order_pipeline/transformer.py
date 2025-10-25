# transformer.py
class Transformer:
    """Cleans and converts validated order data."""

    def __init__(self, orders):
        self.orders = orders  # stores the input orders list

    def _to_float(self, value):
        """Converts price or total strings like '$25.50' to float numbers."""
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Remove $ and commas, then trim spaces
            value = value.replace("$", "").replace(",", "").strip()
            try:
                return float(value)
            except ValueError:
                return 0.0
        return 0.0

    def transform(self):
        """Converts numeric fields and normalizes text fields."""
        cleaned_orders = []

        for order in self.orders:
            new_order = dict(order)

            # Convert quantity, price, total to float
            new_order["quantity"] = self._to_float(order.get("quantity", 0))
            new_order["price"] = self._to_float(order.get("price", 0))
            new_order["total"] = self._to_float(order.get("total", 0))

            # Normalize payment status (paid, pending, refunded)
            if "payment_status" in new_order:
                new_order["payment_status"] = new_order["payment_status"].strip().lower()

            # Recalculate total for consistency
            new_order["total"] = round(new_order["quantity"] * new_order["price"], 2)

            cleaned_orders.append(new_order)

        # ✅ Save cleaned version back to self.orders for other methods
        self.orders = cleaned_orders
        return cleaned_orders

    def rename_column(self, old_name, new_name):
        """Renames a column in all rows if it exists."""
        for row in self.orders:
            if old_name in row:
                row[new_name] = row.pop(old_name)

    def show_preview(self, n=5):
        """Prints the first few rows of transformed data."""
        print(f"--- Showing first {n} transformed rows ---")
        for i, row in enumerate(self.orders[:n]):
            print(f"{i+1}. {row}")

    def get_data(self):
        """Returns the transformed dataset."""
        return self.orders
