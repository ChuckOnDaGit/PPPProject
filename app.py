import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoNotes | Teacher Classroom & Sustainability Portal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for EcoNotes Branding
st.markdown("""
<style>
    /* Global Styles & Palette */
    .stApp {
        background-color: #f8faf9;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        color: white;
        padding: 24px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem !important;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #a7f3d0 !important;
        font-size: 1rem;
        margin-top: 6px;
        margin-bottom: 0;
    }

    /* Metric Card Styling */
    .metric-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #10b981;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #064e3b;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #4b5563;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #059669;
        margin-top: 4px;
    }

    /* Status Badges */
    .status-active {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .status-warning {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .status-danger {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }

    /* Hide Streamlit Branding Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MOCK DATA GENERATION
# -----------------------------------------------------------------------------
@st.cache_data
def generate_mock_students():
    names = [
        "Aarav Sharma", "Ananya Verma", "Rohan Gupta", "Priya Iyer",
        "Vikram Singh", "Sneha Patel", "Devansh Mehta", "Kavya Reddy",
        "Ishaan Joshi", "Tanvi Nair", "Aditya Deshmukh", "Riya Kapoor",
        "Siddharth Rao", "Meera Sen", "Kabir Chatterjee", "Diya Choudhury",
        "Arjun Bhat", "Nisha Malhotra", "Yash Agarwal", "Pooja Hegde"
    ]
    
    np.random.seed(42)
    statuses = ["Actively Note-Taking", "Actively Note-Taking", "Actively Note-Taking", "Reviewing Handout", "Idle", "Potential Distraction"]
    
    data = []
    for name in names:
        status = np.random.choice(statuses)
        focus_score = np.random.randint(65, 99) if status != "Potential Distraction" else np.random.randint(30, 55)
        note_intensity = np.random.randint(120, 480) # words written
        paper_saved = np.random.randint(15, 45) # pages saved this week
        quiz_score = np.random.randint(70, 100)
        
        data.append({
            "Student ID": f"STU-{np.random.randint(1000, 9999)}",
            "Name": name,
            "Current Status": status,
            "Focus Score (%)": focus_score,
            "Notes Word Count": note_intensity,
            "Pages Saved (Wk)": paper_saved,
            "Quiz Avg (%)": quiz_score,
            "Backpack Relief (kg)": round(paper_saved * 0.08, 2), # approx weight per page/notebook fraction
            "Last Sync": (datetime.now() - timedelta(minutes=int(np.random.randint(1, 12)))).strftime("%H:%M:%S")
        })
    return pd.DataFrame(data)

df_students = generate_mock_students()

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/leaf.png", width=60)
    st.title("EcoNotes Faculty")
    st.caption("Synchronized Learning & Paperless Portal")
    st.divider()

    selected_class = st.selectbox(
        "🏫 Active Classroom Session",
        ["ENV-101: Environmental Systems", "BIO-202: Ecosystem Ecology", "CS-105: Tech & Sustainability"]
    )
    
    selected_period = st.radio(
        "⏱️ Session Control",
        ["Live Classroom Mode", "Post-Class Review & Analytics"]
    )
    
    st.divider()
    st.markdown("### 🎛️ Teacher Quick Commands")
    if st.button("📢 Push Live Announcement", use_container_width=True):
        st.toast("Announcement broadcasted to all active student screens!", icon="🚀")
    
    if st.button("⚡ Trigger 1-Min Focus Check", use_container_width=True):
        st.toast("Interactive pulse poll sent to student devices.", icon="🎯")
        
    if st.button("🔒 Lock Screens for Discussion", use_container_width=True):
        st.toast("Student screens set to 'Teacher Focus Mode'.", icon="🔒")
        
    st.divider()
    st.caption("EcoNotes v2.4 • Campus Sustainability Network")

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <h1>🌱 EcoNotes Teacher Dashboard</h1>
    <p>Monitoring <b>{selected_class}</b> • Real-time Attentiveness, Paperless Handouts & Ergonomic Impact</p>
</div>
""", unsafe_allow_html=True)

