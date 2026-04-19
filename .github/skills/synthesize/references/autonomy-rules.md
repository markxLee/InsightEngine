# Autonomy Rules — Reference

## Overview

InsightEngine's autonomy rules govern when and how the pipeline adjusts its
level of interactivity based on user signals. There are three interaction modes:

| Mode | Description | Trigger |
|------|-------------|---------|
| `guided` | Show plan → wait for approval → ask at each major step | Default, first run |
| `standard` | Show plan → wait for approval → execute autonomously | After plan confirmed (US-12.1.1) |
| `silent` | Execute immediately after intent analysis, minimal output | User frustration signal detected |

---

## Frustration Signal Detection

### Signal Categories

```yaml
FRUSTRATION_SIGNALS:

  EXPLICIT_OVERLOAD:
    # User directly states too many questions
    patterns:
      - "sao hỏi nhiều vậy"
      - "tại sao phải xác nhận nhiều thứ"
      - "cứ làm đi đừng hỏi"
      - "không cần hỏi"
      - "hỏi ít thôi"
      - "just do it"
      - "stop asking"
      - "just proceed"
      - "too many questions"
      - "cứ tự làm đi"
      - "không cần xác nhận"
      - "làm luôn đi"
    confidence: HIGH
    action: switch_to_silent_mode

  IMPATIENCE:
    # Short commands implying "obviously":
    patterns:
      - "ok" (repeated 2+ times in a row)
      - "tiếp", "tiếp đi"
      - "đồng ý rồi, làm tiếp"
      - "yes yes"
      - "cứ làm thôi"
      - "thôi được rồi làm đi"
    confidence: MEDIUM
    action: activate_autonomy_mode (if not already active)

  REPEATED_APPROVAL:
    # User has approved 3+ consecutive prompts without modification
    condition: consecutive_approvals >= 3
    confidence: MEDIUM
    action: add_note_to_user + activate_autonomy_mode
    note: >
      "💡 Bạn đã xác nhận nhiều bước liên tiếp. Lần sau tôi sẽ tự thực hiện
      toàours mà không hỏi thêm. Gõ 'guided' nếu muốn tôi hỏi lại."

  EXPLICIT_N8N_COMPARISON:
    # User compares InsightEngine unfavorably to automation tools
    patterns:
      - "n8n không hỏi nhiều vậy"
      - "tự động hơn được không"
      - "giống n8n thì tốt hơn"
      - "không tự động như n8n"
      - "cần nhiều bước quá"
    confidence: HIGH
    action: switch_to_silent_mode + explain_autonomy_mode
```

### Detection Rules

```yaml
DETECTION_RULES:
  when_to_check:
    - After every user message
    - Apply to the full message text (case-insensitive, accent-normalized)
    
  pattern_matching:
    - Check all EXPLICIT_OVERLOAD patterns first (high confidence)
    - Check IMPATIENCE patterns second
    - Track consecutive_approvals counter throughout session
    - Check EXPLICIT_N8N_COMPARISON if any n8n/auto/tự động keyword present
    
  normalization:
    - Lowercase
    - Strip diacritics for comparison: "hỏi" → "hoi" (optional, for pattern variants)
    - Trim whitespace
```

---

## Mode Switching Protocol

```yaml
MODE_SWITCHING:
  
  guided → standard:
    trigger: User confirms plan at Step 1.5
    action: SET session_mode=standard, SET autonomy_mode=true
    announce: (silent — just proceed)
    
  guided/standard → silent:
    trigger: FRUSTRATION_SIGNAL detected (HIGH confidence) or EXPLICIT_OVERLOAD
    action:
      1. SET session_mode=silent
      2. Acknowledge once in Vietnamese (friendly, non-apologetic)
      3. Proceed immediately with best assumptions
    announce: |
      "Được rồi! Tôi sẽ tự thực hiện và chỉ báo khi có kết quả.
      Bạn có thể gõ 'hỏi lại' bất lúc nào nếu muốn tôi confirm từng bước."
      
  silent → guided:
    trigger: User says "guided", "hỏi lại tôi", "confirm từng bước"
    action: SET session_mode=guided, RESET autonomy_mode=false
    announce: |
      "Được! Tôi sẽ hỏi xác nhận ở mỗi bước quan trọng."

  PERSIST:
    - Mode persists for entire session
    - Saved to session state: session_mode field
    - NOT reset between pipeline runs in same session
```

---

## Silent Mode Behavior

When `session_mode=silent`:

```yaml
SILENT_MODE:
  skip:
    - Plan presentation (just execute with inferred plan)
    - All inter-step confirmations
    - "Bạn có muốn..." questions
    - Progress updates between sub-steps
    
  keep:
    - ONE brief intake confirmation ("🔍 Thu thập từ 5 nguồn về AI Vietnam...")
    - ONE notification when EACH major output file is ready
    - Final delivery summary
    - Critical error reporting
    
  infer_automatically:
    - Content depth (default: comprehensive)
    - Output format (infer from context or last used)
    - Style (infer from context or corporate default)
    - Source platforms (use standard search strategy)
    
  word_budget: 200 words max for entire user-visible output during execution
```

---

## Implementation Note for Orchestrator

```yaml
ORCHESTRATOR_INTEGRATION:
  on_every_user_message:
    1. Check for frustration signals BEFORE processing intent
    2. If signal detected: update session_mode, announce mode change (once), proceed
    3. Log mode transitions: "session_mode changed from {old} to {new} at {step}"
    
  session_state_fields:
    session_mode: "guided | standard | silent"  # default: guided
    consecutive_approvals: integer              # reset on modification
    frustration_detected: boolean
    frustration_signal: string | null           # which pattern triggered it
    
  reference: ".github/skills/synthesize/references/autonomy-rules.md"
```
