# WF-04: Translation Template

> Scenario: User wants content translated between languages.  
> Flow: Read source → translate → output in desired format.

---

## Basic Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    instructions: "Read source file(s) or URL(s)."
    quality_gate: none
    
  - id: translate
    skill: bien-soan
    mode: translation
    instructions: "Translate content [source_lang] → [target_lang]. Preserve structure and formatting."
    quality_gate: self_review (check completeness, no untranslated sections)
    
  - id: output
    skill: tao-word | tao-pdf
    instructions: "Generate output in same structure as source."
    quality_gate: none

audit: none
advisory_calls: 0
max_retries: 1
estimated_agent_calls: 3-4
```

---

## Standard Variant (default)

```yaml
steps:
  - id: gather
    skill: thu-thap
    instructions: "Read all source content. Preserve section structure."
    quality_gate: self_review (check content captured completely)
    
  - id: translate
    skill: bien-soan
    mode: translation
    instructions: "Natural translation preserving tone, technical terms, and formatting. Section by section."
    quality_gate: agent_audit (naturalness, completeness, terminology)
    
  - id: output
    skill: tao-word | tao-pdf
    template: match source format
    instructions: "Generate output matching source document style."
    quality_gate: self_review

audit: final_audit (section count match, no missing content)
advisory_calls: 0
max_retries: 2
estimated_agent_calls: 5-8
```

---

## Advanced Variant

```yaml
steps:
  - id: gather
    skill: thu-thap
    instructions: "Read source. Identify domain-specific terminology."
    quality_gate: self_review
    
  - id: translate
    skill: bien-soan
    mode: translation
    instructions: "Expert translation with domain awareness. Adapt cultural references. Maintain idiomatic quality."
    quality_gate: agent_audit (naturalness + domain accuracy)
    
  - id: output
    skill: tao-word | tao-pdf
    template: match source
    instructions: "Professional output matching or exceeding source quality."
    quality_gate: self_review

audit: final_audit
advisory_calls: 0
max_retries: 2
estimated_agent_calls: 6-10
```
