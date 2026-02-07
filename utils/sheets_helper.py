import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

def connect_sheet(sheet_name="Department Feedback"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def save_feedback(entry):
    sheet = connect_sheet()
    sheet.append_row([
        entry["Timestamp"],
        entry["Location"],
        entry["Rating"],
        entry["Comment"]
    ])

def delete_feedback(row_number):
    sheet = connect_sheet()
    sheet.delete_rows(row_number)