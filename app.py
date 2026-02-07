import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
from utils.sheets_helper import save_feedback, connect_sheet
import os

# --- Page Config for Mobile ---
st.set_page_config(
    page_title="Department Feedback",
    page_icon="🏫",
    layout="centered"  # keeps things readable on mobile
)

# --- Custom CSS for Big Fonts & Attractive UI ---
st.markdown("""
    <style>
    /* Bigger titles */
    .css-10trblm, .css-1d391kg {
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
    }
    /* Bigger labels */
    label, .stTextInput label, .stSelectbox label, .stSlider label {
        font-size: 18px !important;
        font-weight: 600;
    }
    /* Input boxes */
    .stTextInput input, .stTextArea textarea {
        font-size: 16px !important;
        padding: 10px;
    }
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Sidebar styling */
    .css-1d391kg {
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏫 Department Facilities Feedback")

# --- Feedback Form (students can always submit) ---
location = st.selectbox("📍 Location", ["HOD Cabin", "IoT Lab", "SL1", "SL2", "Classroom 1", "Classroom 2"])
rating = st.slider("⭐ Condition Rating (1-5)", 1, 5, 3)
comment = st.text_area("💬 Comment (complaint, suggestion, or note)")

if st.button("Submit Feedback"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "Timestamp": timestamp,
        "Location": location,
        "Rating": rating,
        "Comment": comment
    }
    save_feedback(entry)
    st.success("✅ Feedback submitted successfully!")

# --- AUTHENTICATION LAYER ---
st.sidebar.header("🔒 Authorized Access")

PASSWORD = os.getenv("DASHBOARD_PASSWORD")
password_input = st.sidebar.text_input("Enter Dashboard Password", type="password")
submit_pass = st.sidebar.button("Unlock Dashboard")

if submit_pass:
    if PASSWORD is None:
        st.error("⚠️ No password set in environment. Please configure DASHBOARD_PASSWORD.")
    elif password_input == PASSWORD:
        st.success("✅ Access granted")
        st.header("📊 Facilities Feedback Dashboard")
        sheet = connect_sheet()
        data = pd.DataFrame(sheet.get_all_records())
        data.columns = data.columns.str.strip()

        if not data.empty:
            # Metrics
            st.metric("Average Condition Rating", round(data["Rating"].mean(), 2))
            st.metric("Total Feedback Entries", len(data))

            # Charts
            fig1 = px.bar(data, x="Location", y="Rating", title="Average Rating per Location", height=400)
            st.plotly_chart(fig1, use_container_width=True)

            fig2 = px.pie(data, names="Rating", title="Condition Rating Distribution", height=400)
            st.plotly_chart(fig2, use_container_width=True)

            fig3 = px.line(data, x="Timestamp", y="Rating", title="Condition Trend Over Time", height=400)
            st.plotly_chart(fig3, use_container_width=True)

            # Raw feedback with color-coded ratings
            st.subheader("📋 All Feedback Entries")
            def rating_color(val):
                if val <= 2:
                    return 'background-color: #ff9999'  # red
                elif val in [3, 4]:
                    return 'background-color: #fff799'  # yellow
                else:
                    return 'background-color: #99ff99'  # green

            st.dataframe(data.style.applymap(rating_color, subset=["Rating"]))
    else:
        st.error("❌ Incorrect password. Access denied.")
else:
    st.warning("🔒 Dashboard access restricted. Enter password and click Unlock.")