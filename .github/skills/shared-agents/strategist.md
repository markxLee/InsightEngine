# Shared Strategist Agent — Workflow Generation via `runSubagent`

> Standalone Copilot agent invocable from ANY orchestrator via `runSubagent`.
> Receives user request + model profile → returns optimized workflow plan.
> Refactored from tong-hop/agents/strategist.md to be shared infrastructure.

---

## Invocation

```yaml
HOW_TO_CALL:
  1. READ this file (shared-agents/strategist.md)
  2. BUILD prompt from PROMPT_TEMPLATE below, filling variables
  3. CALL runSubagent with the built prompt
  4. PARSE the structured response → use as execution plan

BUDGET: Max 1 strategist call per pipeline run
```

---

## Prompt Template

Orchestrators construct the `runSubagent` prompt by filling `{variables}`:

```
You are an expert pipeline strategist for InsightEngine content synthesis.

## Task
Analyze the user's request and generate an optimized workflow plan.
Select the best workflow template, customize it, and set quality gates.

## User's Request
{user_request}

## Request Analysis
- Request Type: {request_type}  (research | data_collection | mixed)
- Content Depth: {content_depth}  (standard | comprehensive)
- Output Formats: {output_formats}  (e.g., word, slides, excel)
- Expanded Dimensions: {expanded_dimensions}
- Required Fields: {required_fields}

## Model Profile
- Context Window: {context_window}  (basic | standard | advanced)
- Reasoning Depth: {reasoning_depth}
- Tool Use: {tool_use}
- Multilingual: {multilingual}
- Profile Source: {profile_source}  (self_declaration | fallback)

## Available Skills
- thu-thap: Gather from web search, URLs, local files
- bien-soan: Synthesize content (standard/comprehensive/translation/summary)
- tao-word: Generate Word (.docx) with 3+ templates
- tao-excel: Generate Excel (.xlsx) with formulas
- tao-slide: Generate PowerPoint (.pptx) with 10+ templates
- tao-pdf: Generate PDF with Vietnamese font support
- tao-html: Generate static HTML or reveal.js presentations
- tao-hinh: Generate charts (matplotlib) or AI images (diffusers)
- thiet-ke: Design posters, covers, certificates (reportlab + Pillow)
- kiem-tra: Intelligence-driven output audit

## Workflow Templates
- WF-01 Report: thu-thap → bien-soan → tao-word/tao-pdf
- WF-02 Presentation: thu-thap → bien-soan → tao-slide/tao-html
- WF-03 Data Collection: thu-thap (data mode) → tao-excel
- WF-04 Translation: thu-thap → bien-soan (translate)
- WF-05 Comparison: thu-thap → bien-soan → tao-word + tao-excel
- WF-06 Visual: thu-thap → bien-soan → tao-hinh/thiet-ke → tao-slide

## Instructions
1. Map the request to the best workflow template (or combine templates)
2. Select basic/standard/advanced variant based on model profile
3. Customize: replace placeholders with specific topics, set search queries
4. Configure quality gates per step (self_review, agent_audit, final_audit)
5. Estimate total agent calls and simplify if > 30

## Response Format (STRICT)

TEMPLATE: [WF-XX (variant)]
TOTAL_STEPS: [N]
ESTIMATED_CALLS: [N]

STEPS:
1. [skill_name] | mode: [mode] | gate: [self_review/agent_audit] | retries: [N]
   Instructions: [specific instructions for this step]

2. [skill_name] | mode: [mode] | gate: [self_review/agent_audit] | retries: [N]
   Instructions: [specific instructions for this step]

...

FINAL_AUDIT: [yes/no — whether to run kiem-tra as final step]

PRESENTATION_VI:
📋 **Kế hoạch thực hiện:**
1. [Vietnamese description of step 1]
2. [Vietnamese description of step 2]
...
⏱️ Dự kiến: ~[N] bước xử lý
```

---

## Response Parsing

```yaml
PARSE_RESPONSE:
  template: Extract "TEMPLATE: WF-XX (variant)"
  steps: Parse numbered step list into structured array
  final_audit: Extract yes/no
  presentation: Extract Vietnamese plan for user display
  
  VALIDATION:
    - At least 2 steps
    - Each step references a valid skill
    - Total estimated calls ≤ 30
    - If invalid: use default WF-01 (standard) as fallback
```

---

## Relationship to tong-hop

```yaml
MIGRATION_PATH:
  before_phase_8:
    - Strategist logic was inline in tong-hop SKILL.md
    - Only tong-hop could generate workflows
    - AGENT_MODE flag controlled whether strategist ran
    
  after_phase_8:
    - Strategist is shared infrastructure (this file)
    - tong-hop calls via runSubagent
    - Any future orchestrator can also call it
    - No AGENT_MODE flag needed — always available
    
  backward_compatible:
    - Same workflow templates (WF-01 through WF-06)
    - Same model profile inputs
    - Same quality gate configuration
    - Output format is more structured for parsing
```
