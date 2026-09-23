
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from model.risk_engine import calculate_risk
from utils.calculations import calculate_gait_score, classify_gait

from model.data.utils.database import (
    create_database,
    save_patient,
    get_all_patients,
    get_patient,
    delete_patient
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="OA Early Detection System",
    page_icon="🦴",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "logged_in": False,
    "page": "Dashboard",
    "patient_data": {},
    "questionnaire_score": 0,
    "gait_score": 0,
    "gait_class": "",
    "voice_language": "English",
    "last_page_voice": ""
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# LANGUAGE
# =========================================================

LANGUAGE_CODES = {
    "English": "en-US",
    "Tamil": "ta-IN",
    "Hindi": "hi-IN"
}


# =========================================================
# VOICE TEXT
# =========================================================

VOICE_TEXT = {

    "welcome": {
        "English": "Welcome to the Osteoarthritis Early Detection System.",
        "Tamil": "ஆஸ்டியோ ஆர்த்ரைடிஸ் ஆரம்ப கண்டறிதல் அமைப்பிற்கு வரவேற்கிறோம்.",
        "Hindi": "ऑस्टियोआर्थराइटिस अर्ली डिटेक्शन सिस्टम में आपका स्वागत है."
    },

    "dashboard": {
        "English": "This is the dashboard. Here you can view patient and gait analysis information.",
        "Tamil": "இது டாஷ்போர்டு. இங்கே நோயாளி மற்றும் நடை பகுப்பாய்வு தகவல்களை பார்க்கலாம்.",
        "Hindi": "यह डैशबोर्ड है। यहां मरीज और गैट विश्लेषण की जानकारी देख सकते हैं."
    },

    "registration": {
        "English": "Enter the patient details in the registration section.",
        "Tamil": "பதிவு பகுதியில் நோயாளியின் விவரங்களை உள்ளிடவும்.",
        "Hindi": "पंजीकरण अनुभाग में मरीज की जानकारी दर्ज करें."
    },

    "questionnaire": {
        "English": "Complete the osteoarthritis questionnaire.",
        "Tamil": "ஆஸ்டியோ ஆர்த்ரைடிஸ் கேள்வித்தாளை முடிக்கவும்.",
        "Hindi": "ऑस्टियोआर्थराइटिस प्रश्नावली पूरी करें."
    },

    "gait": {
        "English": "Enter the gait assessment parameters.",
        "Tamil": "நடை மதிப்பீட்டு அளவுருக்களை உள்ளிடவும்.",
        "Hindi": "गैट असेसमेंट पैरामीटर दर्ज करें."
    },

    "risk": {
        "English": "Complete the risk assessment.",
        "Tamil": "ஆபத்து மதிப்பீட்டை முடிக்கவும்.",
        "Hindi": "जोखिम मूल्यांकन पूरा करें."
    },

    "report": {
        "English": "View patient reports and risk information.",
        "Tamil": "நோயாளி அறிக்கைகள் மற்றும் ஆபத்து தகவல்களை பார்க்கவும்.",
        "Hindi": "मरीज की रिपोर्ट और जोखिम की जानकारी देखें."
    },

    "patient_saved": {
        "English": "Patient details saved successfully.",
        "Tamil": "நோயாளியின் விவரங்கள் வெற்றிகரமாக சேமிக்கப்பட்டன.",
        "Hindi": "मरीज की जानकारी सफलतापूर्वक सेव हो गई."
    },

    "questionnaire_saved": {
        "English": "Questionnaire saved successfully.",
        "Tamil": "கேள்வித்தாள் வெற்றிகரமாக சேமிக்கப்பட்டது.",
        "Hindi": "प्रश्नावली सफलतापूर्वक सेव हो गई."
    },

    "gait_completed": {
        "English": "Gait assessment completed successfully.",
        "Tamil": "நடை மதிப்பீடு வெற்றிகரமாக முடிந்தது.",
        "Hindi": "गैट असेसमेंट सफलतापूर्वक पूरा हुआ."
    },

    "risk_completed": {
        "English": "Risk assessment completed successfully.",
        "Tamil": "ஆபத்து மதிப்பீடு வெற்றிகரமாக முடிந்தது.",
        "Hindi": "जोखिम मूल्यांकन सफलतापूर्वक पूरा हुआ."
    },

    "patient_deleted": {
        "English": "Patient deleted successfully.",
        "Tamil": "நோயாளி வெற்றிகரமாக நீக்கப்பட்டார்.",
        "Hindi": "मरीज सफलतापूर्वक डिलीट हो गया."
    }
}


# =========================================================
# AUTOMATIC VOICE
# =========================================================

def automatic_voice(text, language):

    language_code = LANGUAGE_CODES.get(
        language,
        "en-US"
    )

    safe_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
    )

    html_code = f"""
    <script>

        setTimeout(function() {{

            if ("speechSynthesis" in window) {{

                window.speechSynthesis.cancel();

                const message =
                    new SpeechSynthesisUtterance(
                        `{safe_text}`
                    );

                message.lang = "{language_code}";
                message.rate = 0.90;
                message.pitch = 1.0;
                message.volume = 1.0;

                window.speechSynthesis.speak(
                    message
                );
            }}

        }}, 300);

    </script>
    """

    components.html(
        html_code,
        height=0
    )


