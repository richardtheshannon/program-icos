# Fix Plan — PS01 (Powerful Silence)

## Phase 1 — Project Scaffolding & Docker Setup

**Goal**: Empty Django project that runs in Docker, with custom User model, seeded superuser, and Ralph configured for autonomous development.

### Tasks
- [x] Install Python dependencies from requirements.txt (`pip install -r requirements.txt`)
- [x] Create Django project with `django-admin startproject config .`
- [x] Create the `core` app with `python manage.py startapp core`
- [x] Configure `config/settings.py`: AUTH_USER_MODEL, DATABASE_URL via python-decouple, INSTALLED_APPS (core, whitenoise, crispy_forms, crispy_tailwind, axes), CRISPY settings, TIME_ZONE, LOGIN_URL/LOGIN_REDIRECT_URL, middleware stack (SecurityMiddleware → WhiteNoise → Session → Common → CSRF → Auth → Messages → XFrame → LoginRequiredMiddleware → AxesMiddleware)
- [x] Implement `core/models.py` — Custom User model with UUID primary key, sobriety_date, fellowship fields, sobriety_days() method
- [x] Implement `core/middleware.py` — LoginRequiredMiddleware (exempt: /login/, /admin/, /static/; redirect unauthenticated to login)
- [x] Implement `core/management/commands/seed_user.py` — Creates superuser from environment variables (PS01_USER_EMAIL, PS01_USER_PASSWORD, PS01_USER_FIRST_NAME, PS01_USER_LAST_NAME), idempotent (skip if user exists)
- [x] Register User model in `core/admin.py`
- [x] Run migrations: `python manage.py makemigrations core && python manage.py migrate`
- [x] Run seed_user: `python manage.py seed_user`
- [x] Create `conftest.py` for pytest configuration

### Verification
- [x] Django project runs without errors: `python manage.py runserver 0.0.0.0:8000`
- [x] Container connects to host PostgreSQL successfully
- [ ] Seeded superuser can log into Django admin at `/admin/`
- [ ] LoginRequiredMiddleware redirects unauthenticated users to `/login/`

## Notes
- PostgreSQL runs on Windows host — container connects via `host.docker.internal:5432`
- Database: `ps01_db`, User: `ps01_user`, Password: `devpassword123`
- Reference: `00_research/PS01-Implementation-Guide.md` for detailed specs
- Dockerfile and docker-compose.yml already created (pre-setup)
- .env already configured with credentials
- Tests use SQLite via `config/settings_test.py` (pytest.ini `--ds` flag overrides docker-compose env var)
