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
    "admin": {"password": "admin123", "role": "Admin"},
    "student": {"password": "student123", "role": "Student", "student_id": 101},
    "teacher": {"password": "teacher123", "role": "Teacher"}
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
def render_access_denied():
    st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(145deg, #1e1e1e, #2d1a1a); border-radius: 16px; border: 1px solid #ef4444; box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.15); margin-top: 2rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem; text-shadow: 0 0 20px rgba(239, 68, 68, 0.5);">🛑</div>
            <h2 style="color: #ef4444; font-size: 2.2rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1rem;">Access Denied</h2>
            <div style="height: 3px; background: linear-gradient(90deg, transparent, #ef4444, transparent); width: 60%; margin: 0 auto 1.5rem auto;"></div>
            <p style="color: #e2e8f0; font-size: 1.2rem; font-weight: 500; margin-bottom: 0.5rem;">You don't have the necessary access to view this module.</p>
            <p style="color: #94a3b8; font-size: 1rem;">🔒 This Analytics Dashboard is strictly reserved for Administrators.</p>
        </div>
    """, unsafe_allow_html=True)

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

def render_bulk_upload():
    st.markdown("### 📂 Bulk Upload Student Marks")
    st.markdown("Upload a CSV file containing student marks. The file must contain the following columns: `student_id`, `topic`, `score`, `time_spent`, `attempts`, `difficulty_level`.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            expected_cols = ["student_id", "topic", "score", "time_spent", "attempts", "difficulty_level"]
            
            if all(col in df.columns for col in expected_cols):
                st.write("Preview:")
                st.dataframe(df.head())
                
                if st.button("Process Bulk Upload", type="primary", use_container_width=True):
                    with st.spinner("Processing records..."):
                        success_count = 0
                        for _, row in df.iterrows():
                            payload = {
                                "student_id": int(row["student_id"]),
                                "topic": str(row["topic"]),
                                "score": float(row["score"]),
                                "time_spent": float(row["time_spent"]),
                                "attempts": int(row["attempts"]),
                                "difficulty_level": int(row["difficulty_level"])
                            }
                            try:
                                res = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=5)
                                if res.status_code == 200:
                                    success_count += 1
                            except Exception:
                                pass
                        
                        st.success(f"Successfully processed {success_count} out of {len(df)} records!")
            else:
                st.error(f"Missing columns. Expected: {', '.join(expected_cols)}")
        except Exception as e:
            st.error(f"Error processing file: {e}")

def render_analytics_dashboard():
    st.markdown("---")
    is_student = st.session_state.role == "Student"
    
    if is_student:
        st.markdown("### 📈 My Learning Analytics Dashboard")
    else:
        st.markdown("### 📈 Cohort Analytics Dashboard")
    
    try:
        df = load_data()
        
        if df is None or len(df) == 0:
            if is_student:
                st.info("No analytics data found for your student profile yet. Complete an assessment first.")
            else:
                st.info("No historical data available to generate analytics. Submit predictions to populate the dashboard.")
            return
            
        if is_student:
            logged_in_student_id = st.session_state.student_id
            df = df[df["student_id"].astype(str) == str(logged_in_student_id)]
            if len(df) == 0:
                st.info("No analytics data found for your student profile yet. Complete an assessment first.")
                return
                
        # Filters
        with st.container():
            f1, f2 = st.columns(2)
            
            if is_student:
                student_filter = "All Students"
                f1.info(f"Viewing analytics strictly for your Student ID: {logged_in_student_id}")
            else:
                student_filter = f1.selectbox("Filter by Student", ["All Students"] + sorted(list(df["student_id"].unique())))
                
            topic_filter = f2.selectbox("Filter by Topic", ["All Topics"] + sorted(list(df["topic"].unique())))
            
            filtered_df = df.copy()
            if not is_student and student_filter != "All Students":
                filtered_df = filtered_df[filtered_df["student_id"] == student_filter]
            if topic_filter != "All Topics":
                filtered_df = filtered_df[filtered_df["topic"] == topic_filter]

        if len(filtered_df) == 0:
            st.warning("No data matches the selected filters.")
            return

        # Top KPIs
        k1, k2, k3, k4 = st.columns(4)
        high_risk_pct = (len(filtered_df[filtered_df["risk_level"] == "High"]) / len(filtered_df)) * 100
        
        if is_student:
            k1.metric("My Evaluations", len(filtered_df))
            k2.metric("My Average Score", f"{filtered_df['score'].mean():.1f}%")
            k3.metric("My Avg Attempts", f"{filtered_df['attempts'].mean():.1f}")
            k4.metric("My High Risk Attempts", f"{high_risk_pct:.1f}%")
        else:
            k1.metric("Total Evaluations", len(filtered_df))
            k2.metric("Average Score", f"{filtered_df['score'].mean():.1f}%")
            k3.metric("Avg Attempts", f"{filtered_df['attempts'].mean():.1f}")
            k4.metric("High Risk Population", f"{high_risk_pct:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Charts Section
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"#### {'My Risk Distribution' if is_student else 'Risk Distribution'}")
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
            st.markdown(f"#### {'My Mastery Progress' if is_student else 'Mastery Attainment'}")
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
        
        # Subject-wise scores for a specific student
        if is_student:
            st.markdown("#### My Subject-wise Scores")
        elif student_filter != "All Students":
            st.markdown(f"#### Subject-wise Scores for Student ID: {student_filter}")
            
        if is_student or student_filter != "All Students":
            # Since there could be multiple attempts per topic, take the max score achieved per topic
            subject_df = filtered_df.groupby("topic")["score"].max().reset_index()
            
            fig_subject = px.bar(
                subject_df,
                x="topic",
                y="score",
                color="topic",
                text="score",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_subject.update_traces(texttemplate='%{text:.1f}%', textposition='outside', hovertemplate="%{x}: %{y}%<extra></extra>")
            fig_subject.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False, xaxis_title="Subject", yaxis_title="Highest Score (%)")
            fig_subject.update_yaxes(range=[0, max(100, subject_df['score'].max() + 15) if not subject_df.empty else 100])
            st.plotly_chart(fig_subject, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
        # Time-Series / Trend Section
        st.markdown(f"#### {'My Score Trend' if is_student else 'Longitudinal Score Trends'}")
        
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

def render_nlp_essay(student_id, topic):
    st.markdown("### 📝 NLP Essay Evaluation")
    st.info(f"Submit a short essay on **{topic}** to be graded by the AI NLP Engine.")
    essay_text = st.text_area("Write your legal analysis here:", height=150)
    if st.button("Evaluate Essay", type="primary"):
        with st.spinner("Analyzing text..."):
            try:
                payload = {"student_id": student_id, "topic": topic, "essay_text": essay_text}
                res = requests.post("http://127.0.0.1:8000/evaluate-essay", json=payload, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    st.metric("NLP Score", f"{data['score']}%")
                    st.success(f"**Feedback:** {data['feedback']}")
                    st.info(f"**Key Concepts Found:** {', '.join(data['key_concepts_found']) if data['key_concepts_found'] else 'None'}")
                else:
                    st.error("Error from NLP Engine.")
            except Exception as e:
                st.error(f"Connection failed: {e}")

def render_genai_cases(student_id, topic):
    st.markdown("### 🧠 GenAI Case Generation")
    st.info("Dynamically generate custom legal scenarios based on your current topic.")
    if st.button("Generate Case Study", type="primary"):
        with st.spinner("Generating..."):
            try:
                res = requests.post("http://127.0.0.1:8000/generate-scenario", json={"student_id": student_id, "weak_topic": topic}, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f"**Generated Scenario ({topic}):**")
                    st.write(data["scenario_text"])
                    st.markdown("**Questions to Consider:**")
                    for q in data["questions"]:
                        st.write(f"- {q}")
            except Exception as e:
                st.error("API Error")
                
def render_ai_tutor_chat():
    st.markdown("### 🤖 SLM AI Tutor Chat")
    query = st.text_input("Ask a legal concept question:")
    if st.button("Ask Tutor", type="primary"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://127.0.0.1:8000/tutor-chat", json={"query": query}, timeout=10)
                if res.status_code == 200:
                    st.info(f"**AI Tutor:** {res.json()['response']}")
            except:
                st.error("Tutor offline.")

def render_agent_alert(student_id):
    st.markdown("---")
    st.markdown("### 🕵️ Proactive Agentic AI")
    if st.button("Run Background Audit (Simulate)", use_container_width=True):
        with st.spinner("Auditing student profile..."):
            try:
                res = requests.get(f"http://127.0.0.1:8000/agent-audit/{student_id}", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    st.warning(data["agent_alert"])
                    st.info(f"**Recommended Action:** {data['recommended_action']}")
                    st.text_area("Drafted Email for Student:", data["email_draft"], height=150)
            except:
                st.error("Agent offline.")

# ================= MAIN APP =================
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_header()
        
        student_id, topic, score, time_spent, attempts, difficulty_level, submit = render_sidebar()
        
        if st.session_state.role == "Admin":
            st.sidebar.markdown("---")
            render_agent_alert(student_id)
            
            tabs = st.tabs(["🎯 Live Prediction", "📝 NLP Essay", "🧠 GenAI Cases", "🤖 Tutor Chat", "📂 Bulk File Upload", "📈 Analytics Dashboard"])
            with tabs[0]:
                if submit: render_prediction_panel(student_id, topic, score, time_spent, attempts, difficulty_level)
                else: st.info("👈 Enter metrics and click 'Generate Prediction'")
            with tabs[1]: render_nlp_essay(student_id, topic)
            with tabs[2]: render_genai_cases(student_id, topic)
            with tabs[3]: render_ai_tutor_chat()
            with tabs[4]: render_bulk_upload()
            with tabs[5]: render_analytics_dashboard()
                
        elif st.session_state.role == "Teacher":
            st.sidebar.markdown("---")
            render_agent_alert(student_id)
            
            tabs = st.tabs(["🎯 Live Prediction", "📝 NLP Essay", "🧠 GenAI Cases", "🤖 Tutor Chat", "📂 Bulk File Upload", "📈 Analytics Dashboard"])
            with tabs[0]:
                if submit: render_prediction_panel(student_id, topic, score, time_spent, attempts, difficulty_level)
                else: st.info("👈 Enter metrics and click 'Generate Prediction'")
            with tabs[1]: render_nlp_essay(student_id, topic)
            with tabs[2]: render_genai_cases(student_id, topic)
            with tabs[3]: render_ai_tutor_chat()
            with tabs[4]: render_bulk_upload()
            with tabs[5]: render_analytics_dashboard()
                
        else:
            tabs = st.tabs(["🎯 Live Prediction", "📝 NLP Essay", "🧠 GenAI Cases", "🤖 Tutor Chat", "📈 Analytics Dashboard"])
            with tabs[0]:
                if submit: render_prediction_panel(student_id, topic, score, time_spent, attempts, difficulty_level)
                else: st.info("👈 Enter metrics and click 'Generate Prediction'")
            with tabs[1]: render_nlp_essay(student_id, topic)
            with tabs[2]: render_genai_cases(student_id, topic)
            with tabs[3]: render_ai_tutor_chat()
            with tabs[4]: render_analytics_dashboard()

if __name__ == "__main__":
    main()