# =========================================================
# PAGE VOICE
# =========================================================

def page_voice(page, language):

    voice_map = {

        "Dashboard": "dashboard",

        "Patient Registration": "registration",

        "OA Questionnaire": "questionnaire",

        "Gait Assessment": "gait",

        "Risk Assessment": "risk",

        "Patient Report": "report"
    }

    key = voice_map.get(page)

    if key is None:
        return

    voice_id = f"{page}_{language}"

    if st.session_state.last_page_voice != voice_id:

        automatic_voice(
            VOICE_TEXT[key][language],
            language
        )

        st.session_state.last_page_voice = voice_id


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.title(
        "🦴 OA Early Detection System"
    )

    st.write(
        "Osteoarthritis Risk Screening & Gait Analysis"
    )

    automatic_voice(
        VOICE_TEXT["welcome"][
            st.session_state.voice_language
        ],
        st.session_state.voice_language
    )

    st.subheader(
        "🔐 Login"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    language = st.selectbox(
        "🌐 Voice Language",
        [
            "English",
            "Tamil",
            "Hindi"
        ]
    )

    st.session_state.voice_language = language

    if st.button(
        "Login",
        use_container_width=True
    ):

        if (
            username == "admin"
            and password == "admin123"
        ):

            st.session_state.logged_in = True
            st.session_state.page = "Dashboard"
            st.session_state.last_page_voice = ""

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

            automatic_voice(
                "Invalid username or password.",
                language
            )

    st.info(
        "Demo Login: admin / admin123"
    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "🦴 OA Detection"
)

st.sidebar.caption(
    "Patient Screening System"
)


# =========================================================
# LANGUAGE SELECTOR
# =========================================================

language = st.sidebar.selectbox(
    "🌐 Voice Language",
    [
        "English",
        "Tamil",
        "Hindi"
    ],
    index=[
        "English",
        "Tamil",
        "Hindi"
    ].index(
        st.session_state.voice_language
    )
)

if language != st.session_state.voice_language:

    st.session_state.voice_language = language

    st.session_state.last_page_voice = ""

    st.rerun()


# =========================================================
# NAVIGATION
# =========================================================

pages = [

    "Dashboard",

    "Patient Registration",

    "OA Questionnaire",

    "Gait Assessment",

    "Risk Assessment",

    "Patient Report"
]


selected_page = st.sidebar.radio(
    "📌 Main Menu",
    pages,
    index=pages.index(
        st.session_state.page
    )
)


if selected_page != st.session_state.page:

    st.session_state.page = selected_page

    st.session_state.last_page_voice = ""

    st.rerun()


# =========================================================
# LOGOUT
# =========================================================

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.session_state.last_page_voice = ""

    st.rerun()


# =========================================================
# PAGE VOICE
# =========================================================

page_voice(
    st.session_state.page,
    st.session_state.voice_language
)


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.title(
        "🦴 Osteoarthritis Early Detection & Gait Analysis"
    )

    st.write(
        "AI-assisted prototype for early osteoarthritis "
        "risk screening using patient, questionnaire "
        "and gait parameters."
    )

    st.divider()

    patients = get_all_patients()

    total_patients = len(
        patients
    )

    high_risk = 0
    moderate_risk = 0
    low_risk = 0

    for patient in patients:

        risk_level = patient[8]

        if risk_level == "High Risk":

            high_risk += 1

        elif risk_level == "Moderate Risk":

            moderate_risk += 1

        elif risk_level == "Low Risk":

            low_risk += 1


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Total Patients",
        total_patients
    )

    col2.metric(
        "🔴 High Risk",
        high_risk
    )

    col3.metric(
        "🟠 Moderate Risk",
        moderate_risk
    )

    col4.metric(
        "🟢 Low Risk",
        low_risk
    )


    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    st.subheader(
        "📈 Risk Distribution"
    )

    risk_data = pd.DataFrame({

        "Risk Level": [

            "High Risk",

            "Moderate Risk",

            "Low Risk"
        ],

        "Patients": [

            high_risk,

            moderate_risk,

            low_risk
        ]
    })

    st.bar_chart(
        risk_data.set_index(
            "Risk Level"
        )
    )


    # =====================================================
    # PATIENT RISK SCORE
    # =====================================================

    if patients:

        risk_chart_data = pd.DataFrame(

            patients,

            columns=[

                "patient_id",

                "name",

                "age",

                "gender",

                "bmi",

                "occupation",

                "location",

                "risk_score",

                "risk_level",

                "date_time"
            ]
        )

        st.subheader(
            "📊 Patient Risk Scores"
        )

        st.bar_chart(

            risk_chart_data.set_index(
                "patient_id"
            )["risk_score"]
        )


    # =====================================================
    # SEARCH PATIENT
    # =====================================================

    st.subheader(
        "🔎 Search Patient"
    )

    search_text = st.text_input(
        "Search by Patient ID or Name"
    )

    if patients:

        search_df = pd.DataFrame(

            patients,

            columns=[

                "patient_id",

                "name",

                "age",

                "gender",

                "bmi",

                "occupation",

                "location",

                "risk_score",

                "risk_level",

                "date_time"
            ]
        )

        if search_text:

            search_lower = (
                search_text.lower()
            )

            filtered_df = search_df[

                search_df[
                    "patient_id"
                ]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )

                |

                search_df[
                    "name"
                ]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )
            ]

        else:

            filtered_df = search_df


        st.dataframe(

            filtered_df,

            use_container_width=True
        )

    else:

        st.info(
            "No patients registered yet."
        )


    # =====================================================
    # GAIT ANALYSIS DASHBOARD
    # =====================================================

    st.divider()

    st.header(
        "🚶 Gait Analysis Dashboard"
    )

    st.write(
        "Gait parameters from the sample dataset."
    )

    try:

        csv_path = (
            "data/sample_data.csv"
        )

        gait_df = pd.read_csv(
            csv_path
        )


        required_columns = [

            "patient_id",

            "walking_speed",

            "stride_length",

            "cadence",

            "step_count",

            "gait_variability"
        ]


        missing_columns = [

            column

            for column in required_columns

            if column not in gait_df.columns
        ]


        if missing_columns:

            st.error(

                "Missing columns in "
                "sample_data.csv: "

                + ", ".join(
                    missing_columns
                )
            )

        else:

            # ---------------------------------------------
            # GAIT SCORE
            # ---------------------------------------------

            gait_df[
                "gait_score"
            ] = gait_df.apply(

                lambda row:
                calculate_gait_score(

                    row[
                        "walking_speed"
                    ],

                    row[
                        "stride_length"
                    ],

                    row[
                        "cadence"
                    ],

                    row[
                        "step_count"
                    ],

                    row[
                        "gait_variability"
                    ]
                ),

                axis=1
            )


            # ---------------------------------------------
            # GAIT CLASSIFICATION
            # ---------------------------------------------

            gait_df[
                "gait_class"
            ] = gait_df[
                "gait_score"
            ].apply(
                classify_gait
            )


            # ---------------------------------------------
            # GAIT METRICS
            # ---------------------------------------------

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(

                "Average Walking Speed",

                f"{gait_df['walking_speed'].mean():.2f} m/s"
            )

            col2.metric(

                "Average Stride Length",

                f"{gait_df['stride_length'].mean():.2f} m"
            )

            col3.metric(

                "Average Cadence",

                f"{gait_df['cadence'].mean():.0f}"
            )

            col4.metric(

                "Average Gait Score",

                f"{gait_df['gait_score'].mean():.1f}"
            )


            # ---------------------------------------------
            # GAIT SCORE CHART
            # ---------------------------------------------

            st.subheader(
                "📊 Gait Score"
            )

            gait_score_chart = gait_df[

                [
                    "patient_id",

                    "gait_score"
                ]

            ].set_index(
                "patient_id"
            )

            st.bar_chart(
                gait_score_chart
            )


            # ---------------------------------------------
            # WALKING SPEED
            # ---------------------------------------------

            st.subheader(
                "🚶 Walking Speed"
            )

            walking_speed_chart = gait_df[

                [
                    "patient_id",

                    "walking_speed"
                ]

            ].set_index(
                "patient_id"
            )

            st.line_chart(
                walking_speed_chart
            )


            # ---------------------------------------------
            # STRIDE LENGTH
            # ---------------------------------------------

            st.subheader(
                "📏 Stride Length"
            )

            stride_chart = gait_df[

                [
                    "patient_id",

                    "stride_length"
                ]

            ].set_index(
                "patient_id"
            )

            st.line_chart(
                stride_chart
            )


            # ---------------------------------------------
            # CADENCE
            # ---------------------------------------------

            st.subheader(
                "👣 Cadence"
            )

            cadence_chart = gait_df[

                [
                    "patient_id",

                    "cadence"
                ]

            ].set_index(
                "patient_id"
            )

            st.line_chart(
                cadence_chart
            )


            # ---------------------------------------------
            # GAIT VARIABILITY
            # ---------------------------------------------

            st.subheader(
                "📉 Gait Variability"
            )

            variability_chart = gait_df[

                [
                    "patient_id",

                    "gait_variability"
                ]

            ].set_index(
                "patient_id"
            )

            st.line_chart(
                variability_chart
            )


            # ---------------------------------------------
            # GAIT CLASSIFICATION
            # ---------------------------------------------

            st.subheader(
                "🧠 Gait Classification"
            )

            gait_class_count = (

                gait_df[
                    "gait_class"
                ]
                .value_counts()
            )

            st.bar_chart(
                gait_class_count
            )


            # ---------------------------------------------
            # GAIT DATA TABLE
            # ---------------------------------------------

            st.subheader(
                "📋 Gait Analysis Data"
            )

            gait_display = gait_df[

                [
                    "patient_id",

                    "walking_speed",

                    "stride_length",

                    "cadence",

                    "step_count",

                    "gait_variability",

                    "gait_score",

                    "gait_class"
                ]
            ]

            st.dataframe(

                gait_display,

                use_container_width=True
            )


    except FileNotFoundError:

        st.warning(
            "sample_data.csv not found."
        )


    except Exception as e:

        st.error(

            "Unable to load gait analysis data: "

            + str(e)
        )


