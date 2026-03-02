# PS01 — Powerful Silence Project Context

## What Is This?
A Django-based 12-step recovery web application (AA-focused, architected for multi-program). Users work through all 12 steps with original guided questions, track progress, maintain daily recovery practices, and manage amends.

## Live Site
- **App:** https://12steps.powerfulsilence.com (Django app on cPanel/Passenger)
- **Landing page:** `index.html` in project root (static, self-contained, links to app)
- **Repository:** https://github.com/richardtheshannon/powerfulsilence-com (private)
- **Status:** All 13 development phases complete. Deployed and running.

## Tech Stack
- **Backend:** Python 3.12, Django 5.2.x, PostgreSQL
- **Frontend:** HTMX 2.x + Alpine.js 3.x + Tailwind CSS 3.x (all CDN, no build step)
- **Icons:** Lucide Icons (CDN)
- **Forms:** django-crispy-forms + crispy-tailwind
- **Security:** django-axes (rate limiting), WhiteNoise (static files)
- **Config:** python-decouple (.env)
- **PDF Export:** ReportLab
- **Testing:** pytest + pytest-django (126 tests, all passing)

## Django App Structure
```
config/          # Django project package (settings, urls, wsgi)
core/            # Custom User model (UUID PK), auth, dashboard, middleware
steps/           # 12 steps, 136 original questions, responses, progress tracking
journal/         # Daily check-in (Step 10/11 inventory), gratitude journal, streaks
amends/          # Steps 8/9 amends list, letters, status tracking
```

## Running Locally (Windows)
```bash
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_user       # Create user from .env credentials
py manage.py seed_steps      # Seed 12 steps + 136 questions (idempotent)
py manage.py runserver       # Visit http://localhost:8000
```

## Local Database
- **Engine:** PostgreSQL 18 (native Windows)
- **Database:** `ps01_db` / **User:** `ps01_user` / **Host:** `localhost:5432`
- **psql:** `"C:\Program Files\PostgreSQL\18\bin\psql.exe"`

## Testing
```bash
py -m pytest                 # Run all 126 tests
py -m pytest core/           # Core app tests only
py -m pytest steps/          # Steps app tests only
py -m pytest journal/        # Journal app tests only
py -m pytest amends/         # Amends app tests only
```
Tests use SQLite via `config/settings_test.py` (overrides PostgreSQL for speed).

## Key URLs
| URL | View | Description |
|-----|------|-------------|
| `/` | root_redirect | Redirects to /dashboard/ |
| `/dashboard/` | DashboardView | Progress overview, sobriety counter, widgets |
| `/login/` | PS01LoginView | Login page |
| `/steps/` | StepListView | 12 steps overview with progress |
| `/steps/<number>/` | step_detail_view | Individual step with question form |
| `/steps/auto-save/` | auto_save_view | HTMX auto-save endpoint |
| `/journal/` | DailyCheckinView | Daily Step 10/11 inventory |
| `/journal/history/` | JournalHistoryView | Past check-in entries |
| `/journal/gratitude/` | GratitudeView | Today's gratitude entries |
| `/journal/gratitude/history/` | GratitudeHistoryView | Past gratitude entries |
| `/amends/` | PersonListView | Amends list |
| `/amends/<uuid>/` | PersonDetailView | Full amend workflow |
| `/admin/` | Django Admin | Admin interface |

## Key Design Decisions
- **Single seeded user** — multi-user registration planned for future
- **UUID primary keys** on all models
- **All frontend via CDN** — no npm, no webpack, no node_modules
- **Dark theme** — appropriate for recovery/reflection context
- **HTMX** for dynamic interactions (auto-save, inline add/delete)
- **Alpine.js** for client-side state (conditional fields, mobile menu)
- **Free forever** — no payment infrastructure
- **No AI features**
- **Original content only** — 136 guided questions written from scratch

