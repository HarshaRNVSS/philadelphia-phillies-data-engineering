from src.transform import flatten_pitch

def test_missing_events_results_in_null_batter_id():
    record = {
        "events": [],
        "summary_acts": {},
    }
    result = flatten_pitch(record)
    assert result["batter_id"] is None
