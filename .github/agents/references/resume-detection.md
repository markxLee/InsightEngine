# Resume Detection Protocol (Orchestrator)

> Extracted from orchestrator.agent.md for maintainability.
> Referenced by: orchestrator core agent.

---

## Resume Check

On every session start, orchestrator checks for in-progress state and offers
intelligent resume that works across chat sessions, context resets, and crashes.

```yaml
RESUME_CHECK:
  1. Run: python3 scripts/save_state.py check
  
  2. If IN_PROGRESS (schema v2):
     a. Run: python3 scripts/save_state.py resume-plan
     b. Parse step_states to identify:
        - last_completed: last step with status=completed
        - failed_step: step with status=failed (if any)
        - next_pending: first step with status=pending
     c. Verify output files still exist (check paths from output_files[])
     d. Restore session_mode and autonomy_mode from state:
        - SET session_mode from state.session_mode
        - SET autonomy_mode from state.autonomy_mode
        (User does NOT need to re-confirm mode on resume)
     e. Present resume summary in Vietnamese:
        "📋 Phát hiện pipeline đang dở:
         Yêu cầu: {raw_prompt[:150]}
         Intent: {intent_classification}
         Đã xong: {completed_count}/{total_count} bước
         Bước cuối: {last_completed.name} ✅
         Bước tiếp: {next_pending.name}
         {if failed_step: '⚠️ Bước lỗi: {failed_step.name} — {error}'}
         {if missing_files: '⚠️ File output bị thiếu: {missing_files}'}
         
         Chọn:
         1. Tiếp tục từ bước {next_pending.name}
         2. Làm lại từ bước {failed_step.name} (nếu có lỗi)
         3. Bắt đầu lại hoàn toàn (archive state cũ)"
     e. Execute based on user choice:
        continue: Skip completed steps, resume from next_pending
        retry_failed: Re-execute failed step, then continue
        restart: Archive state, start fresh pipeline
  
  3. If IN_PROGRESS (schema v1 — legacy):
     - Show basic summary
     - Ask: "Bạn muốn tiếp tục hay bắt đầu lại?"
     - Resume from last current_step
  
  4. If NO_STATE or COMPLETED: start fresh
```

---

## Cross-Session Resume

```yaml
CROSS_SESSION_RESUME:
  how_it_works:
    - State is persisted to tmp/.session-state.json (file system, survives chat reset)
    - Each step saves incrementally — never lose more than 1 step of progress
    - Output files are tracked with hashes — detect if files were modified externally
    - Works across: new chat sessions, context compressor resets, VS Code restarts
    
  limitations:
    - Cannot resume if tmp/ directory is cleaned
    - Cannot resume if output files are deleted (will re-generate from failed step)
    - State file grows with score_history — archive periodically
    
  triggers:
    - "tiếp tục", "resume", "tiếp tục từ lần trước"
    - "pipeline đang dở", "continue from where I left off"
    - Any new request when IN_PROGRESS state exists → prompt resume choice
```
