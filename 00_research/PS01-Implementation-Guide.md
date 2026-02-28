# PS01 Implementation Guide
## Powerful Silence — 12-Step Recovery Web Application

**Project:** PS01 (Powerful Silence v0.1)
**Domain:** powerfulsilence.com
**Framework:** Django 5.x
**Database:** PostgreSQL
**Created:** February 2026

---

## Project Summary

PS01 is a Django-based web application that guides AA (Alcoholics Anonymous) members through all 12 steps of recovery using interactive forms. Users create an account, progress through structured step-work worksheets with original guided questions, save their responses to a database, track their progress on a dashboard, and maintain ongoing daily recovery practices (Step 10 inventory, Step 11 prayer/meditation check-ins, gratitude journaling).

**Key decisions:**
- Standalone Django project (separate from SF4)
- Single-user seeded account (multi-user registration added later)
- AA-focused (architected for future multi-program support)
- Free forever (no payment infrastructure)
- No AI features
- PostgreSQL database (consistent with SF4 patterns)
- Same tech stack as SF4: Django + HTMX + Alpine.js + Tailwind CSS (CDN)
- Deployed on same WHM VPS as SF4, under the `powerfulsilence` cPanel account

---

## Tech Stack

### Backend
- **Python:** 3.12
- **Framework:** Django 5.x
- **Database:** PostgreSQL (dev: local, prod: server — requires upgrade from 9.6 to 16+)
- **WSGI Server:** Dev: `runserver` / Prod: Passenger (mod_passenger)

### Frontend
- **Templates:** Django template engine (server-side rendering)
- **HTMX:** 2.x (dynamic interactions, auto-save, lazy loading)
- **Alpine.js:** 3.x (local UI state, dropdowns, collapsibles)
- **Tailwind CSS:** 3.x (CDN, no build step)
- **Icons:** Lucide Icons (CDN)

### Key Python Dependencies
- **django-crispy-forms** + **crispy-tailwind** — Form rendering
- **python-decouple** — Environment variable management
- **psycopg2-binary** — PostgreSQL adapter
- **whitenoise** — Static file serving with compression
- **django-axes** — Login attempt rate limiting

### No Build Step
All JS/CSS loaded via CDN. No npm, no webpack, no node_modules.

---

## Project Structure

```
d:\_dev\powerfulsilence-com\
├── config/                      # Django project package (settings, urls, wsgi)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                        # Core app (User model, auth, middleware)
│   ├── models.py                # Custom User model
│   ├── views.py                 # Login, logout, dashboard
│   ├── middleware.py             # LoginRequiredMiddleware
│   ├── admin.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_user.py     # Seeded superuser command
│   └── templates/
│       ├── base.html            # Base layout + sidebar
│       ├── components/
│       │   ├── sidebar.html
│       │   ├── topbar.html
│       │   └── messages.html
│       ├── core/
│       │   ├── login.html
│       │   └── dashboard.html
│       └── registration/
│           └── login.html
├── steps/                       # Step work app (the heart of the application)
│   ├── models.py                # Step, Question, Response, StepProgress
│   ├── views.py                 # Step list, step detail/form, auto-save
│   ├── forms.py                 # Dynamic step work forms
│   ├── admin.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_steps.py    # Seed 12 steps + questions
│   ├── templates/
│   │   └── steps/
│   │       ├── step_list.html          # All 12 steps overview
│   │       ├── step_detail.html        # Single step with form
│   │       └── partials/
│   │           ├── step_card.html      # Step card for list view
│   │           ├── question_field.html # Single question field
│   │           └── progress_bar.html   # Step completion indicator
│   └── templatetags/
│       └── step_tags.py         # Custom template filters
├── journal/                     # Daily practice app (Steps 10, 11, gratitude)
│   ├── models.py                # DailyInventory, GratitudeEntry
│   ├── views.py                 # Daily check-in, history, streaks
│   ├── forms.py
│   ├── admin.py
│   ├── templates/
│   │   └── journal/
│   │       ├── daily_checkin.html
│   │       ├── history.html
│   │       └── partials/
│   │           ├── entry_row.html
│   │           └── streak_widget.html
├── amends/                      # Steps 8 & 9 amends management
│   ├── models.py                # Person, Amend, AmendLetter
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── templates/
│   │   └── amends/
│   │       ├── person_list.html
│   │       ├── person_detail.html
│   │       ├── person_form.html
│   │       └── partials/
│   │           ├── person_row.html
│   │           └── amend_status.html
├── templates/                   # Project-level template overrides
├── static/                      # Project-level static files (minimal — CDN-first)
│   ├── css/
│   │   └── custom.css           # Any Tailwind overrides
│   └── img/
│       └── logo.svg
├── 00_research/                 # Research docs (analysis, implementation guide)
├── _TEMP/                       # Temp docs (prompts, workflow guides)
├── .ralph/                      # Ralph autonomous agent configuration
│   ├── PROMPT.md                # Ralph per-loop prompt (project context)
│   ├── AGENT.md                 # Build/test/run commands
│   ├── fix_plan.md              # Current phase task checklist
│   └── logs/                    # Ralph execution logs
├── Dockerfile                   # Dev container (Python 3.12 + Claude Code CLI)
├── docker-compose.yml           # Dev container service (connects to host PostgreSQL)
├── manage.py
├── conftest.py                  # pytest configuration
├── requirements.txt
├── .env                         # Environment variables (not in git)
├── .env.example                 # Template for .env
├── .ralphrc                     # Ralph project configuration
├── .gitignore
└── README.md
```

---

## Data Models

### Core App

```python
# core/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model. Mirrors SF4 pattern."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sobriety_date = models.DateField(null=True, blank=True)
    fellowship = models.CharField(max_length=50, default='AA')  # Future: choices for NA, OA, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def sobriety_days(self):
        """Returns number of days sober, or None if no sobriety date set."""
        if self.sobriety_date:
            from django.utils import timezone
            return (timezone.now().date() - self.sobriety_date).days
        return None

    def __str__(self):
        return self.email or self.username
```

### Steps App

