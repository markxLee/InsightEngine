# AGENT_MODE — Standalone Copilot Agent Pipeline

> **Status: ACTIVE.** All agent calls go through standalone Copilot agents at `.github/agents/*.agent.md`.
> Inline agent stubs at `synthesize/agents/` were deleted in Phase 10 cleanup.
> Calling protocol: VS Code custom-agent runtime via `runSubagent(agentName=..., prompt=..., description=...)`.

---

## Architecture

```yaml
STANDALONE_AGENTS:
  orchestrator:
    file: .github/agents/orchestrator.agent.md
    user_invocable: true
    purpose: Central request handler — classifies intent and routes to skills/agents

  strategist:
    file: .github/agents/strategist.agent.md
    budget: max 5 calls per pipeline run (initial_plan + replan + child_workflow share budget)
    purpose: Generate dynamic workflow from user request + model profile

  auditor:
    file: .github/agents/auditor.agent.md
    user_invocable: true
    budget: max 5 calls per pipeline run
    purpose: 100-point weighted quality verification at per-step audit gates + final audit

  advisory:
    file: .github/agents/advisory.agent.md
    budget: max 2 calls per pipeline
    purpose: Multi-perspective decision support when routing is ambiguous

CALLING_CONVENTION:
  pattern: |
    READ .github/agents/<name>.agent.md →
    BUILD prompt from agent's documented input format →
    CALL runSubagent(agentName="<name>", prompt=<built_prompt>, description="<purpose>") →
    PARSE response per agent's documented output format
```

---

## Pipeline Flow (Standalone Agents)

```yaml
PIPELINE_FLOW:
  step_A1_model_detection:
    reference: references/model-detection.md
    action: |
      Detect current model's capabilities (context window, reasoning, tool_use, etc.).
      Write model_profile to shared context (tmp/.session-state.json).

  step_A2_init_session_state:
    reference: references/agent-context-schema.md
    action: |
      Initialize tmp/.session-state.json via:
        python3 scripts/save_state.py init "<raw_prompt>" "<intent>"
      Then extract structured requirements (RULE-6):
        python3 scripts/save_state.py extract-requirements '<json>'

  step_A3_strategist:
    agent: .github/agents/strategist.agent.md
    call_via: runSubagent(agentName="strategist", ...)
    action: |
      READ strategist.agent.md → BUILD prompt → CALL runSubagent.
      Strategist reads user_request + model_profile, returns workflow plan
      (template selection, variant, customized steps, quality gates).
      Write workflow to session state.
    budget: 1 initial_plan call (additional calls allowed for replan/child_workflow within total cap of 5)
    fallback: Use static pipeline if budget exhausted

  step_A4_execute_workflow:
    action: |
      Execute steps from strategist's generated workflow. For each step:
      1. Read step config from workflow.steps[i]
      2. Execute the assigned skill (gather, search, compose, gen-*, design, etc.)
      3. Apply quality gate:
         - Tier 1 self-review: always (VERIFY-OR-LOOP per SKILL.md)
         - Tier 2 agent audit: critical steps → call auditor agent
      4. If quality gate fails: retry with instructions (max 2 per step)
      5. Update session state: step status, audit_history
      6. Move to next step
    reference: references/tiered-audit.md, references/per-step-audit.md

  step_A5_advisory_decisions:
    agent: .github/agents/advisory.agent.md
    call_via: runSubagent(agentName="advisory", ...)
    action: |
      Called DURING execution when a non-trivial decision is needed:
      - Ambiguous routing (which skill to use?)
      - Quality tradeoff (retry or deliver?)
      - Skill gap detected (forge new skill or use alternative?)
    budget: max 2 calls per pipeline
    reference: references/conditional-skill-forge.md, references/public-skill-clone.md

  step_A6_final_audit:
    reference: references/final-audit-rollback.md
    agent: .github/agents/auditor.agent.md
    call_via: runSubagent(agentName="auditor", ...)
    action: |
      Compare final output against user's original request and structured requirements.
      If fails: identify failing step → rollback → re-execute from that step.
      Fail-fast: if score doesn't improve between retries, deliver best available with gap report.
    budget: shared with per-step auditor calls (5 total per pipeline)

PIPELINE_BUDGET:
  strategist: max 5 (initial_plan + replan + child_workflow)
  advisory:   max 2
  auditor:    max 5 (per-step + final)
  total:      max 12 agent calls per pipeline run
  enforcement: Check budget before every runSubagent call
```

---

## Migration History

```yaml
HISTORY:
  phase_8:
    note: Created shared-agents directory (later removed) for cross-skill agent reuse.

  phase_9:
    note: |
      Migrated to VS Code standalone agent format (.github/agents/*.agent.md).
      Each agent file has YAML frontmatter (name, description, tools, user-invocable).

  phase_10:
    note: |
      Deleted the legacy directory under .github/skills/ entirely.
      Updated all references to point to .github/agents/.
      Deleted archived inline stubs at synthesize/agents/{strategist,advisory}.md.

  active_invocation:
    pattern: runSubagent(agentName="<name>", prompt=..., description=...)
    locations: All gen-*/SKILL.md Step 5 auditor gates use this pattern.
```
