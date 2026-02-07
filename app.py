import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
from utils.sheets_helper import save_feedback, connect_sheet, delete_feedback
import os

# --- Page Config for Mobile ---
st.set_page_config(
    page_title="Department Feedback",
    page_icon="🏫",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .css-10trblm, .css-1d391kg {
        font-size: 28px !important;
        font-weight: bold;
        text-align: center;
    }
    label, .stTextInput label, .stSelectbox label, .stSlider label {
        font-size: 18px !important;
        font-weight: 600;
    }
    .stTextInput input, .stTextArea textarea {
        font-size: 16px !important;
        padding: 10px;
    }
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
    .css-1d391kg {
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏫 Department Facilities Feedback")

# --- Feedback Form ---
location = st.selectbox("📍 Location", ["HOD Cabin", "IoT Lab", "SL1", "SL2", "Classroom 1", "Classroom 2"])
rating = st.slider("⭐ Condition Rating (1-5)", 1, 5, 3)
comment = st.text_area("💬 Comment (complaint, suggestion, or note)")

if st.button("Submit Feedback"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Timestamp": timestamp, "Location": location, "Rating": rating, "Comment": comment}
    save_feedback(entry)
    st.success("✅ Feedback submitted successfully!")

# --- AUTHENTICATION LAYER ---
st.sidebar.header("🔒 Authorized Access")
PASSWORD = os.getenv("DASHBOARD_PASSWORD")

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if not st.session_state.unlocked:
    password_input = st.sidebar.text_input("Enter Dashboard Password", type="password")
    if st.sidebar.button("Unlock Dashboard"):
        if PASSWORD is None:
            st.error("⚠️ No password set in environment. Please configure DASHBOARD_PASSWORD.")
        elif password_input == PASSWORD:
            st.session_state.unlocked = True
            st.success("✅ Access granted")
        else:
            st.error("❌ Incorrect password. Access denied.")

# --- Dashboard (only if unlocked) ---
if st.session_state.unlocked:
    st.header("📊 Facilities Feedback Dashboard")

    # Load and clean data
    sheet = connect_sheet()
    data = pd.DataFrame(sheet.get_all_records())
    data.columns = [str(c).strip() for c in data.columns]
    data = data.dropna(how="all")
    data.reset_index(drop=True, inplace=True)
    data.insert(0, "Row Index", data.index)

    if not data.empty:
        # Metrics
        if "Rating" in data.columns:
            st.metric("Average Condition Rating", round(data["Rating"].mean(), 2))
        st.metric("Total Feedback Entries", len(data))

        # Simple Pie Chart
        if "Rating" in data.columns:
            st.subheader("📊 Rating Distribution")
            pie_data = data["Rating"].value_counts().reset_index()
            pie_data.columns = ["Rating", "Count"]
            st.plotly_chart(
                px.pie(pie_data, names="Rating", values="Count", title="Feedback by Rating"),
                use_container_width=True
            )

        # Feedback Table
        st.subheader("📋 All Feedback Entries (Row Index = 0 to n-1)")

        def rating_color(val):
            try:
                val = int(val)
                if val <= 2:
                    return 'background-color: #ff9999'
                elif val in [3, 4]:
                    return 'background-color: #fff799'
                else:
                    return 'background-color: #99ff99'
            except:
                return ''

        if "Rating" in data.columns:
            st.dataframe(data.style.applymap(rating_color, subset=["Rating"]))
        else:
            st.dataframe(data)

        # Delete Section
        st.subheader("🗑️ Delete Feedback Entry")
        row_index = st.number_input(
            "Select row index to delete (starts from 0)", 
            min_value=0, 
            max_value=len(data) - 1, 
            step=1
        )
        if st.button("Delete Row"):
            sheet.delete_rows(row_index + 2)  # +2 to skip header and match Google Sheets indexing
            st.success(f"✅ Row {row_index} deleted successfully!")

            # Refresh data
            sheet = connect_sheet()
            data = pd.DataFrame(sheet.get_all_records())
            data.columns = [str(c).strip() for c in data.columns]
            data = data.dropna(how="all")
            data.reset_index(drop=True, inplace=True)
            data.insert(0, "Row Index", data.index)

            if "Rating" in data.columns:
                st.dataframe(data.style.applymap(rating_color, subset=["Rating"]))
            else:
                st.dataframe(data)
    else:
        st.info("No feedback entries found.")