# Top KPI Row
col1, col2, col3, col4 = st.columns(4)

active_students = len(df_students[df_students["Current Status"] != "Potential Distraction"])
avg_focus = int(df_students["Focus Score (%)"].mean())
total_pages = df_students["Pages Saved (Wk)"].sum()
co2_saved = round(total_pages * 0.0045, 2) # kg CO2 per page approx

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Engagement</div>
        <div class="metric-value">{active_students} / {len(df_students)}</div>
        <div class="metric-sub">🟢 {int(active_students/len(df_students)*100)}% active note-taking</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Classroom Focus Index</div>
        <div class="metric-value">{avg_focus}%</div>
        <div class="metric-sub">📈 +4% higher than last week</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Paper Saved This Week</div>
        <div class="metric-value">{total_pages} pgs</div>
        <div class="metric-sub">🌳 Equivalent to ~{round(total_pages/500, 1)} paper reams</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Backpack Relief Avg</div>
        <div class="metric-value">2.4 kg</div>
        <div class="metric-sub">🎒 Reduced student back strain</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------------------------
# TABBED INTERFACE
# -----------------------------------------------------------------------------
tab_monitor, tab_notes, tab_sustainability, tab_analytics = st.tabs([
    "🖥️ Live Classroom Monitor (LANschool Style)",
    "📝 Paperless Lesson Notes & Handouts",
    "🌱 Sustainability & Ergonomics Impact",
    "📊 Student Progression Index"
])

