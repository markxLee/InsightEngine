# Deep Research Mode — Iterative Multi-Round Search

## The Problem This Solves

When a user asks something like "find AI trends 2024-present, which models were released,
which are open source, classify them, and get their benchmarks", a single search query
like "AI trends 2024" captures only a fraction of what's needed. The request contains
multiple research dimensions, each requiring its own search strategy, and the results from
early searches should inform what to search for next.

## When Deep Research Activates

Deep research mode is NOT the default — it activates when the request has **research
complexity**. Signals that a request needs deep research:

- **Multiple information dimensions**: the user asks for several categories of information
  (models + benchmarks + classification + timelines)
- **Temporal range**: "from 2024 to now", "over the past 3 years", "trends over time"
- **Comparison/classification**: "classify", "compare", "categorize", "phân loại", "so sánh"
- **Exhaustive intent**: "tất cả", "comprehensive", "đầy đủ", "chi tiết", "toàn bộ"
- **Data aggregation**: "tổng hợp điểm benchmark", "list all", "collect all data points"
- **Multi-step reasoning**: the answer requires connecting information from different sources

If the user just says "tìm kiếm về AI" → standard single-query search is fine.
If the user says "tìm kiếm về xu hướng AI 2024-2026, các model đã release, so sánh benchmark"
→ deep research mode.

---

## Phase 1: Query Decomposition

Before searching, decompose the user's request into distinct **research dimensions**.
Each dimension becomes its own search thread.

### How to decompose

Read the request and identify every distinct piece of information the user wants.
Think of it as: "If I were a researcher given this task, what separate questions
would I need to answer?"

**Example:**
Request: "tìm kiếm về xu hướng AI 2024-hiện tại, những model AI nào được release từng năm,
model nào opensource, phân loại các AI model, tổng hợp điểm benchmark"

Decomposition:
```
1. AI trends overview 2024-2026 (landscape, key developments)
2. Major AI models released in 2024 (GPT-4o, Claude 3, Gemini, Llama 3, etc.)
3. Major AI models released in 2025 (GPT-4.5, Claude 3.5/4, Gemini 2, etc.)
4. Major AI models released in 2026 (what's out so far)
5. Open-source vs closed-source AI models comparison
6. AI model taxonomy/classification (LLM, multimodal, code, image, etc.)
7. AI model benchmark scores (MMLU, HumanEval, MATH, etc.)
8. AI benchmark leaderboards and comparison tables
```

### Query generation rules

For each dimension, generate 1-2 specific search queries:
- Use English for technical topics (better search results)
- Include year/date qualifiers when relevant
- Add specific terms: "benchmark scores", "comparison table", "list of models"
- Vary query phrasing between dimensions to get diverse results

**Bad queries** (too vague, too literal):
- "AI trends 2024" ← captures only one slice
- "xu hướng AI" ← Vietnamese query gets fewer technical results

**Good queries** (specific, targeted):
- "major AI models released 2024 2025 comparison"
- "open source AI models 2024 2025 list Llama Mistral"
- "AI benchmark MMLU HumanEval scores 2024 2025 leaderboard"
- "AI model classification taxonomy LLM multimodal 2024"

Present the decomposition to the user (in pipeline mode, auto-approve):
```
🔬 Phân tích yêu cầu nghiên cứu:
Tôi đã chia thành {N} hướng tìm kiếm:
1. {dimension_1} → query: "{query_1}"
2. {dimension_2} → query: "{query_2}"
...
Bắt đầu tìm kiếm?
```

---

## Phase 2: Round 1 — Broad Search

Execute searches for ALL dimensions (not just the first one). For each dimension:

1. Run `vscode-websearchforcopilot_webSearch` with the constructed query
2. From results, select the **2-3 most relevant URLs** (prefer authoritative sources:
   official blogs, arxiv, reputable tech publications, leaderboard sites)
3. Fetch each URL via `fetch_webpage`
4. Extract and tag the content: `[Dimension: {name}] [Source: {url}]`

**Source quality ranking** (prefer higher):
- Official release blogs (openai.com/blog, anthropic.com, meta.ai)
- Research papers and arxiv
- Reputable tech media (The Verge, TechCrunch, Ars Technica, VentureBeat)
- Benchmark leaderboard sites (huggingface.co/spaces, paperswithcode.com)
- Wikipedia and encyclopedia entries
- Personal blogs and forums (lowest priority, but useful for opinions)

**Parallel execution**: search all dimensions before fetching. This way you can batch
URL fetches and avoid waiting for each dimension sequentially.

After Round 1, report:
```
🔍 Vòng 1 hoàn tất:
- {N} hướng tìm kiếm
- {M} nguồn đã thu thập
- ~{total_chars} ký tự
Đang phân tích để tìm gaps...
```

---

## Phase 3: Gap Analysis — The Critical Step

This is what distinguishes deep research from simple search. After Round 1, **read and
analyze** what you've collected, then identify what's missing.

### How to identify gaps

1. **Check each dimension**: does the collected content adequately answer the question?
   - If a dimension has < 500 chars of relevant content → it's a gap
   - If content is superficial (mentions topic but no data/details) → it's a gap

2. **Check for missing specifics**: the user asked for benchmark scores — do you have
   actual numbers, or just mentions that benchmarks exist?

3. **Check temporal coverage**: if the user asked for 2024-2026, do you have data for
   each year? Missing a year = gap.

