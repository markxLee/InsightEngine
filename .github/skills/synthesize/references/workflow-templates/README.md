# Workflow Templates — Index

> Pre-built workflow templates for common scenarios × model capability levels.  
> Used by strategist agent to quickly generate customized workflows.

---

## Template Index

| ID | Scenario | File | Description |
|----|----------|------|-------------|
| WF-01 | Research Report | `report.md` | Web search → synthesize → Word/PDF |
| WF-02 | Presentation | `presentation.md` | Content → slides (PPTX or HTML) |
| WF-03 | Data Collection | `data-collection.md` | Platform search → extract → Excel |
| WF-04 | Translation | `translation.md` | Read source → translate → output |
| WF-05 | Comparison | `comparison.md` | Multi-source → compare → report |

---

## Template Structure

Each template has 3 variants based on model capability:

```yaml
VARIANT_MAPPING:
  basic:
    # For models with limited reasoning/context
    - Simpler steps, more explicit instructions
    - Fewer quality gates
    - Shorter outputs (standard depth)
    - No advisory agent calls
    
  standard:
    # Default for most models
    - Full pipeline with quality gates
    - Comprehensive depth
    - 1 advisory call for critical decisions
    - Standard retry limits
    
  advanced:
    # For top-tier models
    - Full pipeline with deep quality gates
    - Comprehensive depth with auto-enrichment
    - Advisory agent available
    - Higher retry limits, trust model judgment
```

---

## How Strategist Uses Templates

```yaml
STRATEGIST_FLOW:
  1. Receive user request + model profile
  2. Match request to template ID (by scenario type)
  3. Select variant (basic/standard/advanced) based on model profile
  4. Customize template:
     - Replace [TOPIC] with actual topic
     - Adjust output format per user request
     - Add/remove steps based on specific needs
  5. Write final workflow to shared context
```
