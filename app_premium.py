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
    --bg-card: rgba(30, 41, 59, 0.5);
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --border-color: rgba(148, 163, 184, 0.1);
}

/* Global Styles */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 2rem 0 3rem 0;
    margin-bottom: 2rem;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
}

/* Glass Card */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid var(--border-color);
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    border-color: rgba(99, 102, 241, 0.3);
}

/* Section Headers */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
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

/* Input Styling */
.stSelectbox, .stSlider, .stNumberInput {
    margin-bottom: 1rem;
}

.stSelectbox label, .stSlider label, .stNumberInput label {
    font-weight: 500;
    color: var(--text-primary);
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

/* Prediction Results */
.prediction-container {
    margin: 2rem 0;
}

.result-card-high-risk {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
    border: 2px solid var(--danger-color);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: pulse-danger 2s ease-in-out infinite;
}

.result-card-low-risk {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
    border: 2px solid var(--success-color);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: pulse-success 2s ease-in-out infinite;
}

.result-card-medium-risk {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
    border: 2px solid var(--warning-color);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    animation: pulse-warning 2s ease-in-out infinite;
}

@keyframes pulse-danger {
    0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }
}

@keyframes pulse-success {
    0%, 100% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); }
    50% { box-shadow: 0 0 40px rgba(16, 185, 129, 0.5); }
}

@keyframes pulse-warning {
    0%, 100% { box-shadow: 0 0 20px rgba(245, 158, 11, 0.3); }
    50% { box-shadow: 0 0 40px rgba(245, 158, 11, 0.5); }
}

.result-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    display: block;
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

/* Stats Cards */
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
    background-clip: text;
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

.risk-factor-name {
    font-weight: 500;
    color: var(--text-primary);
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

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(99, 102, 241, 0.6);
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(20px);
}

.sidebar-content {
    padding: 1rem;
}

/* Metrics */
.metric-container {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 1.25rem;
    border: 1px solid var(--border-color);
    margin-bottom: 1rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: rgba(30, 41, 59, 0.3);
    padding: 0.5rem;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
}

/* Info Box */
.info-box {
    background: rgba(59, 130, 246, 0.1);
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: var(--text-secondary);
}

