import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

#======== PAGE CONFIG ========
st.set_page_config(
    page_title="Telecom Churn Intelligence Platform",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

#======== PREMIUM DESIGN SYSTEM ========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
    --bg-dark: #0f172a;
    --bg-card: rgba(30,41,59,0.5);
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --border-color: rgba(148,163,184,0.1);
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

#MainMenu, header, footer {visibility: hidden;}

/* Hero */
.hero-section {text-align: center; padding: 2rem 0 3rem 0;}
.hero-title {
    font-size: 3.5rem; font-weight: 700;
    background: linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-subtitle {font-size: 1.2rem; color: var(--text-secondary);}

/* Cards */
.glass-card {
    background: var(--bg-card); backdrop-filter: blur(18px);
    padding: 1.7rem; border-radius: 20px;
    border: 1px solid var(--border-color);
    margin-bottom: 1.5rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border-radius: 12px; border: none; color: white;
    padding: 0.75rem 1.5rem; font-size: 1.1rem;
    width: 100%;
}

/* Result Cards */
.result-card-high-risk {
    background: rgba(239,68,68,0.15);
    border: 2px solid var(--danger-color);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-card-medium-risk {
    background: rgba(245,158,11,0.15);
    border: 2px solid var(--warning-color);
    border-radius: 20px; padding: 2rem; text-align: center;
}
.result-card-low-risk {
    background: rgba(16,185,129,0.15);
    border: 2px solid var(--success-color);
    border-radius: 20px; padding: 2rem; text-align: center;
}

.probability-display {
    font-size: 3rem; font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
}
.section-header {font-size: 1.8rem; margin-bottom: 1rem; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

#======== HERO ========
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📡 Telecom Churn Intelligence</div>
    <div class="hero-subtitle">Advanced ML-powered customer retention analytics</div>
</div>
""", unsafe_allow_html=True)


#======== LOAD MODEL ========
@st.cache_resource
def load_model():
    with open("churn_pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)
    return pipeline["model"], pipeline["scaler"], pipeline["columns"]

model, scaler, feature_cols = load_model()


#======== FIX: CLEAN ENCODING FUNCTION ========
def prepare_input_for_model(raw_df, feature_cols):
    # Convert categorical vars to encoded dummy columns
    df_encoded = pd.get_dummies(raw_df)

    # Add missing columns (very important)
    for col in feature_cols:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    # Ensure correct order
    df_encoded = df_encoded[feature_cols]

    return df_encoded


#======== SIDEBAR ========
with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.radio("Prediction Mode", ["🎯 Single Customer", "📊 Batch Analysis"])
    st.markdown("---")
    st.subheader("📊 Model Info")
    st.metric("Accuracy", "~80%")
    st.markdown("---")
    st.info("Uses ML to predict churn based on customer behavior.")
    
#======== MAIN ========
if mode == "🎯 Single Customer":

    st.markdown("<div class='section-header'>Customer Information</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Has Partner", ["Yes", "No"])
        dependents = st.selectbox("Has Dependents", ["Yes", "No"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])

        if internet != "No":
            online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        else:
            online_security = online_backup = device_protection = tech_support = streaming_tv = streaming_movies = "No internet service"
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ])
        charges = st.number_input("Monthly Charges ($)", 10.0, 200.0, 70.0)
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, float(charges * tenure))
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🔮 Predict Churn", use_container_width=True):

        raw = pd.DataFrame([{
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": charges,
            "TotalCharges": total_charges
        }])

        try:
            df_encoded = prepare_input_for_model(raw, feature_cols)
            df_scaled = scaler.transform(df_encoded)
            churn_prob = model.predict_proba(df_scaled)[0][1]

            if churn_prob >= 0.7:
                box = "result-card-high-risk"
                label = "HIGH RISK"
            elif churn_prob >= 0.4:
                box = "result-card-medium-risk"
                label = "MEDIUM RISK"
            else:
                box = "result-card-low-risk"
                label = "LOW RISK"

            st.markdown(f"""
            <div class='{box}'>
                <div class='result-title'>{label}</div>
                <div class='probability-display'>{churn_prob:.1%}</div>
                <div style="color:#cbd5e1">Churn Probability</div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


else:
    st.markdown("<div class='section-header'>Batch Prediction</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV", type="csv")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.success(f"Loaded {len(df)} customers")

        if st.button("Analyze Batch", use_container_width=True):

            try:
                df_encoded = prepare_input_for_model(df, feature_cols)
                df_scaled = scaler.transform(df_encoded)
                preds = model.predict_proba(df_scaled)[:, 1]

                df["Churn_Probability"] = preds
                df["Risk_Level"] = pd.cut(preds,
                                          bins=[0, 0.4, 0.7, 1.0],
                                          labels=["LOW", "MEDIUM", "HIGH"])

                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
