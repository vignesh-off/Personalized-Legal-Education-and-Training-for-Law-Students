import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.analytics import load_data

st.set_page_config(page_title="Legal AI Platform", layout="wide", page_icon="⚖️")

# ================= CUSTOM CSS FOR SAAS LOOK =================
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header Gradient */
    .saas-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .saas-header h1 { margin: 0; font-size: 2.2rem; font-weight: 700; color: #FFFFFF; }
    .saas-header p { margin: 0.5rem 0 0 0; color: #E0E7FF; font-size: 1.1rem; }
    
    /* Card Styling */
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    .metric-title { font-size: 0.9rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 0.5rem; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #0F172A; }
    
    /* Risk Colors */
    .risk-high { background-color: #FEF2F2; border: 1px solid #FCA5A5; color: #991B1B; padding: 1rem; border-radius: 8px; }
    .risk-medium { background-color: #FFFBEB; border: 1px solid #FCD34D; color: #92400E; padding: 1rem; border-radius: 8px; }
    .risk-low { background-color: #F0FDF4; border: 1px solid #86EFAC; color: #166534; padding: 1rem; border-radius: 8px; }
    
    hr { margin-top: 2rem; margin-bottom: 2rem; border-color: #E2E8F0; }
    
    /* Hide Streamlit form enter instructions */
    [data-testid="InputInstructions"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ================= HELPER FUNCTIONS =================
def generate_student_insight(score, attempts, difficulty_level, mastery_level, risk_level):
    """Generates a dynamic human-readable insight for a specific prediction."""
    insights = []
    
    if risk_level == "High":
        insights.append("🚨 **High Risk Flagged**: ")
        if score < 50:
            insights.append(f"Student scored significantly low ({score}%) on a level {difficulty_level} topic. ")
        if attempts >= 3:
            insights.append(f"Student is struggling, requiring {attempts} attempts. Immediate intervention is recommended.")
    elif risk_level == "Medium":
        insights.append("⚠️ **Moderate Risk**: ")
        if attempts == 2:
            insights.append("Student needed a second attempt to pass. ")
        if 50 <= score < 70:
            insights.append("Score is borderline. Consider assigning review materials.")
    else:
        insights.append("✅ **On Track**: ")
        insights.append(f"Student demonstrated strong comprehension, achieving {score}% in {attempts} attempt(s).")
        
    return "".join(insights)

def generate_global_insights(df):
    """Generates AI insights for the analytics section."""
    if len(df) == 0:
        return "Not enough data for insights."
    
    most_common_mastery = df["mastery_level"].mode()[0]
    high_risk_count = len(df[df["risk_level"] == "High"])
    total = len(df)
    avg_score = df["score"].mean()
    
    insight = f"🧠 **AI Global Insight**: The dominant mastery level across the cohort is **{most_common_mastery}** with an average score of **{avg_score:.1f}**.\n\n"
    if high_risk_count / total > 0.2:
        insight += "📉 **Attention Required**: Over 20% of students are classified as high risk. Review the curriculum difficulty or provide targeted tutoring for recent topics."
    else:
        insight += "📈 **Healthy Cohort**: Risk levels are well within manageable thresholds. Current pedagogical strategies are effective."
        
    return insight

# ================= AUTHENTICATION =================
CREDENTIALS = {
    "student": {"password": "student123", "role": "Student", "student_id": 101},
    "teacher": {"password": "teacher123", "role": "Teacher/Admin"}
}

def render_login():
    st.markdown("""
        <div style='text-align: center; margin-top: 5rem;'>
            <h1 style='color: #1E1B4B;'>⚖️ Legal Education Intelligence</h1>
            <p style='color: #64748B; font-size: 1.2rem;'>Sign in to access your dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if username in CREDENTIALS and CREDENTIALS[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = CREDENTIALS[username]["role"]
                    if CREDENTIALS[username]["role"] == "Student":
                        st.session_state.student_id = CREDENTIALS[username]["student_id"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
                    


# ================= UI SECTIONS =================
def render_header():
    st.markdown("""
        <div class="saas-header">
            <h1>⚖️ Legal Education Intelligence</h1>
            <p>Real-time Mastery Prediction & Risk Analytics Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    st.sidebar.markdown(f"**👤 {st.session_state.role}** | {st.session_state.username}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧑 New Student Evaluation")
    
    with st.sidebar.form(key="prediction_form"):
        is_student = st.session_state.role == "Student"
        default_id = st.session_state.student_id if is_student else 101
        
        student_id = st.number_input("Student ID", min_value=1, value=default_id, disabled=is_student)
        topic = st.selectbox("Topic Module", [
            "Introduction to Law", "Contracts", "Torts", 
            "Criminal Law", "Property Law", "Constitutional Law"
        ])
        
        st.markdown("---")
        score = st.slider("Assessment Score (%)", 0, 100, 75)
        
        col1, col2 = st.columns(2)
        with col1:
            time_spent = st.number_input("Time (min)", min_value=1, value=45)
        with col2:
            attempts = st.number_input("Attempts", min_value=1, value=1)
            
        difficulty_level = st.slider("Module Difficulty", 1, 5, 3)
        
        submit = st.form_submit_button("🚀 Generate Prediction", use_container_width=True)
        
    if st.sidebar.button("🔄 Reset Form", use_container_width=True):
        st.rerun()

    return student_id, topic, score, time_spent, attempts, difficulty_level, submit

def render_prediction_panel(student_id, topic, score, time_spent, attempts, difficulty_level):
    st.markdown("### 🎯 Live Prediction Results")
    
    with st.spinner("🧠 AI is analyzing student performance patterns..."):
        payload = {
            "student_id": student_id,
            "topic": topic,
            "score": score,
            "time_spent": time_spent,
            "attempts": attempts,
            "difficulty_level": difficulty_level
        }
        
        data_ml = None
        try:
            res_ml = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10)
            if res_ml.status_code == 200:
                data_ml = res_ml.json()
            else:
                st.warning(f"Backend API returned {res_ml.status_code}. Using local ML fallback.")
        except Exception:
            st.warning("API connection failed or timed out. Using local ML fallback.")
            
        if not data_ml:
            # Fallback logic if API completely fails
            if score < 40:
                f_mastery, f_risk = "Beginner", "High"
            elif 40 <= score <= 69:
                f_mastery, f_risk = "Intermediate", "Medium"
            else:
                f_mastery, f_risk = "Expert", "Low"
                
            data_ml = {
                'mastery_level': f_mastery,
                'risk_level': f_risk,
                'next_topic_recommendation': "Review Fundamentals" if score < 40 else "Next Module"
            }

        data_dl = None
        try:
            res_dl = requests.post("http://127.0.0.1:8000/predict-dl", json=payload, timeout=5)
            if res_dl.status_code == 200:
                data_dl = res_dl.json()
        except Exception:
            pass

        st.markdown("#### ⚖️ Model Comparison")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title" style="color:#0EA5E9;">Machine Learning Model</div>
                <div style="font-size: 0.8rem; color:#64748B; margin-bottom:5px;">Random Forest Classifier</div>
                <div class="metric-value" style="font-size: 1.4rem;">{data_ml['mastery_level']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            if data_dl:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title" style="color:#8B5CF6;">Deep Learning Model</div>
                    <div style="font-size: 0.8rem; color:#64748B; margin-bottom:5px;">Neural Network Layer</div>
                    <div class="metric-value" style="font-size: 1.4rem;">{data_dl['dl_mastery_level']}</div>
                    <div style="font-size: 0.8rem; color:#64748B; margin-top:5px;">Confidence: {data_dl['dl_confidence']}%</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="opacity: 0.6;">
                    <div class="metric-title" style="color:#8B5CF6;">Deep Learning Model</div>
                    <div style="font-size: 0.8rem; color:#64748B; margin-bottom:5px;">Neural Network Layer</div>
                    <div class="metric-value" style="font-size: 1.0rem; color: #DC2626;">DL Unavailable</div>
                    <div style="font-size: 0.8rem; color:#64748B; margin-top:5px;">Fallback used</div>
                </div>
                """, unsafe_allow_html=True)
            
        with c3:
            if data_dl:
                if data_ml['mastery_level'] == data_dl['dl_mastery_level']:
                    decision = data_ml['mastery_level']
                    decision_color = "#10B981"
                    msg = "ML and DL agree on the prediction."
                else:
                    decision = "Needs Review"
                    decision_color = "#F59E0B"
                    msg = "ML and DL differ, use conservative recommendation."
            else:
                decision = data_ml['mastery_level']
                decision_color = "#0EA5E9"
                msg = "DL engine did not respond. Using primary ML prediction."
                
            st.markdown(f"""
            <div class="metric-card" style="border: 2px solid {decision_color};">
                <div class="metric-title">Final Hybrid Decision</div>
                <div style="font-size: 0.8rem; color:#64748B; margin-bottom:5px;">ML + DL + Risk Logic</div>
                <div class="metric-value" style="color: {decision_color}; font-size: 1.4rem;">{decision}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info(f"💡 **Analysis Consensus:** {msg}")
        
        st.markdown(
            "<div style='font-size: 0.85rem; color:#64748B; text-align: center; margin-top: 10px; margin-bottom: 20px;'>"
            "Machine Learning predicts the primary mastery level using Random Forest. Deep Learning provides a "
            "neural-network-based comparative prediction. Final decision combines ML, DL, and rule-based risk assessment."
            "</div>", unsafe_allow_html=True
        )
        
        st.markdown("#### 📊 Risk Assessment & Recommendation")
        rc1, rc2 = st.columns(2)
        with rc1:
            risk = data_ml['risk_level']
            risk_color = "#DC2626" if risk == "High" else "#D97706" if risk == "Medium" else "#059669"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Rule-Based Risk Assessment</div>
                <div class="metric-value" style="color: {risk_color};">{risk} Risk</div>
            </div>
            """, unsafe_allow_html=True)
        with rc2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Recommended Action</div>
                <div class="metric-value" style="font-size: 1.2rem; padding-top: 0.5rem;">{data_ml['next_topic_recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        risk_class = f"risk-{data_ml['risk_level'].lower()}"
        insight_text = generate_student_insight(score, attempts, difficulty_level, data_ml['mastery_level'], data_ml['risk_level'])
        
        st.markdown(f"""
        <div class="{risk_class}">
            {insight_text}
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("⚙️ View Raw API Response"):
            st.json({"ML_Output": data_ml, "DL_Output": data_dl if data_dl else "Failed/Timeout"})

def render_analytics_dashboard():
    st.markdown("---")
    st.markdown("### 📈 Cohort Analytics Dashboard")
    
    try:
        df = load_data()
        
        if df is None or len(df) == 0:
            st.info("No historical data available to generate analytics. Submit predictions to populate the dashboard.")
            return
            
        # Filters
        with st.container():
            f1, f2 = st.columns(2)
            
            is_student = st.session_state.role == "Student"
            
            if is_student:
                student_filter = st.session_state.student_id
                f1.info(f"Viewing analytics strictly for Student ID: {student_filter}")
            else:
                student_filter = f1.selectbox("Filter by Student", ["All Students"] + sorted(list(df["student_id"].unique())))
                
            topic_filter = f2.selectbox("Filter by Topic", ["All Topics"] + sorted(list(df["topic"].unique())))
            
            filtered_df = df.copy()
            if student_filter != "All Students":
                filtered_df = filtered_df[filtered_df["student_id"] == student_filter]
            if topic_filter != "All Topics":
                filtered_df = filtered_df[filtered_df["topic"] == topic_filter]

        if len(filtered_df) == 0:
            st.warning("No data matches the selected filters.")
            return

        # Top KPIs
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Evaluations", len(filtered_df))
        k2.metric("Average Score", f"{filtered_df['score'].mean():.1f}%")
        k3.metric("Avg Attempts", f"{filtered_df['attempts'].mean():.1f}")
        high_risk_pct = (len(filtered_df[filtered_df["risk_level"] == "High"]) / len(filtered_df)) * 100
        k4.metric("High Risk Population", f"{high_risk_pct:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Charts Section
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("#### Risk Distribution")
            risk_df = filtered_df["risk_level"].value_counts().reset_index()
            risk_df.columns = ["Risk Level", "Count"]
            
            fig_donut = px.pie(
                risk_df, 
                names="Risk Level", 
                values="Count", 
                hole=0.6,
                color="Risk Level",
                color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
            )
            fig_donut.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=True)
            fig_donut.update_traces(textposition='inside', textinfo='percent+label', hovertemplate="%{label}: %{value} students<extra></extra>")
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with c2:
            st.markdown("#### Mastery Attainment")
            mastery_df = filtered_df["mastery_level"].value_counts().reset_index()
            mastery_df.columns = ["Mastery Level", "Count"]
            
            fig_bar = px.bar(
                mastery_df, 
                x="Mastery Level", 
                y="Count", 
                color="Mastery Level",
                color_discrete_sequence=["#3B82F6", "#8B5CF6", "#10B981"]
            )
            fig_bar.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False, xaxis_title=None)
            fig_bar.update_traces(hovertemplate="%{x}: %{y} students<extra></extra>")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Time-Series / Trend Section
        st.markdown("#### Longitudinal Score Trend")
        
        # 1. Create proper time/sequence axis and moving average
        trend_df = filtered_df.reset_index(drop=True).copy()
        trend_df["session"] = range(1, len(trend_df) + 1)
        trend_df["Moving Avg"] = trend_df["score"].rolling(window=3, min_periods=1).mean()
        
        # 2. Identify Best/Worst/Drop points
        if len(trend_df) > 1:
            best_session = trend_df.loc[trend_df["score"].idxmax()]
            worst_session = trend_df.loc[trend_df["score"].idxmin()]
        else:
            best_session = worst_session = trend_df.iloc[0]
        
        # Calculate drops (if previous score was significantly higher)
        trend_df["score_diff"] = trend_df["score"].diff().fillna(0)
        major_drops = trend_df[trend_df["score_diff"] <= -15]
        
        # 3. Generate AI Trend Insight
        trend_insight = "📈 **Trend Analysis**: "
        if len(trend_df) < 3:
            trend_insight += "Not enough sessions to determine a stable trend."
        else:
            mean_score = trend_df["score"].mean()
            recent_avg = trend_df["score"].tail(3).mean()

            if recent_avg >= mean_score + 5:
                trend_insight += "Performance improving above baseline. "
            elif recent_avg < mean_score - 10:
                trend_insight += "Performance declining below baseline. "
            else:
                trend_insight += "Performance stable around baseline. "
                
            if not major_drops.empty:
                trend_insight += f"⚠️ Detected {len(major_drops)} significant performance drop(s)."
        
        st.info(trend_insight)
        
        # 4. Build Plotly Figure
        fig_line = go.Figure()
        
        # Actual Scores
        fig_line.add_trace(go.Scatter(
            x=trend_df["session"], y=trend_df["score"], 
            mode='lines+markers',
            name='Actual Score',
            line=dict(color='#93C5FD', width=2),
            marker=dict(size=8, color='#3B82F6', symbol='circle'),
            hovertemplate="Session %{x}<br>Score: %{y}<extra></extra>"
        ))
        
        # Moving Average
        fig_line.add_trace(go.Scatter(
            x=trend_df["session"], y=trend_df["Moving Avg"],
            mode='lines',
            name='3-Period Moving Avg',
            line=dict(color='#1E3A8A', width=3, shape='spline'),
            hovertemplate="Moving Avg: %{y:.1f}<extra></extra>"
        ))
        
        # Highlight Best/Worst
        fig_line.add_trace(go.Scatter(
            x=[best_session["session"]], y=[best_session["score"]],
            mode='markers+text',
            name='Best Score',
            text=["🏆 Best"], textposition="top center",
            marker=dict(size=12, color='#10B981', symbol='star'),
            showlegend=False, hoverinfo="skip"
        ))
        fig_line.add_trace(go.Scatter(
            x=[worst_session["session"]], y=[worst_session["score"]],
            mode='markers+text',
            name='Lowest Score',
            text=["⚠️ Lowest"], textposition="bottom center",
            marker=dict(size=10, color='#EF4444', symbol='x'),
            showlegend=False, hoverinfo="skip"
        ))

        fig_line.update_layout(
            hovermode="x unified",
            xaxis_title="Evaluation Session",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, max(100, trend_df["score"].max() + 10)]), # Added padding for text markers
            xaxis=dict(tickmode='linear', tick0=1, dtick=1), # Ensure integer sessions
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Global Insights
        st.markdown("#### 🤖 Global AI Insights")
        st.info(generate_global_insights(filtered_df))

    except Exception as e:
        st.error(f"Analytics Engine Error: Unable to load dashboard data. ({e})")

# ================= MAIN APP =================
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_header()
        
        student_id, topic, score, time_spent, attempts, difficulty_level, submit = render_sidebar()
        
        if submit:
            render_prediction_panel(student_id, topic, score, time_spent, attempts, difficulty_level)
        else:
            st.info("👈 Please enter student metrics in the sidebar and click 'Generate Prediction' to analyze a student.")
            
        render_analytics_dashboard()

if __name__ == "__main__":
    main()