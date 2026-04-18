# Public Skill Clone — Security-First Adoption Protocol

> When creating a new skill at runtime, prioritize cloning from verified  
> public repositories over building from scratch. Mandatory security  
> review before any cloned skill is used.

---

## Overview

```yaml
PURPOSE:
  Save time and improve quality by reusing battle-tested public skills
  instead of building from scratch — but NEVER at the cost of security.

PRIORITY_ORDER:
  1. Clone + adapt from whitelisted public repos → PREFERRED
  2. Build from scratch → FALLBACK (when no suitable public skill exists)

MANDATORY:
  Security check MUST pass before ANY cloned skill is executed.
  No exceptions. No bypasses. No "trust me" shortcuts.
```

---

## Clone Sources Whitelist

```yaml
WHITELISTED_SOURCES:
  # Only these repositories are approved for cloning.
  # Adding new sources requires manual review.
  
  - name: Anthropic Skills
    url: github.com/anthropics/skills
    trust_level: high
    notes: Official Anthropic skill library
    
  - name: OpenClaw Skills
    url: github.com/openclaw/openclaw/tree/main/skills
    trust_level: medium
    notes: Community-maintained, actively reviewed
    
  - name: OpenAI Skills
    url: github.com/openai/skills
    trust_level: high
    notes: Official OpenAI skill library

BLOCKED_SOURCES:
  - Any repository not in the whitelist
  - Personal forks (github.com/<random-user>/...)
  - Gists
  - Non-GitHub sources
  
  on_blocked_source:
    action: REJECT clone attempt
    fallback: Build from scratch
    log: "clone_rejected: source not whitelisted: {url}"
```

---

## Clone Discovery Flow

```yaml
DISCOVERY_STEPS:
  context: Skill-forge has been approved by advisory (see conditional-skill-forge.md)
  
  1_search_whitelisted_repos:
    for_each_source: in WHITELISTED_SOURCES
    method: |
      Search repository for skills matching the needed capability.
      Match by: skill name, description, triggers, purpose.
      
      Example: Need audio processing →
        Search anthropic/skills for "audio", "transcription", "speech"
        Search openclaw/skills for "audio", "transcription"
        Search openai/skills for "audio", "transcription"
    
    tools:
      - fetch_webpage (to browse repo README/index)
      - grep_search on local clone (if available in workspace)
      
  2_evaluate_candidates:
    for_each_match:
      - Read SKILL.md to understand capability
      - Check compatibility with InsightEngine conventions
      - Assess adaptation effort (minor tweak vs major rewrite)
      
    scoring:
      capability_match: 0-100 (does it do what we need?)
      adaptation_effort: low | medium | high
      recency: last commit date (prefer active repos)
      
    select: Best match with capability_match >= 70 AND adaptation_effort <= medium
    
  3_decide:
    if_good_match_found:
      action: Clone and adapt (proceed to Clone Protocol)
      
    if_no_match:
      action: Build from scratch (fall back to conditional-skill-forge creation steps)
      log: "clone_search_no_match: searched {N} repos, no suitable skill found"
```

---

## Clone Protocol

```yaml
CLONE_STEPS:
  1_fetch_skill_files:
    method: |
      Download SKILL.md and associated files from the source repo.
      Use fetch_webpage to get raw content.
      Save to tmp/ for security review BEFORE placing in .github/skills/
    
    save_to: tmp/cloned-skill/
    files: SKILL.md, scripts/*, references/*
    
  2_security_review:
    # ⚠️ MANDATORY — CANNOT BE SKIPPED
    action: Run full security check (see Security Check Protocol below)
    
    on_pass: Proceed to adaptation
    on_fail: |
      REJECT cloned skill entirely
      DELETE tmp/cloned-skill/
      Fall back to building from scratch
      Log: "clone_security_failed: {reasons}"
      
  3_adapt_to_insightengine:
    changes:
      naming: |
        Rename to Vietnamese, lowercase, hyphenated
        e.g., "audio-processor" → "xu-ly-audio"
        
      conventions: |
        Update SKILL.md to follow InsightEngine format:
        - YAML frontmatter
        - English body
        - Bilingual triggers
        - Shared context integration
        
      scripts: |
        Update file paths for InsightEngine structure:
        - Scripts → /scripts
        - Output → /output
        - Tmp → /tmp
        Add CLI arguments (no hardcoded paths)
        
      dependencies: |
        Check required packages against requirements.txt
        Add any missing packages
        
  4_place_in_skills:
    move: tmp/cloned-skill/ → .github/skills/<vietnamese-name>/
    cleanup: rm -rf tmp/cloned-skill/
    
  5_test:
    same_as: conditional-skill-forge.md → Creation Steps → 4_test_skill
```