```python
# steps/models.py
import uuid
from django.db import models
from django.conf import settings

class Step(models.Model):
    """One of the 12 steps. Seeded via management command."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveIntegerField(unique=True)  # 1-12
    title = models.CharField(max_length=200)            # e.g. "Admitting Powerlessness"
    description = models.TextField()                     # The step's principle text
    focus = models.TextField()                           # "Focus of step" guidance
    recovery_outcome = models.TextField()                # "How this step helps us recover"
    spiritual_principle = models.CharField(max_length=100)  # e.g. "Honesty"
    order = models.PositiveIntegerField(default=0)
    is_recurring = models.BooleanField(default=False)    # True for steps 10, 11, 12

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"Step {self.number}: {self.title}"


class Question(models.Model):
    """A guided question within a step. Seeded via management command."""

    class QuestionType(models.TextChoices):
        TEXT = 'text', 'Open-ended text'
        YESNO_ELABORATE = 'yesno', 'Yes/No + Elaborate'
        LIST_BUILDER = 'list', 'List builder'
        LETTER = 'letter', 'Letter writing'
        ACTION_PLAN = 'action', 'Action planning'
        DAILY = 'daily', 'Daily recurring'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='questions')
    number = models.PositiveIntegerField()               # Order within the step
    text = models.TextField()                             # The question itself
    help_text = models.TextField(blank=True)              # Optional guidance/context
    question_type = models.CharField(
        max_length=10,
        choices=QuestionType.choices,
        default=QuestionType.TEXT
    )
    is_required = models.BooleanField(default=False)     # All optional — recovery is personal

    class Meta:
        ordering = ['step__number', 'number']
        unique_together = ['step', 'number']

    def __str__(self):
        return f"Step {self.step.number}, Q{self.number}"


class Response(models.Model):
    """A user's answer to a question. One response per user per question."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer = models.TextField(blank=True)                 # The user's written response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user} — {self.question}"


class StepProgress(models.Model):
    """Tracks a user's progress on a specific step."""

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETE = 'complete', 'Complete'
        REVISITING = 'revisiting', 'Revisiting'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='step_progress')
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)                  # Personal notes about this step
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'step']
        ordering = ['step__number']

    def __str__(self):
        return f"{self.user} — Step {self.step.number}: {self.status}"

    def completion_percentage(self):
        """Calculate % of questions answered for this step."""
        total = self.step.questions.count()
        if total == 0:
            return 0
        answered = Response.objects.filter(
            user=self.user,
            question__step=self.step
        ).exclude(answer='').count()
        return int((answered / total) * 100)
```

### Journal App

```python
# journal/models.py
import uuid
from django.db import models
from django.conf import settings

class DailyInventory(models.Model):
    """Step 10 daily personal inventory. One per user per day."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inventories')
    date = models.DateField()
    
    # Step 10 daily prompts
    what_helped_serenity = models.TextField(blank=True,
        verbose_name="What did I do today that helped me obtain serenity and peace of mind?")
    what_failed_serenity = models.TextField(blank=True,
        verbose_name="What failed to bring serenity? What can I learn from this?")
    was_resentful = models.BooleanField(default=False, verbose_name="Was I resentful today?")
    resentful_details = models.TextField(blank=True)
    was_selfish = models.BooleanField(default=False, verbose_name="Was I self-serving today?")
    selfish_details = models.TextField(blank=True)
    was_dishonest = models.BooleanField(default=False, verbose_name="Was I dishonest today?")
    dishonest_details = models.TextField(blank=True)
    amends_needed = models.TextField(blank=True,
        verbose_name="Do I owe anyone an amend from today? What happened?")
    
    # Step 11 spiritual check-in
    did_pray_morning = models.BooleanField(default=False, verbose_name="Did I pray this morning?")
    did_pray_evening = models.BooleanField(default=False, verbose_name="Did I pray this evening?")
    did_meditate = models.BooleanField(default=False, verbose_name="Did I meditate today?")
    spiritual_notes = models.TextField(blank=True,
        verbose_name="Notes on my conscious contact with my Higher Power today")
    
    # General
    overall_mood = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="How am I feeling overall? (1-10)"
    )
    additional_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        verbose_name_plural = 'Daily inventories'

    def __str__(self):
        return f"{self.user} — {self.date}"


class GratitudeEntry(models.Model):
    """Daily gratitude list. Supports multiple entries per day."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gratitude_entries')
    date = models.DateField()
    entry = models.TextField(verbose_name="I am grateful for...")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'order']
        verbose_name_plural = 'Gratitude entries'

    def __str__(self):
        return f"{self.user} — {self.date}: {self.entry[:50]}"
```

### Amends App

```python
# amends/models.py
import uuid
from django.db import models
from django.conf import settings

class Person(models.Model):
    """A person on the user's Step 8 amends list."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='amends_people')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=200, blank=True,
        verbose_name="Relationship to me (e.g., mother, ex-wife, former boss)")
    how_i_harmed_them = models.TextField(blank=True,
        verbose_name="How did my behavior affect their life?")
    how_it_affected_relationship = models.TextField(blank=True,
        verbose_name="How did it affect our relationship?")
    is_addiction_related = models.BooleanField(default=True,
        verbose_name="Is this harm related to my addiction?")
    willingness_level = models.PositiveIntegerField(
        default=5,
        verbose_name="Willingness to make amends (1-10)"
    )
    notes = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'People'

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class Amend(models.Model):
    """Step 9 amends tracking for a specific person."""

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        LETTER_DRAFTED = 'letter_drafted', 'Letter/Apology Drafted'
        DISCUSSED_WITH_SPONSOR = 'discussed', 'Discussed with Sponsor'
        AMEND_MADE = 'amend_made', 'Amend Made'
        ONGOING = 'ongoing', 'Ongoing / Living Amend'
        NOT_POSSIBLE = 'not_possible', 'Not Possible (would cause harm)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='amends')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    
    # Letter writing (Step 9 exercises)
    anger_letter = models.TextField(blank=True,
        verbose_name="Letter expressing anger (DO NOT SEND)")
    apology_letter = models.TextField(blank=True,
        verbose_name="Apology / statement of amends (DO NOT SEND)")
    actionable_amends = models.TextField(blank=True,
        verbose_name="List of actionable amends I can make")
    sponsor_feedback = models.TextField(blank=True,
        verbose_name="Sponsor's comments on my amends plan")
    
    # After making amends
    what_happened = models.TextField(blank=True,
        verbose_name="What happened when I made amends?")
    what_i_learned = models.TextField(blank=True,
        verbose_name="What did I learn from this experience?")
    did_defend_self = models.BooleanField(null=True, blank=True,
        verbose_name="Did I have a desire to defend myself?")
    defense_details = models.TextField(blank=True)
    further_amends_needed = models.BooleanField(default=False,
        verbose_name="Do I need to make further amends?")
    further_amends_notes = models.TextField(blank=True)
    
    amend_date = models.DateField(null=True, blank=True,
        verbose_name="Date amend was made")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Amend to {self.person.name}: {self.status}"
```

---

## Development Phases

Each phase is designed to be completable in 1-3 sessions. Phases are strictly ordered — do not skip ahead. Each phase ends with a testable, working state.

---

