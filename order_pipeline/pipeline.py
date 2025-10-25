# pipeline.py

from .reader import Reader
from .validator import Validator
from .transformer import Transformer
from .analyzer import Analyzer
from .exporter import Exporter


class OrderPipeline:
    """Runs the full ShopLink data processing pipeline."""

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        """Executes the data pipeline step by step."""

        print(" Reading data...")
        reader = Reader(self.input_file)
        orders = reader.read()

        print(f"   Loaded {len(orders)} records.\n")

        print("Validating data...")
        validator = Validator(orders)
        validator.validate()
        valid_orders = validator.valid_rows
        invalid_orders = validator.invalid_rows

        print(f"   Valid rows: {len(valid_orders)} | Invalid rows: {len(invalid_orders)}\n")

        print(" Transforming data...")
        transformer = Transformer(valid_orders)
        cleaned_orders = transformer.transform()
        print(f"    Cleaned {len(cleaned_orders)} records.\n")

        print(" Analyzing data...")
        analyzer = Analyzer(cleaned_orders)
        summary = analyzer.compute_summary()

        print("   Summary of results:")
        print(summary, "\n")

        print(" Exporting results...")
        exporter = Exporter(cleaned_orders, self.output_file)
        exporter.export()
        print(f"   Results exported to {self.output_file}\n")

        print(" Pipeline completed successfully!")


if __name__ == "__main__":
    # Example file paths (adjust if needed)
    pipeline = OrderPipeline("shoplink.json", "shoplink_cleaned.json")
    pipeline.run()
