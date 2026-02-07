import streamlit as st
import pandas as pd
import pickle

# Load your model pipeline
with open("churn_pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

model = pipeline["model"]
scaler = pipeline["scaler"]
feature_cols = pipeline["columns"]

# Prediction Function
def predict_churn(data):
    df = pd.DataFrame([data])
    df_encoded = pd.get_dummies(df)

    # Add missing columns
    for col in feature_cols:
        if col not in df_encoded:
            df_encoded[col] = 0

    df_encoded = df_encoded[feature_cols]
    df_scaled = scaler.transform(df_encoded)

    prob = model.predict_proba(df_scaled)[0][1]
    pred = "Yes" if prob >= 0.5 else "No"
    return pred, prob

# ---------------- STREAMLIT UI ----------------
st.title("📦 Customer Churn Prediction App")
st.write("Enter customer details and predict churn:")

gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", [0, 1])
tenure = st.slider("Tenure (months)", 0, 72, 12)
internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
monthly = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=50.0)
payment = st.selectbox("Payment Method", ["Electronic check", "Credit card", "Mailed check"])

if st.button("Predict"):
    pred, prob = predict_churn({
        "gender": gender,
        "SeniorCitizen": senior,
        "tenure": tenure,
        "InternetService": internet,
        "MonthlyCharges": monthly,
        "PaymentMethod": payment,
    })

    st.success(f"Churn: **{pred}**")
    st.info(f"Probability: **{prob:.2f}**")
