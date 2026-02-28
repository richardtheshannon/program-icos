# PS01 Build — Ralph Phase-by-Phase Workflow

## Overview

Use Ralph (autonomous Claude Code loop) to build **Powerful Silence (PS01)** — a Django-based 12-step recovery web application — one phase at a time. Each phase is defined in `00_research/PS01-Implementation-Guide.md` (13 phases total, plus future phases).

Two modes:
- **Autonomous mode** (recommended) — `ralph-schedule.sh` runs Ralph in 2hr cycles with 1hr pauses, fully unattended
- **Manual mode** — start/stop Ralph yourself, load one phase at a time

---

## Prerequisites (One-Time Setup)

Complete these before starting Phase 1:

- [ ] Ralph installed on WSL host
- [ ] `.ralph/` initialized with `ralph-enable`
- [ ] `.ralph/PROMPT.md` configured for PS01
- [ ] `.ralph/AGENT.md` configured with build/test/run commands
- [ ] `.ralphrc` set with `ALLOWED_TOOLS="Write,Read,Edit,Bash"`
- [ ] `Dockerfile` and `docker-compose.yml` in project root
- [ ] Docker container built and working
- [ ] Claude Code authenticated inside container
- [ ] PostgreSQL running on Windows host with `ps01_db` database created
- [ ] `.env` file configured with database credentials

---

## Phase Tracker

Update this checklist as you complete each phase:

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Project Scaffolding & Docker Setup | ⬜ Not Started |
| 2 | Base Templates & Layout | ⬜ Not Started |
| 3 | Step Data Models & Seed Data (~130 questions) | ⬜ Not Started |
| 4 | Step List View (12 Steps Overview) | ⬜ Not Started |
| 5 | Step Detail View & Form (Core Step Work) | ⬜ Not Started |
| 6 | Auto-Save with HTMX | ⬜ Not Started |
| 7 | Dashboard (Progress Overview) | ⬜ Not Started |
| 8 | Daily Check-In (Journal App — Steps 10 & 11) | ⬜ Not Started |
| 9 | Gratitude Journal | ⬜ Not Started |
| 10 | Amends Management (Steps 8 & 9) | ⬜ Not Started |
| 11 | Export & Print (PDF generation) | ⬜ Not Started |
| 12 | Git, CI/CD & Production Deployment | ⬜ Not Started |
| 13 | Polish & UX Refinements | ⬜ Not Started |

---

## Autonomous Mode (Recommended)

Runs Ralph completely unattended: 2 hours on, 1 hour pause, repeat. Auto-resets the circuit breaker. Stops when all tasks are done.

### Model Selection

Choose your model before starting. Set `MODEL` at the top of `ralph-schedule.sh`:

| Model | ID | Use when |
|-------|----|----------|
| **Sonnet** (default) | `claude-sonnet-4-6` | Standard implementation tasks — views, forms, templates, HTMX integration. Fast, cost-effective. |
| **Opus** | `claude-opus-4-6` | Complex model design, seed data creation (Phase 3), debugging, architecture decisions — slower, ~5x cost |

For most phases, **Sonnet is the right choice**. Consider Opus for Phase 3 (seed data — requires writing ~130 original questions) and Phase 5 (dynamic form system).

### The Script

Save as `ralph-schedule.sh` in the project root inside the container:

```bash
#!/bin/bash
# Ralph autonomous scheduler — 2hr run / 1hr pause cycle
# Runs until no unchecked tasks remain in .ralph/fix_plan.md

# --- Model Selection ---
# Options:
#   claude-sonnet-4-6  (recommended — fast, cost-effective, great for Django views/templates)
#   claude-opus-4-6    (use for complex logic/architecture — slower, ~5x more expensive)
MODEL="claude-sonnet-4-6"

RUN_DURATION="2h"
PAUSE_DURATION="1h"
RALPH_ARGS="--live --verbose --allowed-tools Write,Read,Edit,Bash"
LOG_FILE=".ralph/logs/schedule.log"
MAX_CYCLES=50   # safety cap — prevents infinite loop if done-check breaks

mkdir -p .ralph/logs
cycle=1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Ralph Scheduler Started (model: $MODEL) ==="

# Write model into .ralphrc so Ralph picks it up
sed -i "s|^# CLAUDE_CODE_CMD=.*|CLAUDE_CODE_CMD=\"claude --model $MODEL\"|" .ralphrc
grep -q '^CLAUDE_CODE_CMD=' .ralphrc || echo "CLAUDE_CODE_CMD=\"claude --model $MODEL\"" >> .ralphrc
log "=== Model set to: $MODEL ==="

while [ $cycle -le $MAX_CYCLES ]; do
    # Check if any unchecked tasks remain
    if ! grep -q '\- \[ \]' .ralph/fix_plan.md 2>/dev/null; then
        log "=== All tasks complete! Exiting. ==="
        break
    fi

    log "=== Cycle $cycle: Resetting circuit breaker ==="
    ralph --reset-circuit >> "$LOG_FILE" 2>&1

    log "=== Cycle $cycle: Starting Ralph (limit: $RUN_DURATION) ==="
    timeout $RUN_DURATION ralph $RALPH_ARGS 2>&1 | tee -a "$LOG_FILE"

    log "=== Cycle $cycle complete. Pausing $PAUSE_DURATION ==="
    cycle=$((cycle + 1))
    sleep $PAUSE_DURATION
done

log "=== Scheduler finished after $((cycle - 1)) cycles ==="
```

