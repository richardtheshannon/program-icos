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

# Note: Model selection via CLAUDE_CODE_CMD in .ralphrc is not compatible
# with Ralph's stdbuf invocation. Model defaults to Claude's configured default.
log "=== Using default Claude model ==="

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