---

## Security Check Protocol

```yaml
SECURITY_CHECK:
  # ⚠️ This check is MANDATORY for ALL cloned skills
  # Runs on files in tmp/cloned-skill/ BEFORE they are adopted
  
  checks:
    1_no_malware:
      description: No obfuscated code, no encoded payloads, no suspicious patterns
      scan_for:
        - Base64 encoded strings longer than 100 chars
        - eval() / exec() calls with dynamic input
        - Obfuscated variable names (single chars in loops with network calls)
        - Minified/packed code blocks
      on_detect: FAIL with reason "potential malware pattern"
      
    2_no_data_exfiltration:
      description: No unauthorized network calls or data sending
      scan_for:
        - HTTP/HTTPS requests to non-whitelisted domains
        - Webhook URLs
        - Email sending functions
        - File upload to external services
        - API calls to unknown endpoints
      allowed_network:
        - fetch_webpage (Copilot built-in)
        - vscode-websearchforcopilot_webSearch (Copilot built-in)
        - PyPI/npm (package installation only)
      on_detect: FAIL with reason "unauthorized network access"
      
    3_no_dangerous_commands:
      description: No destructive or privilege-escalation commands
      scan_for:
        - rm -rf / (or similar destructive patterns)
        - sudo / su commands
        - chmod 777 / permissive permissions
        - Shell injection patterns (unsanitized user input in os.system/subprocess)
        - File operations outside project directory
        - Registry/system config modifications
      on_detect: FAIL with reason "dangerous command detected"
      
    4_no_credential_harvesting:
      description: No attempts to read or transmit credentials
      scan_for:
        - Reading ~/.ssh, ~/.aws, ~/.config
        - Environment variable harvesting (os.environ bulk read)
        - Keychain/keyring access
        - Token/API key patterns in output
      on_detect: FAIL with reason "credential access attempt"
      
    5_dependency_check:
      description: No suspicious or known-malicious packages
      scan_for:
        - Packages not in PyPI/npm top 10K (flag for manual review)
        - Known malicious package names (typosquatting)
        - Pinned versions pointing to compromised releases
      on_detect: WARN (flag for review, don't auto-fail)
      
  result_format:
    status: pass | fail | warn
    checks_passed: N / 5
    issues: ["specific issue description with file:line"]
    recommendation: "adopt | reject | review_manually"
    
  logging:
    write_to: shared context → decisions array
    entry:
      type: "security_review"
      skill_source: "url"
      skill_name: "name"
      status: "pass | fail | warn"
      checks: { ... }
      timestamp: ISO-8601
```

---

## Integration with Skill-Forge

```yaml
INTEGRATION:
  called_by: conditional-skill-forge.md (after advisory approves creation)
  
  flow:
    1. Advisory approves skill creation (conditional-skill-forge.md)
    2. THIS PROTOCOL: Search whitelisted repos for existing skill
    3. IF found: Clone → Security check → Adapt → Test → Use
    4. IF not found OR security fails: Build from scratch
    5. Return to conditional-skill-forge.md flow
    
  budget_impact:
    clone_search: 1 agent call (searching repos)
    security_review: 0 extra calls (inline analysis)
    adaptation: Shared with conditional-skill-forge budget
    total_additional: 1 call for clone search
```

---

## Examples

### Example 1: Successful Clone

```yaml
scenario: Need data visualization skill beyond basic charts
search: Found "plotly-dashboard" skill in openclaw/skills
security_check:
  no_malware: pass
  no_data_exfiltration: pass
  no_dangerous_commands: pass
  no_credential_harvesting: pass
  dependency_check: pass (plotly is top-100 PyPI package)
  result: pass
adaptation:
  renamed: "tao-bieu-do-nang-cao"
  updated: Vietnamese triggers, InsightEngine paths
  tested: Generated sample dashboard → pass
result: Skill adopted and used in pipeline
```

### Example 2: Clone Rejected (Security)

```yaml
scenario: Found "web-scraper-pro" in openclaw/skills
security_check:
  no_malware: pass
  no_data_exfiltration: FAIL — sends data to analytics.example.com
  result: fail
action: Rejected, building from scratch
log: "clone_security_failed: unauthorized network call to analytics.example.com"
```

### Example 3: No Match Found

```yaml
scenario: Need skill for generating 3D models
search:
  anthropic/skills: no match
  openclaw/skills: no match
  openai/skills: no match
action: Build from scratch (conditional-skill-forge.md creation steps)
log: "clone_search_no_match: searched 3 repos for '3D model generation'"
```
