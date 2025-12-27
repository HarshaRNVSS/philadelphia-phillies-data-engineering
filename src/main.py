import json
import os
import pandas as pd

from transform import flatten_pitch


def load_raw_json(file_path: str) -> list:
    """
    Load raw JSON data from disk.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def run_pipeline():
    # Paths
    input_path = os.path.join("data", "batch_raw.json")
    output_path = os.path.join("data", "processed_pitches.parquet")

    # Load raw data
    raw_records = load_raw_json(input_path)
    print(f"Loaded {len(raw_records)} raw pitch records")

    # Transform records
    transformed_rows = [flatten_pitch(record) for record in raw_records]
    df = pd.DataFrame(transformed_rows)

    print("Transformation complete")
    print(df.head())

    # Write output
    df.to_parquet(output_path, index=False)
    print(f"Processed dataset written to {output_path}")


if __name__ == "__main__":
    run_pipeline()
