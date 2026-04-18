# Decision Maps — Model Capability Categories

> Model-name-agnostic decision maps. Based on capabilities, not brands.  
> Used by strategist agent to select optimal workflow per model profile.

---

## Overview

5 capability categories × 3 levels each. The pipeline detects the current model's
level per category, then uses these maps to choose workflow strategies.

**Key principle:** Never trust model self-reports blindly. Verify claims against
behavioral tests (e.g., can it actually handle 100K context? does it follow
complex multi-step instructions?).

---

## Category 1: Context Window

```yaml
context_window:
  basic:
    range: "4K-16K tokens"
    characteristics:
      - Cannot hold full documents in context
      - Loses early instructions in long conversations
      - Struggles with multi-file analysis
    workflow_recommendations:
      - Chunk large documents (max 3K tokens per chunk)
      - Repeat critical instructions in each message
      - Process one file at a time, save intermediate results to tmp/
      - Use shorter SKILL.md files (< 200 lines)
      - Frequent state saves to tmp/.agent-context.json

  standard:
    range: "32K-64K tokens"
    characteristics:
      - Can hold 2-3 medium documents
      - Retains instructions well within single conversation
      - May lose context in very long pipelines
    workflow_recommendations:
      - Process up to 3 files concurrently
      - Save state every 2-3 steps (not every step)
      - Standard SKILL.md length OK (< 300 lines)
      - Use context compressor after 40+ tool calls

  advanced:
    range: "128K-200K+ tokens"
    characteristics:
      - Can hold 10+ documents simultaneously
      - Maintains coherence across entire pipeline
      - Handles complex cross-reference analysis
    workflow_recommendations:
      - Batch process multiple files
      - State saves optional (for crash recovery only)
      - Full SKILL.md files OK
      - Rare need for context compression
```

---

## Category 2: Reasoning Depth

```yaml
reasoning_depth:
  basic:
    characteristics:
      - Follows explicit step-by-step instructions well
      - Struggles with implicit requirements
      - May produce shallow analysis
      - Needs specific examples for each pattern
    workflow_recommendations:
      - Provide explicit, numbered instructions (no implicit "figure it out")
      - Include examples for each output type
      - Use templates with fill-in-the-blank sections
      - bien-soan: use standard mode, not comprehensive
      - Skip multi-perspective analysis (advisory agent)
      - Quality gates: check format compliance, not depth

  standard:
    characteristics:
      - Handles multi-step reasoning with guidance
      - Produces solid analysis with clear instructions
      - Can infer some implicit requirements
      - Good at following established patterns
    workflow_recommendations:
      - bien-soan: comprehensive mode with clear section outlines
      - Advisory agent: 1 call max (for critical decisions only)
      - Strategist: use pre-built templates, minimal customization
      - Quality gates: check both format and content depth

  advanced:
    characteristics:
      - Handles complex multi-step reasoning independently
      - Produces deep, nuanced analysis
      - Infers implicit requirements accurately
      - Can design novel approaches when needed
    workflow_recommendations:
      - bien-soan: comprehensive mode, trust model to find depth
      - Advisory agent: full multi-perspective analysis
      - Strategist: can customize templates or build from scratch
      - Quality gates: full depth + format + insight checks
```

---

## Category 3: Tool Use

```yaml
tool_use:
  basic:
    characteristics:
      - Can use 1-2 tools per turn reliably
      - May forget to use tools when needed
      - Struggles with complex tool chains
      - May misformat tool arguments
    workflow_recommendations:
      - Explicit "USE tool X now" instructions at each step
      - One tool call per instruction, verify result before next
      - Avoid parallel tool calls
      - Include tool argument examples in SKILL.md
      - Manual verification after each tool use

  standard:
    characteristics:
      - Uses multiple tools fluently
      - Chains tools effectively with guidance
      - Occasionally misses optimal tool choice
      - Handles most argument formats correctly
    workflow_recommendations:
      - Can chain 2-3 tools per step
      - Suggest optimal tools but allow model flexibility
      - Moderate parallelism OK
      - Verify critical tool results (file creation, git operations)

  advanced:
    characteristics:
      - Expert tool chaining and selection
      - Knows when to use which tool without guidance
      - Handles complex argument structures
      - Can recover from tool failures autonomously
    workflow_recommendations:
      - Trust model's tool selection
      - Allow parallel tool execution
      - Minimal verification (only destructive operations)
      - Can handle auto-escalation protocol independently
```

