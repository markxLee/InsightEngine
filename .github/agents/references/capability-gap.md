# Capability Gap Evaluation & Runtime Creation (Orchestrator)

> Extracted from orchestrator.agent.md for maintainability.
> Referenced by: orchestrator core agent.

---

## Capability Gap Evaluation

Before executing any workflow, orchestrator evaluates whether existing skills and agents
can fulfill the request.

```yaml
GAP_EVALUATION:
  trigger: After intent classification, before workflow execution
  
  steps:
    1. MAP request requirements to available skills/agents
    2. IDENTIFY specific gaps (missing skill, lacking mode/feature, no agent)
    3. CLASSIFY gap severity: critical | moderate | minor
    4. REPORT to user (Vietnamese, guided mode only):
       IF session_mode == "guided":
         "⚠️ Phát hiện thiếu khả năng:
          - {gap}: {description} (mức: {severity})
          Đề xuất: {solution}"
       ELSE:
         → Log gap to session state for improve session later
    5. IF user approves creation → Route to runtime creation protocol
    6. IF user declines OR autonomy/silent mode → Proceed with existing capabilities
```

---

## Runtime Agent Creation

```yaml
RUNTIME_AGENT_CREATION:
  trigger: Gap evaluation identifies missing agent capability
  constraint: guided mode only — skip in autonomy/silent mode
  
  protocol:
    1. DETECT gap type (decision domain, specialized reasoning, cross-domain coordination)
    2. PROPOSE to user (Vietnamese, always ask first)
    3. IF approved:
       a. Create .github/agents/{name}.agent.md with VS Code standard frontmatter
       b. Register in copilot-instructions.md agents section
       c. Log creation in session state (created_skills[])
    4. IF declined → Skip, proceed with best available alternative

  constraints:
    - ALWAYS ask user before creating
    - Never duplicate existing capabilities
    - Max 2 runtime agent creations per pipeline run
    - Each agent must have a budget limit
    - Follow VS Code .agent.md standard (YAML frontmatter)
```

---

## Runtime Skill Creation & Upgrade

```yaml
RUNTIME_SKILL_MANAGEMENT:
  create_new_skill:
    trigger: No existing skill covers the requirement
    constraint: guided mode only
    protocol:
      1. PROPOSE to user with skill name, purpose, triggers
      2. IF approved: Create .github/skills/{skill-name}/SKILL.md, register
      3. IF declined: Use closest available skill, log for improve session
    constraints: Max 2 new skills per pipeline run

  upgrade_existing_skill:
    trigger: Skill exists but lacks needed capability
    constraint: guided mode only
    protocol:
      1. PROPOSE upgrade with current vs needed capability
      2. IF approved: Add new mode/capability section to SKILL.md
      3. IF declined: Proceed with existing capability
    constraints: Max 3 upgrades per run, never remove existing capabilities
```
