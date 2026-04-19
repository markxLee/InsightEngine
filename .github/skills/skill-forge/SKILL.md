---
name: skill-forge
version: 1.0
description: >
  Advanced skill creation and refinement pipeline. Wraps skill-creator with an automatic
  multi-criteria review loop that grades skills on quality, usefulness, alternatives analysis,
  and implementation — then iteratively improves until all criteria reach grade A, or stops
  after 10 loops with no further improvement. Use this skill whenever the user wants to
  create a high-quality, production-grade skill with rigorous self-review, or wants to
  upgrade/audit an existing skill to professional standards. Also triggers when the user
  says "tạo skill nâng cao", "forge a skill", "create and review skill", "auto-improve skill",
  "skill chất lượng cao", "nâng cấp skill", "review skill", "audit skill quality", or
  wants a skill that's been validated through multiple rounds of critical analysis rather
  than just a first draft.
---

# Skill Forge — Advanced Skill Creator with Auto-Review Loop

**Governance:** Read and follow `.github/RULE.md` — it overrides all instructions below.

Skill Forge builds on top of `skill-creator` by adding a structured review-and-improve cycle. The idea is simple: creating a skill draft is only step one. What makes a skill genuinely useful is pressure-testing it from multiple angles — quality standards, real-world usefulness, alternative approaches, implementation rigor — and then systematically closing the gaps.

## When This Skill Activates

**Create mode** — User wants a new skill:
- "Tạo skill mới cho X", "build me a skill for Y", "turn this into a polished skill"
- Forge creates the initial draft via skill-creator, then runs the review loop

**Review/Update mode** — User has an existing skill to improve:
- "Review skill này", "nâng cấp skill X", "audit this skill", "improve my skill"
- Forge reviews the existing skill, then iterates improvements

**The key difference from plain skill-creator**: Forge doesn't stop after one draft. It automatically evaluates, critiques, and refines — handling the "is this actually good?" question that usually requires human judgment.

---

## The Forge Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                    SKILL FORGE PIPELINE                  │
│                                                         │
│  1. CREATE or LOAD skill (via skill-creator)            │
│  2. AUTO-REVIEW against 6 criteria (A/B/C/D grading)   │
│  3. ANALYZE alternatives — could this be done better?   │
│  4. SYNTHESIZE improvement plan from review findings    │
│  5. UPDATE skill (via skill-creator patterns)           │
│  6. RE-REVIEW — loop until all criteria ≥ A             │
│     or 10 iterations with no score improvement → stop   │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: Create or Load

**New skill**: Follow the skill-creator workflow — capture intent, interview, write SKILL.md. The goal here is a solid first draft, not perfection. Don't over-polish at this stage; the review loop handles refinement.

**Existing skill**: Read the SKILL.md and all bundled resources. Understand what the skill does, how it's structured, and what its current strengths/weaknesses are.

### Phase 2: Auto-Review

This is the core of Forge. Evaluate the skill against six criteria, each graded A through D. The review should be honest and specific — vague "looks good" feedback helps no one.

#### Review Rubric

| # | Criterion | What It Measures |
|---|-----------|-----------------|
| 1 | **Skill Structure** | Does the SKILL.md follow skill-creator conventions? Progressive disclosure, frontmatter, clear organization, appropriate length (<500 lines body) |
| 2 | **Instruction Clarity** | Are instructions explanatory (why, not just what)? Would a capable LLM follow them correctly without ambiguity? No excessive MUSTs/NEVERs without rationale |
| 3 | **Real-World Usefulness** | Does this skill solve a genuine problem users actually have? Is the trigger description accurate and comprehensive? Would a user be glad this skill exists? |
| 4 | **Alternative Analysis** | Has the space of solutions been explored? Could the same goal be achieved with existing tools, simpler approaches, or a different skill design? Is the current approach the best one? |
| 5 | **Implementation Quality** | Are scripts functional and well-organized? Error handling present where needed? Dependencies reasonable? Edge cases covered? |
| 6 | **Description & Triggering** | Is the description field optimized for triggering? Does it cover the right range of user phrasings without being too broad or too narrow? |

#### Grade Definitions

| Grade | Meaning | Action |
|-------|---------|--------|
| **A** | Excellent — production-ready, no meaningful improvements possible | No changes needed for this criterion |
| **B** | Good — works well, minor polish opportunities | Improve if easy; acceptable to ship |
| **C** | Adequate — functional but has notable gaps | Needs improvement before shipping |
| **D** | Needs work — significant issues that undermine the skill's value | Must fix before proceeding |

