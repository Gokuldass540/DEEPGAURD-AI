# 🛡️ DEEPGUARD AI — AI-Based Deepfake Detection System

A complete, modern, attractive, and fully functional full-stack web application designed for detecting AI-generated and manipulated images and videos. Built as a college mini-project with a premium cybersecurity visual identity.

---

## 📌 Project Overview

**DeepGuard AI** allows users to upload images or videos and inspect them for facial manipulation, generative synthetic anomalies, and temporal inconsistencies.

### Key Features:
- 🔍 **Image & Video Upload Support**: Validates and processes `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov`, `.avi`.
- 👁️ **OpenCV Face Detection**: Automated face detection using OpenCV Haar cascades with cyan bounding box annotations and face crop extractions.
- 🎞️ **Configurable Video Sampling**: Sample N frames (10 to 60 frames) across video duration to analyze frame-by-frame temporal consistency.
- 🧠 **PyTorch Neural & Multi-Layer Feature Engine**: Fast Fourier Transform (FFT) power spectrum analysis, Laplacian blur variance, color chrominance distribution, combined with PyTorch MobileNet backbone.
- ⚙️ **Demo Mode Toggle**: Clearly separated Demo Mode toggle (`Demo Mode – AI model not yet connected`) for easy demonstration and model replacement.
- 📊 **Interactive Dashboard**: KPI metrics (Total Scans, Real Count, Fake Count, Avg Confidence) and Chart.js dynamic visualizations.
- 📜 **Detection History & Filters**: Searchable history table, media filters, verdict filters, and record deletion.
- 🛡️ **Role-Based Authentication**: Secure password hashing with Werkzeug, user accounts, and dedicated Admin Control Panel.
- 🎨 **Futuristic Cybersecurity UI**: Glassmorphism cards, dark navy theme (`#060911`), glowing cyan highlights, particle grid animations, responsive design.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Chart.js 4.x, FontAwesome 6 |
| **Backend** | Python 3.14, Flask 3.1.3, Werkzeug |
| **Database** | SQLite, SQLAlchemy ORM |
| **AI / ML & CV** | OpenCV 5.0, PyTorch 2.14, NumPy 2.5, Pillow 12.3, Scikit-Learn |

---

## 📁 Project Architecture

```
DeepGuard-AI/
├── app.py                      # Flask Application Entry Point
├── config.py                   # Configuration Settings
├── requirements.txt            # Package Dependencies
├── generate_demo_data.py       # Seed Script for Demo Data & Media
├── README.md                   # Complete Documentation
│
├── models/                     # SQLAlchemy Database Models
│   ├── __init__.py
│   ├── user.py                 # User Account Model & Password Hashing
│   └── detection.py            # Media Detection Result Model
│
├── routes/                     # Flask Blueprints / Controllers
│   ├── __init__.py
│   ├── auth.py                 # Register, Login, Profile, Logout
│   ├── dashboard.py            # User Dashboard & KPI Metrics
│   ├── detection.py           # Upload, API Pipeline, Result Page, History
│   └── admin.py                # Admin Console & User Management
│
├── ai/                         # Modular AI Engine
│   ├── __init__.py
│   ├── detector.py             # Main DeepGuard Detector Service
│   ├── preprocessing.py        # FFT Spectrum, Laplacian Blur, Color Variance
│   └── model_loader.py         # PyTorch Model Backbone & Custom Weight Loader
│
├── utils/                      # Helper Utilities
│   ├── __init__.py
│   ├── face_detection.py       # OpenCV Face Bounding Box & Cropping
│   ├── video_processing.py     # Video Frame Extraction & Frame Sampling
│   └── file_validation.py      # Filename Sanitization & Extension Validation
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Main Cyber Layout & Navigation
│   ├── index.html              # Landing Page (Hero, Capabilities, 5-Step Pipeline)
│   ├── login.html              # Authentication Login Page
│   ├── register.html           # Authentication Register Page
│   ├── profile.html            # Profile Settings Page
│   ├── dashboard.html          # User Dashboard & Chart.js Visualizations
│   ├── detection.html          # Drag-Drop Upload & Scanning Animation
│   ├── result.html             # Analysis Report & Circular Confidence Meter
│   ├── history.html            # Searchable Detection History Table
│   ├── about.html              # About Project & Problem/Solution
│   ├── admin.html              # Admin Management Panel
│   ├── 404.html                # Custom 404 Page
│   ├── 500.html                # Custom 500 Page
│   └── 413.html                # Custom File Size Error Page
│
├── static/                     # Static Web Assets
│   ├── css/
│   │   └── style.css           # Premium Dark Cyber Glassmorphism Styles
│   ├── js/
│   │   ├── app.js              # Particle Canvas & Flash Alert Dismissal
│   │   ├── detection.js        # Drag-Drop Handler & Progress Animation
│   │   └── dashboard.js        # Chart.js Dashboard Visualizations
│   └── uploads/                # User Uploaded Media & Face Crops
│
└── database/
    └── deepguard.db            # SQLite Database File
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisite
Ensure Python 3.10+ is installed on your system.

### 2. Navigate to Project Directory
```bash
cd DeepGuard-AI
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Demo Seed Data (Optional but Recommended)
```bash
python generate_demo_data.py
```

### 5. Launch the Server
```bash
python app.py
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🔐 Default Credentials

| Account Role | Email Address | Password |
|---|---|---|
| **Administrator** | `admin@deepguard.ai` | `Admin@123` |
| **Security Analyst (User)** | `user@deepguard.ai` | `User@123` |

---

## 📡 API Documentation

### Authentication Endpoints
- `POST /register`: Registers new user account
- `POST /login`: Authenticates user & sets session
- `GET /logout`: Terminates user session

### Detection Endpoints
- `POST /api/detect`: Uploads media file (Form-Data: `media`, `frame_count`, `demo_mode`) and returns detection JSON result.
- `GET /api/history`: Returns JSON list of user's past detection records (Query Params: `q`, `media_type`, `prediction`).
- `DELETE /api/history/<id>`: Deletes specific detection record.

### Admin Endpoints
- `GET /admin`: Admin management portal.
- `DELETE /admin/users/<id>`: Removes user account.
- `DELETE /admin/detections/<id>`: Removes detection record.

---

## 🚀 Future Scope
1. **Real-time Webcam Deepfake Inspection**: Continuous frame analysis directly from browser media streams.
2. **Browser Security Extension**: One-click social media image verification extension.
3. **Synthetic Audio Deepfake Detection**: Spectrogram analysis for voice cloning detection.

---

&copy; 2026 DeepGuard AI. College Mini-Project Implementation.
