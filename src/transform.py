from typing import Dict, Any, Optional
def extract_batter_id(events):
    """
    Extract batter MLB ID from events array.
    Returns None if missing.
    """
    if not events:
        return None

    person = events[0].get("personId")

    if isinstance(person, dict):
        return person.get("mlbId")

    return person

def extract_exit_velocity(record: Dict[str, Any]) -> Optional[float]:
    """
    Extract exit velocity (mph) from nested hit summary.
    Returns None if no contact occurred.
    """
    return (
        record.get("summary_acts", {})
              .get("hit", {})
              .get("speed", {})
              .get("mph")
    )


def validate_exit_velocity(exit_velocity: Optional[float]) -> Optional[float]:
    """
    Validate exit velocity using realistic baseball constraints.
    Acceptable range: 0–125 mph.
    """
    if exit_velocity is None:
        return None

    if 0 <= exit_velocity <= 125:
        return exit_velocity

    # Invalid values are nulled instead of dropping the row
    return None


def is_swing_detected(record: Dict[str, Any]) -> bool:
    """
    Determine whether a swing occurred based on bat tracking data.
    A swing is defined by the presence of non-empty samples_bat.
    """
    samples_bat = record.get("samples_bat")
    return samples_bat is not None and len(samples_bat) > 0


def flatten_pitch(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten a raw pitch JSON object into a single-row dictionary
    suitable for tabular storage and downstream analytics.
    """

    # Batter ID
    batter_id = extract_batter_id(record.get("events", []))

    # Exit velocity
    raw_exit_velocity = extract_exit_velocity(record)
    exit_velocity = validate_exit_velocity(raw_exit_velocity)

    # Swing detection
    is_swing = is_swing_detected(record)

    # Enriched feature: contact indicator
    is_contact = is_swing and exit_velocity is not None

    # Optional contextual fields (safe to include)
    raw_pitch_type = (
        record.get("summary_acts", {})
              .get("pitch", {})
              .get("type")
    )
    pitch_type = raw_pitch_type if isinstance(raw_pitch_type,str) else None
    raw_pitch_result = (
        record.get("summary_acts", {})
              .get("pitch", {})
              .get("result")
    )
    pitch_result = raw_pitch_result if isinstance(raw_pitch_result, str) else None
    return {
        "batter_id": batter_id,
        "pitch_type": pitch_type,
        "pitch_result": pitch_result,
        "exit_velocity": exit_velocity,
        "is_swing": is_swing,
        "is_contact": is_contact,
    }