# -----------------------------------------------------------------------------
# TAB 1: LIVE CLASSROOM MONITOR
# -----------------------------------------------------------------------------
with tab_monitor:
    st.subheader("🖥️ Real-time Student Focus Grid")
    st.caption("Monitor live note-taking status, focus scores, and identify disengaged students instantly without intrusive surveillance.")
    
    # Filter tools
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        status_filter = st.multiselect(
            "Filter by Status:",
            options=df_students["Current Status"].unique(),
            default=df_students["Current Status"].unique()
        )
    with col_f2:
        sort_by = st.selectbox("Sort Students By:", ["Focus Score (Low to High)", "Focus Score (High to Low)", "Name"])

    filtered_df = df_students[df_students["Current Status"].isin(status_filter)].copy()
    if sort_by == "Focus Score (Low to High)":
        filtered_df = filtered_df.sort_values("Focus Score (%)", ascending=True)
    elif sort_by == "Focus Score (High to Low)":
        filtered_df = filtered_df.sort_values("Focus Score (%)", ascending=False)
    else:
        filtered_df = filtered_df.sort_values("Name")

    # Display grid cards
    grid_cols = st.columns(4)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        col_idx = idx % 4
        with grid_cols[col_idx]:
            status_class = "status-active"
            if row["Current Status"] == "Idle":
                status_class = "status-warning"
            elif row["Current Status"] == "Potential Distraction":
                status_class = "status-danger"
                
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
                <div style="display:flex; justify-shadow:space-between; align-items:center; margin-bottom: 8px;">
                    <span style="font-weight:700; color:#111827; font-size:1rem;">{row['Name']}</span>
                </div>
                <div style="margin-bottom: 8px;">
                    <span class="{status_class}">{row['Current Status']}</span>
                </div>
                <div style="font-size:0.85rem; color:#4b5563; margin-top:8px;">
                    🎯 <b>Focus Score:</b> {row['Focus Score (%)']}%<br>
                    ✍️ <b>Notes Written:</b> {row['Notes Word Count']} words<br>
                    ⏱️ <b>Last Sync:</b> {row['Last Sync']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.popover(f"Actions for {row['Name'].split()[0]}"):
                st.write(f"**Manage {row['Name']}**")
                if st.button(f"📩 Send Gentle Ping", key=f"ping_{row['Student ID']}"):
                    st.toast(f"Ping sent to {row['Name']}", icon="🔔")
                if st.button(f"👁️ View Live Notes", key=f"view_{row['Student ID']}"):
                    st.info(f"Opening live note buffer for {row['Name']}...")

    # Real-time Focus Trend
    st.divider()
    st.subheader("📈 Live Classroom Attentiveness Timeline (Current Session)")
    
    minutes = [f"00:{i:02d}" for i in range(0, 50, 5)]
    focus_trend = [78, 82, 88, 85, 91, 89, 74, 86, 92, 90]
    note_speed = [12, 18, 25, 30, 28, 22, 15, 27, 31, 29]
    
    fig_timeline = go.Figure()
    fig_timeline.add_trace(go.Scatter(
        x=minutes, y=focus_trend, name="Avg Focus Score (%)",
        line=dict(color="#10b981", width=3)
    ))
    fig_timeline.add_trace(go.Bar(
        x=minutes, y=note_speed, name="Class Note Velocity (words/min)",
        yaxis="y2", opacity=0.3, marker_color="#047857"
    ))
    
    fig_timeline.update_layout(
        title="Classroom Engagement vs. Note-Taking Speed",
        xaxis_title="Class Time (MM:SS)",
        yaxis=dict(title="Focus Score (%)", range=[0, 100]),
        yaxis2=dict(title="Words Written / Min", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: PAPERLESS LESSON NOTES & HANDOUTS
# -----------------------------------------------------------------------------
with tab_notes:
    st.subheader("📝 Publish Digital Lesson Notes & Handouts")
    st.caption("Distribute structured notes directly to student devices to eliminate paper handouts and printing waste.")
    
    col_n1, col_n2 = st.columns([3, 2])
    
    with col_n1:
        with st.form("publish_note_form"):
            st.text_input("Lesson Topic Title", "Module 4: Planetary Boundaries & Resource Management")
            st.multiselect("Target Subject / Section", ["ENV-101 Sec A", "ENV-101 Sec B"], default=["ENV-101 Sec A"])
            st.text_area("Key Keynotes & Discussion Outlines (Markdown Supported)", 
"""### Today's Core Concepts:
1. **Planetary Boundaries**: Framework defining environmental limits within which humanity can safely operate.
2. **Key Stress Areas**:
   - Freshwater depletion in agriculture.
   - Land-system change & deforestation.
   - Atmospheric aerosol loading.

### Classroom Activity & Prompts:
* *Prompt 1*: Note down 3 ways our university campus can reduce direct paper usage in administrative offices.
* *Prompt 2*: Outline the trade-off between digital server energy use vs. paper manufacturing water footprint.
""", height=220)
            
            allow_offline = st.checkbox("Enable Offline Sync Mode (Students can edit without active Wi-Fi)", value=True)
            submitted = st.form_submit_button("🚀 Broadcast Paperless Handout", use_container_width=True)
            if submitted:
                st.success("Lesson handout published and synced to all 20 student EcoNotes apps!")

    with col_n2:
        st.markdown("### 📥 Student Note Submissions")
        st.caption("Recent student digital note uploads:")
        
        for name in df_students["Name"].head(4):
            with st.expander(f"📄 {name}'s Digital Notebook"):
                st.write(f"**Sync Status:** Synced offline buffer at {datetime.now().strftime('%H:%M')}")
                st.markdown(f"> *\"Discussed freshwater consumption in paper mills. Key takeaway: 1 ream of paper takes ~300 liters of water...\"*")
                st.slider(f"Grade / Feedback for {name.split()[0]}", 1, 10, 9, key=f"grade_{name}")

# -----------------------------------------------------------------------------
# TAB 3: SUSTAINABILITY & ERGONOMICS IMPACT
# -----------------------------------------------------------------------------
with tab_sustainability:
    st.subheader("🌱 Campus Ecological & Ergonomic Impact Calculator")
    st.caption("Quantifying the environmental benefits and student physical health improvements driven by EcoNotes.")
    
    # Interactive Slider for Institutional Scale
    st.markdown("#### 🏫 Scale Impact Projection")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        num_students = st.slider("Total Campus Students", 500, 10000, 2500, step=250)
    with col_s2:
        avg_notebooks = st.slider("Notebooks Used per Student/Yr", 4, 15, 10)
    with col_s3:
        avg_commute_km = st.slider("Avg Student Daily Commute (km)", 2, 25, 12)

    # Calculations
    total_notebook_pages = num_students * avg_notebooks * 160
    reams_saved = (total_notebook_pages * 0.6) / 500 # assuming 60% reduction via digital
    trees_saved = round(reams_saved / 16, 1)
    water_saved_liters = round(reams_saved * 350, 0)
    weight_reduced_kg = round(avg_notebooks * 0.6 * 0.45, 1) # ~0.45kg per notebook

    st.write("")
    st.markdown("### 📈 Projected Annual Campus Benefits")
    
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("📄 Paper Reams Saved", f"{int(reams_saved):,}")
    b2.metric("🌳 Trees Preserved", f"{trees_saved:,}")
    b3.metric("💧 Water Saved", f"{int(water_saved_liters):,} L")
    b4.metric("🎒 Backpack Load Reduced", f"-{weight_reduced_kg} kg / student")

    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Paper Savings Breakdown Chart
        categories = ["Lecture Notes", "Homework", "Exams & Quizzes", "Admin Forms"]
        paper_before = [1200, 600, 400, 300]
        paper_after = [240, 120, 100, 30]
        
        fig_paper = go.Figure(data=[
            go.Bar(name='Traditional Paper (Reams)', x=categories, y=paper_before, marker_color='#ef4444'),
            go.Bar(name='With EcoNotes (Reams)', x=categories, y=paper_after, marker_color='#10b981')
        ])
        fig_paper.update_layout(
            title="Paper Waste Reduction by Academic Category",
            barmode='group',
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_paper, use_container_width=True)

    with col_chart2:
        # Ergonomic Ergometer Survey
        ergo_labels = ["No Back/Shoulder Pain", "Mild Fatigue", "Moderate Back Strain", "Severe Musculoskeletal Strain"]
        ergo_values = [58, 28, 10, 4]
        
        fig_ergo = px.pie(
            names=ergo_labels, 
            values=ergo_values, 
            title="Student Reported Back Comfort (Post EcoNotes Rollout)",
            color_discrete_sequence=["#059669", "#34d399", "#fbbf24", "#f87171"],
            hole=0.4
        )
        fig_ergo.update_layout(height=320)
        st.plotly_chart(fig_ergo, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: STUDENT PROGRESSION INDEX
# -----------------------------------------------------------------------------
with tab_analytics:
    st.subheader("📊 Student Participation & Progression Index")
    st.caption("Combines live engagement, note completeness, and quiz response rates into an equitable academic progress indicator.")
    
    # Calculate composite score
    df_students["Progression Index"] = (
        (df_students["Focus Score (%)"] * 0.4) + 
        (df_students["Quiz Avg (%)"] * 0.4) + 
        (np.minimum(df_students["Notes Word Count"] / 4, 100) * 0.2)
    ).astype(int)

    # Scatter plot: Note Intensity vs Quiz Performance
    fig_scatter = px.scatter(
        df_students,
        x="Notes Word Count",
        y="Quiz Avg (%)",
        size="Focus Score (%)",
        color="Progression Index",
        hover_name="Name",
        title="Correlation: Note-Taking Intensity vs. Academic Outcome",
        labels={"Notes Word Count": "Notes Volume (Words Written)", "Quiz Avg (%)": "Quiz Average (%)"},
        color_continuous_scale="Greens"
    )
    fig_scatter.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("📋 Student Detail Roster")
    
    # Render searchable data frame
    st.dataframe(
        df_students[[
            "Student ID", "Name", "Current Status", "Focus Score (%)", 
            "Notes Word Count", "Pages Saved (Wk)", "Progression Index"
        ]],
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# FOOTER / ACTION BAR
# -----------------------------------------------------------------------------
st.divider()
st.caption("EcoNotes Project • Group Code: G03D05 • Broad Area: Reduction of Paper Usage & Enhanced Student Ergonomics")
`
