# 📘 Imperial Adaptive Learning Scheduler

> An intelligent, data-driven student planner for Imperial College that integrates learning analytics, personalized scheduling, and machine learning–powered fail-risk predictions.

---

## 🚀 Overview

**Imperial Adaptive Learning Scheduler** is a web platform that helps Imperial students organize their studies effectively.

It combines personalized time management, module material ratings, and adaptive scheduling powered by machine learning.

Students log in with their **Imperial email and password**, view their modules, rate learning materials, and receive **AI-generated study plans** that dynamically adapt to their real learning behavior.

---

## ✨ Key Features

### 🔐 Authentication
- Secure login via **Imperial email + password**
- User sessions managed securely

### 📚 Modules & Materials
- Each module displays uploaded materials (lecturer slides, Panopto recordings, notes, etc.)
- Students can **rate materials** (1–5 stars + comments) for usefulness
- Aggregated usefulness score displayed for each material
- Search, sort, and filter materials by lecturer, date, or usefulness

### 🗓️ Calendar Integration
- Import **Outlook calendar** files (CSV/JSON/ICS)
- Visual calendar event preview
- Drag & drop file upload
- Show timeline views with color-coded events

### 🧠 Adaptive Scheduling (ML-powered)
- Machine learning model estimates how long each assignment should take
- Generates **personalized time allocations**
- Automatically reschedules if a task is missed

---

## 🛠️ Setup

### Requirements
- Python 3.11+
- PostgreSQL (optional, for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd team-a
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**
   ```bash
   python main.py
   ```

4. **Access the application**
   - Main App: http://localhost:8080/app
   - Login: http://localhost:8080/
   - API Docs: http://localhost:8080/docs

---

## 🧩 System Architecture

| Layer | Components | Tech Stack |
|-------|-------------|------------|
| **Frontend** | Modules, Calendar UI | HTML, CSS, JavaScript |
| **Backend API** | Auth, Modules, Ratings, Calendar Sync, Scheduler | Python (FastAPI) |
| **Database** | (In-memory for development, PostgreSQL ready) | Python Dicts / PostgreSQL |
| **Machine Learning** | Time estimation, fail-risk prediction | Python (scikit-learn) |
| **Scheduling Engine** | Optimized study block allocation | Custom heuristic |

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Login with email and password |
| `POST` | `/api/auth/signup` | Create account |
| `GET` | `/api/modules` | List all modules |
| `GET` | `/api/modules/{id}/materials` | Get module materials & ratings |
| `POST` | `/api/materials/{id}/rate` | Submit a rating/comment |
| `POST` | `/api/assignments` | Create assignment |
| `GET` | `/api/ml/predict` | Predict fail-risk and time allocation |

Full API documentation available at: http://localhost:8080/docs

---

## 📁 Project Structure

```
team-a/
├── app/                  # Main application
│   ├── api/             # FastAPI routes
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   └── static/          # Frontend (HTML, CSS, JS)
├── backend/             # Database & JWT auth (for production)
├── data/                # Dataset files
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🚀 Quick Start

1. **Start server:**
   ```bash
   python main.py
   ```

2. **Open browser:**
   - http://localhost:8080/

3. **Create account:**
   - Use Imperial email: `test@imperial.ac.uk`
   - Password: (8+ characters)

4. **Access app:**
   - http://localhost:8080/app

---

## 📝 License

This project is part of the ILA Hackathon 2025.

---

## 👥 Team

Imperial College London - Hackathon Team
