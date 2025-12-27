# Phillies Pitch-Level Data Engineering Assessment

## Overview

This project implements a Python-based data pipeline to ingest, clean, validate, enrich, and aggregate high-frequency pitch tracking data from a baseball game. The goal is to transform nested JSON pitch data into an analytics-ready dataset and compute batter-level performance metrics using SQL.

The pipeline is designed to be defensive against missing or malformed data, easy to run and reproduce, and suitable for downstream analytics and research workflows.

---

## GitHub Repository

The complete source code for this project is available on GitHub:

🔗 **[https://github.com/HarshaRNVSS/philadelphia-phillies-data-engineering](https://github.com/HarshaRNVSS/philadelphia-phillies-data-engineering)**

## Project Structure

```text
PhiladelphiaPhilliesProject/
│
├── data/
│   ├── batch_raw.json              # Raw pitch tracking input
│   ├── processed_pitches.parquet   # Cleaned, pitch-level dataset
│   └── batter_summary.csv          # Batter-level aggregated metrics
│
├── src/
│   ├── __init__.py
│   ├── transform.py                # Data cleaning & feature engineering
│   ├── main.py                     # Pipeline entry point
│   └── aggregate.py                # SQL aggregation using DuckDB
│
├── tests/
│   └── test_transform.py           # Unit test for transformation logic
│
├── requirements.txt
├── README.md
└── venv/
```
---
## Environment Setup
This project uses a Python virtual environment.

### Step 1: Create a virtual environment
``` text
python3 -m venv venv
```
### Step 2: Activate the virtual environment
``` text
source venv/bin/activate
```
You should see (venv) in your terminal prompt.
### Step 3: Install dependencies
``` text
python -m pip install -r requirements.txt
```
---
## Running the pipeline
All commands should be run from the project root directory with the virtual environment activated.

### Step 1: Transform raw pitch data
``` text
python src/main.py
```
This step:
	•	Loads data/batch_raw.json
	•	Flattens nested JSON so each row represents one pitch
	•	Validates and cleans key fields
	•	Enriches the dataset with derived features
	•	Writes the processed output to:
``` text
data/processed_pitches.parquet
```
### Step 2: Aggregate batter-level metrics
```text
python src/aggregate.py
```
This step:
	•	Loads the processed pitch-level dataset
	•	Uses DuckDB (in-memory SQL engine) for aggregation
	•	Produces one row per batter
	•	Writes results to:
```text
data/batter_summary.csv
```
Metrics computed:
	•	Swing count
	•	Whiff rate (percentage of swings with no contact)
	•	Maximum exit velocity (mph)
---
## Running Unit Tests
A basic unit test is included to validate core transformation logic.
From the project root, run:
```text
pytest
```
Expected output:
```text
1 passed
```
---
## Key Assumptions & Design Choices
	•	One JSON object represents one pitch
	•	Missing events or personId values are allowed; batter_id is set to null
	•	A swing is defined by the presence of non-empty samples_bat
	•	Contact is defined as a swing with a valid exit velocity
	•	Exit velocity values are validated using realistic baseball constraints (0–125 mph)
	•	Rows are not dropped due to missing data; invalid values are safely nulled
	•	DuckDB is used for SQL aggregation to keep analytics logic simple and transparent

Rows with missing batter_id are grouped under NULL during aggregation, reflecting incomplete tracking data rather than data loss.
---
## Technologies Used
	•	Python 3
	•	pandas
	•	DuckDB
	•	PyArrow (Parquet)
	•	pytest
---
## Outputs
	•	processed_pitches.parquet — clean, pitch-level dataset suitable for analytics
	•	batter_summary.csv — batter-level performance summary

