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

## Phase 4 — Step List View (The 12 Steps Overview) (COMPLETE)

**Goal**: A page showing all 12 steps with progress indicators and navigation to individual step forms.

### Tasks
- [x] Implement `steps/views.py` — `StepListView` with progress data per user
- [x] Create `steps/templates/steps/step_list.html` — Grid of 12 step cards
- [x] Create `steps/templates/steps/partials/step_card.html` — Individual step card with status/progress
- [x] Create `steps/templates/steps/partials/progress_bar.html` — Color-coded progress bar
- [x] Create `steps/templatetags/step_tags.py` — `get_item` filter for dict lookup
- [x] Configure `steps/urls.py` and wire into `config/urls.py`
- [x] Update sidebar "My Step Work" link to point to `/steps/` with active highlighting
- [x] Add placeholder `step_detail_view` + template (Phase 5 will implement full form)
- [x] Write 6 tests for step list view (30 total tests passing)

### Verification
- [x] `/steps/` shows all 12 steps with status and progress bars
- [x] Each step card links to `/steps/<number>/` detail page
- [x] Steps 10, 11, 12 marked with recurring indicator
- [x] First incomplete step highlighted as "Continue here"
- [x] StepProgress records auto-created on first visit

---

## Phase 5 — Step Detail View & Form (Core Step Work)

**Goal**: Users can view a single step, answer all its questions in a form, and save their responses.

### Tasks
- [ ] Implement `steps/forms.py` — Dynamic form for step questions
- [ ] Implement `StepDetailView` in `steps/views.py` — Form rendering and saving
- [ ] Create `steps/templates/steps/step_detail.html` — Step form page
- [ ] Create `steps/templates/steps/partials/question_field.html` — Per-question-type field rendering
- [ ] Add HTMX auto-save for individual question responses
- [ ] Write tests for step detail view and form submission

### Verification
- [ ] `/steps/1/` shows Step 1 with all 19 questions
- [ ] User can type answers and save
- [ ] Saved answers persist across page reloads
- [ ] Progress bar updates on step list after answering

## Notes
- PostgreSQL runs on Windows host — container connects via `host.docker.internal:5432`
- Database: `ps01_db`, User: `ps01_user`, Password: `devpassword123`
- Reference: `00_research/PS01-Implementation-Guide.md` for detailed specs
- Tests use SQLite via `config/settings_test.py` (pytest.ini `--ds` flag overrides docker-compose env var)
