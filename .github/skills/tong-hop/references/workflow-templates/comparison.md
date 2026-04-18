# WF-05: Comparison Template

> Scenario: User wants multi-source comparison/analysis.  
> Flow: Gather from multiple sources → compare → report with tables/charts.

---

## Basic Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    instructions: "Read all source files/URLs. Keep sources separate for comparison."
    quality_gate: none
    
  - id: compare
    skill: bien-soan
    mode: standard
    instructions: "Create comparison table. List similarities and differences."
    quality_gate: self_review (all sources represented)
    
  - id: output
    skill: tao-word | tao-excel
    instructions: "Generate output with comparison table."
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
    instructions: "Gather content from all comparison targets. Ensure consistent data for each."
    quality_gate: self_review (balance check — similar depth per source)
    
  - id: compare
    skill: bien-soan
    mode: comprehensive
    instructions: "Deep comparison across multiple dimensions. Include: feature matrix, pros/cons, scoring, recommendation."
    quality_gate: agent_audit (balance, depth, objectivity)
    
  - id: charts
    skill: tao-hinh
    mode: chart
    condition: "if quantitative data available"
    instructions: "Generate comparison charts (radar, bar, grouped)."
    quality_gate: self_review
    
  - id: output
    skill: tao-word | tao-excel
    instructions: "Professional report with embedded charts and comparison tables."
    quality_gate: self_review

audit: final_audit (all sources covered, balanced analysis)
advisory_calls: 0-1
max_retries: 2
estimated_agent_calls: 8-14
```

---

## Advanced Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    mode: deep_research
    instructions: "Deep research on each comparison target. Find quantitative data, reviews, benchmarks."
    quality_gate: self_review (data completeness per target)
    
  - id: compare
    skill: bien-soan
    mode: comprehensive
    instructions: "Expert comparison with weighted scoring, SWOT per target, and synthesis recommendation."
    quality_gate: agent_audit
    
  - id: charts
    skill: tao-hinh
    instructions: "Comprehensive visualization: radar chart, feature matrix, trend lines."
    quality_gate: self_review
    
  - id: output
    skill: tao-word | tao-excel
    instructions: "Consulting-grade comparison report."
    quality_gate: self_review

audit: final_audit (comprehensive)
advisory_calls: 1
max_retries: 3
estimated_agent_calls: 14-22
```
