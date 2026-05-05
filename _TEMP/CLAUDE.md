# PS01 — Powerful Silence Project Context

## What Is This?
A Django-based 12-step recovery web application (AA-focused, architected for multi-program). Users work through all 12 steps with original guided questions, track progress, maintain daily recovery practices, and manage amends.

## Deployments
- **Active CI target:** https://program.icos.dev — what `master` pushes deploy to via GitHub Actions FTP. cPanel-managed on InMotion VPS (`vps138804`, user `icos`).
- **Marketing-linked instance:** https://12steps.powerfulsilence.com — referenced from `index.html` landing page and service worker. Separate cPanel host (`powerfulsilence` user, FTP at `ftp.powerfulsilence.com`). Same codebase; deployment mechanism varies (manual / different workflow).
- **Landing page:** `index.html` in project root — static, self-contained, **excluded from the FTP deploy** (commit `fb3eb29`) to avoid overwriting the root-level subdomain app. Edit it locally and deploy independently if needed.
- **Repository:** https://github.com/richardtheshannon/powerfulsilence-com (private)

## Status (as of 2026-05)
- Core feature set complete (dashboard, 12 steps with 136 questions, daily check-in, gratitude, amends).
- **In-flight:** V003.0 visual reskin — 9-phase Frame Studio port (commit `8b32781`, phases A–I). Some test strings still reference pre-reskin copy; the test gate in `deploy.yml` was dropped so deploys ship regardless of these stale failures (commit `80253a6`). Tests to be updated in follow-up.
- **Recent fix (this session):** prod `program.icos.dev` was missing seeded `Step` rows — dashboard rendered "Begin step work" with empty progress. Resolved by running `python manage.py migrate && python manage.py seed_steps` in cPanel Terminal. See "Production Deployment → Post-deploy manual step" below.

## Tech Stack
- **Backend:** Python 3.12, Django 5.2.x, PostgreSQL
- **Frontend:** HTMX 2.x + Alpine.js 3.x + Tailwind CSS 3.x (all CDN, no build step)
- **Icons:** Lucide Icons (CDN)
- **Forms:** django-crispy-forms + crispy-tailwind
- **Security:** django-axes (rate limiting), WhiteNoise (static files)
- **Config:** python-decouple (.env)
- **PDF Export:** ReportLab
- **Testing:** pytest + pytest-django

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
py manage.py runserver       # http://localhost:8000
```

## Local Database
- **Engine:** PostgreSQL 18 (native Windows)
- **Database:** `ps01_db` / **User:** `ps01_user` / **Host:** `localhost:5432`
- **psql:** `"C:\Program Files\PostgreSQL\18\bin\psql.exe"`

## Testing
```bash
py -m pytest                 # Run all tests
py -m pytest core/           # Per-app
py -m pytest steps/
py -m pytest journal/
py -m pytest amends/
```
Tests use SQLite via `config/settings_test.py` (overrides PostgreSQL for speed). Note: ~16 tests currently fail on string mismatches from the V003 reskin (see Status).

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
- **No AI features** (current direction; AI insights occasionally floated, not implemented)
- **Original content only** — 136 guided questions written from scratch

## Key Files
| File | Purpose |
|------|---------|
| `index.html` | Static landing page (excluded from FTP deploy) |
| `.env` | Environment variables (DB creds, secret key, user seed data) |
| `config/settings.py` | Main Django settings |
| `config/settings_test.py` | Test settings (SQLite override) |
| `config/settings_production.py` | Production settings (DEBUG=False, HSTS, secure cookies) |
| `requirements.txt` | Python dependencies |
| `passenger_wsgi.py` | Passenger WSGI entry point |
| `.github/workflows/deploy.yml` | CI/CD workflow (test + FTP deploy to `program.icos.dev`) |
| `Dockerfile` | Dev container (Python 3.12, Node.js 22, Claude Code) |
| `docker-compose.yml` | Dev container orchestration |

---

## Production Deployment — `program.icos.dev` (active CI target)

### Infrastructure (verified this session)
- **Host:** cPanel/Passenger on InMotion VPS — hostname `vps138804`, cPanel user `icos`
- **App dir:** `~/public_html/program.icos.dev/` (where `manage.py` lives)
- **Python venv:** `~/virtualenv/program-icos/3.12/` (cPanel "Setup Python App" — NOT a `venv/` next to `manage.py`)
- **System Python:** `/bin/python3` is 3.6.8 (too old for Django 5; always activate the cPanel venv)
- **Settings:** `config/settings_production.py`
- **WSGI:** `passenger_wsgi.py` (Phusion Passenger)
- **Static files:** WhiteNoise (CompressedManifestStaticFilesStorage)
- **Database:** PostgreSQL on `localhost:5432` (managed via cPanel)

### CI/CD Pipeline
- **Workflow:** `.github/workflows/deploy.yml`
- **Trigger:** Push to `master` branch
- **Flow:** Run tests (pytest) → FTP deploy to cPanel. Test failures **do not** block deploy (gate dropped per commit `80253a6`).
- **FTP Action:** SamKirkland/FTP-Deploy-Action@v4.3.5
- **GitHub Secrets:** `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
- **Excludes:** `.git*`, `__pycache__/`, `.env`, `db.sqlite3`, `.ralph/`, `00_research/`, `_TEMP/`, `pip-cache/`, `bin/`, `Dockerfile`, `docker-compose.yml`, `pytest.ini`, `.gitignore`, `staticfiles/`, `index.html`

