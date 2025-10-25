ShopLink Shopping System

A simple data processing pipeline for cleaning, validating, analyzing, and exporting e-commerce order data.

Overview

The ShopLink Shopping System automates the end-to-end data workflow for order data:

Reads raw order records (JSON file)

Validates data entries to detect errors or missing fields

Transforms and cleans the valid records

Analyzes trends and summary metrics

Exports the cleaned dataset to a new csv file

All steps are managed by the OrderPipeline class.

Project Structure
de-week3-advancedtesting-ObaloluwaAdeleke/
│
├── order_pipeline/
│   ├── reader.py
│   ├── validator.py
│   ├── transformer.py
│   ├── analyzer.py
│   ├── exporter.py
│   └── pipeline.py
│
├── tests/
│   ├── test_reader.py
│   ├── test_validator.py
│   ├── test_transformer.py
│   ├── test_analyzer.py
│   ├── test_exporter.py
│   └── test_pipeline_integration.py
│
├── shoplink.json          # Sample input file
├── shoplink_cleaned.json  # Output file after running pipeline
├── requirements.txt
└── README.md



Activate your virtual environment

.venv\Scripts\activate


Run the pipeline

python -m order_pipeline.pipeline



Run all unit tests:

pytest


Run with coverage report:

pytest --cov=order_pipeline

Example Output
 Reading data...
   Loaded 50 records.

 Validating data...
   Valid rows: 45 | Invalid rows: 5

 Transforming data...
   Cleaned 45 records.

 Analyzing data...
   Summary of results:
   {'total_orders': 45, 'total_sales': 25000, 'top_category': 'Electronics'}

 Exporting results...
   Results exported to shoplink_cleaned.json

 Pipeline completed successfully!
