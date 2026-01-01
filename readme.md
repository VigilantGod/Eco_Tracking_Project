# EcoTrack Logistics System (RAD Prototype)

**Team Group:** [Insert Group Number]  
**Unit:** CCS1562 - Rapid Application Development  
**Client:** EcoTrack Logistics  
**Deadline:** January 16, 2026

---

## Project Overview
This project is a web-based prototype designed for **EcoTrack Logistics**. It serves as a centralized platform for:
1.  **Parcel Tracking:** Real-time tracking simulation using GPS logic.
2.  **Route Optimization:** Calculating the shortest path and lowest CO₂ emissions.
3.  **Customer Support:** A ticketing system for managing delivery issues.

**Technology Stack:**
* **Language:** Python 3.10+
* **Framework:** Streamlit (for Rapid Prototyping)
* **Mapping:** Folium & OpenStreetMap
* **Database:** SQLite (Built-in)

---

## Setup Instructions (Read Carefully)

### 1. Prerequisites
Ensure you have **Python** installed.
* Check by running: `python --version` in your terminal.

### 2. Clone the Repository
```bash
git clone 
cd EcoTrack_System

### 3.Install required packages
`pip install -r requirements.txt`

### Run the app.py
`streamlit run app.py`

# Project Structure
EcoTrack_System/
├── app.py                  # MAIN FILE (Traffic Controller - Run this!)
├── requirements.txt        # List of required packages
├── modules/                # ⚠️ DEV TEAM WORK HERE
│   ├── auth.py             # Login/Register Logic
│   ├── tracking.py         # Parcel Tracking & Map Logic (Dev 3)
│   ├── routing.py          # Route Optimization Algorithms (Dev 3)
│   └── ticketing.py        # Customer Support Forms (Dev 4)
├── data/
│   └── ecotrack.db         # Database (Auto-generated, do not delete)
├── docs/                   # User Manuals & Tech Docs (Team 4 & 5)
└── assets/                 # Images & Logos