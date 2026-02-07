import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheet(sheet_name="Department Feedback"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "config/credentials.json", scope
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