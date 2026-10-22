# 🧠 HalluciGuard AI
## Prompt Engineering Based Hallucination Reduction in Large Language Models

A production-ready Django web application for comparing prompt engineering techniques and analyzing AI hallucination rates using the Google Gemini API. It features a custom administrative console, user directories, platform-wide theme synchronization, and robust role boundaries.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **4 Prompt Types** | Zero-Shot, Few-Shot, Chain-of-Thought, Role-Based prompt comparison |
| **Gemini API Integration** | Real responses from Google Gemini Pro API client |
| **Hallucination Analysis** | Hybrid rule-based + semantic + keyword overlap detection engine |
| **6 Chart Types** | Interactive Bar, Pie, Radar, Area, Heatmap analytics + comparison summaries |
| **Excel Export** | Download detailed analysis data tables as `.xlsx` spreadsheets |
| **User Authentication** | User signups, sign-ins, sign-outs, and session management |
| **Deactivated Signup Flow** | New researcher accounts are **deactivated by default** until approved by an administrator |
| **Custom Admin Module** | Secure separate administrative console to manage, update, delete, and toggle user active states |
| **Default Admin Credentials** | Initial secure administration default account: `admin` / `admin` (stored as database hashed) |
| **Synchronized Theme Toggle** | Persistent, platform-wide White (Light) and Dark mode switching using `hg_theme` |
| **Glassmorphism UI** | Premium AI analytics dashboard aesthetics with dynamic layout elements |
| **Responsive Design** | Fluid layouts optimized for desktop, tablet, and mobile browsers |

---

## 📁 Project Directory Summary

* **`hallucination_project/`**: Main Django configuration root (routing, settings).
* **`authentication/`**: Handles user registrations, custom logins, and secure activity logging.
* **`custom_admin/`**: Implements custom administrator tables, dashboard stats, and user directory update/activation controls.
* **`prompt_engine/`**: Generates and submits comparative prompt templates to standard LLM endpoints.
* **`llm_api/`**: Google Gemini API client wrapper.
* **`hallucination_detector/`**: Factual consistency, rule matching, and keyword overlap scoring engine.
* **`templates/`**: Premium HTML layouts, base structures, user dashboard grids, and custom admin directories.
* **`static/`**: Core CSS stylesheets (`main.css` with dynamic theme variables) and JS dashboard helpers (`dashboard.js`).

---

## ⚙️ Setup & Installation Instructions

### 1. Extract the project and enter the folder
```bash
unzip hallucination_project.zip
cd hallucination_project
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and set your configuration values:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key-here
```

### 5. Get a Gemini API Key (Free)
1. Navigate to **https://aistudio.google.com/**
2. Click **"Get API Key"**
3. Generate a new API Key, copy it, and paste it into your `.env` file.

### 6. Run database migrations
```bash
python manage.py makemigrations authentication
python manage.py makemigrations prompt_engine
python manage.py makemigrations custom_admin
python manage.py migrate
```

### 7. Start the development server
```bash
python manage.py runserver
```

---

## 🔑 Administrative Sign In & Portal Actions

Newly registered accounts are deactivated by default. To review, activate, deactivate, update, or delete accounts, sign in to the **Custom Admin Console**:

| URL Endpoint | Description |
|---|---|
| **`/custom-admin/login/`** | Secure admin login card. Use default admin credentials: `admin` / `admin` |
| **`/custom-admin/dashboard/`** | Administrative metrics dashboard (Total Users, Active, Pending, AI Queries) |
| **`/custom-admin/users/`** | Searchable User Directory to activate/deactivate, edit details, or delete accounts |

---

## 🌐 Complete Route Index

| URL Endpoint | Target Page Description |
|---|---|
| **`http://127.0.0.1:8000/`** | Platform landing homepage (features theme-aware light/dark grids) |
| **`http://127.0.0.1:8000/auth/login/`** | Standard Researcher Sign In |
| **`http://127.0.0.1:8000/auth/register/`** | Standard Researcher Signup (enters deactivated state showing warning) |
| **`http://127.0.0.1:8000/dashboard/`** | Core User Dashboard (for activated standard users) |
| **`http://127.0.0.1:8000/dashboard/test/`** | comparative prompt playground tests |
| **`http://127.0.0.1:8000/analytics/`** | ApexCharts graphical evaluation charts |
| **`http://127.0.0.1:8000/custom-admin/login/`** | Secure administrative credentials sign-in portal |

---

## 📊 Hallucination Evaluation Logic

The automated `HallucinationAnalyzer` combines multiple analytical techniques:
1. **Factual Consistency**: Evaluates semantic alignment between query requirements and responses.
2. **Rule-Based Patterns**: Detects overconfidence qualifiers, evasive language, and hedging indicators.
3. **Keyword Overlap**: Compares keyword overlaps between the primary query and outputs.
4. **Composite Score Weights**:
   - Factual consistency: 40%
   - Confidence score: 30%
   - Keyword overlap: 30%

Responses exceeding a **42% hallucination rating** are flagged automatically as `is_hallucinated = True`.

---

## 📄 License
MIT License — Feel free to use, modify, and distribute.
