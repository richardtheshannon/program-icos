# Fix Plan — PS01 (Powerful Silence)

## Phase 1 — Project Scaffolding & Docker Setup (COMPLETE)

**Goal**: Empty Django project that runs in Docker, with custom User model, seeded superuser, and Ralph configured for autonomous development.

### Tasks
- [x] Install Python dependencies from requirements.txt
- [x] Create Django project with `django-admin startproject config .`
- [x] Create the `core` app with `python manage.py startapp core`
- [x] Configure `config/settings.py` (AUTH_USER_MODEL, DATABASE_URL, INSTALLED_APPS, middleware stack)
- [x] Implement `core/models.py` — Custom User model (UUID PK, sobriety_date, fellowship)
- [x] Implement `core/middleware.py` — LoginRequiredMiddleware
- [x] Implement `core/management/commands/seed_user.py`
- [x] Register User model in `core/admin.py`
- [x] Run migrations and seed_user
- [x] Create `conftest.py` for pytest configuration

### Verification
- [x] Django project runs without errors
- [x] Container connects to host PostgreSQL successfully
- [x] Seeded superuser can log into Django admin at `/admin/` (verified via test)
- [x] LoginRequiredMiddleware redirects unauthenticated users to `/login/` (verified via test)

---

## Phase 2 — Base Templates & Layout (COMPLETE)

**Goal**: Base HTML layout with sidebar navigation, topbar, Tailwind styling, login/logout flow.

### Tasks
- [x] Create `core/templates/base.html` — Dark theme, CDN links (Tailwind, HTMX, Alpine.js, Lucide), sidebar + main layout
- [x] Create `core/templates/components/sidebar.html` — Navigation links, sobriety counter, user info
- [x] Create `core/templates/components/topbar.html` — Page title, mobile menu, welcome message
- [x] Create `core/templates/components/messages.html` — Auto-dismiss Django messages with Alpine.js
- [x] Create `core/templates/core/login.html` — Standalone centered login form with dark theme
- [x] Create `core/templates/core/dashboard.html` — Placeholder cards for all features
- [x] Implement `core/views.py` — DashboardView, PS01LoginView, PS01LogoutView, root_redirect
- [x] Configure `core/urls.py` and `config/urls.py` — Routes for /, /dashboard/, /login/, /logout/
- [x] Write and pass 15 tests (models, middleware, views)

### Verification
- [x] Login page renders with dark Tailwind styling
- [x] Successful login redirects to dashboard
- [x] Dashboard shows sidebar navigation with placeholder links
- [x] Logout works and redirects to login
- [x] All pages require authentication except login and admin

---

## Phase 3 — Step Data Models & Seed Data (COMPLETE)

**Goal**: Steps and Questions tables created and populated with original content for all 12 steps.

### Tasks
- [x] Create the `steps` app with `python manage.py startapp steps`
- [x] Add `steps` to `INSTALLED_APPS`
- [x] Implement `steps/models.py` — Step, Question, Response, StepProgress models (UUID PKs)
- [x] Run migrations: `python manage.py makemigrations steps && python manage.py migrate`
- [x] Implement `steps/management/commands/seed_steps.py` — Seed all 12 steps with original questions (136 total)
- [x] Run seed command: `python manage.py seed_steps`
- [x] Register models in `steps/admin.py` (with QuestionInline on Step)
- [x] Write 9 tests for step models and seed command

### Verification
- [x] All 12 steps visible in Django admin
- [x] 136 original questions seeded
- [x] Steps 10, 11, 12 have `is_recurring = True`
- [x] `seed_steps` command is idempotent
- [x] 24 total tests passing (15 core + 9 steps)

---

## Phase 4 — Step List View (The 12 Steps Overview)

**Goal**: A page showing all 12 steps with progress indicators and navigation to individual step forms.

### Tasks
- [ ] Implement `steps/views.py` — `StepListView` with progress data
- [ ] Create `steps/templates/steps/step_list.html` — Grid of 12 step cards
- [ ] Create `steps/templates/steps/partials/step_card.html` — Individual step card partial
- [ ] Create `steps/templates/steps/partials/progress_bar.html` — Reusable progress bar
- [ ] Configure `steps/urls.py` and wire into `config/urls.py`
- [ ] Update sidebar links to point to step list
- [ ] Write tests for step list view

### Verification
- [ ] `/steps/` shows all 12 steps with status and progress
- [ ] Each step card links to step detail page
- [ ] Steps 10, 11, 12 marked as recurring

## Notes
- PostgreSQL runs on Windows host — container connects via `host.docker.internal:5432`
- Database: `ps01_db`, User: `ps01_user`, Password: `devpassword123`
- Reference: `00_research/PS01-Implementation-Guide.md` for detailed specs
- Tests use SQLite via `config/settings_test.py` (pytest.ini `--ds` flag overrides docker-compose env var)
