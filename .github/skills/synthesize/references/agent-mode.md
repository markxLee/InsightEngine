# AGENT_MODE — Shared Agent Pipeline (Phase 8 Migration)

> **Status: ALWAYS ON.** The AGENT_MODE feature flag has been retired.  
> All agent calls now use **shared agents** at `.github/skills/shared-agents/`.  
> Inline agents at `tong-hop/agents/` are ARCHIVED — do not use.  
> Calling protocol: `.github/skills/shared-agents/agent-protocol.md`

---

## Architecture (Post-Migration)

```yaml
SHARED_AGENTS:
  strategist:
    file: .github/skills/shared-agents/strategist.md
    budget: max 1 call per pipeline
    purpose: Generate dynamic workflow from user request + model profile
    
  auditor:
    file: .github/skills/shared-agents/auditor.md
    budget: max 5 calls per pipeline
    purpose: Quality verification at tier-2 audit gates + final audit
    
  advisory:
    file: .github/skills/shared-agents/advisory.md
    budget: max 2 calls per pipeline
    purpose: Multi-perspective decision support when routing is ambiguous

CALLING_CONVENTION:
  protocol: .github/skills/shared-agents/agent-protocol.md
  pattern: READ agent .md → BUILD prompt from template → CALL runSubagent → PARSE response
  
ARCHIVED_INLINE_AGENTS:
  - tong-hop/agents/strategist.md → ARCHIVED (replaced by shared-agents/strategist.md)
  - tong-hop/agents/advisory.md → ARCHIVED (replaced by shared-agents/advisory.md)
```

---

## Pipeline Flow (Shared Agents)

```yaml
PIPELINE_FLOW:
  # Agents provide orchestration intelligence on top of the same sub-skills.
  # All calls use shared-agents/ via runSubagent (see agent-protocol.md).

  step_A1_model_detection:
    reference: references/model-detection.md
    action: |
      Detect current model's capabilities (context window, reasoning, tool_use, etc.)
      Write model_profile to shared context (tmp/.agent-context.json)

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

  step_A3_strategist:
    agent: .github/skills/shared-agents/strategist.md
    call_via: runSubagent (see agent-protocol.md)
    action: |
      READ shared-agents/strategist.md → BUILD prompt → CALL runSubagent.
      Strategist reads user_request + model_profile.
      Generates dynamic workflow:
      - Selects workflow template (report/presentation/data-collection/translation/comparison)
      - Chooses variant (basic/standard/advanced) based on model profile
      - Customizes steps, quality gates, budget estimates
      Writes workflow to shared context.
    budget: 1 call
    fallback: Use static pipeline (Step 2 → Step 3 → Step 4)

  step_A4_execute_workflow:
    action: |
      Execute steps from strategist's generated workflow.
      Each step:
      1. Read step config from shared context workflow.steps[i]
      2. Execute the assigned skill (thu-thap, bien-soan, tao-*, etc.)
      3. Apply quality gate:
         - Tier 1 self-review: always (VERIFY-OR-LOOP in SKILL.md)
         - Tier 2 agent audit: critical steps → call shared-agents/auditor.md via runSubagent
      4. If quality gate fails: retry with instructions (max per step)
      5. Update shared context: step status, audit_history
      6. Move to next step
    reference: references/tiered-audit.md

  step_A5_advisory_decisions:
    agent: .github/skills/shared-agents/advisory.md
    call_via: runSubagent (see agent-protocol.md)
    action: |
      Called DURING execution when a decision is needed:
      - Ambiguous routing (which skill to use?)
      - Quality tradeoff (retry or deliver?)
      - Skill gap detected (forge new skill or use alternative?)
    budget: max 2 calls per pipeline
    reference: references/conditional-skill-forge.md, references/public-skill-clone.md

  step_A6_final_audit:
    reference: references/final-audit-rollback.md
    agent: .github/skills/shared-agents/auditor.md
    call_via: runSubagent
    action: |
      Compare final output against user's original request.
      If fails: identify failing step → rollback → re-execute from that step.
      Fail-fast: if score doesn't improve between retries, deliver best available.
    budget: 1 call + retries within pipeline budget cap
    
PIPELINE_BUDGET:
  # Aligned with agent-protocol.md budgets
  strategist: 1
  advisory: max 2
  auditor: max 5 (includes tier-2 audits + final audit)
  total: max 8 agent calls per pipeline run
  enforcement: Check budget before every runSubagent call
```

---

## Archived Inline Agents

```yaml
ARCHIVED:
  tong-hop/agents/strategist.md:
    status: ARCHIVED — replaced by shared-agents/strategist.md
    reason: Phase 8 migration to shared Copilot agent architecture
    action: Do NOT read or call this file. Use shared-agents/strategist.md instead.
    
  tong-hop/agents/advisory.md:
    status: ARCHIVED — replaced by shared-agents/advisory.md
    reason: Phase 8 migration to shared Copilot agent architecture
    action: Do NOT read or call this file. Use shared-agents/advisory.md instead.
```
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