### Phase 1: Project Scaffolding & Docker Setup
**Goal:** Empty Django project that runs in Docker, with custom User model, seeded superuser, and Ralph configured for autonomous development.
**Depends on:** Nothing (starting from scratch)
**Prerequisites:** PostgreSQL running on Windows host, Docker Desktop installed, WSL with Ralph installed

**Tasks:**

1.1. Create `Dockerfile` (based on SF4 v1 pattern):
```dockerfile
FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    jq \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (required for Claude Code CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user for security
RUN useradd -m -s /bin/bash developer
USER developer
WORKDIR /home/developer/project

# Python dependencies will be installed via requirements.txt at runtime
ENV PATH="/home/developer/.local/bin:$PATH"

CMD ["bash"]
```

1.2. Create `docker-compose.yml` (dev container only — connects to host PostgreSQL):
```yaml
services:
  dev:
    build: .
    container_name: ps01-dev
    environment:
      - DATABASE_URL=postgresql://ps01_user:devpassword123@host.docker.internal:5432/ps01_db
      - DJANGO_SETTINGS_MODULE=config.settings
      - PYTHONDONTWRITEBYTECODE=1
      - SECRET_KEY=dev-secret-key-change-in-production
      - DEBUG=True
      - ALLOWED_HOSTS=*
      - PS01_USER_EMAIL=${PS01_USER_EMAIL:-admin@powerfulsilence.com}
      - PS01_USER_PASSWORD=${PS01_USER_PASSWORD:-devpassword123}
      - PS01_USER_FIRST_NAME=${PS01_USER_FIRST_NAME:-Admin}
      - PS01_USER_LAST_NAME=${PS01_USER_LAST_NAME:-User}
    volumes:
      - .:/home/developer/project
      - pip-cache:/home/developer/.cache/pip
      - ~/.claude:/home/developer/.claude
    ports:
      - "8000:8000"
    stdin_open: true
    tty: true
    command: bash

volumes:
  pip-cache:
```

1.3. Create PostgreSQL database on Windows host:
```bash
# From Windows — using psql or pgAdmin
createdb ps01_db
createuser ps01_user -P   # Set password: devpassword123
# Grant privileges:
psql -c "GRANT ALL PRIVILEGES ON DATABASE ps01_db TO ps01_user;"
```

1.4. Create `.env` file with required variables:
```bash
SECRET_KEY=your-generated-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://ps01_user:devpassword123@host.docker.internal:5432/ps01_db
PS01_USER_EMAIL=your@email.com
PS01_USER_PASSWORD=your-secure-password
PS01_USER_FIRST_NAME=YourFirst
PS01_USER_LAST_NAME=YourLast
```

1.5. Build Docker container and enter it:
```bash
# From WSL:
cd /mnt/d/_dev/powerfulsilence-com
docker compose build
docker compose up -d
docker compose exec dev bash
```

1.6. Install initial dependencies (inside Docker container):
```bash
pip install django psycopg2-binary python-decouple whitenoise django-crispy-forms crispy-tailwind django-axes
pip freeze > requirements.txt
```

1.7. Create Django project (inside Docker container):
```bash
django-admin startproject config .
```

1.8. Create the `core` app:
```bash
python manage.py startapp core
```

1.9. Configure `config/settings.py`:
- Set `AUTH_USER_MODEL = 'core.User'`
- Configure database from `DATABASE_URL` via `python-decouple`
- Add `core` to `INSTALLED_APPS`
- Add `whitenoise`, `crispy_forms`, `crispy_tailwind`, `axes` to `INSTALLED_APPS`
- Set `CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"` and `CRISPY_TEMPLATE_PACK = "tailwind"`
- Set `TIME_ZONE = 'America/Los_Angeles'` and `USE_TZ = True`
- Set `LOGIN_URL = '/login/'` and `LOGIN_REDIRECT_URL = '/dashboard/'`
- Configure middleware stack (matching SF4 pattern: SecurityMiddleware → WhiteNoise → Session → Common → CSRF → Auth → Messages → XFrame → LoginRequiredMiddleware → AxesMiddleware)

1.10. Implement `core/models.py` — Custom User model (as defined in Data Models section above)

1.11. Implement `core/middleware.py` — `LoginRequiredMiddleware`:
- Exempt paths: `/login/`, `/admin/`, `/static/`
- Redirect unauthenticated users to login

1.12. Implement `core/management/commands/seed_user.py`:
- Creates superuser from `.env` variables
- Idempotent (skip if user exists)

1.13. Run migrations and seed (inside Docker container):
```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_user
```

1.14. Create `.env.example` (template without secrets)

1.15. Create `.gitignore`

1.16. Initialize Ralph configuration:
- Create `.ralph/PROMPT.md` — PS01 project context for Ralph
- Create `.ralph/AGENT.md` — Build/test/run commands
- Create `.ralphrc` — Ralph project config

1.17. Verify: `python manage.py runserver 0.0.0.0:8000` → login at `localhost:8000/admin/`

**Deliverables:**
- [ ] Docker container builds and runs
- [ ] Django project runs without errors inside container
- [ ] Container connects to host PostgreSQL successfully
- [ ] Custom User model with UUID primary key
- [ ] Seeded superuser can log into admin
- [ ] LoginRequiredMiddleware redirects to `/login/`
- [ ] `.env.example` committed, `.env` in `.gitignore`
- [ ] Ralph configured (`.ralph/`, `.ralphrc` ready)
- [ ] `requirements.txt` includes all dependencies

---

### Phase 2: Base Templates & Layout
**Goal:** Base HTML layout with sidebar navigation, topbar, Tailwind styling, login/logout flow.
**Depends on:** Phase 1

**Tasks:**

2.1. Create `core/templates/base.html`:
- HTML5 boilerplate
- CDN links: Tailwind CSS, HTMX 2.x, Alpine.js 3.x, Lucide Icons
- CSRF token via `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on `<body>`
- Two-column layout: fixed sidebar + scrollable main content
- Django messages display area
- Dark background theme appropriate for recovery/reflection context

2.2. Create `core/templates/components/sidebar.html`:
- App logo/name ("Powerful Silence")
- Navigation links:
  - Dashboard
  - My Step Work (links to step list)
  - Daily Check-In (links to journal)
  - Gratitude Journal
  - Amends List (Steps 8 & 9)
- Sobriety date counter display (if set)
- Active link highlighting via Alpine.js or template tag

2.3. Create `core/templates/components/topbar.html`:
- Page title (block)
- User greeting
- Logout link

2.4. Create `core/templates/components/messages.html`:
- Django messages framework display
- Auto-dismiss with Alpine.js (`x-init="setTimeout(() => show = false, 5000)"`)

2.5. Create `core/templates/core/login.html`:
- Simple centered login form
- No sidebar (standalone layout)
- App name and brief tagline

2.6. Create `core/templates/core/dashboard.html`:
- Extends base.html
- Placeholder cards for: Step Progress Overview, Today's Check-In, Sobriety Counter, Recent Activity
- Static content for now (wired up in later phases)

2.7. Implement `core/views.py`:
- `DashboardView` — renders dashboard template
- Login/logout using Django's built-in `LoginView` / `LogoutView`

2.8. Configure `core/urls.py` and `config/urls.py`:
- `/` → redirect to `/dashboard/`
- `/dashboard/` → DashboardView
- `/login/` → LoginView
- `/logout/` → LogoutView
- `/admin/` → Django admin

**Deliverables:**
- [ ] Login page renders with Tailwind styling
- [ ] Successful login redirects to dashboard
- [ ] Dashboard shows sidebar navigation
- [ ] Sidebar links are present (point to `#` for now)
- [ ] Logout works and redirects to login
- [ ] All pages require authentication except login
- [ ] Responsive layout (sidebar collapses on mobile)

