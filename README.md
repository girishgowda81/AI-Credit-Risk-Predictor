# NexaLend AI: Credit Risk & Loan Default Prediction System

A complete end-to-end machine learning system for predicting loan default risk, enabling financial institutions to make data-driven credit decisions with explainable AI.

## 🚀 Features
- **ML Engine**: XGBoost classifier with 89%+ accuracy.
- **Explainable AI**: Integrated SHAP values for feature-level risk breakdown.
- **REST API**: Built with FastAPI for high performance (<500ms latency).
- **React Dashboard**: Modern, interactive UI built with React 18 and Vite.
- **Automated Pipeline**: Synthetic data generation, preprocessing, and training.
- **Dockerized**: Full-stack deployment with Docker Compose and Nginx.

## 🏃 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & npm (for frontend development)
- Docker Desktop (for deployment)

### 2. Local Development (Quick Start)
The easiest way to start both the backend and frontend:
1. Double-click **`run.bat`** in the root directory.
2. The dashboard will open at `http://localhost:3000`.

### 3. Production Deployment (Docker)
To deploy the full-stack system with a PostgreSQL database:
1. Double-click **`deploy.bat`**.
2. Visit `http://localhost` to access the production dashboard.
3. Visit `http://localhost:8001/docs` for API documentation.

## 📊 Technical Architecture
- **Frontend**: React 18, Vite, Chart.js, Lucide Icons.
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL.
- **ML Layer**: XGBoost, SHAP Explainer, Joblib.
- **Infrastructure**: Docker, Nginx (Reverse Proxy).

---
> [!IMPORTANT]
> Ensure you have Docker Desktop running before using `deploy.bat`. The system uses a multi-stage build to optimize the final production images.
