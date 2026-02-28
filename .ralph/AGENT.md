# Ralph Agent Configuration — PS01

## Build Instructions

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate
```

## Test Instructions

```bash
# Run all tests
python -m pytest

# Run tests for a specific app
python -m pytest core/
python -m pytest steps/
python -m pytest journal/
python -m pytest amends/
```

## Run Instructions

```bash
# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

## Seed Data

```bash
# Create initial superuser (reads from .env / environment variables)
python manage.py seed_user

# Seed 12 steps + questions (Phase 3)
python manage.py seed_steps
```

## Static Files

```bash
# Collect static files (production)
python manage.py collectstatic --noinput
```

## Notes
- Database: PostgreSQL on Windows host (`ps01_db`) — connects via `host.docker.internal`
- All environment variables loaded via python-decouple from `.env`
- Frontend assets are CDN-only — no npm or build step required
- Always run migrations after model changes
