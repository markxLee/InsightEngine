# Adaptive Flow Reference — Advisory Fallback & User Presentation

## Overview

When a search sub-flow fails after 2 attempts, the adaptive flow system:
1. Calls the advisory agent (DC-6) to generate alternative approaches
2. Presents these alternatives to the user in a clear, actionable format (DC-7)
3. Waits for user selection before retrying
4. Records the choice in session state to avoid repeating the prompt

This reference covers DC-7 (user presentation) and session state management in detail.

---

## DC-7: User-Facing Alternatives Presentation

### When to Trigger

```yaml
TRIGGER:
  - DC-6 has been called and returned alternatives
  - No prior user choice exists in session state for this source/step
  
DO_NOT_TRIGGER_IF:
  - Session state already has a choice: skip presentation, execute choice directly
  - Advisory budget exhausted: proceed with available items, note the gap
```

### Presentation Format

```
⚡ Không tìm được đủ {item_type} từ {source_domain} sau 2 lần thử.

Tôi đã thử:
• Lần 1: {search_approach_1} → {result_summary_1}
• Lần 2: {search_approach_2} → {result_summary_2}

Advisory agent đề xuất {N} phương án thay thế:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Phương án 1: {alternative_1.name}**
{alternative_1.description}
Ví dụ thực hiện: {alternative_1.example}
✅ {alternative_1.pros[0]}
⚠️ {alternative_1.cons[0]}

**Phương án 2: {alternative_2.name}**
{alternative_2.description}
Ví dụ thực hiện: {alternative_2.example}
✅ {alternative_2.pros[0]}
⚠️ {alternative_2.cons[0]}

**Phương án 3: Tiếp tục với {N} items đã thu thập**
Bỏ qua {source_domain}, tiếp tục xử lý với kết quả hiện có.
✅ Không tốn thêm thời gian
⚠️ Output có thể thiếu {gap_count} items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nhập 1, 2, hoặc 3 để chọn — hoặc mô tả hướng dẫn khác:
```

### Handling User Response

```yaml
RESPONSE_HANDLING:
  "1" or "phương án 1":
    action: Execute alternative_1 from advisory result
    
  "2" or "phương án 2":
    action: Execute alternative_2 from advisory result
    
  "3" or "tiếp tục":
    action: Accept current partial results, skip this source
    
  freeform_text:
    action: Use as custom guidance for the next attempt
    example: "thử tìm trực tiếp trên linkedin" → construct LinkedIn-specific query
    
  no_response_in_context:
    # User didn't respond (rare — only if context window is full)
    action: Default to alternative_1 (most capable, higher effort)
    note_to_user: "Đã tự động chọn phương án 1 vì không nhận được phản hồi"
```

---

## Session State Management

### State Structure

```yaml
# Stored in session state (in-memory during this pipeline run)
adaptive_flow_state:
  advisory_calls_used: 0       # Current count
  advisory_calls_max: 2        # Hard limit
  
  per_source:
    "{source_domain}":
      attempts: 0              # How many sub-flow attempts made
      advisory_called: false   # Whether advisory was called
      user_choice: null        # null = not yet asked | "1"/"2"/"3"/custom
      chosen_alternative: null # The alternative object from advisory
      resolved: false          # Whether source reached acceptable result
```

### State Transitions

```
PLANNED → attempt 1 → attempt 2 → [if still thin] → advisory called
→ alternatives presented → user selects → execute selected → resolved
```

### How to Read/Write State

State lives in the current session's working memory — it does NOT persist to disk.
Reference it using these operations within the pipeline run:

```python
# Pseudo-code for state management within gather skill
state = session_state.get("adaptive_flow_state", default_state)

# Check if advisory already called for this source
if state["per_source"][source]["advisory_called"]:
    # Use stored choice directly
    choice = state["per_source"][source]["user_choice"]
else:
    # Call DC-6, then DC-7
    alternatives = call_advisory_agent(context)
    state["per_source"][source]["advisory_called"] = True
    state["advisory_calls_used"] += 1
    
    # Present to user (DC-7)
    user_choice = present_and_await(alternatives)
    state["per_source"][source]["user_choice"] = user_choice

session_state.set("adaptive_flow_state", state)
```

---

## Example End-to-End Scenario

**Request:** "Tìm 10 tin tuyển dụng React developer tại HCM trên ITViec với URL trực tiếp"

**Sub-flow attempt 1:**
- site:itviec.com react developer ho chi minh → 1 result (thin)

**DOM exploration:**
- Fetched itviec.com homepage, found search form at `/it-jobs?query=`
- Internal search: itviec.com/it-jobs?query=react+developer&city=ho-chi-minh → 2 results

**Sub-flow attempt 2:**
- site:itviec.com "react" "ho chi minh" → 2 results
- Total: still only 3 items, need 10

**DC-6 triggered:** Advisory called with:
```yaml
item_type: job
attempted_sources: ["itviec.com — 3 items found"]
target_quantity: 10
gap_count: 7
failed_queries: ["site:itviec.com react developer ho chi minh", ...]
```

**Advisory returns:**
```
1. TopCV platform search — site:topcv.vn "react" "hồ chí minh" → likely 5-10 results
2. VietnamWorks combined — fetch vietnamworks.com/job-search/q-react-developer-ho-chi-minh
3. Accept 3 ITViec items and supplement with LinkedIn search
```

**DC-7 presentation:** User sees the 3 options, selects "1".

**Execute alternative 1:** Runs TopCV search → finds 7 more items → total 10 ✅

---

## Advisory Response Schema

When calling the advisory agent for alternative flows, expect this response structure:

```yaml
advisory_response:
  analysis: "<brief analysis of why the sub-flow failed>"
  alternatives:
    - name: "<short name>"
      description: "<2-3 sentence description of the approach>"
      example: "<concrete URL, query, or command to illustrate>"
      implementation_steps:
        - "<step 1>"
        - "<step 2>"
      pros:
        - "<benefit 1>"
      cons:
        - "<tradeoff 1>"
      estimated_yield: "<rough estimate: '5-10 items', 'uncertain', 'platform-dependent'>"
```

If the advisory agent response doesn't match this schema, extract the best-effort equivalent
and present it to the user using the DC-7 format above.
