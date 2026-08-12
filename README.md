# Advanced AI Medical Intelligence Platform 🫁🤖

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg)](.github/workflows/ci-cd.yml)

> An end-to-end medical decision support system featuring **Deep Learning Disease Classification**, **Explainable AI (Grad-CAM)** visual attention heatmaps, **LLM Clinical Report Generation (Groq Llama-3.1)**, **FastAPI REST API**, **SQLAlchemy SQLite Persistence**, and a **Dark Glassmorphism Streamlit Dashboard**.

---

## 🌟 Key Features

1. **Medical Image Analysis & Deep Learning**
   - Classifies Chest X-Rays into **PNEUMONIA** vs. **NORMAL** with exact confidence scores.
   - Powered by a fine-tuned **EfficientNet-B0** PyTorch model (`models/checkpoints/best_efficientnet_b0.pth`).

2. **Explainable AI (Grad-CAM XAI)**
   - Visualizes critical lung regions guiding model predictions using `pytorch-grad-cam`.
   - Interactive dashboard controls for **Heatmap**, **Overlay**, and **Original** image views.

3. **AI-Assisted Medical Report Generation**
   - Generates structured clinical reports (*Summary*, *Key Findings*, *Recommendations*, *Disclaimer*) using **Groq API (`llama-3.1-8b-instant`)**.
   - Includes automatic rule-based fallback generation and **One-Click PDF Report Download (`fpdf2`)**.

4. **Production REST API Engine**
   - Built with **FastAPI** offering `/health`, `/predictions/analyze`, and `/predictions/history` endpoints.
   - Interactive Swagger API documentation at `/docs`.

5. **Patient History & SQLite Persistence**
   - Automatically logs prediction records, confidence scores, Grad-CAM output paths, and generated reports into `medical_intelligence.db`.

6. **Containerization & CI/CD Pipeline**
   - Multi-stage **Dockerfile** (Python 3.11) & **`docker-compose.yml`**.
   - **GitHub Actions Workflow** (`.github/workflows/ci-cd.yml`) automating `ruff` linting, `pytest` unit testing, and Docker builds.

---

## 📂 Project Architecture

```text
Advanced AI Medical Intellegence/
├── .github/workflows/       # GitHub Actions CI/CD pipeline (ci-cd.yml)
├── app/                      # Backend Core & API Architecture
│   ├── api/                  # FastAPI REST routes (health, prediction, history)
│   ├── core/                 # Configuration & settings management
│   ├── database/             # SQLAlchemy DB models & SQLite session manager
│   ├── llm/                  # Groq LLM integration & report schemas
│   ├── ml/                   # EfficientNet-B0 architecture & Grad-CAM XAI engine
│   └── services/             # PredictionService pipeline orchestrator
├── data/                     # Upload storage & raw image dataset splits
├── models/                   # PyTorch checkpoints (best_efficientnet_b0.pth) & XAI outputs
├── scripts/                  # Training, evaluation, and dataset setup utility scripts
├── streamlit_app/            # Streamlit Dashboard Frontend
│   ├── app.py                # Main multi-page Streamlit application
│   ├── components.py         # UI cards, KPI metrics, PDF generator & Cloud banner
│   ├── styles.py             # Dark Navy Glassmorphism CSS design system
│   └── api_client.py         # REST API client bridge
├── tests/                    # Automated Pytest test suite (14 passing tests)
├── .dockerignore             # Docker build exclusion rules
├── .env.example              # Environment variables template
├── Dockerfile                # Production Docker container definition (Python 3.11)
├── docker-compose.yml        # Docker service orchestration configuration
├── Procfile                  # Local process manager runner (Honcho)
├── Procfile.docker           # Container process manager runner
└── requirements.txt          # Python project dependencies
```

---

## ⚙️ Environment Setup (`.env`)

Create a `.env` file in the root directory (or copy `.env.example`):

```ini
APP_NAME="Advanced AI Medical Intelligence Platform"
APP_VERSION="1.0.0"
ENVIRONMENT="development"

# Server Ports & Hosts
HOST="127.0.0.1"
PORT=8000
STREAMLIT_PORT=8501

# File Storage Paths
MODEL_PATH="models/checkpoints/best_efficientnet_b0.pth"
XAI_OUTPUT_DIR="models/xai"
UPLOAD_DIR="data/uploads"
DATABASE_URL="sqlite:///./medical_intelligence.db"

# LLM API Keys (Groq)
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="llama-3.1-8b-instant"
```

---

## 🚀 Quick Start Guide

### Option 1: Local Development (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Advanced-AI-Medical-Intelligence.git
   cd "Advanced AI Medical Intellegence"
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Launch both FastAPI Backend & Streamlit Dashboard in parallel:**
   ```bash
   honcho start
   ```

5. **Access Applications:**
   - **Streamlit Dashboard:** [http://localhost:8501](http://localhost:8501)
   - **FastAPI Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Run with Docker & Docker Compose

Launch the containerized stack with a single command:

```bash
# Build and run using Docker Compose
docker-compose up --build
```

To stop containers:
```bash
docker-compose down
```

---

## 🧪 Testing & Quality Assurance

Run the automated Pytest test suite and Ruff code linting:

```bash
# Run Code Quality Check
ruff check app/ streamlit_app/ --ignore BLE001,S110

# Run All Unit & API Tests
pytest tests/ -v --cov=app
```

---

## 📡 REST API Documentation

FastAPI provides an interactive OpenAPI Swagger interface at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **`GET`** | `/health` | Application status & version check |
| **`POST`** | `/predictions/analyze` | Upload chest X-ray image for Deep Learning, Grad-CAM & LLM Report generation |
| **`GET`** | `/predictions/history` | Retrieve historical analysis records |

---

## 🏋️ Model Training & Dataset Scripts

To re-train or evaluate the model on your dataset:

```bash
# Prepare dataset splits
python scripts/setup_data.py

# Train EfficientNet-B0 PyTorch model
python scripts/train.py

# Evaluate model performance & metrics
python scripts/evaluate.py
```

---

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
