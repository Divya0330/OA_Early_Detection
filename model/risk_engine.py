
def calculate_risk(age, bmi, pain_level, questionnaire_score, gait_score):
    """
    Calculate a simple OA risk score.
    This is a prototype/demo calculation and not a medical diagnosis.
    """

    risk_score = 0

    # Age
    if age >= 60:
        risk_score += 25
    elif age >= 45:
        risk_score += 15
    else:
        risk_score += 5

    # BMI
    if bmi >= 30:
        risk_score += 20
    elif bmi >= 25:
        risk_score += 10

    # Pain
    risk_score += pain_level * 3

    # Questionnaire
    risk_score += questionnaire_score * 5

    # Gait
    if gait_score < 40:
        risk_score += 15
    elif gait_score < 70:
        risk_score += 8

    # Maximum score
    risk_score = min(risk_score, 100)

    # Risk classification
    if risk_score < 30:
        risk_level = "Low Risk"

    elif risk_score < 60:
        risk_level = "Moderate Risk"

    else:
        risk_level = "High Risk"

    return {
        "score": risk_score,
        "level": risk_level
    }