### Post-deploy manual step (cPanel Terminal)
The workflow only ships files via FTP — it does **not** run Django commands on the server. After any deploy that touches `steps/migrations/` or `steps/management/commands/seed_steps.py`, run in cPanel Terminal:

```bash
cd ~/public_html/program.icos.dev
source ~/virtualenv/program-icos/3.12/bin/activate
python manage.py migrate --noinput
python manage.py seed_steps
touch tmp/restart.txt          # restart Passenger if app behavior changed
```

`seed_steps` is idempotent (`update_or_create`), so re-running is safe. A reminder comment to this effect lives at the top of `.github/workflows/deploy.yml`.

For dependency or static changes, also run:
```bash
pip install -r requirements.txt              # if requirements.txt changed
python manage.py collectstatic --noinput     # if static/ changed
touch tmp/restart.txt
```

### Server Notes
- `.env`, the cPanel-managed venv, and `staticfiles/` are managed on the server (not deployed via FTP)
- `.htaccess` is managed by cPanel — do not overwrite
- DATABASE_URL parser uses `rsplit("@", 1)` to handle `@` in passwords (commit `8328e51`)
- Passenger config is managed via cPanel Application Manager (changes require WHM root)
- `index.html` is excluded from FTP because the FTP root is shared with another subdomain app — pushing it would overwrite that app's homepage

### Marketing instance — `12steps.powerfulsilence.com`
Different cPanel host. Separate FTP credentials and DB. Not on the GitHub Actions deploy path; deploys are manual or via a different mechanism. Treat as out-of-scope for the standard CI flow unless explicitly working on it.

---

## Development Guidelines

### Code Style
- Follow existing patterns in each Django app
- Use class-based views for standard CRUD; function views for HTMX endpoints
- All models use UUID primary keys (`models.UUIDField(primary_key=True, default=uuid.uuid4)`)
- Templates use Tailwind utility classes via CDN (no custom CSS build)

### Frontend Patterns
- **HTMX:** `hx-post`, `hx-target`, `hx-swap` for dynamic interactions
- **Alpine.js:** `x-data`, `x-show`, `x-on` for client-side state
- **No JavaScript files** — all behavior via HTMX/Alpine inline attributes (with the small set of files in `static/js/` for cross-cutting concerns like preferences, frame, service worker)
- **Dark theme classes:** Tailwind dark palette (`bg-gray-900`, `text-gray-100`, etc.)

### Editing Principles (per project owner)
- **Minimal, surgical edits** — reuse existing systems; avoid new dependencies unless absolutely necessary
- **Warn before changes** that could break functionality or layouts
- **No user guides** unless explicitly requested
- **Flag context degradation** so the session can be reset
- **Wikilink format** (`[[filename]]`) when referencing files in markdown files you write or edit (per repo `CLAUDE.md`)

### Testing
- Write tests for all new views, models, and management commands
- Use `pytest` with `config/settings_test.py` (SQLite, no PostgreSQL needed)
- Mock external dependencies and `.env` variables in tests
- CI runs tests but **does not block** deploy on failure (current state — see Status)

### Git Workflow
- Single branch: `master`
- Push to `master` triggers CI/CD (test → FTP deploy to `program.icos.dev`)
- Write descriptive commit messages

### Protected Directories (do not modify without coordination)
- `.ralph/` — Ralph agent infrastructure
- `_TEMP/` — Project documentation and specs (this file lives here)
- `00_research/` — Research documents and implementation guide
- `_prompting/` — Prompting templates and snippets
