
def calculate_gait_score(
    walking_speed,
    stride_length,
    cadence,
    step_count,
    gait_variability
):
    score = 100

    # Walking speed
    if walking_speed < 0.8:
        score -= 20
    elif walking_speed < 1.0:
        score -= 10

    # Stride length
    if stride_length < 1.0:
        score -= 15
    elif stride_length < 1.1:
        score -= 5

    # Cadence
    if cadence < 90:
        score -= 15
    elif cadence < 100:
        score -= 5

    # Step count
    if step_count < 80:
        score -= 10

    # Gait variability
    if gait_variability > 15:
        score -= 20
    elif gait_variability > 10:
        score -= 10

    return max(0, min(score, 100))


def classify_gait(gait_score):

    if gait_score >= 70:
        return "Normal Gait"

    elif gait_score >= 40:
        return "Moderate Abnormality"

    else:
        return "Abnormal Gait"

