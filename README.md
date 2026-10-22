# HalluciGuard AI
### LLM Hallucination Detection & Prompt Evaluation Platform

**Evaluating AI-generated responses. Comparing prompt strategies. Making LLM reliability more measurable.**

HalluciGuard AI is a web-based platform designed to evaluate the reliability of Large Language Model (LLM) responses. It analyzes generated content for potential hallucinations using semantic similarity analysis, rule-based validation, and response quality evaluation. It also compares multiple prompt engineering strategies to help identify responses with lower estimated hallucination risk.

Built with Django and Python, the platform integrates Google's Gemini API with an evaluation pipeline, interactive analytics, historical tracking, and downloadable reports.

---

## Overview

Large Language Models can generate convincing responses that contain fabricated facts, unsupported claims, or inconsistencies. Fluency alone does not guarantee factual correctness, making systematic response evaluation an important part of building reliable AI applications.

HalluciGuard AI addresses this challenge by providing a structured workflow for testing prompts, analyzing generated responses, comparing evaluation metrics, and reviewing results through a web interface.

### Key Capabilities

- **Hallucination Risk Analysis** — Evaluate responses for potential hallucinations using semantic and rule-based checks.
- **Prompt Strategy Comparison** — Test multiple prompt variations against the same query and compare their outputs.
- **Multi-Metric Evaluation** — Analyze responses across hallucination, accuracy, confidence, consistency, fluency, semantic similarity, and factual consistency metrics.
- **Interactive Analytics** — Visualize response evaluation results and prompt performance.
- **Historical Tracking** — Store and revisit previous queries and analysis results.
- **Report Generation** — Export evaluation reports to Excel for further analysis.
- **User & Admin Management** — Support authentication, user management, and administrative activity monitoring.

## System Architecture

HalluciGuard AI follows a modular architecture that separates the web interface, application logic, LLM integration, evaluation pipeline, and data persistence.

```text
                User Query
                    |
                    v
          Django Web Application
                    |
                    v
           Prompt Generation
                    |
                    v
           Gemini API Integration
                    |
                    v
           Generated Responses
                    |
                    v
          Hallucination Analyzer
          /         |          \
         v          v           v
     Semantic    Rule-Based   Quality
     Analysis    Validation   Scoring
          \         |          /
                    v
          Response Comparison
                    |
             +------+------+
             |             |
             v             v
        Analytics      Report Export
             |             |
             +------+------+
                    |
                    v
             SQLite Database
```

*Architecture overview: conceptual representation of the documented system workflow.*

## Evaluation Pipeline

The platform organizes response evaluation into the following stages:

1. **Query Processing** — Accept a user query through the web interface.
2. **Prompt Generation** — Create multiple prompt variations using different prompting strategies.
3. **Response Generation** — Send prompts to the Gemini API and collect generated responses.
4. **Response Analysis** — Apply the implemented semantic similarity and rule-based evaluation techniques.
5. **Comparative Evaluation** — Compare response metrics and rank prompt strategies based on the configured evaluation criteria.
6. **Visualization & Reporting** — Present results through dashboards, preserve analysis history, and generate downloadable reports.

## Evaluation Metrics

| Metric | Purpose |
|---|---|
| Hallucination Score | Estimates potential hallucination risk |
| Accuracy Score | Represents the system's configured response accuracy assessment |
| Confidence Score | Represents the configured confidence assessment |
| Consistency Score | Evaluates consistency according to the implemented checks |
| Fluency Score | Assesses response fluency |
| Semantic Similarity | Measures semantic similarity between evaluated text |
| Factual Consistency | Assesses factual consistency using the implemented evaluation approach |

**Evaluation note:** These metrics provide structured indicators of response quality. Their reliability depends on the underlying scoring methods, validation data, and evaluation criteria. A low hallucination score does not independently prove that a response is factually correct.

## Technology Stack

**Backend**
- Python
- Django

**LLM Integration**
- Google Gemini API

**AI / NLP**
- Natural Language Processing (NLP)
- Semantic Similarity Analysis
- Rule-Based Validation
- Prompt Engineering
- Response Quality Evaluation

**Database & Data Processing**
- SQLite
- Pandas

**Frontend & Visualization**
- HTML
- CSS
- JavaScript
- Chart-Based Data Visualization

## Project Structure

```text
HalluciGuardAI/
├── analytics/                 # Analytics and reporting
├── authentication/            # User authentication
├── custom_admin/              # Administrative functionality
├── hallucination_detector/    # Response evaluation logic
│   └── analyzer.py
├── hallucination_project/     # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── llm_api/                   # Gemini API integration
│   └── gemini_client.py
├── prompt_engine/             # Prompt generation and evaluation
│   └── prompt_generator.py
├── static/                    # CSS and JavaScript assets
├── templates/                 # Django HTML templates
├── .env.example               # Environment variable template
├── .gitignore
├── manage.py
├── requirements.txt
├── PROJECT_STRUCTURE.md
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9 or later
- Git
- A Google Gemini API key
- Internet connectivity for API access

### 1. Clone the repository

```bash
git clone https://github.com/SreejaShetty01/HalluciGuardAI.git
cd HalluciGuardAI
```

### 2. Create a virtual environment

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure the variables expected by your application.

Example:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Use the exact variable name expected by the Gemini API integration in your code. Store the real API key only in your local `.env` file and never commit it to Git.

### 5. Initialize the database

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the local development address displayed by Django in your terminal, typically:

`http://127.0.0.1:8000/`

*Setup note: The commands assume the project uses Django's standard management workflow. Additional configuration may be required depending on the current application settings and installed dependencies.*

## Security Considerations

- Keep API keys and credentials in environment variables.
- Never commit `.env` files containing real secrets.
- Use `.env.example` only for placeholder values.
- Configure Django's `DEBUG` setting appropriately before deployment.
- Use a strong, environment-specific Django `SECRET_KEY`.
- Restrict access to user data, historical queries, and generated reports.
- Rotate any API credentials that may have been exposed in Git history.

## Current Scope & Limitations

HalluciGuard AI provides a structured approach to evaluating LLM outputs, but automated scoring has limitations.

- Semantic similarity does not independently establish factual truth.
- Rule-based checks can miss subtle or context-dependent hallucinations.
- Evaluation scores should not be interpreted as calibrated probabilities unless validated accordingly.
- The current documented implementation integrates Gemini; multi-model comparison is a potential extension.
- Retrieval-Augmented Generation (RAG), external knowledge verification, and advanced evidence-grounded fact-checking are future enhancements, not assumed current capabilities.

## Future Enhancements

- **Multi-LLM Evaluation:** Compare responses from Gemini, GPT, Claude, and open-source models.
- **Evidence-Grounded Verification:** Integrate Retrieval-Augmented Generation and trusted knowledge sources to validate factual claims.
- **Advanced Detection Models:** Explore learned hallucination classifiers and more sophisticated factual consistency methods.
- **Explainable Evaluation:** Show why a response receives a particular score or risk assessment.
- **Domain-Specific Evaluation:** Introduce tailored evaluation criteria for research, education, healthcare, and other domains.
- **Multilingual Analysis:** Extend response evaluation to additional languages.
- **Evaluation Benchmarking:** Test the framework against labeled datasets and report precision, recall, F1-score, and other suitable metrics.

## Contributing

Contributions, bug reports and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request describing the changes and validation performed.

---

*HalluciGuard AI — Building more transparent and measurable evaluation workflows for AI-generated content.*
