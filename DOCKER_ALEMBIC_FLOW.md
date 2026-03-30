# Database (Docker) + Alembic workflow

This guide covers how the database container and Alembic migrations work together in this project.

## Architecture overview

Only PostgreSQL runs in Docker. The FastAPI backend runs directly on the host with Python.

```
docker compose up -d      →  starts PostgreSQL on localhost:<POSTGRES_PORT_HOST>
fastapi dev app/main.py   →  starts the backend on localhost:8000
```

This means:
- No image rebuilds when you change Python code.
- Fast feedback loop during development.
- The database is isolated and reproducible across machines.

---

## What Alembic is

Alembic is a migration tool. A migration is a versioned file that describes how to move the database schema forward (and optionally backward).

Instead of editing ad-hoc SQL scripts, you create migration files that are committed to git. Every developer and every environment applies exactly the same sequence of changes.

---

## Why not `docker-entrypoint-initdb.d`

`/docker-entrypoint-initdb.d` scripts run only when the PostgreSQL data directory is empty (first initialization). This breaks iterative development:

1. You change the SQL script.
2. You restart the container.
3. Nothing changes — data already exists.
4. The team deletes data to force re-creation.

With Alembic, schema updates are explicit and repeatable without destroying data.

---

## First-time setup

```bash
cp .env.example .env       # fill in your secrets
docker compose up -d       # start Postgres
alembic upgrade head       # create all tables
fastapi dev app/main.py    # start the backend
```

---

## Schema change workflow

Whenever you modify an ORM model, follow this order:

1. Edit the model (e.g. add a column in `app/models/user.py`).
2. Generate a migration:

```bash
alembic revision --autogenerate -m "add column foo to users"
```

3. Review the generated file in `alembic/versions/`.
4. Apply it:

```bash
alembic upgrade head
```

5. Commit the model **and** the migration file together.

Never commit model changes without the corresponding migration file.

---

## Common Alembic commands

| Command | Description |
|---------|-------------|
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Roll back one migration |
| `alembic current` | Show the current revision |
| `alembic history` | Show full migration history |
| `alembic revision --autogenerate -m "msg"` | Generate migration from model diff |

---

## How the database URL is resolved

`alembic.ini` does **not** contain a real URL. `alembic/env.py` reads the URL at runtime from `app.core.config.settings`, which pulls it from the `DATABASE_URL` environment variable (or builds it from `POSTGRES_*` variables).

This keeps secrets out of version control and makes the same `alembic` commands work identically in every developer's environment.

---

## Reset scenarios

Stop Postgres (data is preserved in the named volume):

```bash
docker compose down
```

Full reset — destroys all data:

```bash
docker compose down -v     # removes the postgres_data volume
docker compose up -d
alembic upgrade head
```

Upload files live in `data/uploads/` on the host. They are not touched by `docker compose down -v`.

---

## Team rules

1. Alembic is the single source of truth for schema evolution.
2. No schema changes in `docker-entrypoint-initdb.d` scripts.
3. Every PR that changes a model must include the migration file.
4. Avoid `docker compose down -v` unless a reset is intentional.
5. Keep `.env` out of version control and rotate secrets if exposed.
