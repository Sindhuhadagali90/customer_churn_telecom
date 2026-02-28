import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

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
.hero-section {
    text-align: center; 
    padding: 2rem 0 3rem 0;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 3.5rem; 
    font-weight: 700;
    background: linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899);
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.hero-subtitle {
    font-size: 1.2rem; 
    color: var(--text-secondary);
}

/* Cards */
.glass-card {
    background: var(--bg-card); 
    backdrop-filter: blur(18px);
    padding: 1.7rem; 
    border-radius: 20px;
    border: 1px solid var(--border-color);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border-radius: 12px; 
    border: none; 
    color: white;
    padding: 0.75rem 1.5rem; 
    font-size: 1.05rem;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
}

/* Result Cards */
.result-card-high-risk {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(220,38,38,0.1));
    border: 2px solid var(--danger-color);
    border-radius: 20px; 
    padding: 2.5rem; 
    text-align: center;
    animation: pulse-danger 2s ease-in-out infinite;
    margin: 2rem 0;
}

.result-card-medium-risk {
    background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(217,119,6,0.1));
    border: 2px solid var(--warning-color);
    border-radius: 20px; 
    padding: 2.5rem; 
    text-align: center;
    animation: pulse-warning 2s ease-in-out infinite;
    margin: 2rem 0;
}

.result-card-low-risk {
    background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.1));
    border: 2px solid var(--success-color);
    border-radius: 20px; 
    padding: 2.5rem; 
    text-align: center;
    animation: pulse-success 2s ease-in-out infinite;
    margin: 2rem 0;
}

@keyframes pulse-danger {
    0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }
}

@keyframes pulse-warning {
    0%, 100% { box-shadow: 0 0 20px rgba(245, 158, 11, 0.3); }
    50% { box-shadow: 0 0 40px rgba(245, 158, 11, 0.5); }
}

@keyframes pulse-success {
    0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
    50% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.5); }
}

.result-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.result-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.result-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

.probability-display {
    font-size: 3.5rem; 
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    margin: 1rem 0;
}

.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem; 
    margin-bottom: 1.5rem; 
    font-weight: 600;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-header::before {
    content: '';
    width: 4px;
    height: 28px;
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    border-radius: 2px;
}

/* Stat Cards */
.stat-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid var(--border-color);
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
}

/* Risk Factors */
.risk-factor {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background: rgba(30, 41, 59, 0.3);
    border-radius: 12px;
    margin-bottom: 0.75rem;
    border-left: 3px solid var(--primary-color);
}

