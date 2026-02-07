import streamlit as st
import pandas as pd
import pickle

#======== PAGE CONFIG ========
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="centered"
)

#======== PREMIUM UI CSS ========
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.big-title {
    font-size: 38px;
    font-weight: 600;
    text-align: center;
    color: #ffffff;
}

.subtitle {
    font-size: 18px;
    text-align: center;
    color: #d3d3d3;
}

.card {
    padding: 25px;
    border-radius: 16px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 20px;
}

.result-yes {
    padding: 20px;
    font-size: 26px;
    border-radius: 12px;
    background: #ff4d4d;
    color: white;
    font-weight: 600;
    text-align: center;
}

.result-no {
    padding: 20px;
    font-size: 26px;
    border-radius: 12px;
    background: #4CAF50;
    color: white;
    font-weight: 600;
    text-align: center;
}

.prob-box {
    padding: 20px;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    text-align: center;
    font-size: 20px;
    color: white;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

#======== TITLE ========
st.markdown("<p class='big-title'>🔮 Customer Churn Prediction App</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter customer details and get prediction instantly.</p><br>", unsafe_allow_html=True)

#======== LOAD PIPELINE ========
with open("churn_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

model = pipeline["model"]
scaler = pipeline["scaler"]
feature_cols = pipeline["columns"]

#================ UI INPUT CARD ================
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
    charges = st.number_input("Monthly Charges", 10, 200, 70)
    payment = st.selectbox("Payment Method", [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ])
    
    st.markdown("</div>", unsafe_allow_html=True)

#======== PREDICT FUNCTION ========
def predict(gender, senior, tenure, internet, charges, payment):
    df = pd.DataFrame([{
        "gender": gender,
        "SeniorCitizen": senior,
        "tenure": tenure,
        "InternetService": internet,
        "MonthlyCharges": charges,
        "PaymentMethod": payment
    }])

    df_scaled = scaler.transform(df[feature_cols])
    prob = model.predict_proba(df_scaled)[0][1]
    pred = "Yes" if prob > 0.5 else "No"
    return pred, prob

#========= PREDICTION BUTTON =========
if st.button("💡 Predict Churn", use_container_width=True):
    pred, prob = predict(gender, senior, tenure, internet, charges, payment)

    st.markdown("<br>", unsafe_allow_html=True)

    if pred == "Yes":
        st.markdown(f"<div class='result-yes'>⚠️ Customer Will Churn</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-no'>✔ Customer Will Stay</div>", unsafe_allow_html=True)

    st.markdown(f"<br><div class='prob-box'>Churn Probability: <b>{prob:.2f}</b></div>", unsafe_allow_html=True)
