# WF-02: Presentation Template

> Scenario: User wants a slide presentation.  
> Flow: Content source → synthesize into slides → PPTX/HTML output.

---

## Basic Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    instructions: "Read provided files/URLs. If no source, search for [TOPIC] (3 queries max)."
    quality_gate: none
    
  - id: synthesize
    skill: bien-soan
    mode: standard
    instructions: "Structure content for slides. Max 12 slides. Keep bullet points concise."
    quality_gate: self_review (check slide count, readability)
    
  - id: output
    skill: tao-slide
    mode: quick (pptxgenjs)
    template: corporate
    instructions: "Generate PPTX with simple layout."
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
  - id: gather
    skill: thu-thap
    instructions: "Gather content from all sources. Ensure each slide topic has supporting data."
    quality_gate: self_review (coverage check)
    
  - id: synthesize
    skill: bien-soan
    mode: comprehensive
    instructions: "Structure for 12-20 slides. Each slide must have a key insight + supporting detail."
    quality_gate: self_review (depth per slide)
    
  - id: output
    skill: tao-slide
    mode: quick (pptxgenjs)
    template: auto-detect
    instructions: "Generate professional PPTX with visual elements per slide."
    quality_gate: self_review (visual check)

audit: final_audit (content coverage vs request)
advisory_calls: 0
max_retries: 2
estimated_agent_calls: 6-10
```

---

## Advanced Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    mode: deep_research
    instructions: "Deep research for presentation. Find data, stats, case studies."
    quality_gate: self_review
    
  - id: synthesize
    skill: bien-soan
    mode: comprehensive
    instructions: "Expert-level slide narrative. Each slide has insight + data + visual suggestion."
    quality_gate: agent_audit
    
  - id: charts
    skill: tao-hinh
    mode: chart
    condition: "if data tables in synthesized content"
    instructions: "Generate charts for data slides."
    quality_gate: self_review
    
  - id: output
    skill: tao-slide
    mode: pro (ppt-master)
    template: consulting-grade
    instructions: "Generate consulting-grade PPTX with native DrawingML shapes."
    quality_gate: self_review

audit: final_audit
advisory_calls: 1
max_retries: 3
estimated_agent_calls: 12-18
```
