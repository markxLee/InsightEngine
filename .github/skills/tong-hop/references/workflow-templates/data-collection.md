# WF-03: Data Collection Template

> Scenario: User wants specific items collected into structured output.  
> Flow: Platform-specific search → extract fields → Excel output.

---

## Basic Variant

```yaml
steps:
  - id: search
    skill: thu-thap
    mode: data_collection
    instructions: "Search for [ITEMS] on [PLATFORMS]. Collect up to 15 items."
    required_fields: [name, url, source_platform]
    quality_gate: none
    
  - id: output
    skill: tao-excel
    instructions: "Create Excel with collected items. One row per item."
    quality_gate: self_review (check URL validity)

audit: none
advisory_calls: 0
max_retries: 1
estimated_agent_calls: 2-4
```

---

## Standard Variant (default)

```yaml
steps:
  - id: search
    skill: thu-thap
    mode: data_collection
    instructions: "Search for [ITEMS] across 3-5 platforms. Collect 20-30 items. Fetch detail pages for each."
    required_fields: [from user request + auto-added: direct_url, source_platform]
    quality_gate: self_review (check field completeness, URL validity)
    
  - id: enrich
    skill: thu-thap
    mode: supplementary
    condition: "if < 15 items found"
    instructions: "Expand to more platforms or broaden filters."
    quality_gate: none
    
  - id: output
    skill: tao-excel
    instructions: "Professional Excel with formatting, filters, and formulas."
    quality_gate: self_review (formula check, completeness)

audit: final_audit (check required_fields coverage, URL quality)
advisory_calls: 0
max_retries: 2
estimated_agent_calls: 5-8
```

---

## Advanced Variant

```yaml
steps:
  - id: search
    skill: thu-thap
    mode: data_collection
    instructions: "Exhaustive search across all relevant platforms. 30-50 items target."
    required_fields: [all from user + comprehensive defaults]
    quality_gate: self_review (coverage + diversity)
    
  - id: verify
    skill: thu-thap
    mode: verification
    instructions: "Verify top 10 URLs are still active and data is current."
    quality_gate: none
    
  - id: output
    skill: tao-excel
    instructions: "Professional Excel with conditional formatting, charts, summary tab."
    quality_gate: agent_audit (data quality)

audit: final_audit (comprehensive field + URL + freshness check)
advisory_calls: 0-1
max_retries: 3
estimated_agent_calls: 8-14
```