# =========================================================
# PATIENT REGISTRATION
# =========================================================

elif st.session_state.page == "Patient Registration":

    st.title(
        "📝 Patient Registration"
    )

    st.write(
        "Enter the patient details below."
    )

    col1, col2 = st.columns(2)


    with col1:

        patient_id = st.text_input(
            "Patient ID"
        )

        name = st.text_input(
            "Patient Name"
        )

        age = st.number_input(

            "Age",

            min_value=1,

            max_value=120,

            value=30
        )

        gender = st.selectbox(

            "Gender",

            [
                "Male",
                "Female",
                "Other"
            ]
        )

        height_cm = st.number_input(

            "Height (cm)",

            min_value=50.0,

            max_value=250.0,

            value=170.0
        )

        weight_kg = st.number_input(

            "Weight (kg)",

            min_value=10.0,

            max_value=300.0,

            value=70.0
        )


    with col2:

        occupation = st.text_input(
            "Occupation"
        )

        location = st.text_input(
            "Location"
        )

        height_m = (
            height_cm / 100
        )

        bmi = (
            weight_kg /
            (height_m * height_m)
        )

        st.metric(

            "Calculated BMI",

            f"{bmi:.2f}"
        )


    if st.button(

        "💾 Save Patient Details",

        use_container_width=True
    ):

        if not patient_id.strip():

            st.error(
                "Please enter the patient ID."
            )

        elif not name.strip():

            st.error(
                "Please enter the patient name."
            )

        else:

            st.session_state.patient_data = {

                "patient_id":
                    patient_id,

                "name":
                    name,

                "age":
                    age,

                "gender":
                    gender,

                "height_cm":
                    height_cm,

                "weight_kg":
                    weight_kg,

                "bmi":
                    round(
                        bmi,
                        2
                    ),

                "occupation":
                    occupation,

                "location":
                    location
            }

            st.success(

                "Patient details saved temporarily."
            )

            automatic_voice(

                VOICE_TEXT[
                    "patient_saved"
                ][
                    st.session_state.voice_language
                ],

                st.session_state.voice_language
            )


