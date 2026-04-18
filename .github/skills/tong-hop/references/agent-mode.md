# AGENT_MODE — Agent-Enhanced Pipeline

> Feature flag that toggles between the static pipeline (original) and the  
> agent-enhanced pipeline (strategist → dynamic workflow → tiered audit → advisory).  
> Default: `AGENT_MODE: true`. Set to `false` for backward-compatible behavior.

---

## Feature Flag

```yaml
AGENT_MODE: true   # Toggle agent-enhanced pipeline

# When AGENT_MODE: true (default)
#   Pipeline uses the full agent architecture:
#   1. Model detection → capability profile (references/model-detection.md)
#   2. Shared context initialization (references/agent-context-schema.md)
#   3. Strategist agent → dynamic workflow (agents/strategist.md)
#   4. Tiered audit at every step (references/tiered-audit.md)
#   5. Advisory agent for decisions (agents/advisory.md)
#   6. Final audit with step-level rollback (references/final-audit-rollback.md)
#   7. Conditional skill-forge if needed (references/conditional-skill-forge.md)
#
# When AGENT_MODE: false (backward compatible)
#   Pipeline uses the original static flow:
#   Step 0 → Step 1 → Step 1.5 → Step 2 → Step 3 → Step 4 (loop)
#   No agents, no shared context, no dynamic workflow, no tiered audit.
#   All existing skills work exactly as before.
```

---

## AGENT_MODE Pipeline Flow

```yaml
AGENT_MODE_FLOW:
  # This flow WRAPS the existing pipeline — existing skills are NOT modified.
  # Agents provide orchestration intelligence on top of the same sub-skills.

  step_A1_model_detection:
    reference: references/model-detection.md
    action: |
      Detect current model's capabilities (context window, reasoning, tool_use, etc.)
      Write model_profile to shared context (tmp/.agent-context.json)
    skip_if: AGENT_MODE == false

  step_A2_init_shared_context:
    reference: references/agent-context-schema.md
    action: |
      Initialize tmp/.agent-context.json with:
      - user_request (from Step 1 + Step 1.5 analysis)
      - model_profile (from step_A1)
      - workflow: {} (to be filled by strategist)
      - audit_history: []
      - decisions: []
      - escalation_log: []
    skip_if: AGENT_MODE == false

  step_A3_strategist:
    agent: agents/strategist.md
    action: |
      Strategist reads user_request + model_profile from shared context.
      Generates dynamic workflow:
      - Selects workflow template (report/presentation/data-collection/translation/comparison)
      - Chooses variant (basic/standard/advanced) based on model profile
      - Customizes steps, quality gates, budget estimates
      Writes workflow to shared context.
    budget: 1 call
    skip_if: AGENT_MODE == false
    fallback: Use static pipeline (Step 2 → Step 3 → Step 4)

  step_A4_execute_workflow:
    action: |
      Execute steps from strategist's generated workflow.
      Each step:
      1. Read step config from shared context workflow.steps[i]
      2. Execute the assigned skill (thu-thap, bien-soan, tao-*, etc.)
      3. Apply quality gate per tiered-audit.md:
         - Tier 1 self-review: always
         - Tier 2 agent audit: critical steps only
      4. If quality gate fails: retry with instructions (max per step)
      5. Update shared context: step status, audit_history
      6. Move to next step
    reference: references/tiered-audit.md
    skip_if: AGENT_MODE == false (use Step 4 quality loop instead)

  step_A5_advisory_decisions:
    agent: agents/advisory.md
    action: |
      Called DURING execution when a decision is needed:
      - Ambiguous routing (which skill to use?)
      - Quality tradeoff (retry or deliver?)
      - Skill gap detected (forge new skill or use alternative?)
    budget: max 2 calls per pipeline
    reference: references/conditional-skill-forge.md, references/public-skill-clone.md
    skip_if: AGENT_MODE == false (decisions made inline)

  step_A6_final_audit:
    reference: references/final-audit-rollback.md
    action: |
      Compare final output against user's original request.
      If fails: identify failing step → rollback → re-execute from that step.
      Fail-fast: if score doesn't improve between retries, deliver best available.
    budget: 1 call + retries within pipeline budget cap (30 total)
    skip_if: AGENT_MODE == false (use Step 4.7 kiem-tra instead)

AGENT_MODE_BUDGET:
  total_agent_calls: 30 (hard cap)
  breakdown:
    model_detection: 0 (inline)
    context_init: 0 (inline)
    strategist: 1
    advisory: 0-2
    tier_2_audits: 0-4
    final_audit: 1
    retries: remaining budget
  enforcement: references/agent-context-protocol.md (budget check before every write)
```

---

## Backward Compatibility (AGENT_MODE: false)

```yaml
BACKWARD_COMPATIBLE:
  principle: |
    When AGENT_MODE is false, the pipeline behaves EXACTLY as before v1.3.
    No agents are called. No shared context file is created.
    The original Step 0 → Step 1 → Step 1.5 → ... → Step 4 flow runs unchanged.
    
  what_changes:
    - No tmp/.agent-context.json created
    - No strategist, advisory, or audit agents called
    - Quality review uses existing Step 4 inline loop (max 2 retries)
    - Final check uses kiem-tra skill directly (no rollback protocol)
    - No model detection or capability profiling
    
  what_stays_the_same:
    - All sub-skills (thu-thap, bien-soan, tao-*) work identically
    - File placement rules still enforced
    - Auto-escalation still works (it's per-skill, not agent-dependent)
    - Session resume via save_state.py still works
    - Request deep analysis (Step 1.5) still runs
    - Output chaining still works
    - Content depth defaults still apply (comprehensive)
    
  user_experience:
    - User still says request → gets output
    - User doesn't know or care about AGENT_MODE
    - Only difference: with agents, quality is more systematically checked
```