---

### Phase 3: Step Data Models & Seed Data
**Goal:** Steps and Questions tables created and populated with original content for all 12 steps.
**Depends on:** Phase 2

**Tasks:**

3.1. Create the `steps` app:
```bash
python manage.py startapp steps
```

3.2. Add `steps` to `INSTALLED_APPS`

3.3. Implement `steps/models.py` — Step, Question, Response, StepProgress models (as defined in Data Models section above)

3.4. Run migrations:
```bash
python manage.py makemigrations steps
python manage.py migrate
```

3.5. Implement `steps/management/commands/seed_steps.py`:

This is the most content-heavy task. For each of the 12 steps, seed:
- Step number, title, description, focus text, recovery outcome text, spiritual principle, is_recurring flag
- All questions with number, text, help_text, and question_type

**Step content to create (fully original questions — reference `00_research/12steppers-analysis.md` for thematic structure only, do NOT copy questions):**

**Step 1 — Admitting Powerlessness** (Spiritual Principle: Honesty)
- Focus: Recognizing that addiction has made life unmanageable
- ~15-19 questions covering: discovery of addiction, impact on relationships, isolation, financial damage, attempts to hide, health consequences, loss of control, career impact, moment of realization
- Question types: mostly `text`, some `yesno`

**Step 2 — Coming to Believe** (Spiritual Principle: Hope)
- Focus: Restoration of hope through openness to a Higher Power
- ~10-11 questions covering: beliefs about order in the universe, childhood spiritual background, current spiritual practice, anger at God/Higher Power, prior prayer experiences, conception of Higher Power
- Question types: mostly `text`

**Step 3 — Turning It Over** (Spiritual Principle: Faith)
- Focus: Surrendering control to a Higher Power
- ~9 questions covering: fear of losing control, rational vs emotional loss of control, daily Higher Power maintenance, prayer practice, trust history, life meaning, difficulty of surrender
- Question types: mostly `text`

**Step 4 — Moral Inventory** (Spiritual Principle: Courage)
- Focus: Honest self-assessment of character — both deficiencies and strengths
- ~18 questions covering: resentments, self-perception, anger patterns, revenge, self-loathing, confidence, character traits, trauma, decision patterns, responsibility, shame, self-judgment
- Question types: mostly `text`, some `list`
- NOTE: Most writing-intensive step

**Step 5 — Admitting Wrongs** (Spiritual Principle: Integrity)
- Focus: Sharing insights about flaws with others
- ~8 questions covering: loss from addiction, supportive relationships, tough love vs soft approach, sponsor relationship, fear of sharing, experience of sharing, readiness
- Question types: mostly `text`

**Step 6 — Becoming Ready** (Spiritual Principle: Willingness)
- Focus: Identifying character defects and becoming willing to have them removed
- ~12 questions covering: honesty with Higher Power, unhealthy coping, practical improvement habits, destructive patterns, community contribution, character defects list, clinging to flaws
- Question types: `text`, one `list` (five most significant defects)

**Step 7 — Humbly Asking** (Spiritual Principle: Humility)
- Focus: Asking Higher Power to remove shortcomings
- ~11 questions covering: identity without defects, letter to Higher Power, shortcomings returning, losing hope, gratitude, time with loved ones, hopefulness, losses from addiction, realistic expectations, happiness, improving the world
- Question types: `text`, one `letter`

**Step 8 — Making a List** (Spiritual Principle: Justice)
- Focus: Creating the amends list
- ~9 questions covering: damaged relationships, non-addiction apologies, picturing amends, fear of amends, potential harm from amends, worst/best expectations, releasing expectations, amends vs apology, the actual list
- Question types: `text`, one `list` (the amends list — this connects to the `amends` app)

**Step 9 — Making Amends** (Spiritual Principle: Forgiveness)
- Focus: Making amends the right way, without ulterior motives
- ~13 questions covering: prior amends attempts, genuineness check, guilt-tripping check, anger processing, sponsor collaboration, roleplay, results, self-defense urge, relationship impact, further amends
- Question types: `text`, `letter` (anger letter, apology letter), `action` (actionable amends list)
- NOTE: Several questions produce separate documents — linked to `amends` app

**Step 10 — Continued Inventory** (Spiritual Principle: Perseverance)
- Focus: Daily self-assessment and ongoing recovery practice
- ~8 questions covering: daily serenity reflection, making time for reflection, triggers, resentful/selfish/dishonest check, applying amends daily, sanity, real-time honesty, continued effort
- `is_recurring = True`
- Question types: `text`, `daily`

**Step 11 — Conscious Contact** (Spiritual Principle: Spiritual Awareness)
- Focus: Deepening relationship with Higher Power through prayer and meditation
- ~10 questions covering: belief evolution, explaining beliefs, afterlife beliefs, religion vs spirituality, prayer frequency, prayer content, meditation practice, connection during meditation, altered self-perception, remembering lack of control
- `is_recurring = True`
- Question types: mostly `text`

**Step 12 — Carrying the Message** (Spiritual Principle: Service)
- Focus: Passing recovery benefits to others, practicing principles
- ~8 questions covering: using Higher Power relationship for others, outreach to other addicts, desired support, conflict handling, recovery solidity, service plans, sponsor readiness, practicing principles
- `is_recurring = True`
- Question types: mostly `text`

3.6. Run seed command:
```bash
python manage.py seed_steps
```

3.7. Register models in `steps/admin.py` for verification

3.8. Verify: All 12 steps and ~130 questions visible in Django admin

**Deliverables:**
- [ ] `Step` table populated with 12 steps (all fields filled)
- [ ] `Question` table populated with ~130 original questions
- [ ] Each question has correct `question_type` assigned
- [ ] Steps 10, 11, 12 have `is_recurring = True`
- [ ] `seed_steps` command is idempotent (safe to re-run)
- [ ] All models visible and editable in Django admin

