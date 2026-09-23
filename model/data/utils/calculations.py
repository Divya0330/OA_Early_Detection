
# =========================================================
# GAIT CALCULATIONS
# =========================================================

def calculate_gait_score(
    walking_speed,
    stride_length,
    cadence,
    step_count,
    gait_variability
):
    """
    Calculate a simple gait score from 0 to 100.

    This is a prototype/demo calculation
    and is not a medical diagnosis.
    """

    score = 100

    # Walking Speed
    if walking_speed < 0.8:
        score -= 20
    elif walking_speed < 1.0:
        score -= 10

    # Stride Length
    if stride_length < 1.0:
        score -= 15
    elif stride_length < 1.1:
        score -= 5

    # Cadence
    if cadence < 90:
        score -= 15
    elif cadence < 100:
        score -= 5

    # Step Count
    if step_count < 80:
        score -= 10

    # Gait Variability
    if gait_variability > 15:
        score -= 20
    elif gait_variability > 10:
        score -= 10

    # Keep score between 0 and 100
    score = max(0, min(score, 100))

    return score


# =========================================================
# GAIT CLASSIFICATION
# =========================================================

def classify_gait(gait_score):

    if gait_score >= 70:
        return "Normal Gait"

    elif gait_score >= 40:
        return "Moderate Abnormality"

    else:
        return "Abnormal Gait"