## Key Files
| File | Purpose |
|------|---------|
| `index.html` | Static landing page for powerfulsilence.com |
| `.env` | Environment variables (DB creds, secret key, user seed data) |
| `config/settings.py` | Main Django settings |
| `config/settings_test.py` | Test settings (SQLite override) |
| `config/settings_production.py` | Production settings |
| `requirements.txt` | Python dependencies |
| `passenger_wsgi.py` | Passenger WSGI entry point |
| `.github/workflows/deploy.yml` | CI/CD workflow (test + FTP deploy) |
| `Dockerfile` | Dev container (Python 3.12, Node.js 22, Claude Code) |
| `docker-compose.yml` | Dev container orchestration |

---

## Production Deployment

### Infrastructure
- **Host:** cPanel/Passenger on InMotion VPS (vps138804)
- **Subdomain:** 12steps.powerfulsilence.com
- **Python:** 3.12 via venv at `~/public_html/12steps.powerfulsilence.com/venv/`
- **WSGI:** `passenger_wsgi.py` (Phusion Passenger)
- **Static files:** WhiteNoise (CompressedManifestStaticFilesStorage)
- **Settings:** `config/settings_production.py`
- **Database:** `12setps` / **User:** `12steps-user` / **Host:** localhost:5432

### CI/CD Pipeline
- **Workflow:** `.github/workflows/deploy.yml`
- **Trigger:** Push to `master` branch
- **Flow:** Run tests (pytest) → FTP deploy to cPanel
- **FTP Action:** SamKirkland/FTP-Deploy-Action@v4.3.5
- **GitHub Secrets:** `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
- **Excludes:** `.git*`, `__pycache__/`, `.env`, `db.sqlite3`, `.ralph/`, `00_research/`, `_TEMP/`, `pip-cache/`, `Dockerfile`, `docker-compose.yml`, `pytest.ini`, `.gitignore`, `staticfiles/`

### Server Commands (via cPanel Terminal)
Code deploys automatically on push to `master`. For server-side changes:
```bash
cd ~/public_html/12steps.powerfulsilence.com
source venv/bin/activate
pip install -r requirements.txt          # If deps changed
python manage.py migrate                 # If models changed
python manage.py collectstatic --noinput # If static files changed
touch tmp/restart.txt                    # Restart Passenger
```

### Server Notes
- `.env`, `venv/`, `staticfiles/` are managed on server (not deployed via FTP)
- `.htaccess` is managed by cPanel — do not overwrite
- DATABASE_URL parser uses `rsplit("@", 1)` to handle `@` in passwords
- Passenger config managed via cPanel Application Manager (changes require WHM root)

---

## Development Guidelines

### Code Style
- Follow existing patterns in each Django app
- Use class-based views for standard CRUD; function views for HTMX endpoints
- All models use UUID primary keys (`models.UUIDField(primary_key=True, default=uuid.uuid4)`)
- Templates use Tailwind utility classes via CDN (no custom CSS build)

### Frontend Patterns
- **HTMX:** Use `hx-post`, `hx-target`, `hx-swap` for dynamic interactions
- **Alpine.js:** Use `x-data`, `x-show`, `x-on` for client-side state
- **No JavaScript files** — all behavior via HTMX/Alpine inline attributes
- **Dark theme classes:** Use Tailwind dark palette (`bg-gray-900`, `text-gray-100`, etc.)

### Testing
- Write tests for all new views, models, and management commands
- Use `pytest` with `config/settings_test.py` (SQLite, no PostgreSQL needed)
- Mock external dependencies and `.env` variables in tests
- CI runs tests before every deploy — failing tests block deployment

### Git Workflow
- Single branch: `master`
- Push to `master` triggers CI/CD (test → deploy)
- Write descriptive commit messages

### Protected Directories (do not modify without coordination)
- `.ralph/` — Ralph agent infrastructure
- `_TEMP/` — Project documentation and specs
- `00_research/` — Research documents and implementation guide