---

## Category 4: Multilingual

```yaml
multilingual:
  basic:
    characteristics:
      - Can output in Vietnamese but quality varies
      - May mix languages unexpectedly
      - Struggles with Vietnamese technical terminology
      - Translation quality is acceptable but not natural
    workflow_recommendations:
      - Provide Vietnamese glossary for technical terms
      - Review Vietnamese output before delivery
      - Keep Vietnamese in user-facing text only
      - bien-soan translation mode: add manual review step

  standard:
    characteristics:
      - Good Vietnamese output quality
      - Consistent language use (doesn't mix unexpectedly)
      - Handles technical Vietnamese adequately
      - Translation is natural for most content
    workflow_recommendations:
      - Standard pipeline (no extra review steps)
      - bien-soan can handle translation directly
      - Minimal glossary needed

  advanced:
    characteristics:
      - Native-quality Vietnamese output
      - Excellent technical vocabulary
      - Handles nuanced Vietnamese idioms
      - Translation indistinguishable from human
    workflow_recommendations:
      - Full trust in Vietnamese output
      - Can generate Vietnamese content without templates
      - No review step needed
```

---

## Category 5: Code Generation

```yaml
code_generation:
  basic:
    characteristics:
      - Can write simple scripts with clear specifications
      - May produce syntax errors in complex code
      - Struggles with library-specific APIs
      - Needs explicit import statements and examples
    workflow_recommendations:
      - Provide complete code templates (not just outlines)
      - Include exact import statements in SKILL.md
      - Test every generated script before use
      - Avoid complex one-liners; prefer verbose, readable code
      - Include error handling examples

  standard:
    characteristics:
      - Writes functional scripts reliably
      - Handles common libraries well (pandas, openpyxl, etc.)
      - May need guidance on less common APIs
      - Code quality is good but not optimized
    workflow_recommendations:
      - Standard script generation (SKILL.md patterns are sufficient)
      - Test critical scripts; trust simple ones
      - Can handle pptxgenjs and python-docx without extra guidance

  advanced:
    characteristics:
      - Expert-level code generation
      - Optimized, idiomatic code
      - Handles edge cases and error recovery
      - Can design scripts from high-level specs
    workflow_recommendations:
      - Minimal code templates needed
      - Trust generated scripts
      - Can create new utility scripts on demand
      - Full auto-escalation protocol support
```

---

## Profile Composition

A model's overall profile is the combination of all 5 categories.
The strategist uses the LOWEST category level as the pipeline's constraint.

```yaml
PROFILE_EXAMPLES:
  conservative_fallback:
    # Used when model cannot self-identify
    context_window: standard
    reasoning_depth: standard
    tool_use: standard
    multilingual: standard
    code_generation: standard
    effective_level: standard

  small_model:
    # e.g., GPT-4o-mini, GPT-3.5-turbo
    context_window: standard
    reasoning_depth: basic
    tool_use: standard
    multilingual: basic
    code_generation: standard
    effective_level: basic  # constrained by weakest

  large_model:
    # e.g., Claude Opus, GPT-4
    context_window: advanced
    reasoning_depth: advanced
    tool_use: advanced
    multilingual: advanced
    code_generation: advanced
    effective_level: advanced
```

---

## Usage by Agents

```yaml
AGENT_USAGE:
  strategist:
    reads: Full decision maps
    uses: Select workflow template variant (basic/standard/advanced)
    
  audit:
    reads: reasoning_depth, multilingual
    uses: Set quality thresholds (lower bar for basic models)
    
  advisory:
    reads: reasoning_depth
    uses: Decide if advisory calls are worthwhile
    
  tong-hop:
    reads: Overall profile
    uses: Decide AGENT_MODE on/off, set retry limits
```