# =========================================================
# OA QUESTIONNAIRE
# =========================================================

elif st.session_state.page == "OA Questionnaire":

    st.title(
        "📋 OA Questionnaire"
    )

    st.write(
        "Answer the following questions."
    )


    q1 = st.slider(

        "1. Difficulty while walking?",

        0,

        5,

        0
    )


    q2 = st.slider(

        "2. Difficulty climbing stairs?",

        0,

        5,

        0
    )


    q3 = st.slider(

        "3. Difficulty standing for a long time?",

        0,

        5,

        0
    )


    q4 = st.slider(

        "4. Knee stiffness?",

        0,

        5,

        0
    )


    q5 = st.slider(

        "5. Difficulty performing daily activities?",

        0,

        5,

        0
    )


    questionnaire_score = (

        q1
        + q2
        + q3
        + q4
        + q5
    )


    st.metric(

        "Questionnaire Score",

        questionnaire_score
    )


    if st.button(

        "💾 Save Questionnaire",

        use_container_width=True
    ):

        st.session_state.questionnaire_score = (

            questionnaire_score
        )

        st.success(

            "Questionnaire saved successfully."
        )

        automatic_voice(

            VOICE_TEXT[
                "questionnaire_saved"
            ][
                st.session_state.voice_language
            ],

            st.session_state.voice_language
        )


