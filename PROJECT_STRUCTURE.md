# Codebase Directory Structure & Architectural Overview
This document outlines the directory structure, component responsibilities, and architectural patterns implemented in the **HalluciGuard AI** project.

---

## 📁 Codebase Directory Tree

```text
hallucination_project/
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # System dependencies
├── db.sqlite3                  # Platform database (SQLite)
├── .env.example                # Environment variables template
├── README.md                   # Main setup & features manual
├── PROJECT_STRUCTURE.md        # This structure blueprint file
│
├── hallucination_project/      # Root Django Configuration
│   ├── __init__.py
│   ├── settings.py            # Global settings, installed apps, theme parameters
│   ├── urls.py                # Main system routing maps (includes app urls)
│   ├── wsgi.py                # WSGI gateway config
│   └── asgi.py                # ASGI gateway config
│
├── authentication/             # User Auth & Activity Log Module
│   ├── __init__.py
│   ├── admin.py               # Auth model registries
│   ├── apps.py
│   ├── forms.py               # RegisterForm (deactivated signup), LoginForm
│   ├── models.py              # UserProfile (metadata), ActivityLog (auditing)
│   ├── urls.py                # Standard auth routes
│   └── views.py               # login_view, register_view (deactivated by default), logout_view
│
├── custom_admin/               # Administrative Control App
│   ├── __init__.py
│   ├── apps.py
│   ├── forms.py               # AdminLoginForm, UserUpdateForm (edit users & bio)
│   ├── models.py              # AdminAccount model (auto-hashing, default credentials)
│   ├── urls.py                # Admin portal route mappings
│   └── views.py               # dashboard, users searchable lists, toggle activation, update, delete
│
├── prompt_engine/              # Prompt Test & Evaluation Hub
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # PromptHistory, Response, HallucinationReport, ModelComparison
│   ├── prompt_generator.py    # Zero-Shot, Few-Shot, CoT, Role prompt compilation
│   ├── urls.py                # Evaluation portal paths
│   └── views.py               # user_dashboard, prompt_test, compare_responses, Excel export
│
├── llm_api/                    # LLM Connector Layer
│   ├── __init__.py
│   └── gemini_client.py       # Google Gemini Pro connection wrapper & rate logging
│
├── hallucination_detector/     # Quantitative Evaluation Engine
│   ├── __init__.py
│   └── analyzer.py            # factual consistency, keyword overlap, pattern scoring
│
├── templates/                  # Frontend Layout Templates
│   ├── base.html              # Core user platform base grid, collapsible sidebar, theme icon controls
│   ├── auth/
│   │   └── auth_combined.html # Slidable signup/signin cards (with float theme toggle)
│   ├── dashboard/
│   │   ├── home.html          # Dynamic landing homepage (with navbar theme switcher)
│   │   └── user_dashboard.html# Activated researcher statistics & summary panels
│   ├── prompts/
│   │   ├── test.html          # Playground playground submission form
│   │   ├── compare.html       # Side-by-side prompt comparisons & ApexCharts radars
│   │   └── history.html       # Test histories and excel downloads
│   ├── analytics/
│   │   └── dashboard.html     # High-end chart evaluations
│   └── custom_admin/          # Premium Administrative templates
│       ├── base.html          # Dedicated admin layout, secure sidebar & theme sync
│       ├── login.html         # Admin login card (with float theme toggle)
│       ├── dashboard.html     # Administrative metrics panels & recent lists
│       ├── users.html         # Interactive searchable table, toggles, edit & delete buttons
│       └── edit_user.html     # User details modification forms
│
└── static/                     # Assets & Static files
    ├── css/
    │   └── main.css           # Premium styling sheet, theme variable definitions (HSL)
    └── js/
        └── dashboard.js       # theme loaders (hg_theme), toggles, spinners, counters
```

---

## 🛠️ App Responsibilities & File Roles

### 1. Root Configuration (`hallucination_project`)
Defines the engine base, connects databases, registers middleware, and distributes incoming requests.
- **[settings.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/hallucination_project/settings.py)**: Configures SQLite database engines, registers installed apps (including `custom_admin`), manages static assets, and configures Django crispy-forms.
- **[urls.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/hallucination_project/urls.py)**: Maps administrative URLs and includes app routing folders.

### 2. User Authentication (`authentication`)
Manages standard researcher accounts and audits active logins.
- **[models.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/authentication/models.py)**: Defines `UserProfile` extending the standard `User` (captures Gemini API keys, total queries, bio details) and `ActivityLog` to record audit trails.
- **[views.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/authentication/views.py)**: Sets user state `is_active = False` on registration, disables auto-login, redirects users with a descriptive block warn, and intercepts deactivated logins with clear notifications.

### 3. Custom Admin Panel (`custom_admin`)
Provides dedicated oversight of standard users, databases, and platform query logs.
- **[models.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/custom_admin/models.py)**: Encapsulates `AdminAccount` credentials. Password values are automatically hashed using Django's PBKDF2 on save. Pre-populates the database with `admin` / `admin` on initial login load if absent.
- **[forms.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/custom_admin/forms.py)**: Implements validation forms. `UserUpdateForm` binds core `User` model changes and `UserProfile` bio details changes into a single save transaction.
- **[views.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/custom_admin/views.py)**: Restricts admin panels via the secure `@admin_required` decorator, lists user directories using dynamic case-insensitive SQL searches, activates/deactivates accounts, edits user info, and removes accounts securely.

### 4. Prompt Engineering Hub (`prompt_engine`)
Takes query inputs, constructs comparative prompts, and generates reports.
- **[prompt_generator.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/prompt_engine/prompt_generator.py)**: Holds template scripts to compile **Zero-Shot**, **Few-Shot**, **Chain-of-Thought (CoT)**, and **Role-Based** prompts.
- **[views.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/prompt_engine/views.py)**: Receives test queries, passes prompt outputs to the model endpoints, logs accuracy analytics, exports xlsx reports using Pandas, and renders comparisons.

### 5. LLM API Client (`llm_api`)
- **[gemini_client.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/llm_api/gemini_client.py)**: Core handler wrapper querying the Google Gemini Pro API safely. Tracks connection latencies, token counts, and API exception logs.

### 6. Hallucination Engine (`hallucination_detector`)
- **[analyzer.py](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/hallucination_detector/analyzer.py)**: Evaluates response outputs, counting keyword overrides, testing matching confidence metrics, checking hedging dictionaries, and returning weighted scoring percentages.

---

## 🎨 Theme & Styling Architecture

The visual layout employs a professional **Glassmorphism Design System** that translates dynamically between Light (White) and Dark modes:
- **HSL Theme Variables**: Inside **[main.css](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/static/css/main.css)**, all background textures, borders, card fills, and text layers are tied to theme variables (`var(--bg-primary)`, `var(--text-1)`, etc.) which switch values automatically under the `[data-theme="light"]` attribute selector.
- **Homepage Light Gradients**: The landing homepage features custom variable gradients (`var(--bg-hero)` and `var(--hero-text-grad)`) that shift automatically to slate-white gradients and deep-indigo text headers in light mode to preserve readability.
- **Theme Synchronization**: The JavaScript toggle helper **[dashboard.js](file:///c:/Users/lenovo/Downloads/hallucination_project/hallucination_project/static/js/dashboard.js)** saves theme selection under a unified `localStorage` key `hg_theme` and synchronizes the state instantly on page load across all modules.