### How to Run It

```bash
# From WSL — start container
cd /mnt/d/_dev/powerfulsilence-com
docker compose up -d
docker compose exec dev bash

# Inside container — create and run the script in tmux
# (tmux keeps it running if your terminal closes)
cat > ralph-schedule.sh << 'EOF'
[paste script above]
EOF
chmod +x ralph-schedule.sh

tmux new-session -s ralph-auto
./ralph-schedule.sh
# Press Ctrl+B then D to detach — it keeps running in background
```

### Monitoring Without Interrupting

```bash
# Attach to see live output
tmux attach -t ralph-auto

# Or just check logs from a second terminal
docker compose exec dev bash
tail -f .ralph/logs/schedule.log
cat .ralph/fix_plan.md | grep -E '^\- \[.\]'
```

### Stopping It

```bash
# Attach and Ctrl+C
tmux attach -t ralph-auto
# Ctrl+C

# Or kill from outside
docker compose exec dev bash -c "pkill -f ralph-schedule"
```

### Adjusting the Settings

Edit the top of `ralph-schedule.sh`:
```bash
MODEL="claude-sonnet-4-6"  # or claude-opus-4-6 for harder tasks
RUN_DURATION="2h"           # how long Ralph runs per cycle (try 1h if still hitting limits)
PAUSE_DURATION="1h"         # how long to wait between cycles (try 2h if limit doesn't reset)
```

---

## Manual Mode

### Step 1: Load Phase Tasks into fix_plan.md

Open `00_research/PS01-Implementation-Guide.md`, find the phase you're working on, and convert its tasks into checkboxes in `.ralph/fix_plan.md`.

**Format:**
```markdown
# Fix Plan — PS01 (Powerful Silence)

## Phase N — [Phase Title]

**Goal**: [Copy goal from PS01-Implementation-Guide.md]

### Tasks
- [ ] Task description 1
- [ ] Task description 2
...

### Verification
- [ ] Verify X works
- [ ] Verify Y works

## Notes
- [Phase-specific notes]
```

For each phase, reference the tasks from PS01-Implementation-Guide.md:
- Phase 1: "Phase 1: Project Scaffolding & Docker Setup"
- Phase 2: "Phase 2: Base Templates & Layout"
- Phase 3: "Phase 3: Step Data Models & Seed Data"
- Phase 4: "Phase 4: Step List View"
- Phase 5: "Phase 5: Step Detail View & Form"
- Phase 6: "Phase 6: Auto-Save with HTMX"
- Phase 7: "Phase 7: Dashboard"
- Phase 8: "Phase 8: Daily Check-In (Journal App)"
- Phase 9: "Phase 9: Gratitude Journal"
- Phase 10: "Phase 10: Amends Management"
- Phase 11: "Phase 11: Export & Print"
- Phase 12: "Phase 12: Git, CI/CD & Production Deployment"
- Phase 13: "Phase 13: Polish & UX Refinements"

### Step 2: Start Docker & Enter Container

```bash
# From WSL Ubuntu:
cd /mnt/d/_dev/powerfulsilence-com
docker compose up -d
docker compose exec dev bash
```

### Step 3: Launch Ralph

```bash
ralph --live --verbose --allowed-tools "Write,Read,Edit,Bash"
```