/* Recommendation Card */
.recommendation-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.recommendation-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.recommendation-text {
    color: var(--text-secondary);
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

#======== HERO SECTION ========
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📡 Telecom Churn Intelligence</div>
    <div class="hero-subtitle">Advanced ML-powered customer retention analytics platform</div>
</div>
""", unsafe_allow_html=True)

#======== LOAD MODEL ========
@st.cache_resource
def load_model():
    try:
        with open("churn_pipeline.pkl", "rb") as f:
            pipeline = pickle.load(f)
        return pipeline["model"], pipeline["scaler"], pipeline["columns"]
    except:
        st.error("⚠️ Model file not found. Please ensure 'churn_pipeline.pkl' is in the directory.")
        st.stop()

model, scaler, feature_cols = load_model()

#======== SIDEBAR ========
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Configuration")
    
    mode = st.radio(
        "Prediction Mode",
        ["🎯 Single Customer", "📊 Batch Analysis"],
        help="Choose between single customer prediction or batch file upload"
    )
    
    st.markdown("---")
    
    st.markdown("### 📈 Model Info")
    st.markdown("""
    <div class="metric-container">
        <div style="font-size: 0.9rem; color: var(--text-secondary);">Accuracy</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">~80%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6;">
    This platform uses machine learning to predict customer churn probability based on:
    <br><br>
    • Customer demographics<br>
    • Service usage patterns<br>
    • Billing information<br>
    • Contract details
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

#======== MAIN CONTENT ========
if mode == "🎯 Single Customer":
    
    # Input Section
    st.markdown('<div class="section-header">👤 Customer Information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**👥 Demographics**")
        gender = st.selectbox("Gender", ["Male", "Female"], help="Customer gender")
        senior = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", 
                             help="Is the customer a senior citizen?")
        partner = st.selectbox("Has Partner", ["Yes", "No"], help="Does the customer have a partner?")
        dependents = st.selectbox("Has Dependents", ["Yes", "No"], help="Does the customer have dependents?")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
            online_security = "No internet service"
            online_backup = "No internet service"
            device_protection = "No internet service"
            tech_support = "No internet service"
            streaming_tv = "No internet service"
            streaming_movies = "No internet service"
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**💳 Billing Information**")
        tenure = st.slider("Tenure (months)", 0, 72, 12, help="How long the customer has been with the company")
        contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ])
        charges = st.number_input("Monthly Charges ($)", 10.0, 200.0, 70.0, step=5.0)
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, float(charges * tenure), step=100.0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        predict_btn = st.button("🔮 Predict Churn Risk", use_container_width=True)
    
    if predict_btn:
        # Prepare data
        input_data = pd.DataFrame([{
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
        
        # Make prediction
        try:
            df_scaled = scaler.transform(input_data[feature_cols])
            churn_prob = model.predict_proba(df_scaled)[0][1]
            
            # Determine risk level
            if churn_prob >= 0.7:
                risk_level = "HIGH"
                risk_class = "result-card-high-risk"
                icon = "🚨"
                message = "Immediate Action Required"
            elif churn_prob >= 0.4:
                risk_level = "MEDIUM"
                risk_class = "result-card-medium-risk"
                icon = "⚠️"
                message = "Monitor Closely"
            else:
                risk_level = "LOW"
                risk_class = "result-card-low-risk"
                icon = "✅"
                message = "Customer Stable"
            
            # Display Results
            st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="{risk_class}">
                <span class="result-icon">{icon}</span>
                <div class="result-title">{risk_level} RISK</div>
                <div class="result-subtitle">{message}</div>
                <div class="probability-display">{churn_prob:.1%}</div>
                <div style="color: var(--text-secondary); font-size: 0.95rem;">Churn Probability</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analytics Dashboard
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 Risk Analytics</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                
                # Risk Gauge Chart
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = churn_prob * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Churn Risk Score", 'font': {'size': 20, 'color': '#f8fafc'}},
                    delta = {'reference': 50, 'increasing': {'color': "#ef4444"}, 'decreasing': {'color': "#10b981"}},
                    number = {'suffix': "%", 'font': {'size': 40, 'color': '#f8fafc'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                        'bar': {'color': "#6366f1"},
                        'bgcolor': "rgba(30, 41, 59, 0.3)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(148, 163, 184, 0.1)",
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(16, 185, 129, 0.2)'},
                            {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.2)'},
                            {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
                        ],
                        'threshold': {
                            'line': {'color': "#ef4444", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#f8fafc", 'family': "Inter"},
                    height=300,
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**🎯 Key Risk Factors**")
                
                # Calculate risk factors
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
                    risk_factors.append(("No major risk factors", "LOW"))
                
                for factor, level in risk_factors[:5]:
                    badge_class = f"risk-{level.lower()}"
                    st.markdown(f"""
                    <div class="risk-factor">
                        <span class="risk-factor-name">{factor}</span>
                        <span class="risk-badge {badge_class}">{level}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Customer Profile Breakdown
            st.markdown('<div class="section-header">📈 Customer Profile Analysis</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            metrics = [
                ("💰", f"${charges:.0f}", "Monthly Spend"),
                ("📅", f"{tenure} mo", "Tenure"),
                ("📋", contract, "Contract"),
                ("💳", payment.split()[0], "Payment")
            ]
            
            for col, (emoji, value, label) in zip([col1, col2, col3, col4], metrics):
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                        <div class="stat-value">{value}</div>
                        <div class="stat-label">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Recommendations
            if churn_prob >= 0.4:
                st.markdown('<div class="section-header">💡 Retention Recommendations</div>', unsafe_allow_html=True)
                
                recommendations = []
                
                if contract == "Month-to-month":
                    recommendations.append(("📋", "Contract Upgrade", 
                                          "Offer incentive to upgrade to 1-year or 2-year contract with 15% discount"))
                
                if tenure < 12:
                    recommendations.append(("🎁", "Welcome Package", 
                                          "Provide onboarding support and loyalty rewards for first year"))
                
                if online_security == "No" or tech_support == "No":
                    recommendations.append(("🛡️", "Service Bundle", 
                                          "Offer free trial of security and support services for 3 months"))
                
                if charges > 80:
                    recommendations.append(("💰", "Price Optimization", 
                                          "Review pricing plan and offer customized package to reduce monthly costs"))
                
                if payment == "Electronic check":
                    recommendations.append(("💳", "Payment Method", 
                                          "Incentivize automatic payment methods with $5/month discount"))
                
                for emoji, title, text in recommendations[:3]:
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="recommendation-title">
                            <span>{emoji}</span> {title}
                        </div>
                        <div class="recommendation-text">{text}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

else:
    # Batch Analysis Mode
    st.markdown('<div class="section-header">📊 Batch Churn Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        📁 Upload a CSV file with customer data to analyze multiple customers at once.
        The file should contain the same columns as the training data.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df_batch = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df_batch)} customers")
        
        if st.button("🔮 Analyze All Customers"):
            try:
                # Make predictions
                df_scaled = scaler.transform(df_batch[feature_cols])
                predictions = model.predict_proba(df_scaled)[:, 1]
                
                df_batch['Churn_Probability'] = predictions
                df_batch['Risk_Level'] = pd.cut(predictions, 
                                                bins=[0, 0.4, 0.7, 1.0], 
                                                labels=['LOW', 'MEDIUM', 'HIGH'])
                
                # Summary Stats
                st.markdown('<div class="section-header">📊 Analysis Summary</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                high_risk = (df_batch['Risk_Level'] == 'HIGH').sum()
                medium_risk = (df_batch['Risk_Level'] == 'MEDIUM').sum()
                low_risk = (df_batch['Risk_Level'] == 'LOW').sum()
                avg_prob = df_batch['Churn_Probability'].mean()
                
                stats = [
                    ("🚨", high_risk, "High Risk"),
                    ("⚠️", medium_risk, "Medium Risk"),
                    ("✅", low_risk, "Low Risk"),
                    ("📊", f"{avg_prob:.1%}", "Avg Risk")
                ]
                
                for col, (emoji, value, label) in zip([col1, col2, col3, col4], stats):
                    with col:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                            <div class="stat-value">{value}</div>
                            <div class="stat-label">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Distribution Chart
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_dist = px.histogram(
                        df_batch, 
                        x='Churn_Probability',
                        nbins=30,
                        title='Churn Probability Distribution',
                        labels={'Churn_Probability': 'Churn Probability'},
                        color_discrete_sequence=['#6366f1']
                    )
                    fig_dist.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(30, 41, 59, 0.3)',
                        font={'color': "#f8fafc", 'family': "Inter"},
                        title_font_size=16,
                        showlegend=False
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                with col2:
                    risk_counts = df_batch['Risk_Level'].value_counts()
                    fig_pie = px.pie(
                        values=risk_counts.values,
                        names=risk_counts.index,
                        title='Risk Level Distribution',
                        color=risk_counts.index,
                        color_discrete_map={'LOW': '#10b981', 'MEDIUM': '#f59e0b', 'HIGH': '#ef4444'}
                    )
                    fig_pie.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'color': "#f8fafc", 'family': "Inter"},
                        title_font_size=16
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Results Table
                st.markdown('<div class="section-header">📋 Detailed Results</div>', unsafe_allow_html=True)
                
                display_cols = ['customerID'] if 'customerID' in df_batch.columns else []
                display_cols += ['Churn_Probability', 'Risk_Level', 'tenure', 'MonthlyCharges', 'Contract']
                display_cols = [col for col in display_cols if col in df_batch.columns]
                
                st.dataframe(
                    df_batch[display_cols].sort_values('Churn_Probability', ascending=False),
                    use_container_width=True,
                    height=400
                )
                
                # Download Results
                csv = df_batch.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results CSV",
                    data=csv,
                    file_name=f"churn_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"Error processing batch: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: var(--text-secondary); font-size: 0.85rem; padding: 2rem 0;">
    Powered by Machine Learning | Built with Streamlit | © 2024 Telecom Churn Intelligence
</div>
""", unsafe_allow_html=True)
