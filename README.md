# 🏫 Department Facilities Feedback Dashboard

A secure, mobile‑friendly feedback system built with **Streamlit**, **Google Sheets**, and **Plotly**.  
This app allows students to submit complaints, suggestions, or notes about college facilities, while faculty can view, analyze, and manage feedback through a password‑protected dashboard.

---

## ✨ Features
- 📋 **Feedback Form** – Students can submit location, rating, and comments.
- 🔒 **Authentication Layer** – Password‑protected faculty dashboard.
- 📊 **Analytics Dashboard** – Average ratings, total entries, and pie chart distribution.
- 🗑️ **Row Deletion** – Faculty can remove outdated or invalid feedback entries.
- 📱 **Mobile‑Friendly UI** – Enlarged text, styled buttons, and expandable feedback cards.
- ☁️ **Cloud Deployment** – Hosted on Streamlit Cloud with secure secrets management.

---

## 🚀 Live Demo
👉 [Open the Dashboard]((https://rupesh-cpu-dept-feedback-app-app-xxgqmh.streamlit.app/))

---

## 🛠️ Tech Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Database**: Google Sheets (via `gspread` + service account)
- **Visualization**: Plotly Express
- **Authentication**: Environment variable (`DASHBOARD_PASSWORD`) stored in Streamlit Secrets

---

## 📂 Project Structure