---

### Phase 4: Step List View (The 12 Steps Overview)
**Goal:** A page showing all 12 steps with progress indicators and navigation to individual step forms.
**Depends on:** Phase 3

**Tasks:**

4.1. Implement `steps/views.py` — `StepListView`:
- Query all 12 steps with prefetch of questions
- For current user, get or create `StepProgress` for each step
- Calculate completion percentage per step
- Pass steps with their progress to template

4.2. Create `steps/templates/steps/step_list.html`:
- Extends `base.html`
- Page title: "My Step Work"
- Grid or list of 12 step cards, each showing:
  - Step number (large, prominent)
  - Step title
  - Spiritual principle
  - Status badge (Not Started / In Progress / Complete / Revisiting)
  - Completion percentage bar
  - Number of questions answered / total
  - Link to step detail page
- Visual distinction for current step (first incomplete step)
- Steps 10, 11, 12 marked with a "recurring" indicator

4.3. Create `steps/templates/steps/partials/step_card.html`:
- HTMX-friendly partial for individual step card
- Used for lazy-loading progress updates

4.4. Create `steps/templates/steps/partials/progress_bar.html`:
- Reusable progress bar component
- Color-coded: gray (not started), blue (in progress), green (complete), amber (revisiting)

4.5. Configure `steps/urls.py`:
- `/steps/` → StepListView

4.6. Wire into `config/urls.py`:
```python
path('steps/', include('steps.urls')),
```
(in `config/urls.py`)

4.7. Update sidebar link to point to `/steps/`

**Deliverables:**
- [ ] `/steps/` shows all 12 steps in order
- [ ] Each step card shows title, spiritual principle, and question count
- [ ] Progress bars show 0% for all steps (no answers yet)
- [ ] Clicking a step card navigates to `/steps/<number>/`
- [ ] Page is styled consistently with dashboard

---

### Phase 5: Step Detail View & Form (Core Step Work)
**Goal:** Users can view a single step, answer all its questions in a form, and save their responses.
**Depends on:** Phase 4

**Tasks:**

5.1. Implement `steps/views.py` — `StepDetailView`:
- Fetch step by number (URL: `/steps/<int:number>/`)
- Fetch all questions for this step
- Fetch existing responses for current user (pre-populate form)
- Get or create `StepProgress` for this user/step
- On first visit, set status to `in_progress` and `started_at`

5.2. Implement `steps/forms.py` — `StepWorkForm`:
- Dynamic form: generates one field per question
- Field names: `q_{question.id}`
- Pre-populates with existing `Response.answer` values
- All fields optional (no forced completion)
- Field types mapped from `Question.question_type`:
  - `text` → `forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))`
  - `yesno` → custom: BooleanField + CharField pair
  - `letter` → `forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))`
  - `list` → `forms.CharField(widget=forms.Textarea(attrs={'rows': 6}))` (future: dynamic rows)
  - `action` → `forms.CharField(widget=forms.Textarea(attrs={'rows': 6}))`
  - `daily` → `forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))`

5.3. Implement `StepDetailView.post()`:
- Save/update `Response` for each answered question
- Update `StepProgress`:
  - If any answers exist → `in_progress`
  - If all questions answered → keep `in_progress` (user marks complete manually)
- Show success message
- Redirect back to same step (stay on page)

5.4. Create `steps/templates/steps/step_detail.html`:
- Extends `base.html`
- Header: Step number, title, spiritual principle
- "Focus of this step" expandable section (Alpine.js collapsible)
- Form with all questions rendered in order
- Each question shows:
  - Question number and text
  - Help text (if any) in muted color
  - Textarea or appropriate field
  - Character count indicator (Alpine.js)
- "Save Progress" button at bottom (and sticky save button for long forms)
- "How this step helps us recover" section at bottom
- Navigation: Previous Step / Next Step links
- Status controls: "Mark as Complete" / "Mark as Revisiting" buttons

5.5. Create `steps/templates/steps/partials/question_field.html`:
- Reusable question rendering partial
- Displays question text, help text, and form field

5.6. Configure URL:
- `/steps/<int:number>/` → StepDetailView

**Deliverables:**
- [ ] `/steps/1/` shows Step 1 with all ~19 questions
- [ ] All questions render as textareas
- [ ] Saving the form persists answers to the database
- [ ] Returning to the step pre-fills previously saved answers
- [ ] Previous/Next step navigation works
- [ ] Step status updates to "In Progress" on first save
- [ ] "Mark as Complete" button sets status to "Complete"
- [ ] Progress on step list view updates after saving

---

### Phase 6: Auto-Save with HTMX
**Goal:** Answers auto-save as the user types, so no work is lost. No full page reload needed.
**Depends on:** Phase 5

**Tasks:**

6.1. Implement `steps/views.py` — `auto_save_response` (HTMX endpoint):
- Accepts POST with `question_id` and `answer`
- Creates or updates the `Response` record
- Returns a small HTML partial confirming save (e.g., "Saved ✓" with timestamp)
- Updates `StepProgress` status if needed

6.2. Add HTMX attributes to each question textarea:
```html
hx-post="/steps/auto-save/"
hx-trigger="keyup changed delay:2000ms"
hx-vals='{"question_id": "{{ question.id }}"}'
hx-target="#save-indicator-{{ question.id }}"
hx-swap="innerHTML"
hx-include="[name='q_{{ question.id }}']"
```

6.3. Create `steps/templates/steps/partials/save_indicator.html`:
- Small "Saved ✓" text with timestamp
- Fades in with CSS transition

6.4. Add a global save indicator in the topbar or sticky footer:
- "All changes saved" / "Saving..." / "Unsaved changes" status
- Alpine.js state management for tracking pending saves

6.5. Configure URL:
- `/steps/auto-save/` → auto_save_response

6.6. Keep the manual "Save All" button as a fallback (standard form POST)

**Deliverables:**
- [ ] Typing in a question textarea triggers auto-save after 2 seconds of inactivity
- [ ] "Saved ✓" indicator appears next to the saved field
- [ ] No page reload during auto-save
- [ ] Manual "Save All" button still works as fallback
- [ ] CSRF token is included in HTMX requests via `hx-headers` on `<body>`
- [ ] Network errors show a non-disruptive warning

---

### Phase 7: Dashboard (Progress Overview)
**Goal:** The dashboard shows meaningful progress data — step completion, sobriety counter, recent activity.
**Depends on:** Phase 6

**Tasks:**

