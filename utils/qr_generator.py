# utils/qr_generator.py
import qrcode
import os

# List of locations
locations = [
    "HOD_Cabin_AIDS",
    "IoT_Lab",
    "SL1_Lab",
    "SL2_Lab",
    "Classroom_1",
    "Classroom_2"
]

# Base URL of your Streamlit app (replace with your deployed link later)
BASE_URL = "https://dept-feedback.streamlit.app/"

# Absolute output folder path
output_dir = r"C:\Users\RUPESH PATARE\Desktop\dept-feedback-app\asset\qr_codes"
os.makedirs(output_dir, exist_ok=True)

for loc in locations:
    url = f"{BASE_URL}?location={loc}"
    qr = qrcode.make(url)
    file_path = os.path.join(output_dir, f"{loc}.png")
    qr.save(file_path)
    print(f"Saved QR code: {file_path}")

print("All QR codes generated successfully!")