4. **Check for emerging topics**: did Round 1 results mention things the user didn't
   ask about but that are clearly relevant? (e.g., user asked about AI models but
   results mention a major AI safety development that contextualizes the trends)

5. **Check for specific entities**: if you found a list of 20 AI models but only have
   benchmark data for 5, the other 15 are gaps.

### Generate follow-up queries

For each gap, generate a targeted query:
- More specific than Round 1 (narrow down to the exact missing piece)
- May include entity names found in Round 1 ("Llama 3 benchmark MMLU score")
- May target specific sources found in Round 1 ("site:huggingface.co open-llm-leaderboard")

Report gaps:
```
📊 Phân tích gaps:
- ✅ Đủ dữ liệu: {covered_dimensions}
- ⚠️ Cần bổ sung: {gap_dimensions}
  - {gap_1}: {reason}
  - {gap_2}: {reason}
Đang tìm kiếm bổ sung...
```

---

## Phase 4: Round 2+ — Targeted Deep Dives

Execute follow-up searches for gaps identified in Phase 3. Same process as Round 1 but:
- Queries are more specific and targeted
- Fewer URLs per query (1-2, targeting exactly what's missing)
- May use different search strategies (e.g., searching for a specific leaderboard URL
  found in Round 1 results)

After Round 2, do another gap analysis. If critical gaps remain, do Round 3.

### Depth limits

To prevent infinite loops:
- **Maximum 3 rounds** of search (Round 1 broad + Round 2 targeted + Round 3 final)
- **Maximum 15 total URL fetches** across all rounds
- **Stop early** if Round N+1 would only add < 10% new content
- **Report honestly** if some dimensions couldn't be fully covered:
  "⚠️ Không tìm được dữ liệu benchmark chi tiết cho model X — nguồn chưa công bố."

---

## Phase 5: Consolidate & Structure

After all rounds, combine content with clear provenance:

```markdown
## Research Summary

### Dimensions Covered
1. {dimension_1}: {coverage_assessment} — {N} sources
2. {dimension_2}: {coverage_assessment} — {M} sources
...

### Gaps Remaining
- {any_unfilled_gaps_with_honest_explanation}

---

{combined_content_organized_by_dimension}
```

This structured output goes to bien-soan for synthesis. The dimension headers and
coverage assessment help bien-soan understand what content is strong vs weak.

---

## Complete Example

**User request:** "tìm kiếm về xu hướng AI 2024-hiện tại, những model AI nào được release
từng năm, model nào opensource, phân loại các AI model, tổng hợp điểm benchmark"

**Decomposition (8 dimensions):**
1. AI landscape overview 2024-2026
2. Models released 2024 (GPT-4o, Claude 3, Gemini 1.5, Llama 3, Mistral)
3. Models released 2025 (GPT-4.5, Claude 3.5 Sonnet/Haiku, Gemini 2, Llama 3.1/3.2)
4. Models released 2026 (Claude 4, Gemini 2.5, etc.)
5. Open-source models list and comparison
6. Model taxonomy (LLM, multimodal, code-gen, image-gen, video-gen)
7. Benchmark scores (MMLU, HumanEval, MATH, GSM8K, ARC)
8. Benchmark leaderboards

**Round 1 queries (8 searches):**
- "major AI models released 2024 GPT Claude Gemini Llama timeline"
- "AI models released 2025 new LLM list"
- "AI models 2026 latest releases"
- "open source AI models 2024 2025 comparison Llama Mistral Qwen"
- "AI model types classification LLM multimodal 2024"
- "AI benchmark scores MMLU HumanEval comparison 2024 2025"
- "huggingface open LLM leaderboard 2025"
- "AI trends 2024 2025 2026 overview developments"

**Round 1 result:** 15 URLs fetched, ~80,000 chars

**Gap analysis:**
- ✅ Model lists 2024-2025: good coverage
- ✅ Open-source vs closed: good
- ⚠️ 2026 models: sparse (year just started)
- ⚠️ Benchmark numbers: found leaderboard references but not actual scores
- ⚠️ Video/image gen models: mostly LLM-focused results

**Round 2 queries (3 follow-up searches):**
- "AI benchmark scores table MMLU GPT-4 Claude Gemini Llama 2025"
- "AI image generation models 2024 2025 DALL-E Midjourney Stable Diffusion"
- "AI video generation models Sora Runway 2024 2025"

**Round 2 result:** 6 more URLs, ~25,000 additional chars

**Final gap analysis:**
- ✅ All dimensions covered with data
- ⚠️ Some 2026 models have no benchmark data yet (honestly noted)

**Total:** 21 URLs, ~105,000 chars, organized by 8 dimensions → passed to bien-soan

---

## Integration with Pipeline

When tong-hop detects a complex research request, it sets `research_depth: deep` in the
thu-thap call. Thu-thap then follows this reference instead of the standard single-query
workflow. The phases above replace Steps 1-4 of the standard thu-thap flow.

tong-hop should also adjust its execution plan to show the research phases:
```
📋 Kế hoạch thực hiện:

**Loại yêu cầu:** Nghiên cứu chuyên sâu (Deep Research)
**Hướng tìm kiếm:** {N} hướng (sẽ tìm kiếm nhiều vòng)

**Các bước:**
1. 🔬 Phân tách yêu cầu thành {N} hướng nghiên cứu
2. 🔍 Vòng 1: Tìm kiếm rộng ({N} queries)
3. 📊 Phân tích gaps và tìm kiếm bổ sung
4. 📝 Biên soạn và tổng hợp
5. 📄 Xuất {format}
```
