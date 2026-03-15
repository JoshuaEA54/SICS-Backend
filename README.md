# SICS — Sistema Integrado de Cumplimiento en Seguridad *(Information Security Compliance System)*

Web platform that allows companies to evaluate how well they comply with information security controls, based on **Costa Rica's Law 8968** and international frameworks including **ISO 27001, ISO 27002, ISO 27005, ISO 27701** and **NIST CSF**.

---

## How it works

1. A company signs in with their corporate Google account and registers their organization
2. They answer a questionnaire of 30 controls organized in 16 groups (Governance, Cryptography, Risk Management, etc.)
3. For each control they answer Yes/No, upload evidence files, and optionally add observations
4. A cybersecurity expert reviews each response and issues a verdict
5. The system calculates the compliance percentage and emails the report to the company

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL |
| Authentication | Google OAuth 2.0 |
| Frontend | React + Vite + TypeScript (separate repository) |

---

## Prerequisites

- Python 3.11+
- PostgreSQL
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/JoshuaEA54/SICS-Backend.git
cd SICS-Backend
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv

# Mac / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of the project with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/sics
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
UPLOAD_FOLDER=uploads/
```

> To get your Google credentials, go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and generate OAuth 2.0 credentials.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
fastapi dev app/main.py
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## Project structure

```
backend/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── api/
│   │   ├── deps.py        # Shared dependencies (get_db, get_current_user)
│   │   └── routes/        # API endpoints
│   ├── core/
│   │   ├── config.py      # Environment variables
│   │   └── security.py    # Google token verification
│   ├── db/
│   │   ├── base.py        # SQLAlchemy base class
│   │   └── session.py     # Database connection
│   ├── models/            # Database tables as Python classes (SQLAlchemy)
│   ├── schemas/           # Request/response validation (Pydantic)
│   ├── crud/              # Database queries
│   └── services/          # Business logic (email, compliance scoring)
├── alembic/               # Database migrations
├── alembic.ini
└── requirements.txt
```

---

## User roles

| Role | Description |
|------|-------------|
| `company_rep` | Company representative. Registers and completes evaluations. |
| `expert` | Cybersecurity expert. Assigned directly in the database. |
