import os
import duckdb
import pandas as pd


def run_aggregation():
    # Paths
    input_path = os.path.join("data", "processed_pitches.parquet")
    output_path = os.path.join("data", "batter_summary.csv")

    # Load processed data
    df = pd.read_parquet(input_path)
    print(f"Loaded {len(df)} processed pitch records")

    # Initialize DuckDB
    con = duckdb.connect()
    con.register("pitches", df)

    # SQL aggregation query
    query = """
    SELECT
        batter_id,
        COUNT(*) FILTER (WHERE is_swing) AS swing_count,
        AVG(
            CASE
                WHEN is_swing AND NOT is_contact THEN 1
                ELSE 0
            END
        ) AS whiff_rate,
        MAX(exit_velocity) AS max_exit_velocity
    FROM pitches
    GROUP BY batter_id
    ORDER BY batter_id
    """

    # Execute query
    result_df = con.execute(query).df()

    # Output results
    print("Batter-level summary:")
    print(result_df)

    result_df.to_csv(output_path, index=False)
    print(f"Aggregation results written to {output_path}")


if __name__ == "__main__":
    run_aggregation()
