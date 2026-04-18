# Skill Review Rubric — InsightEngine Adaptation

> Grading criteria adapted for InsightEngine's Vietnamese-first, pipeline-integrated  
> skill ecosystem. Use alongside skill-forge's 6-criterion review.

---

## InsightEngine-Specific Checks

Beyond the standard 6 criteria, InsightEngine skills must satisfy:

```yaml
INSIGHTENGINE_CHECKS:
  vietnamese_naming:
    rule: Skill directory name must be Vietnamese, lowercase, hyphenated
    examples_good: thu-thap, bien-soan, tao-word, kiem-tra
    examples_bad: data-collector, content-writer, output-checker
    
  bilingual_triggers:
    rule: Triggers must include both Vietnamese (primary) and English (secondary)
    minimum: 3 Vietnamese + 2 English trigger phrases
    
  file_placement:
    rule: Scripts → /scripts, output → /output, tmp → /tmp, input → /input
    verify: No scripts in references/, no output in tmp/
    
  pipeline_integration:
    rule: Skill must work both standalone AND as tong-hop sub-skill
    verify: Accepts pipeline inputs, returns structured output
    
  shared_context:
    rule: If AGENT_MODE compatible, skill reads/writes shared context properly
    verify: Follows agent-context-protocol.md
    
  cli_scripts:
    rule: All scripts accept CLI arguments (no hardcoded paths)
    verify: --input, --output, --style flags present
    
  vietnamese_user_communication:
    rule: All user-facing messages in Vietnamese
    verify: Error messages, progress reports, confirmations
```

---

## Grade Adjustments for InsightEngine

```yaml
GRADE_MODIFIERS:
  # Standard forge grades (A/B/C/D) apply, with these adjustments:
  
  auto_downgrade_to_C:
    - Script exists in references/ instead of scripts/
    - Hardcoded file paths in scripts
    - English-only triggers (missing Vietnamese)
    - Missing thin content guard (for output skills)
    
  auto_downgrade_to_D:
    - Skill name not in Vietnamese
    - No CLI arguments on scripts
    - Output written to wrong directory
    - User-facing messages in English only
    
  auto_upgrade_to_A:
    - Has both references/ AND scripts/ directories
    - Self-review loop built-in
    - Works in both standalone and pipeline mode
    - Handles edge cases documented in examples
```