# =========================================================
# GAIT ASSESSMENT
# =========================================================

elif st.session_state.page == "Gait Assessment":

    st.title(
        "🚶 Gait Assessment"
    )

    st.write(
        "Enter gait parameters."
    )


    col1, col2 = st.columns(2)


    with col1:

        walking_speed = st.number_input(

            "Walking Speed (m/s)",

            min_value=0.0,

            max_value=5.0,

            value=1.0,

            step=0.05
        )


        stride_length = st.number_input(

            "Stride Length (m)",

            min_value=0.0,

            max_value=3.0,

            value=1.1,

            step=0.05
        )


        cadence = st.number_input(

            "Cadence (steps/min)",

            min_value=0,

            max_value=200,

            value=100
        )


    with col2:

        step_count = st.number_input(

            "Step Count",

            min_value=0,

            max_value=500,

            value=100
        )


        gait_variability = st.number_input(

            "Gait Variability",

            min_value=0.0,

            max_value=100.0,

            value=10.0
        )


    if st.button(

        "🔍 Calculate Gait Score",

        use_container_width=True
    ):

        score = calculate_gait_score(

            walking_speed,

            stride_length,

            cadence,

            step_count,

            gait_variability
        )


        gait_class = classify_gait(
            score
        )


        st.session_state.gait_score = score

        st.session_state.gait_class = gait_class


        st.success(

            "Gait assessment completed successfully."
        )


        col1, col2 = st.columns(2)


        col1.metric(

            "Gait Score",

            score
        )


        col2.metric(

            "Gait Classification",

            gait_class
        )


        automatic_voice(

            VOICE_TEXT[
                "gait_completed"
            ][
                st.session_state.voice_language
            ],

            st.session_state.voice_language
        )


# =========================================================
# RISK ASSESSMENT
# =========================================================

