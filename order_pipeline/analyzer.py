
class Analyzer:
    """Analyzes transformed order data for summaries and insights."""

    def __init__(self, data):
        self.data = data  # cleaned orders from Transformer

    def total_orders(self):
        """Returns the number of orders."""
        return len(self.data)

    def total_sales(self):
        """Calculates total revenue from all orders."""
        total = 0.0
        for order in self.data:
            total += order.get("total", 0)
        return round(total, 2)

    def average_order_value(self):
        """Finds the average total value per order."""
        num_orders = len(self.data)
        if num_orders == 0:
            return 0.0
        return round(self.total_sales() / num_orders, 2)

    def payment_status_summary(self):
        """Counts how many orders are paid, pending, or refunded."""
        summary = {"paid": 0, "pending": 0, "refunded": 0}

        for order in self.data:
            status = str(order.get("payment_status", "")).lower()
            if status in summary:
                summary[status] += 1

        return summary

    def compute_summary(self):
        """Gathers all key stats into one summary dictionary."""
        return {
            "total_orders": self.total_orders(),
            "total_sales": self.total_sales(),
            "average_order_value": self.average_order_value(),
            "payment_summary": self.payment_status_summary()
        }

    def print_report(self):
        """Prints a summary report of all metrics."""
        print("\n--- SALES ANALYSIS REPORT ---")
        print(f"Total Orders: {self.total_orders()}")
        print(f"Total Sales: ${self.total_sales()}")
        print(f"Average Order Value: ${self.average_order_value()}")
        print("Payment Summary:", self.payment_status_summary())

