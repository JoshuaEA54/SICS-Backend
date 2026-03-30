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

## Architecture

The database runs in Docker; the backend runs directly on the host with Python.

```
┌─────────────────────┐        ┌─────────────────────────────┐
│   Docker            │        │   Host (your machine)       │
│                     │        │                             │
│  ┌───────────────┐  │        │  ┌────────────────────────┐ │
│  │  PostgreSQL   │◄─┼────────┼──│  FastAPI (uvicorn)     │ │
│  │  port 5432    │  │        │  │  localhost:8000        │ │
│  └───────────────┘  │        │  └────────────────────────┘ │
└─────────────────────┘        └─────────────────────────────┘
```

This setup gives you fast iteration (no image rebuilds) while keeping the database isolated and reproducible.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL (Docker) |
| Authentication | Google OAuth 2.0 |
| Frontend | React + Vite + TypeScript (separate repository) |

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Run the backend |
| Docker + Docker Compose | Run PostgreSQL |
| Git | Version control |

---

## Quickstart

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

```bash
cp .env.example .env
```

Open `.env` and fill in your values. The important ones:

```env
# Must match the credentials you set for the Postgres container
POSTGRES_USER=sics
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=sicsdb
POSTGRES_PORT_HOST=5432

# Must point to localhost:<POSTGRES_PORT_HOST>
DATABASE_URL=postgresql+psycopg://sics:your_secure_password@localhost:5432/sicsdb

# From Google Cloud Console → APIs & Services → Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

> To get Google credentials, go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and generate OAuth 2.0 credentials.

### 5. Start the database

```bash
docker compose up -d
```

Postgres will be available at `localhost:<POSTGRES_PORT_HOST>` (default `5432`).

Wait a few seconds for the container to be ready, then verify:

```bash
docker compose ps        # should show postgres-db as healthy
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the backend

Development server (auto-reload):

```bash
fastapi dev app/main.py
```

Production-like server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API is available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## Daily development workflow

```
1. docker compose up -d          # start Postgres (once per session)
2. source .venv/bin/activate      # activate venv
3. fastapi dev app/main.py        # run backend with auto-reload
```

When you change a model:

```bash
alembic revision --autogenerate -m "describe change"
# Review alembic/versions/<new_file>.py
alembic upgrade head
```

---

## Alembic workflow

Never update the schema via ad-hoc SQL. Always use migration files.

| Command | Description |
|---------|-------------|
| `alembic revision --autogenerate -m "msg"` | Generate migration from model changes |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic current` | Show current revision |
| `alembic history` | Show full migration history |
| `alembic downgrade -1` | Roll back one step |

Detailed guide: [DOCKER_ALEMBIC_FLOW.md](DOCKER_ALEMBIC_FLOW.md)

---

## Stopping and resetting the database

Stop Postgres (data is preserved):

```bash
docker compose down
```

Full reset (destroys all data — use with caution):

```bash
docker compose down -v
docker compose up -d
alembic upgrade head
```

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
│   │   ├── config.py      # Environment variables (pydantic-settings)
│   │   └── security.py    # Google token verification
│   ├── db/
│   │   ├── base.py        # SQLAlchemy declarative base
│   │   └── session.py     # Database engine and session factory
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── crud/              # Database query helpers
│   └── services/          # Business logic (email, compliance scoring)
├── alembic/               # Migration environment
│   ├── env.py             # Reads DATABASE_URL from app settings
│   └── versions/          # Migration files
├── alembic.ini            # Alembic config (URL injected at runtime)
├── docker-compose.yml     # PostgreSQL only
├── requirements.txt
└── .env.example           # Copy to .env and fill in secrets
```

---

## User roles

| Role | Description |
|------|-------------|
| `company_rep` | Company representative. Registers and completes evaluations. |
| `expert` | Cybersecurity expert. Assigned directly in the database. |