elif st.session_state.page == "Risk Assessment":

    st.title(
        "⚠️ OA Risk Assessment"
    )


    if not st.session_state.patient_data:

        st.warning(
            "Please register a patient first."
        )

    else:

        patient = (
            st.session_state.patient_data
        )


        st.subheader(
            "Patient Information"
        )


        col1, col2, col3 = st.columns(3)


        col1.write(

            f"**Patient ID:** "
            f"{patient['patient_id']}"
        )


        col2.write(

            f"**Name:** "
            f"{patient['name']}"
        )


        col3.write(

            f"**Age:** "
            f"{patient['age']}"
        )


        pain_level = st.slider(

            "Pain Level",

            0,

            10,

            0
        )


        questionnaire_score = (

            st.session_state.questionnaire_score
        )


        gait_score = (

            st.session_state.gait_score
        )


        st.write(

            f"Questionnaire Score: "
            f"**{questionnaire_score}**"
        )


        st.write(

            f"Gait Score: "
            f"**{gait_score}**"
        )


        if st.button(

            "⚠️ Calculate Risk",

            use_container_width=True
        ):


            result = calculate_risk(

                patient["age"],

                patient["bmi"],

                pain_level,

                questionnaire_score,

                gait_score
            )


            risk_score = result["score"]

            risk_level = result["level"]


            st.subheader(
                "Risk Result"
            )


            col1, col2 = st.columns(2)


            col1.metric(

                "Risk Score",

                risk_score
            )


            col2.metric(

                "Risk Level",

                risk_level
            )


            patient_to_save = {

                "patient_id":
                    patient["patient_id"],

                "name":
                    patient["name"],

                "age":
                    patient["age"],

                "gender":
                    patient["gender"],

                "bmi":
                    patient["bmi"],

                "occupation":
                    patient["occupation"],

                "location":
                    patient["location"],

                "risk_score":
                    risk_score,

                "risk_level":
                    risk_level
            }


            save_patient(
                patient_to_save
            )


            st.success(

                "Risk assessment saved successfully."
            )


            automatic_voice(

                VOICE_TEXT[
                    "risk_completed"
                ][
                    st.session_state.voice_language
                ],

                st.session_state.voice_language
            )


# =========================================================
# PATIENT REPORT
# =========================================================

elif st.session_state.page == "Patient Report":

    st.title(
        "📄 Patient Report"
    )


    patients = get_all_patients()


    if not patients:

        st.info(
            "No patient records available."
        )


    else:

        patient_ids = [

            patient[0]

            for patient in patients
        ]


        selected_id = st.selectbox(

            "Select Patient",

            patient_ids
        )


        patient = get_patient(
            selected_id
        )


        if patient:

            st.subheader(
                "Patient Information"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Patient ID:** {patient[0]}"
                )

                st.write(
                    f"**Name:** {patient[1]}"
                )

                st.write(
                    f"**Age:** {patient[2]}"
                )

                st.write(
                    f"**Gender:** {patient[3]}"
                )

                st.write(
                    f"**BMI:** {patient[4]}"
                )


            with col2:

                st.write(
                    f"**Occupation:** {patient[5]}"
                )

                st.write(
                    f"**Location:** {patient[6]}"
                )

                st.write(
                    f"**Risk Score:** {patient[7]}"
                )

                st.write(
                    f"**Risk Level:** {patient[8]}"
                )

                st.write(
                    f"**Date & Time:** {patient[9]}"
                )


            st.divider()


            if st.button(

                "🗑️ Delete Patient",

                use_container_width=True
            ):

                delete_patient(
                    selected_id
                )


                st.success(

                    "Patient deleted successfully."
                )


                automatic_voice(

                    VOICE_TEXT[
                        "patient_deleted"
                    ][
                        st.session_state.voice_language
                    ],

                    st.session_state.voice_language
                )


                st.rerun()


            report_data = pd.DataFrame(

                [patient],

                columns=[

                    "patient_id",

                    "name",

                    "age",

                    "gender",

                    "bmi",

                    "occupation",

                    "location",

                    "risk_score",

                    "risk_level",

                    "date_time"
                ]
            )


            csv_data = report_data.to_csv(

                index=False
            )


            st.download_button(

                label="⬇️ Download Patient Report",

                data=csv_data,

                file_name=f"{selected_id}_report.csv",

                mime="text/csv",

                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "🦴 OA Early Detection System | Academic Prototype"
)


st.caption(
    "Risk and gait calculations are for demonstration "
    "purposes and are not a medical diagnosis."
)

