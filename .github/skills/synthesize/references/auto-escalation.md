# Auto-Escalation Protocol — InsightEngine

> When a tool or approach fails, automatically escalate to a more powerful alternative.  
> Never ask the user technical questions. Never expose tool names to user.

---

## Core Principle

```yaml
ESCALATION_RULE:
  on_failure: Try next tier automatically
  ask_user: ONLY when ALL tiers exhausted
  expose_internals: NEVER (no "Playwright tier 3" messages)
  user_message_on_escalation: "Đang thử phương pháp khác..." (generic)
  logging: All attempts logged to tmp/.agent-context.json → escalation_log
```

---

## Skill Escalation Tiers

### thu-thap (Content Gathering)

```yaml
url_fetching:
  tier_1:
    tool: fetch_webpage (Copilot built-in)
    when: Default for all URLs
    fail_signals: empty content, HTTP error, < 50 chars returned
    
  tier_2:
    tool: httpx + beautifulsoup4
    script: scripts/httpx_fetch.py
    when: tier_1 returns empty/error
    fail_signals: HTTP 403/429, empty body, connection refused
    
  tier_3:
    tool: Playwright stealth mode
    script: scripts/playwright_fetch.py
    when: tier_2 fails (bot protection detected)
    fail_signals:
      - "Just a moment", "Checking your browser"
      - Cloudflare challenge page
      - CAPTCHA wall
      - JavaScript-rendered SPA returning empty
    
  exhausted:
    action: Log failure, skip this URL, continue pipeline
    user_message: "Không thể truy cập URL này. Bỏ qua và tiếp tục."

web_search:
  tier_1:
    tool: vscode-websearchforcopilot_webSearch
    when: Default for all search queries
    fail_signals: no results, empty response
    
  tier_2:
    tool: Reformulate query (broader terms, different language)
    when: tier_1 returns irrelevant/empty results
    
  exhausted:
    action: Report to user that search found no results
    user_message: "Không tìm thấy kết quả cho chủ đề này."

file_reading:
  tier_1:
    tool: markitdown
    when: Default for all file types
    fail_signals: empty output, garbled text, encoding errors
    
  tier_2:
    tool: Format-specific library (python-docx, openpyxl, pdfplumber)
    when: markitdown returns garbled/empty
    
  tier_3:
    tool: Binary read + manual parsing
    when: tier_2 also fails
    
  exhausted:
    action: Report unreadable file
    user_message: "Không thể đọc file này. Vui lòng kiểm tra định dạng."
```

### tao-slide (Presentation Generation)

```yaml
slide_generation:
  tier_1:
    tool: pptxgenjs (Node.js quick mode)
    when: Default, simple slides
    fail_signals: Node.js error, template not found
    
  tier_2:
    tool: ppt-master SVG→PPTX pipeline
    when: tier_1 fails OR user needs professional quality
    fail_signals: SVG rendering error, missing fonts
    
  exhausted:
    action: Deliver tier_1 output with quality warning
    user_message: "File slide đã tạo nhưng có thể cần chỉnh sửa thêm."
```

### tao-hinh (Chart/Image Generation)

```yaml
chart_generation:
  tier_1:
    tool: matplotlib + seaborn
    when: Default for all charts
    fail_signals: rendering error, missing data
    
  tier_2:
    tool: Simplified chart (fewer series, basic style)
    when: complex chart fails
    
  exhausted:
    action: Report chart generation failure
    user_message: "Không thể tạo biểu đồ với dữ liệu hiện tại."

image_generation:
  tier_1:
    tool: diffusers + torch/MPS (Apple Silicon)
    when: Default for AI image gen
    fail_signals: CUDA/MPS error, OOM, model download failure
    
  tier_2:
    tool: Simpler model (SD-Turbo instead of SDXL)
    when: tier_1 fails
    
  tier_3:
    tool: Skip image, use placeholder
    when: No GPU available
    
  exhausted:
    action: Continue without images
    user_message: "Bỏ qua hình ảnh AI — tiếp tục với nội dung."
```

### bien-soan (Content Synthesis)

```yaml
synthesis:
  tier_1:
    mode: comprehensive (default)
    when: Default for all synthesis
    fail_signals: output < 1000 words for comprehensive, thin sections
    
  tier_2:
    mode: Re-synthesize with explicit section outlines + min word targets
    when: tier_1 produces thin content
    
  tier_3:
    mode: Section-by-section synthesis (one section per call)
    when: tier_2 still produces thin content (likely context limitation)
    
  exhausted:
    action: Deliver best available with quality note
    user_message: "Nội dung đã tổng hợp — có thể cần bổ sung thêm."
```

---

## Logging Format

Each escalation attempt is logged to `tmp/.agent-context.json → escalation_log`:

```json
{
  "skill": "thu-thap",
  "tool_tried": "fetch_webpage",
  "target": "https://example.com",
  "result": "failure",
  "error": "HTTP 403 Forbidden",
  "next_tier": "httpx",
  "timestamp": "2026-04-18T10:30:00Z"
}
```

---

## User-Facing Messages

```yaml
MESSAGES:
  # These are the ONLY messages users should see during escalation.
  # Never mention tool names, tier numbers, or technical details.
  
  during_escalation: "Đang thử phương pháp khác..."
  url_skip: "Không thể truy cập URL này. Bỏ qua và tiếp tục."
  search_empty: "Không tìm thấy kết quả. Thử với từ khóa khác?"
  file_unreadable: "Không thể đọc file này. Vui lòng kiểm tra định dạng."
  image_skip: "Bỏ qua hình ảnh — tiếp tục với nội dung."
  quality_note: "Nội dung đã tạo — có thể cần bổ sung thêm chi tiết."
  all_failed: "Không thể hoàn thành bước này sau nhiều lần thử. Bỏ qua và tiếp tục."
```
