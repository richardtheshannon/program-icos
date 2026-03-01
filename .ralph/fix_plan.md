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

## Phase 5 — Step Detail View & Form (Core Step Work) (COMPLETE)

**Goal**: Users can view a single step, answer all its questions in a form, and save their responses.

### Tasks
- [x] Implement `steps/forms.py` — Dynamic `StepWorkForm` with per-question fields (mapped by question_type)
- [x] Implement `step_detail_view` in `steps/views.py` — Form rendering, saving, status changes
- [x] Create `steps/templates/steps/step_detail.html` — Full step form page with header, progress, navigation
- [x] Create `steps/templates/steps/partials/question_field.html` — Per-question-type field rendering with character count
- [x] Add HTMX auto-save via `/steps/auto-save/` endpoint with 2s debounce + save indicator
- [x] Create `steps/templates/steps/partials/save_indicator.html` — "Saved ✓" indicator partial
- [x] Add "Mark Complete" / "Revisit Step" status controls
- [x] Add Previous/Next step navigation
- [x] Write 14 new tests (form, detail view, auto-save) — 44 total passing (15 core + 29 steps)

### Verification
- [x] `/steps/1/` shows Step 1 with all 19 questions
- [x] User can type answers and save (form POST + HTMX auto-save)
- [x] Saved answers persist across page reloads (pre-populated in form)
- [x] Progress bar updates on step list after answering
- [x] Mark Complete / Revisit Step status controls work
- [x] 44 total tests passing

---

## Phase 6 — Auto-Save with HTMX (COMPLETE — implemented in Phase 5)

**Note**: Auto-save was already implemented as part of Phase 5. HTMX auto-save endpoint, 2s debounce, save indicators, and manual "Save All" fallback are all in place.

---

## Phase 7 — Dashboard (Progress Overview) (COMPLETE)

**Goal**: The dashboard shows meaningful progress data — step completion, sobriety counter, recent activity.

### Tasks
- [x] Update `core/views.py` — `DashboardView`: query StepProgress for user, calculate overall completion (steps complete / 12), get current step (first non-complete), get sobriety days, get recent Response updates (last 5-10)
- [x] Create `core/templates/core/partials/sobriety_widget.html` — days sober (large number), sobriety date, prompt to set if not set
- [x] Create `core/templates/core/partials/step_progress_widget.html` — 12-step visual progress (numbered circles filled/empty/active), current step with "Continue" button, overall percentage
- [x] Create `core/templates/core/partials/checkin_widget.html` — today's check-in status (Complete/Not yet), quick link to daily check-in
- [x] Create `core/templates/core/partials/recent_activity_widget.html` — last 5 answers saved (step name, question snippet, time ago), HTMX lazy-loaded
- [x] Update `core/templates/core/dashboard.html` to use real widget partials instead of placeholder cards
- [x] Implement sobriety date setting — simple form/modal to set User.sobriety_date (HTMX inline edit or settings page)
- [x] Write tests for dashboard view with real data

### Verification
- [x] Dashboard shows sobriety counter (or prompt to set sobriety date)
- [x] Step progress visualization shows completion status for all 12 steps
- [x] "Continue Step Work" button links to current step
- [x] Recent activity shows last few saved answers
- [x] Dashboard loads quickly (lazy-load heavy widgets)

---

## Phase 8 — Daily Check-In (Journal App)

**Goal**: Users can complete a daily Step 10/11 inventory and track streaks.