#### How to Conduct the Review

For each criterion, produce:

```yaml
criterion: "Skill Structure"
grade: "B"
evidence: |
  - SKILL.md is 320 lines, well within limit
  - Missing progressive disclosure: large reference block should move to references/
  - Frontmatter description is present but could be more specific
strengths:
  - Clean section organization
  - Good use of examples
weaknesses:
  - Reference data inline inflates context unnecessarily
  - No table of contents for the long reference section
suggestions:
  - Move the API reference to references/api.md
  - Add a TOC comment at the top of the reference file
```

Be specific. Quote from the skill. Point to exact lines or sections. Generic observations like "could be better organized" aren't actionable.

### Phase 3: Alternative Analysis

This phase asks a question most skill authors skip: **is a skill even the right solution?**

Evaluate these dimensions:

1. **Existing coverage**: Does another skill already handle this? Could an existing skill be extended instead of creating a new one?
2. **Built-in sufficiency**: Can standard Copilot tools (read_file, grep_search, run_in_terminal) handle this without a skill? If so, a skill adds overhead without proportional value.
3. **Design alternatives**: Could the same goal be achieved with a different skill architecture? (e.g., a single skill vs. composition of smaller skills, scripts vs. inline instructions, reference files vs. embedded knowledge)
4. **Simplification potential**: Is the skill over-engineered for what it does? Could 80% of the value be delivered with 20% of the complexity?

Produce a comparison:

```yaml
alternatives_analysis:
  current_approach:
    description: "Dedicated skill with 3 scripts and reference files"
    pros: ["Complete automation", "Handles edge cases", "Consistent output"]
    cons: ["Complex setup", "Heavy context load", "Maintenance burden"]
    usefulness_score: "B"
    
  alternative_1:
    description: "Extend existing skill X with a new mode"
    pros: ["Less duplication", "Shared maintenance", "User already knows skill X"]
    cons: ["Might bloat skill X", "Different enough to warrant separation"]
    usefulness_score: "B"
    
  alternative_2:
    description: "Lightweight skill — instructions only, no scripts"
    pros: ["Simple", "Easy to maintain", "Fast to load"]
    cons: ["Less consistent output", "User must do more manual work"]
    usefulness_score: "C"
    
  recommendation: |
    Current approach is justified because [specific reasoning].
    Consider borrowing [specific element] from alternative_2 to reduce complexity.
```

### Phase 4: Synthesize Improvement Plan

Combine findings from the review and alternatives analysis into a concrete improvement plan. Prioritize by impact:

1. **Must fix** — Anything graded D (blocks shipping)
2. **Should fix** — Anything graded C (notably weakens the skill)
3. **Nice to fix** — B-grade items with easy improvements
4. **Architectural changes** — If alternatives analysis reveals a better design

The plan should be specific enough to execute without further clarification.

### Phase 5: Update

Apply the improvement plan. Follow skill-creator patterns:
- Edit SKILL.md for instruction/structure changes
- Create/update scripts in `scripts/`
- Move content to `references/` if it's too long for inline
- Update the description field if triggering needs improvement

After updating, document what changed and why in a brief changelog entry (stored in the review state — not a separate file).

### Phase 6: Re-Review (Loop)

Run the full review again on the updated skill. Compare grades to the previous iteration.

**Loop termination conditions** (any of these stops the loop):

1. **All criteria graded A** → Skill is production-ready. Done.
2. **10 iterations completed** → Diminishing returns. Present the best version.
3. **No score improvement for 5 consecutive iterations** → Plateau reached. Each iteration might try a different angle or approach — sometimes improvement comes from an unexpected direction. Only stop after 5 failed attempts, and present the best version seen so far with an explanation of what was tried.
4. **User interrupts** → Always respect user's desire to stop early.

---

## Review State Tracking

Track progress across iterations so the loop has memory:

```yaml
# Store as <skill-name>-workspace/forge-state.yaml
forge_state:
  skill_name: "example-skill"
  mode: "create"  # or "update"
  current_iteration: 3
  max_iterations: 10
  
  iterations:
    - iteration: 1
      grades:
        skill_structure: "C"
        instruction_clarity: "B"
        real_world_usefulness: "B"
        alternative_analysis: "C"
        implementation_quality: "D"
        description_triggering: "C"
      lowest_grade: "D"
      changes_made: |
        - Moved API reference to references/api.md
        - Added error handling to main script
        - Rewrote description for better triggering
        
    - iteration: 2
      grades:
        skill_structure: "B"
        instruction_clarity: "A"
        real_world_usefulness: "A"
        alternative_analysis: "B"
        implementation_quality: "B"
        description_triggering: "B"
      lowest_grade: "B"
      changes_made: |
        - Simplified script by removing unused helper
        - Added edge case examples to SKILL.md
        - Narrowed description to avoid false triggers
        
  best_iteration: 2
  converged: false
  convergence_reason: null  # "all_a" | "max_iterations" | "plateau" | "user_stopped"
```

---

## Working with skill-creator

Forge delegates to skill-creator for the actual creation and editing work. Think of it this way:

- **skill-creator** = the craftsperson who writes and tests skills
- **skill-forge** = the quality assurance process that makes sure the output is excellent

When Forge needs to create or update a skill, it follows skill-creator's patterns:
- Interview the user (for new skills)
- Write SKILL.md with proper frontmatter and structure
- Create test cases and run evaluations (when appropriate)
- Optimize the description for triggering

What Forge adds on top:
- Structured multi-criteria review after each iteration
- Alternative solution exploration
- Grade-based convergence logic
- Automatic loop management

For test cases and evaluations, Forge uses skill-creator's eval infrastructure (evals.json, grader agent, eval-viewer) when the user wants quantitative validation. But the core value of Forge is the qualitative review loop — not every skill needs full benchmarks to be good.

---

## Communicating with the User

Follow the same principle as skill-creator: adapt to the user's technical level. Some additional guidelines for Forge:

- **Show the review summary** after each iteration — the grade table is the most important thing for the user to see. Keep it scannable.
- **Explain your reasoning** when you grade something below A. The user should understand what you're seeing and why it matters.
- **Present alternatives fairly** — don't dismiss them to justify the current approach. If an alternative is genuinely better, say so and pivot.
- **Report progress** between iterations: "Iteration 3 done — 4 criteria at A, 2 at B. Focusing on implementation quality and description triggering next."
- **Vietnamese by default** for this workspace (as per copilot-instructions.md). Review artifacts and SKILL.md internals stay in English.

---

## Quick Reference

| Situation | What Forge Does |
|-----------|----------------|
| "Tạo skill mới cho X" | Create via skill-creator → auto-review loop |
| "Review skill Y" | Load existing → auto-review → improve loop |
| "Nâng cấp skill Z" | Load → review → update → review loop |
| User says "đủ rồi" / "good enough" | Stop loop, present final state |
| All grades reach A | Auto-stop, present final skill |
| 10 iterations, no improvement | Auto-stop, explain plateau |

---

## Example Flow

```
User: "Tạo skill mới để tự động tạo changelog từ git log"

Forge:
  1. Interview → understand: auto-generate CHANGELOG.md from git commits
  2. Create draft SKILL.md (via skill-creator patterns)
  
  3. AUTO-REVIEW iteration 1:
     ┌───────────────────────────┬───────┐
     │ Criterion                 │ Grade │
     ├───────────────────────────┼───────┤
     │ Skill Structure           │   B   │
     │ Instruction Clarity       │   B   │
     │ Real-World Usefulness     │   A   │
     │ Alternative Analysis      │   C   │  ← hasn't explored git-cliff, etc.
     │ Implementation Quality    │   C   │  ← no script for parsing
     │ Description & Triggering  │   B   │
     └───────────────────────────┴───────┘
     Lowest: C → needs improvement
  
  4. Improvement plan:
     - Research git-cliff, auto-changelog, conventional-changelog
     - Compare to current "parse git log manually" approach
     - Add a bundled script for commit parsing
     - Tighten description
  
  5. UPDATE skill
  
  6. RE-REVIEW iteration 2:
     ┌───────────────────────────┬───────┐
     │ Criterion                 │ Grade │
     ├───────────────────────────┼───────┤
     │ Skill Structure           │   A   │
     │ Instruction Clarity       │   A   │
     │ Real-World Usefulness     │   A   │
     │ Alternative Analysis      │   A   │  ← compared 3 approaches
     │ Implementation Quality    │   B   │  ← script works, minor edge case
     │ Description & Triggering  │   A   │
     └───────────────────────────┴───────┘
     Lowest: B → one more round
  
  7. Fix edge case in script → RE-REVIEW iteration 3 → All A → Done!

  8. Present final skill to user with full review history.
```