7.1. Update `core/views.py` — `DashboardView`:
- Query all `StepProgress` for current user
- Calculate overall completion (steps complete / 12)
- Get current step (first non-complete step)
- Get sobriety days from `User.sobriety_date`
- Get recent `Response` updates (last 5-10)
- Get today's `DailyInventory` (if exists — may be None until Phase 8)
- Get today's gratitude entries count

7.2. Update `core/templates/core/dashboard.html`:
- **Sobriety Counter Widget:**
  - Days sober (large number)
  - Sobriety date
  - If not set, prompt to set it (link to profile/settings)
- **Step Progress Widget:**
  - 12-step visual progress (numbered circles, filled/empty/active)
  - Current step highlighted with "Continue" button
  - Overall percentage complete
- **Today's Check-In Widget:**
  - Status: Complete / Not yet done
  - Quick link to daily check-in form
- **Recent Activity Widget:**
  - Last 5 answers saved (step name, question snippet, time ago)
  - HTMX lazy-loaded: `hx-trigger="load"` → `/dashboard/partials/recent-activity/`

7.3. Create dashboard partial templates:
- `core/templates/core/partials/sobriety_widget.html`
- `core/templates/core/partials/step_progress_widget.html`
- `core/templates/core/partials/checkin_widget.html`
- `core/templates/core/partials/recent_activity_widget.html`

7.4. Implement sobriety date setting:
- Simple form/modal to set `User.sobriety_date`
- HTMX inline edit or dedicated settings page

**Deliverables:**
- [ ] Dashboard shows sobriety counter (or prompt to set sobriety date)
- [ ] Step progress visualization shows completion status for all 12 steps
- [ ] "Continue Step Work" button links to current step
- [ ] Recent activity shows last few saved answers
- [ ] Dashboard loads quickly (lazy-load heavy widgets)

---

### Phase 8: Daily Check-In (Journal App)
**Goal:** Users can complete a daily Step 10/11 inventory and track streaks.
**Depends on:** Phase 7

**Tasks:**

8.1. Create the `journal` app:
```bash
python manage.py startapp journal
```

8.2. Add `journal` to `INSTALLED_APPS`

8.3. Implement `journal/models.py` — `DailyInventory` and `GratitudeEntry` (as defined in Data Models section)

8.4. Run migrations:
```bash
python manage.py makemigrations journal
python manage.py migrate
```

8.5. Implement `journal/forms.py`:
- `DailyInventoryForm` — ModelForm for DailyInventory
- Conditional fields: show `resentful_details` only if `was_resentful` is True (Alpine.js)
- Same for `selfish_details` and `dishonest_details`

8.6. Implement `journal/views.py`:
- `DailyCheckinView` — GET: load today's inventory (or blank form) / POST: save
  - If inventory exists for today, pre-populate
  - If not, create new
- `JournalHistoryView` — paginated list of past daily inventories
- `StreakView` (HTMX partial) — calculate current streak of consecutive days with check-ins

8.7. Create templates:
- `journal/daily_checkin.html`:
  - Date (today) displayed prominently
  - Step 10 section: serenity questions, resentful/selfish/dishonest toggles with conditional detail fields
  - Step 11 section: prayer/meditation checkboxes, spiritual notes
  - Overall mood slider (1-10)
  - Additional notes
  - Save button
- `journal/history.html`:
  - Calendar or list view of past entries
  - Click to view/edit past entries
- `journal/partials/streak_widget.html`:
  - Current streak count
  - "🔥 5 day streak!" style display

