# OA Early Detection System

## Project Overview

OA Early Detection System is an academic prototype designed to screen and analyze the risk of Osteoarthritis (OA) using patient information, questionnaire responses, and gait parameters.

## Main Features

* Patient Registration
* OA Questionnaire
* Gait Assessment
* OA Risk Assessment
* Patient Report
* Patient Search
* Patient Delete
* CSV Report Download
* Dashboard with Risk Analysis
* Gait Analysis Charts

## Technologies Used

* Python
* Streamlit
* Pandas
* SQLite
* HTML / CSS
* Browser Speech Synthesis

## Gait Parameters

The system analyzes:

* Walking Speed
* Stride Length
* Cadence
* Step Count
* Gait Variability

## Risk Assessment

The prototype considers:

* Age
* BMI
* Pain Level
* Questionnaire Score
* Gait Score

## Important Note

This is an academic/demo prototype for early screening and educational purposes. The calculated risk score and gait classification are not a medical diagnosis and should not replace evaluation by a qualified healthcare professional.

## Project Structure

```text
OA_Early_Detection/
├── app.py
├── app_backup.py
├── oa_data.db
├── data/
│   └── sample_data.csv
├── model/
│   ├── __init__.py
│   ├── risk_engine.py
│   └── data/
│       └── utils/
│           └── database.py
└── utils/
    ├── __init__.py
    └── calculations.py
```
