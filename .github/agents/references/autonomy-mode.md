# Autonomy Mode & Dynamic Mode Switching (Orchestrator)

> Extracted from orchestrator.agent.md for maintainability.
> Referenced by: orchestrator core agent.

---

## Autonomy Mode

After the user confirms the plan (Step 4), `autonomy_mode=true` activates for this pipeline run.

```yaml
AUTONOMY_MODE:
  description: >
    Fire-and-forget execution. User said "go" — now pipeline runs end-to-end
    without interruption. No technical gates. One final delivery message.

  activates_when:
    - User responds to plan presentation with any approval signal:
        ["ok", "đồng ý", "tiếp tục", "được", "yes", "go", "làm đi", "bắt đầu"]
    - Signal is case-insensitive; short confirmations count

  behavior_when_active:
    execute_autonomously:
      - All steps per the approved plan
      - All technical decisions (library choice, query strategy, batch size, retry count)
      - All file format details (page size, font, column widths, chart type)
      - Retry logic: auto-retry up to 2x before marking step failed
    
    suppress:
      - "Bạn có muốn tiếp tục không?" style questions
      - Step-by-step confirmations between skills
      - Technical questions like "dùng thư viện nào?", "format gì?"
      - Batch approval gates ("Đã thu thập 10 items, tiếp tục không?")

    allowed_interruptions:
      content_ambiguity:
        description: >
          A CONTENT detail is genuinely unclear and would cause wrong output
          (e.g., which specific province, which company sector)
        action: Ask ONE inline question in Vietnamese, then proceed with best assumption
        max: 1 per pipeline run
      total_failure:
        description: All retry attempts for a critical step are exhausted
        action: Report to user with partial results, stop gracefully

  progress_updates:
    step_done:    "✅ {step_name} — xong ({brief_summary})"
    collecting:   "🔍 {source}: ✅ {count} items"
    generating:   "📄 Đang tạo {file_type}..."
    retrying:     "⚠️ Thử lại {step} ({attempt}/2)..."
    
  delivery:
    format: Single summary message at the end (see Final Delivery section)
    no_intermediate_approvals: true
```

---

## Frustration Signal Detection

On EVERY user message, orchestrator checks for frustration signals BEFORE processing intent.

```yaml
FRUSTRATION_DETECTION:
  reference: ".github/skills/synthesize/references/autonomy-rules.md"
  
  PROCESS:
    1. Check message against EXPLICIT_OVERLOAD patterns (high confidence → silent mode)
    2. Check IMPATIENCE patterns (medium confidence → activate autonomy_mode)
    3. Check consecutive_approvals counter (≥3 → activate autonomy_mode + note)
    4. Check EXPLICIT_N8N_COMPARISON patterns (high confidence → silent mode)
    
  ON_DETECTION:
    silent_mode:
      - SET session_mode=silent
      - Reply ONCE: "Được rồi! Tôi sẽ tự thực hiện..."
      - Proceed immediately
    autonomy_mode:
      - SET autonomy_mode=true (if not already)
      - No announcement needed if plan already in progress
    
  SESSION_STATE_FIELDS:
    session_mode: "guided | standard | silent"   # default: guided
    consecutive_approvals: integer               # reset on any modification
    frustration_detected: boolean
```

---

## Dynamic Mode Switching

Full protocol for transitioning between interaction modes during a session.

```yaml
DYNAMIC_MODE_SWITCHING:
  reference: ".github/skills/synthesize/references/autonomy-rules.md"

  GUIDED_TO_STANDARD:
    trigger: User approves plan at pipeline Step 4 (any approval signal)
    approval_signals: ["ok", "đồng ý", "tiếp tục", "được", "yes", "go", "làm đi", "bắt đầu"]
    action:
      - SET session_mode=standard
      - SET autonomy_mode=true
    announcement: (none — just proceed)
    reversible: Yes (user can say "hỏi lại" to return to guided)

  GUIDED_OR_STANDARD_TO_SILENT:
    trigger: FRUSTRATION_SIGNAL detected with HIGH confidence
    action:
      - SET session_mode=silent
      - SET autonomy_mode=true
      - Announce ONCE: "Được rồi! Tôi sẽ tự thực hiện và chỉ báo khi có kết quả."
      - Proceed immediately
    reversible: Yes (user can say "guided" or "hỏi lại tôi")

  STANDARD_TO_SILENT:
    trigger: EXPLICIT_OVERLOAD or N8N_COMPARISON or 3+ consecutive approvals
    action: Same as GUIDED_OR_STANDARD_TO_SILENT
    
  ANY_TO_GUIDED:
    trigger: User says "guided", "hỏi lại tôi", "confirm từng bước"
    action:
      - SET session_mode=guided
      - SET autonomy_mode=false
      - Announce: "Được! Tôi sẽ hỏi xác nhận ở mỗi bước quan trọng."

  PERSISTENCE:
    mode_persists: Entire session (NOT reset between pipeline runs)
    saved_to_state: session_mode, autonomy_mode fields in session JSON
    on_resume: Restore session_mode from saved state

  MODE_CHARACTERISTICS:
    GUIDED:  { confirmation_gates: "All", questions_allowed: "Unlimited", progress_updates: "Before and after each step" }
    STANDARD: { confirmation_gates: "Plan only", questions_allowed: "Max 1 content", progress_updates: "Non-interactive milestones" }
    SILENT:  { confirmation_gates: "None", questions_allowed: "None", progress_updates: "Final delivery only", word_budget: "200 max" }

  USER_COMMANDS:
    switch_to_guided:    { phrases: ["guided", "hỏi lại tôi", "confirm từng bước"], response: "Được! Tôi sẽ hỏi xác nhận ở mỗi bước quan trọng." }
    switch_to_autonomous: { phrases: ["tự động", "auto mode", "cứ làm đi"], response: "Được! Tôi sẽ tự thực hiện và chỉ báo khi có kết quả." }
    check_mode:          { phrases: ["chế độ hiện tại", "current mode"], response: "Mode hiện tại: {session_mode}" }
```