8.8. Configure URLs:
- `/journal/` → DailyCheckinView (today's check-in)
- `/journal/history/` → JournalHistoryView
- `/journal/<date>/` → DailyCheckinView for a specific past date

8.9. Update sidebar links
8.10. Update dashboard check-in widget to pull real data

**Deliverables:**
- [ ] `/journal/` shows today's daily check-in form
- [ ] Saving persists all fields
- [ ] Returning shows pre-filled form
- [ ] Conditional fields show/hide with Alpine.js
- [ ] `/journal/history/` shows past entries
- [ ] Streak calculation works (consecutive days)
- [ ] Dashboard check-in widget shows today's status

---

### Phase 9: Gratitude Journal
**Goal:** Users can record daily gratitude entries, view history, and build a gratitude practice.
**Depends on:** Phase 8

**Tasks:**

9.1. Implement `journal/views.py` additions:
- `GratitudeView` — show today's gratitude list with inline add form
- `GratitudeAddView` — HTMX endpoint to add a new entry
- `GratitudeDeleteView` — HTMX endpoint to remove an entry
- `GratitudeHistoryView` — browse past gratitude entries by date

9.2. Implement `journal/forms.py` additions:
- `GratitudeEntryForm` — simple ModelForm (just the `entry` text field)

9.3. Create templates:
- `journal/gratitude.html`:
  - Today's date
  - List of today's gratitude entries (if any)
  - Inline "Add gratitude" input with HTMX POST
  - Each entry has a delete button (HTMX DELETE)
  - Prompt: "What are you grateful for today?"
- `journal/gratitude_history.html`:
  - Browse by week/month
  - Entries grouped by date
- `journal/partials/gratitude_entry.html`:
  - Single entry row (for HTMX swap on add/delete)

9.4. HTMX interactions:
- Add entry: `hx-post="/journal/gratitude/add/"` → swaps in new entry row
- Delete entry: `hx-delete="/journal/gratitude/<id>/delete/"` → removes row

9.5. Configure URLs:
- `/journal/gratitude/` → GratitudeView
- `/journal/gratitude/add/` → GratitudeAddView
- `/journal/gratitude/<uuid:pk>/delete/` → GratitudeDeleteView
- `/journal/gratitude/history/` → GratitudeHistoryView

9.6. Update sidebar links
9.7. Update dashboard gratitude count widget

**Deliverables:**
- [ ] `/journal/gratitude/` shows today's gratitude list
- [ ] Adding a gratitude entry works inline (no page reload)
- [ ] Deleting an entry removes it inline
- [ ] History view shows past entries grouped by date
- [ ] Dashboard shows today's gratitude entry count

---

### Phase 10: Amends Management (Steps 8 & 9)
**Goal:** Users can build and manage their amends list, track amends progress, and write private letters.
**Depends on:** Phase 5 (step work forms should be functional)

**Tasks:**

10.1. Create the `amends` app:
```bash
python manage.py startapp amends
```

10.2. Add `amends` to `INSTALLED_APPS`

10.3. Implement `amends/models.py` — Person, Amend (as defined in Data Models section)

10.4. Run migrations

10.5. Implement `amends/forms.py`:
- `PersonForm` — ModelForm for adding/editing a person
- `AmendForm` — ModelForm for the amends process (status, letters, feedback, results)

10.6. Implement `amends/views.py`:
- `PersonListView` — all people on the amends list, with status summary
- `PersonCreateView` — add a new person
- `PersonDetailView` — view person details + amends history
- `PersonUpdateView` — edit person details
- `PersonDeleteView` — remove (with confirmation)
- `AmendCreateView` — start an amend for a person
- `AmendUpdateView` — update amend progress (status changes, letters, results)

10.7. Create templates:
- `amends/person_list.html`:
  - Table/list of all people on amends list
  - Shows: name, relationship, amend status, willingness level
  - "Add Person" button
  - Status filter (all / not started / in progress / complete)
  - Reorderable (drag or up/down buttons)
- `amends/person_form.html`:
  - Add/edit person form
- `amends/person_detail.html`:
  - Full detail view of a person
  - Step 8 info: how harmed, relationship impact
  - Step 9 amend tracking:
    - Status progression (visual: Not Started → Letter Drafted → Discussed → Amend Made → Ongoing)
    - Anger letter editor (with "DO NOT SEND" warning)
    - Apology letter editor (with "DO NOT SEND" warning)
    - Actionable amends list
    - Sponsor feedback notes
    - Post-amend reflection fields
  - Timeline of status changes

10.8. HTMX interactions:
- Status update: `hx-post` to update amend status inline
- Inline add person from step 8 form (future integration)

10.9. Configure URLs:
- `/amends/` → PersonListView
- `/amends/add/` → PersonCreateView
- `/amends/<uuid:pk>/` → PersonDetailView
- `/amends/<uuid:pk>/edit/` → PersonUpdateView
- `/amends/<uuid:pk>/delete/` → PersonDeleteView
- `/amends/<uuid:pk>/amend/` → AmendCreateView
- `/amends/<uuid:pk>/amend/<uuid:amend_pk>/edit/` → AmendUpdateView

10.10. Update sidebar links

**Deliverables:**
- [ ] `/amends/` shows amends list with status for each person
- [ ] Can add, edit, and delete people from the list
- [ ] Person detail shows full amend workflow
- [ ] Letters can be written and saved (with "DO NOT SEND" warnings)
- [ ] Amend status can be updated through the progression
- [ ] Sponsor feedback field is available

---

### Phase 11: Export & Print
**Goal:** Users can export their completed step work, daily journals, and amends as PDF or print-friendly pages.
**Depends on:** Phases 5, 8, 10

**Tasks:**

11.1. Install ReportLab (or weasyprint):
```bash
pip install reportlab
pip freeze > requirements.txt
```

11.2. Implement `steps/views.py` — `StepExportView`:
- Generate PDF of a single step with all questions and the user's answers
- Include: step title, focus, questions with answers, recovery outcome
- Print-friendly formatting

11.3. Implement `steps/views.py` — `AllStepsExportView`:
- Generate PDF of all 12 steps with all answers
- Table of contents
- Page breaks between steps

11.4. Implement `journal/views.py` — `JournalExportView`:
- Export daily inventory entries for a date range as PDF

11.5. Create print-friendly CSS:
- `@media print` styles in base template
- Hide sidebar, navigation, buttons in print mode

11.6. Add export buttons:
- Each step detail page: "Export as PDF" / "Print" button
- Step list page: "Export All Step Work" button
- Journal history: "Export Date Range" button

**Deliverables:**
- [ ] Single step exports to PDF with answers
- [ ] All steps export to a single PDF document
- [ ] Journal entries export for a date range
- [ ] Print-friendly view works in browser (Ctrl+P)

---

### Phase 12: Git, CI/CD & Production Deployment
**Goal:** Code in GitHub, automated deployment to powerfulsilence.com via GitHub Actions.
**Depends on:** All previous phases (or can be done in parallel starting Phase 2)

**Tasks:**

12.1. **Prerequisites (manual, one-time server setup):**
- Upgrade PostgreSQL on production server from 9.6 to 16+ (coordinate with hosting)
- Create PostgreSQL database for PS01 on production
- Set up Python 3.12 virtualenv in `/home/powerfulsilence/`
- Configure Passenger for Python/Django in cPanel
- Create `tmp/` directory for Passenger restart
- Install Python dependencies in virtualenv
- Create production `.env` file
- Configure HTTPS (Let's Encrypt via cPanel)

12.2. **Production directory structure:**
```
/home/powerfulsilence/
├── public_html/                  # Document root (Passenger entry point)
│   ├── passenger_wsgi.py         # Passenger WSGI config
│   ├── tmp/
│   │   └── restart.txt           # Touch to restart Passenger
│   └── static/                   # Collected static files
├── app/                          # Django project (above public_html)
│   ├── config/                   # Project package (settings, urls, wsgi)
│   ├── core/
│   ├── steps/
│   ├── journal/
│   ├── amends/
│   ├── manage.py
│   └── .env                      # Production environment variables
└── venv/                         # Python virtualenv
```

12.3. **Create `passenger_wsgi.py`:**
```python
import sys
import os

sys.path.insert(0, '/home/powerfulsilence/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

12.4. **Initialize Git repository:**
```bash
cd d:\_dev\powerfulsilence-com
git init
git remote add origin git@github.com:YOUR_USERNAME/powerfulsilence-com.git
```

12.5. **Create `.gitignore`:**
```
.env
__pycache__/
*.pyc
db.sqlite3
staticfiles/
media/
*.log
.DS_Store
.ralph/logs/
```

12.6. **Create GitHub Actions workflow (`.github/workflows/deploy.yml`):**
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Collect static files
        run: |
          python manage.py collectstatic --noinput
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DEBUG: 'False'
          DATABASE_URL: 'sqlite:///dummy.db'

      - name: FTP Deploy
        uses: SamKirkland/FTP-Deploy-Action@v4.3.5
        with:
          server: ${{ secrets.FTP_HOST }}
          username: ${{ secrets.FTP_USER }}
          password: ${{ secrets.FTP_PASS }}
          local-dir: ./
          server-dir: /app/
          exclude: |
            **/.git*/**
            **/venv/**
            **/__pycache__/**
            .env

      - name: Restart Passenger
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          password: ${{ secrets.SSH_PASS }}
          script: |
            touch /home/powerfulsilence/public_html/tmp/restart.txt
```

12.7. **Production settings additions (in `config/settings.py`):**
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

12.8. **Post-deployment checklist:**
```bash
# SSH into production
cd /home/powerfulsilence/app
source ../venv/bin/activate
python manage.py migrate
python manage.py seed_user
python manage.py seed_steps
python manage.py collectstatic --noinput
touch ../public_html/tmp/restart.txt
```

**Deliverables:**
- [ ] Code pushed to GitHub
- [ ] GitHub Actions deploys on push to `main`
- [ ] `collectstatic` runs in CI
- [ ] FTP upload transfers code to production
- [ ] Passenger restart works
- [ ] Site loads at https://powerfulsilence.com
- [ ] Login works in production
- [ ] HTTPS enforced
- [ ] Migrations run on production
- [ ] Seed data loaded on production

---

### Phase 13: Polish & UX Refinements
**Goal:** Improve the user experience with visual polish, better navigation, and quality-of-life features.
**Depends on:** All previous phases

**Tasks:**

13.1. **Step navigation improvements:**
- Breadcrumb: Dashboard > Step Work > Step 3
- Step progress indicators in sidebar (small dots or numbers)
- "You are here" indicator on step list

13.2. **Form UX improvements:**
- Auto-expanding textareas (grow as user types)
- Word/character count per field
- Unsaved changes warning before navigation (Alpine.js `@beforeunload`)
- Smooth scroll to first unanswered question option

13.3. **Mobile responsiveness:**
- Collapsible sidebar (hamburger menu on mobile)
- Touch-friendly form elements
- Adequate tap targets for buttons

13.4. **Sobriety counter enhancements:**
- Show years, months, days breakdown
- Milestone celebration messages (30 days, 90 days, 6 months, 1 year, etc.)

13.5. **Accessibility:**
- Proper `aria-label` attributes on interactive elements
- Keyboard navigation for all forms
- Focus management for HTMX-loaded content
- Sufficient color contrast

13.6. **Loading states:**
- HTMX loading indicators for auto-save
- Skeleton screens for lazy-loaded widgets

13.7. **Empty states:**
- Friendly messages when no data exists (no entries, no amends, etc.)
- Clear calls-to-action to get started

**Deliverables:**
- [ ] Mobile-responsive layout works on phone and tablet
- [ ] Auto-save feedback is clear and non-intrusive
- [ ] Navigation feels intuitive
- [ ] Empty states guide the user to action
- [ ] Accessibility audit passes basic checks

---

## Future Phases (Post-MVP)

These are not part of the initial build but are architecturally accounted for:

**Phase 14: Multi-User Registration**
- Self-service registration (email + password)
- Email verification
- Password reset flow
- All data scoped by `user` foreign key (already built into models)

**Phase 15: Multi-Program Support**
- Add program selection (AA, NA, OA, etc.) to user profile
- Customize question language per program
- `Fellowship` model with program-specific step text variants

**Phase 16: Sponsor/Sponsee Relationships**
- Sponsor can invite sponsee via email/link
- Sponsee can share specific step work or daily check-ins with sponsor
- Read-only view for sponsors
- Messaging between sponsor/sponsee

**Phase 17: Community Features**
- Meeting finder (external API integration or directory)
- Anonymous sharing of gratitude entries (opt-in)
- Milestone celebrations shared with community

**Phase 18: Email Notifications**
- Daily check-in reminder (configurable time)
- Weekly progress summary
- Milestone congratulation emails

---

## Environment Variables Reference

### Required (All Environments)
```bash
SECRET_KEY=                      # Django secret key
DEBUG=                           # True/False
ALLOWED_HOSTS=                   # Comma-separated domains
DATABASE_URL=                    # PostgreSQL connection string
DJANGO_SETTINGS_MODULE=config.settings  # Django settings module

# Seeded superuser
PS01_USER_EMAIL=                 # Superuser email
PS01_USER_PASSWORD=              # Superuser password
PS01_USER_FIRST_NAME=            # First name
PS01_USER_LAST_NAME=             # Last name
```

### Development (Docker)
```bash
DATABASE_URL=postgresql://ps01_user:devpassword123@host.docker.internal:5432/ps01_db
DEBUG=True
ALLOWED_HOSTS=*
```

### Static/Media Files
```bash
STATIC_URL=/static/
STATIC_ROOT=/path/to/staticfiles/
MEDIA_URL=/media/
MEDIA_ROOT=/path/to/media/
```

### Production Only
```bash
ALLOWED_HOSTS=powerfulsilence.com,www.powerfulsilence.com
DATABASE_URL=postgresql://ps01_user:PROD_PASSWORD@localhost:5432/ps01_db
DEBUG=False
```

---

## URL Map (Complete)

```
/                               → Redirect to /dashboard/
/login/                         → Login page
/logout/                        → Logout + redirect to login
/dashboard/                     → Main dashboard
/dashboard/partials/*           → HTMX lazy-loaded dashboard widgets

/steps/                         → 12 steps overview (list)
/steps/<int:number>/            → Step detail + question form
/steps/auto-save/               → HTMX auto-save endpoint
/steps/<int:number>/export/     → Export single step as PDF
/steps/export-all/              → Export all steps as PDF

/journal/                       → Today's daily check-in
/journal/history/               → Past daily inventories
/journal/<date>/                → Specific date's inventory
/journal/gratitude/             → Today's gratitude entries
/journal/gratitude/add/         → HTMX add gratitude entry
/journal/gratitude/<id>/delete/ → HTMX delete gratitude entry
/journal/gratitude/history/     → Past gratitude entries
/journal/export/                → Export journal as PDF

/amends/                        → Amends list (all people)
/amends/add/                    → Add person to list
/amends/<id>/                   → Person detail + amend workflow
/amends/<id>/edit/              → Edit person details
/amends/<id>/delete/            → Delete person
/amends/<id>/amend/             → Create amend record
/amends/<id>/amend/<id>/edit/   → Update amend progress

/admin/                         → Django admin
```

---

## Key Conventions (Matching SF4 Patterns)

1. **UUID primary keys** on all models
2. **Django template engine** for all HTML (no Jinja2, no React)
3. **CDN-loaded frontend** — no npm, no build step
4. **HTMX for dynamic interactions** — auto-save, lazy loading, inline updates
5. **Alpine.js for local UI state** — dropdowns, collapsibles, toggles, conditional fields
6. **Tailwind CSS via CDN** — utility-first styling
7. **Crispy Forms + Tailwind pack** — form rendering
8. **`@login_required` via middleware** — all views require auth
9. **CSRF via `hx-headers` on `<body>`** — HTMX CSRF pattern
10. **Management commands for seeding** — `seed_user`, `seed_steps`
11. **Environment variables via `python-decouple`** — never hardcode secrets
12. **WhiteNoise for static files** — compression + caching
13. **Partials in `templates/{app}/partials/`** — HTMX fragment convention
14. **Settings package is `config/`** — not named after the project (matches SF4)
15. **Docker dev environment** — all development happens inside the Docker container
16. **Ralph for autonomous development** — phase-by-phase via `.ralph/fix_plan.md`
17. **PostgreSQL on host** — Docker container connects via `host.docker.internal`

---

*This guide is a living document. Update it as decisions change or new phases are added.*