Ralph will:
1. Read `.ralph/PROMPT.md` (PS01 project context + rules)
2. Read `.ralph/fix_plan.md` (current phase tasks)
3. Read `00_research/PS01-Implementation-Guide.md` (detailed specifications)
4. Work through each unchecked task
5. Check off completed items
6. Exit when all tasks are done

### Step 4: Monitor Progress (Second Terminal)

```bash
cd /mnt/d/_dev/powerfulsilence-com
docker compose exec dev bash

# Check task progress
cat .ralph/fix_plan.md

# Check Ralph status
ralph --status

# Watch logs
tail -f .ralph/logs/*.log
```

### Step 5: Review & Verify

After Ralph completes:

```bash
# Check all tasks are done
cat .ralph/fix_plan.md

# Start dev server (if not running)
python manage.py runserver 0.0.0.0:8000

# Visit http://localhost:8000 and verify
```

**Review checklist:**
- [ ] All tasks in fix_plan.md are checked off
- [ ] Django runs without errors
- [ ] Pages render correctly in browser
- [ ] No JavaScript console errors
- [ ] HTMX interactions work (auto-save, lazy-load, form submit)
- [ ] Database operations work (save/load data)

### Step 6: Commit & Advance

```bash
# From Windows (or WSL):
git add -A && git commit -m "PS01 Phase N — [description]"
```

Then:
1. Update the Phase Tracker table above (change ⬜ to ✅)
2. Load the next phase's tasks into `.ralph/fix_plan.md`
3. Repeat from Step 2

---

## Quick Reference

### Starting a Session
```bash
cd /mnt/d/_dev/powerfulsilence-com
docker compose up -d
docker compose exec dev bash
ralph --live --verbose --allowed-tools "Write,Read,Edit,Bash"
```

### Stopping Ralph
- `Ctrl+C` (may need multiple presses)
- `Ctrl+\` (SIGQUIT if Ctrl+C doesn't work)
- From second terminal: `docker compose exec dev bash -c "pkill -f ralph"`

### Resuming Ralph (picks up where it left off)
```bash
ralph --live --verbose --allowed-tools "Write,Read,Edit,Bash"
```

### If Circuit Breaker Trips
```bash
ralph --circuit-status
ralph --reset-circuit
ralph --live --verbose --allowed-tools "Write,Read,Edit,Bash"
```

### If Something Goes Wrong
- Add fix tasks as new unchecked items in `.ralph/fix_plan.md`
- Re-run Ralph — it picks up new unchecked tasks
- Or fix manually and check off the items yourself

---

## File Reference

| File | Purpose |
|------|---------|
| `00_research/PS01-Implementation-Guide.md` | Full 13-phase implementation spec (models, views, templates, per-phase instructions) |
| `00_research/12steppers-analysis.md` | Content reference (12-step worksheet questions, competitive analysis, feature specs) |
| `.ralph/PROMPT.md` | Ralph's per-loop prompt (PS01 project context, rules, quick reference) |
| `.ralph/fix_plan.md` | Current phase task checklist (load one phase at a time) |
| `.ralph/AGENT.md` | Build/test/run commands |
| `.ralphrc` | Ralph configuration (tools, timeouts, circuit breaker) |

---

## Phase Dependency Chart

```
Phase 1 (Scaffolding + Docker) ──> Phase 2 (Base Templates) ──> Phase 3 (Models + Seed Data)
                                                                         │
                                                                         ▼
                                          Phase 4 (Step List) ──> Phase 5 (Step Detail + Form)
                                                                         │
                                                                         ▼
                                                              Phase 6 (Auto-Save HTMX)
                                                                         │
                                                                         ▼
                                                              Phase 7 (Dashboard)
                                                                    │         │
                                                                    ▼         ▼
                                                    Phase 8 (Journal)   Phase 10 (Amends)
                                                         │
                                                         ▼
                                                    Phase 9 (Gratitude)
                                                                    │
                                                    ────────────────┤
                                                                    ▼
                                                    Phase 11 (Export/Print)
                                                                    │
                                                                    ▼
                                                    Phase 12 (Deployment)
                                                                    │
                                                                    ▼
                                                    Phase 13 (Polish & QA)
```

**Key:** Phases 1-3 build the foundation (Django project, models, seed data). Phases 4-6 deliver core step work functionality. Phase 7 (Dashboard) ties it together. Phases 8-10 add daily practice and amends features. Phases 11-13 are export, deployment, and polish.