### Tasks
- [ ] Create the `journal` app with `python manage.py startapp journal`
- [ ] Add `journal` to `INSTALLED_APPS`
- [ ] Implement `journal/models.py` — DailyInventory model (as defined in Implementation Guide Data Models): user, date, serenity_level (1-10), was_resentful, resentful_details, was_selfish, selfish_details, was_dishonest, dishonest_details, did_pray, did_meditate, spiritual_notes, mood (1-10), additional_notes
- [ ] Implement `journal/models.py` — GratitudeEntry model: user, date, entry (text), order, created_at
- [ ] Run migrations: `python manage.py makemigrations journal && python manage.py migrate`
- [ ] Implement `journal/forms.py` — DailyInventoryForm (ModelForm, conditional fields: show details only if toggle is True via Alpine.js)
- [ ] Implement `journal/views.py` — DailyCheckinView (GET: load today's inventory or blank / POST: save), JournalHistoryView (paginated past entries), StreakView (HTMX partial for consecutive days streak)
- [ ] Create `journal/templates/journal/daily_checkin.html` — date, Step 10 section (serenity, resentful/selfish/dishonest toggles with conditional details), Step 11 section (prayer/meditation checkboxes, spiritual notes), mood slider, save button
- [ ] Create `journal/templates/journal/history.html` — calendar or list view of past entries, click to view/edit
- [ ] Create `journal/templates/journal/partials/streak_widget.html` — current streak count display
- [ ] Configure URLs: `/journal/` → DailyCheckinView, `/journal/history/` → JournalHistoryView, `/journal/<date>/` → DailyCheckinView for specific date
- [ ] Update sidebar "Daily Check-In" link to point to `/journal/` with active highlighting
- [ ] Update dashboard check-in widget to pull real data
- [ ] Register models in `journal/admin.py`
- [ ] Write tests for journal models, views, and streak calculation

### Verification
- [ ] `/journal/` shows today's daily check-in form
- [ ] Saving persists all fields
- [ ] Returning shows pre-filled form for today
- [ ] Conditional fields show/hide with Alpine.js
- [ ] `/journal/history/` shows past entries
- [ ] Streak calculation works (consecutive days)
- [ ] Dashboard check-in widget shows today's status

---

## Phase 9 — Gratitude Journal

**Goal**: Users can record daily gratitude entries, view history, and build a gratitude practice.

### Tasks
- [ ] Implement `journal/views.py` additions — GratitudeView (today's list + inline add), GratitudeAddView (HTMX POST), GratitudeDeleteView (HTMX DELETE), GratitudeHistoryView (browse by date)
- [ ] Implement `journal/forms.py` additions — GratitudeEntryForm (simple ModelForm, just the entry text field)
- [ ] Create `journal/templates/journal/gratitude.html` — today's date, list of entries, inline "Add gratitude" input with HTMX POST, delete buttons, prompt "What are you grateful for today?"
- [ ] Create `journal/templates/journal/gratitude_history.html` — browse by week/month, entries grouped by date
- [ ] Create `journal/templates/journal/partials/gratitude_entry.html` — single entry row (for HTMX swap on add/delete)
- [ ] HTMX interactions: add entry via `hx-post`, delete entry via `hx-delete`, no page reload
- [ ] Configure URLs: `/journal/gratitude/` → GratitudeView, `/journal/gratitude/add/` → GratitudeAddView, `/journal/gratitude/<uuid:pk>/delete/` → GratitudeDeleteView, `/journal/gratitude/history/` → GratitudeHistoryView
- [ ] Update sidebar "Gratitude Journal" link to point to `/journal/gratitude/` with active highlighting
- [ ] Update dashboard gratitude count widget
- [ ] Write tests for gratitude views and HTMX interactions

### Verification
- [ ] `/journal/gratitude/` shows today's gratitude list
- [ ] Adding an entry works inline (no page reload)
- [ ] Deleting an entry removes it inline
- [ ] History view shows past entries grouped by date
- [ ] Dashboard shows today's gratitude entry count

---

## Phase 10 — Amends Management (Steps 8 & 9)

**Goal**: Users can build and manage their amends list, track amends progress, and write private letters.

### Tasks
- [ ] Create the `amends` app with `python manage.py startapp amends`
- [ ] Add `amends` to `INSTALLED_APPS`
- [ ] Implement `amends/models.py` — Person model (user, name, relationship, how_harmed, willingness_level, order) and Amend model (person, status choices [not_started/letter_drafted/discussed/amend_made/ongoing], anger_letter, apology_letter, actionable_amends, sponsor_feedback, post_amend_reflection, created_at, updated_at)
- [ ] Run migrations: `python manage.py makemigrations amends && python manage.py migrate`
- [ ] Implement `amends/forms.py` — PersonForm (ModelForm), AmendForm (ModelForm for status/letters/feedback/results)
- [ ] Implement `amends/views.py` — PersonListView (all people with status summary), PersonCreateView, PersonDetailView (full amend workflow), PersonUpdateView, PersonDeleteView (with confirmation), AmendCreateView, AmendUpdateView
- [ ] Create `amends/templates/amends/person_list.html` — table/list of people, status, willingness, "Add Person" button, status filter
- [ ] Create `amends/templates/amends/person_form.html` — add/edit person form
- [ ] Create `amends/templates/amends/person_detail.html` — Step 8 info (how harmed), Step 9 amend tracking (status progression, anger letter editor with "DO NOT SEND" warning, apology letter editor, actionable amends, sponsor feedback, post-amend reflection), timeline of status changes
- [ ] Create `amends/templates/amends/partials/person_row.html` and `amends/templates/amends/partials/amend_status.html`
- [ ] HTMX interactions: status update via `hx-post` inline
- [ ] Configure URLs: `/amends/` → PersonListView, `/amends/add/` → PersonCreateView, `/amends/<uuid:pk>/` → PersonDetailView, `/amends/<uuid:pk>/edit/` → PersonUpdateView, `/amends/<uuid:pk>/delete/` → PersonDeleteView, `/amends/<uuid:pk>/amend/` → AmendCreateView, `/amends/<uuid:pk>/amend/<uuid:amend_pk>/edit/` → AmendUpdateView
- [ ] Update sidebar "Amends List" link to point to `/amends/` with active highlighting
- [ ] Register models in `amends/admin.py`
- [ ] Write tests for amends models, views, and status progression

### Verification
- [ ] `/amends/` shows amends list with status for each person
- [ ] Can add, edit, and delete people from the list
- [ ] Person detail shows full amend workflow
- [ ] Letters can be written and saved (with "DO NOT SEND" warnings)
- [ ] Amend status can be updated through the progression
- [ ] Sponsor feedback field is available

---

## Phase 11 — Export & Print

**Goal**: Users can export their completed step work, daily journals, and amends as PDF or print-friendly pages.

### Tasks
- [ ] Install ReportLab: `pip install reportlab && pip freeze > requirements.txt`
- [ ] Implement `steps/views.py` — StepExportView: generate PDF of a single step with all questions and user's answers (title, focus, questions with answers, recovery outcome)
- [ ] Implement `steps/views.py` — AllStepsExportView: generate PDF of all 12 steps with answers, table of contents, page breaks between steps
- [ ] Implement `journal/views.py` — JournalExportView: export daily inventory entries for a date range as PDF
- [ ] Create print-friendly CSS: `@media print` styles in base template (hide sidebar, navigation, buttons in print mode)
- [ ] Add export buttons: each step detail page "Export as PDF" / "Print" button, step list page "Export All Step Work" button, journal history "Export Date Range" button
- [ ] Write tests for PDF generation endpoints

### Verification
- [ ] Single step exports to PDF with answers
- [ ] All steps export to a single PDF document
- [ ] Journal entries export for a date range
- [ ] Print-friendly view works in browser (Ctrl+P)

---

## Phase 12 — Git, CI/CD & Production Deployment

**Goal**: Code in GitHub, automated deployment to powerfulsilence.com via GitHub Actions.

### Tasks
- [ ] Create `.github/workflows/deploy.yml` — GitHub Actions workflow: checkout, setup Python 3.12, install deps, collectstatic, FTP deploy to production
- [ ] Create `passenger_wsgi.py` for cPanel/Passenger deployment
- [ ] Create production `config/settings_production.py` or environment-based settings split
- [ ] Configure `collectstatic` with WhiteNoise for production static files
- [ ] Update `.gitignore` for production (staticfiles/, media/)
- [ ] Write deployment documentation in README

### Verification
- [ ] GitHub Actions workflow runs on push to main
- [ ] Static files collected correctly
- [ ] Production settings configured (DEBUG=False, proper ALLOWED_HOSTS)

---

## Phase 13 — Polish & UX Refinements

**Goal**: Improve user experience with visual polish, better navigation, and quality-of-life features.

### Tasks
- [ ] Step navigation improvements: breadcrumb (Dashboard > Step Work > Step 3), step progress indicators in sidebar, "You are here" indicator on step list
- [ ] Form UX improvements: auto-expanding textareas, word/character count per field, unsaved changes warning (Alpine.js @beforeunload), smooth scroll to first unanswered question
- [ ] Mobile responsiveness: collapsible sidebar (hamburger menu on mobile), touch-friendly form elements, adequate tap targets
- [ ] Sobriety counter enhancements: years/months/days breakdown, milestone celebration messages (30 days, 90 days, 6 months, 1 year, etc.)
- [ ] Accessibility: proper aria-label attributes, keyboard navigation for all forms, focus management for HTMX-loaded content, sufficient color contrast
- [ ] Loading states: HTMX loading indicators for auto-save, skeleton screens for lazy-loaded widgets
- [ ] Empty states: friendly messages when no data exists, clear calls-to-action to get started

### Verification
- [ ] Mobile-responsive layout works on phone and tablet
- [ ] Auto-save feedback is clear and non-intrusive
- [ ] Navigation feels intuitive
- [ ] Empty states guide the user to action
- [ ] Accessibility audit passes basic checks

---

## Notes
- PostgreSQL runs on Windows host — container connects via `host.docker.internal:5432`
- Database: `ps01_db`, User: `ps01_user`, Password: `devpassword123`
- Reference: `00_research/PS01-Implementation-Guide.md` for detailed specs
- Tests use SQLite via `config/settings_test.py` (pytest.ini `--ds` flag overrides docker-compose env var)
- Phase 6 (Auto-Save) was completed as part of Phase 5
- After container restart, run `pip install -r requirements.txt` before starting Ralph
