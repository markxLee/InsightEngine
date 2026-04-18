# WF-01: Research Report Template

> Scenario: User wants a research report on a topic.  
> Flow: Web search → synthesize → Word/PDF output.

---

## Basic Variant (limited reasoning models)

```yaml
steps:
  - id: search
    skill: thu-thap
    mode: standard
    instructions: "Search for [TOPIC]. Limit to 3 search queries, fetch top 3 URLs per query."
    quality_gate: none
    
  - id: synthesize
    skill: bien-soan
    mode: standard
    depth: standard
    instructions: "Combine gathered content into a structured report. Follow the outline exactly."
    quality_gate: self_review (format check only)
    
  - id: output
    skill: tao-word | tao-pdf
    template: corporate
    instructions: "Generate output file from synthesized content."
    quality_gate: none

audit: none
advisory_calls: 0
max_retries: 1
estimated_agent_calls: 3-5
```

---

## Standard Variant (default)

```yaml
steps:
  - id: search
    skill: thu-thap
    mode: standard
    instructions: "Search for [TOPIC] across multiple dimensions. Use 3-5 queries, fetch 3-5 URLs each."
    quality_gate: self_review (check coverage of all dimensions)
    
  - id: enrichment
    skill: thu-thap
    mode: supplementary
    instructions: "If search gaps found, do 1 supplementary round with refined queries."
    condition: "only if quality_gate flagged gaps"
    quality_gate: none
    
  - id: synthesize
    skill: bien-soan
    mode: comprehensive
    depth: comprehensive
    instructions: "Synthesize all gathered content into expert-level report. Min 3000 words. Include data, examples, analysis."
    quality_gate: agent_audit (check depth, specificity, analysis quality)
    
  - id: output
    skill: tao-word | tao-pdf
    template: auto-detect
    instructions: "Generate professional output with all sections."
    quality_gate: self_review (format, completeness)

audit: final_audit (compare output vs original request)
advisory_calls: 0-1
max_retries: 2
estimated_agent_calls: 8-12
```

---

## Advanced Variant (top-tier models)

```yaml
steps:
  - id: deep_search
    skill: thu-thap
    mode: deep_research
    instructions: "Deep research on [TOPIC]. Decompose into dimensions, search broadly, analyze gaps, search deeper."
    quality_gate: self_review (coverage + source diversity)
    
  - id: synthesize
    skill: bien-soan
    mode: comprehensive
    depth: comprehensive
    instructions: "Expert-level synthesis. Cross-reference sources, identify patterns, provide original analysis."
    quality_gate: agent_audit (depth + insight + data specificity)
    
  - id: charts
    skill: tao-hinh
    mode: chart
    condition: "if data tables found in synthesized content"
    instructions: "Generate supporting charts from data."
    quality_gate: self_review
    
  - id: output
    skill: tao-word | tao-pdf
    template: auto-detect
    instructions: "Generate professional output with charts embedded."
    quality_gate: self_review

audit: final_audit (comprehensive comparison)
advisory_calls: 1
max_retries: 3
estimated_agent_calls: 12-20
```