.risk-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.risk-high { 
    background: rgba(239, 68, 68, 0.2); 
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.risk-medium { 
    background: rgba(245, 158, 11, 0.2); 
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.risk-low { 
    background: rgba(16, 185, 129, 0.2); 
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

/* Alert boxes */
.alert-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    padding: 1rem;
    color: #fca5a5;
    margin: 1rem 0;
}

.alert-info {
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 1rem;
    color: #a5b4fc;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

#======== HERO ========
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📡 Telecom Churn Intelligence</div>
    <div class="hero-subtitle">Advanced ML-powered customer retention analytics platform</div>
</div>
""", unsafe_allow_html=True)


#======== LOAD MODEL ========
@st.cache_resource
def load_model():
    """Load the trained model pipeline with error handling"""
    try:
        # Check if file exists
        if not os.path.exists("churn_pipeline.pkl"):
            st.error("⚠️ Model file 'churn_pipeline.pkl' not found!")
            st.info("Please ensure the model file is in the same directory as this script.")
            st.stop()
        
        with open("churn_pipeline.pkl", "rb") as f:
            pipeline = pickle.load(f)
        
        # Validate pipeline structure
        if not all(key in pipeline for key in ["model", "scaler", "columns"]):
            st.error("⚠️ Invalid model file structure!")
            st.stop()
            
        return pipeline["model"], pipeline["scaler"], pipeline["columns"]
    
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        st.stop()

model, scaler, feature_cols = load_model()


#======== FIXED: PROPER ENCODING FUNCTION ========
def prepare_input_for_model(raw_df, feature_cols):
    """
    Properly encode input data to match training format.
    Handles both numeric and categorical columns correctly.
    """
    try:
        # Make a copy to avoid modifying original
        df = raw_df.copy()
        
        # Identify numeric columns (these should NOT be one-hot encoded)
        numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']
        
        # Separate numeric and categorical columns
        categorical_cols = [col for col in df.columns if col not in numeric_cols]
        
        # One-hot encode only categorical columns
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
        
        # Ensure all expected columns are present
        for col in feature_cols:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        # Ensure correct column order and select only required columns
        df_encoded = df_encoded[feature_cols]
        
        return df_encoded
    
    except Exception as e:
        st.error(f"Error in data preparation: {str(e)}")
        st.write("Debug Info:")
        st.write("Input columns:", raw_df.columns.tolist())
        st.write("Expected columns:", feature_cols[:10], "... (showing first 10)")
        raise e


#======== SIDEBAR ========
with st.sidebar:
    st.markdown('<div style="padding: 1rem;">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Configuration")
    st.markdown("*Control Panel*")
    st.markdown("---")
    
    mode = st.radio(
        "Prediction Mode",
        ["🎯 Single Customer", "📊 Batch Analysis"],
        help="Choose between single customer prediction or batch file upload"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    
    st.markdown("""
    <div style="background:rgba(30,41,59,0.3);padding:1rem;border-radius:12px;margin:0.5rem 0;">
        <div style="font-size:0.9rem;color:#cbd5e1;margin-bottom:0.5rem;">Accuracy</div>
        <div style="font-size:1.8rem;font-weight:700;color:#10b981;">~80%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("This ML platform predicts customer churn probability based on demographic, service, and billing patterns.")
    
    st.markdown("---")
    st.markdown("### 📈 Features")
    st.markdown("""
    <div style="font-size:0.85rem;color:#cbd5e1;line-height:1.8;">
    ✓ Real-time predictions<br>
    ✓ Batch CSV processing<br>
    ✓ Risk level classification<br>
    ✓ Interactive visualizations<br>
    ✓ Export capabilities
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    
#======== MAIN CONTENT ========
if mode == "🎯 Single Customer":

    st.markdown('<div class="section-header">👤 Customer Information</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("**👥 Demographics**")
        gender = st.selectbox("Gender", ["Male", "Female"], help="Customer gender")
        senior = st.selectbox("Senior Citizen", [0, 1], 
                              format_func=lambda x: "Yes" if x == 1 else "No",
                              help="Is the customer a senior citizen?")
        partner = st.selectbox("Has Partner", ["Yes", "No"], help="Does customer have a partner?")
        dependents = st.selectbox("Has Dependents", ["Yes", "No"], help="Does customer have dependents?")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("**📞 Service Details**")
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
            online_security = online_backup = device_protection = "No internet service"
            tech_support = streaming_tv = streaming_movies = "No internet service"
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("**💳 Billing Information**")
        tenure = st.slider("Tenure (months)", 0, 72, 12, help="How long customer has been with company")
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ])
        charges = st.number_input("Monthly Charges ($)", 10.0, 200.0, 70.0, step=5.0)
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 
                                       float(charges * tenure), step=100.0)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_btn = st.button("🔮 Predict Churn Risk", use_container_width=True)

    if predict_btn:
        with st.spinner("🔄 Analyzing customer data..."):
            
            # Create input dataframe
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
                # Encode and scale
                df_encoded = prepare_input_for_model(raw, feature_cols)
                df_scaled = scaler.transform(df_encoded)
                churn_prob = model.predict_proba(df_scaled)[0][1]

                # Determine risk level
                if churn_prob >= 0.7:
                    risk_level = "HIGH"
                    risk_class = "result-card-high-risk"
                    icon = "🚨"
                    message = "Immediate Action Required"
                    color = "#ef4444"
                elif churn_prob >= 0.4:
                    risk_level = "MEDIUM"
                    risk_class = "result-card-medium-risk"
                    icon = "⚠️"
                    message = "Monitor Closely"
                    color = "#f59e0b"
                else:
                    risk_level = "LOW"
                    risk_class = "result-card-low-risk"
                    icon = "✅"
                    message = "Customer Stable"
                    color = "#10b981"

                # Display result
                st.markdown(f"""
                <div class='{risk_class}'>
                    <span class="result-icon">{icon}</span>
                    <div class="result-title">{risk_level} RISK</div>
                    <div class="result-subtitle">{message}</div>
                    <div class="probability-display">{churn_prob:.1%}</div>
                    <div style="color: var(--text-secondary); font-size: 0.95rem;">Churn Probability</div>
                </div>
                """, unsafe_allow_html=True)

                # Risk factors analysis
                st.markdown('<div class="section-header">🎯 Key Risk Factors</div>', unsafe_allow_html=True)
                
                risk_factors = []
                
                if contract == "Month-to-month":
                    risk_factors.append(("Month-to-month contract", "HIGH"))
                if tenure < 12:
                    risk_factors.append(("Short tenure (<12 months)", "HIGH"))
                if payment == "Electronic check":
                    risk_factors.append(("Electronic check payment", "MEDIUM"))
                if internet == "Fiber optic" and charges > 80:
                    risk_factors.append(("High fiber optic charges", "MEDIUM"))
                if online_security == "No":
                    risk_factors.append(("No online security", "MEDIUM"))
                if tech_support == "No":
                    risk_factors.append(("No tech support", "MEDIUM"))
                if senior == 1:
                    risk_factors.append(("Senior citizen", "LOW"))
                
                if not risk_factors:
                    risk_factors.append(("No major risk factors identified", "LOW"))
                
                col_risk1, col_risk2 = st.columns(2)
                
                with col_risk1:
                    for factor, level in risk_factors[:4]:
                        badge_class = f"risk-{level.lower()}"
                        st.markdown(f"""
                        <div class="risk-factor">
                            <span style="color: var(--text-primary);">{factor}</span>
                            <span class="risk-badge {badge_class}">{level}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_risk2:
                    # Customer metrics
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
                        <div class="stat-value">${charges:.0f}</div>
                        <div class="stat-label">Monthly Spend</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📅</div>
                        <div class="stat-value">{tenure} mo</div>
                        <div class="stat-label">Tenure</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Retention recommendations
                if churn_prob >= 0.4:
                    st.markdown('<div class="section-header">💡 Retention Recommendations</div>', unsafe_allow_html=True)
                    
                    recommendations = []
                    
                    if contract == "Month-to-month":
                        recommendations.append(("📋 Contract Upgrade", 
                                              "Offer 15% discount to upgrade to 1-year or 2-year contract"))
                    
                    if tenure < 12:
                        recommendations.append(("🎁 Welcome Package", 
                                              "Provide onboarding support and loyalty rewards for first year"))
                    
                    if online_security == "No" or tech_support == "No":
                        recommendations.append(("🛡️ Service Bundle", 
                                              "Offer free trial of security and support services for 3 months"))
                    
                    if charges > 80:
                        recommendations.append(("💰 Price Optimization", 
                                              "Review pricing plan and offer customized package"))
                    
                    if payment == "Electronic check":
                        recommendations.append(("💳 Payment Method", 
                                              "Incentivize automatic payment methods with $5/month discount"))
                    
                    for emoji_title, text in recommendations[:3]:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(99,102,241,0.05), rgba(139,92,246,0.05));
                             border: 1px solid rgba(99,102,241,0.2); border-radius: 16px; padding: 1.5rem; margin: 1rem 0;">
                            <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); 
                                 margin-bottom: 0.75rem;">{emoji_title}</div>
                            <div style="color: var(--text-secondary); line-height: 1.6;">{text}</div>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                <div class="alert-error">
                    <strong>❌ Prediction Error</strong><br>
                    {str(e)}<br><br>
                    Please check that all fields are filled correctly.
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("🔍 Debug Information"):
                    st.write("Input DataFrame shape:", raw.shape)
                    st.write("Input columns:", raw.columns.tolist())
                    st.write("Expected features:", len(feature_cols))


else:  # Batch Analysis Mode
    st.markdown("<div class='section-header'>📊 Batch Churn Analysis</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-info">
        📁 Upload a CSV file with customer data to analyze multiple customers at once.
        The file should contain the same columns as the training data.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Choose a CSV file", type="csv", 
                                help="Upload a CSV with customer data")

    if uploaded:
        try:
            df_batch = pd.read_csv(uploaded)
            st.success(f"✅ Successfully loaded {len(df_batch)} customers")
            
            # Show preview
            with st.expander("👁️ Preview Data"):
                st.dataframe(df_batch.head(10), use_container_width=True)

            if st.button("🔮 Analyze All Customers", use_container_width=True):
                with st.spinner("🔄 Processing batch predictions..."):
                    
                    try:
                        # Encode and scale
                        df_encoded = prepare_input_for_model(df_batch, feature_cols)
                        df_scaled = scaler.transform(df_encoded)
                        predictions = model.predict_proba(df_scaled)[:, 1]

                        # Add results to dataframe
                        df_batch['Churn_Probability'] = predictions
                        df_batch['Risk_Level'] = pd.cut(predictions,
                                                        bins=[0, 0.4, 0.7, 1.0],
                                                        labels=["LOW", "MEDIUM", "HIGH"])

                        # Summary statistics
                        st.markdown('<div class="section-header">📊 Analysis Summary</div>', unsafe_allow_html=True)

                        col1, col2, col3, col4 = st.columns(4)

                        high_risk = (df_batch['Risk_Level'] == 'HIGH').sum()
                        medium_risk = (df_batch['Risk_Level'] == 'MEDIUM').sum()
                        low_risk = (df_batch['Risk_Level'] == 'LOW').sum()
                        avg_prob = df_batch['Churn_Probability'].mean()

                        with col1:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚨</div>
                                <div class="stat-value" style="color: #ef4444;">{high_risk}</div>
                                <div class="stat-label">High Risk</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚠️</div>
                                <div class="stat-value" style="color: #f59e0b;">{medium_risk}</div>
                                <div class="stat-label">Medium Risk</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col3:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
                                <div class="stat-value" style="color: #10b981;">{low_risk}</div>
                                <div class="stat-label">Low Risk</div>
                            </div>
                            """, unsafe_allow_html=True)

                        with col4:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                                <div class="stat-value">{avg_prob:.1%}</div>
                                <div class="stat-label">Avg Risk</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # Visualizations
                        col_chart1, col_chart2 = st.columns(2)

                        with col_chart1:
                            # Distribution histogram
                            fig_dist = px.histogram(
                                df_batch,
                                x='Churn_Probability',
                                nbins=30,
                                title='Churn Probability Distribution',
                                labels={'Churn_Probability': 'Churn Probability'},
                                color_discrete_sequence=['#6366f1']
                            )
                            fig_dist.update_layout(
                                paper_bgcolor='#0d1117',
                                plot_bgcolor='rgba(30, 41, 59, 0.3)',
                                font={'color': "#f8fafc", 'family': "Inter"},
                                title_font_size=16,
                                showlegend=False,
                                margin=dict(l=10, r=10, t=40, b=10)
                            )
                            st.plotly_chart(fig_dist, use_container_width=True)

                        with col_chart2:
                            # Risk level pie chart
                            risk_counts = df_batch['Risk_Level'].value_counts()
                            fig_pie = px.pie(
                                values=risk_counts.values,
                                names=risk_counts.index,
                                title='Risk Level Distribution',
                                color=risk_counts.index,
                                color_discrete_map={
                                    'LOW': '#10b981',
                                    'MEDIUM': '#f59e0b',
                                    'HIGH': '#ef4444'
                                }
                            )
                            fig_pie.update_layout(
                                paper_bgcolor='#0d1117',
                                plot_bgcolor='#0d1117',
                                font={'color': "#f8fafc", 'family': "Inter"},
                                title_font_size=16,
                                margin=dict(l=10, r=10, t=40, b=10)
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)

                        # Results table
                        st.markdown('<div class="section-header">📋 Detailed Results</div>', unsafe_allow_html=True)

                        display_cols = []
                        if 'customerID' in df_batch.columns:
                            display_cols.append('customerID')
                        display_cols += ['Churn_Probability', 'Risk_Level']
                        
                        if 'tenure' in df_batch.columns:
                            display_cols.append('tenure')
                        if 'MonthlyCharges' in df_batch.columns:
                            display_cols.append('MonthlyCharges')
                        if 'Contract' in df_batch.columns:
                            display_cols.append('Contract')

                        display_cols = [col for col in display_cols if col in df_batch.columns]

                        st.dataframe(
                            df_batch[display_cols].sort_values('Churn_Probability', ascending=False),
                            use_container_width=True,
                            height=400
                        )

                        # Download button
                        csv = df_batch.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results CSV",
                            data=csv,
                            file_name=f"churn_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    except Exception as e:
                        st.markdown(f"""
                        <div class="alert-error">
                            <strong>❌ Batch Processing Error</strong><br>
                            {str(e)}<br><br>
                            Please ensure your CSV has the correct columns.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("🔍 Debug Information"):
                            st.write("DataFrame shape:", df_batch.shape)
                            st.write("Columns in uploaded file:", df_batch.columns.tolist())
                            st.write("Expected columns:", feature_cols[:10], "... (first 10 shown)")

        except Exception as e:
            st.markdown(f"""
            <div class="alert-error">
                <strong>❌ File Upload Error</strong><br>
                {str(e)}<br><br>
                Please ensure you're uploading a valid CSV file.
            </div>
            """, unsafe_allow_html=True)


# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); font-size: 0.85rem; padding: 2rem 0;">
    Powered by Machine Learning | Built with Streamlit | © 2024 Telecom Churn Intelligence
</div>
""", unsafe_allow_html=True)
