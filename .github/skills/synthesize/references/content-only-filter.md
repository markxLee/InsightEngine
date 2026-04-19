# Content-Only Question Filter — Reference

## Overview

When `autonomy_mode=true`, the pipeline is allowed to ask the user at most ONE question.
This filter classifies every potential question as CONTENT or TECHNICAL:

- **CONTENT questions:** about what to deliver (allowed, max 1)
- **TECHNICAL questions:** about how to deliver it (suppressed entirely)

---

## Question Classification

### CONTENT Questions (allowed — ask if genuinely ambiguous)

These affect WHAT the output contains. Without clarity, the output could be meaningfully wrong.

```yaml
CONTENT_QUESTIONS:
  scope:
    - "Bạn muốn báo cáo về tỉnh nào cụ thể?" (which province)
    - "Bao gồm cả công ty nước ngoài không?" (foreign companies)
    - "Muốn tập trung vào phân khúc nào?" (which segment)
    
  format_preference:
    - "Bạn muốn file Word hay PDF?" (ONLY if format is completely unspecified)
    - "Bao nhiêu trang khoảng?" (ONLY if length is completely unspecified)
    
  target_audience:
    - "Báo cáo này dùng cho nội bộ hay chia sẻ ra ngoài?"
    
  data_cutoff:
    - "Dữ liệu tính đến tháng nào?" (ONLY if time range is genuinely unclear)
```

### TECHNICAL Questions (suppressed — always decide automatically)

These affect HOW to deliver. The pipeline decides; user should never see these.

```yaml
TECHNICAL_QUESTIONS_SUPPRESSED:
  library_choice:
    examples:
      - "Dùng openpyxl hay pandas để tạo Excel?"
      - "Tạo slide bằng pptxgenjs hay ppt-master?"
    decision: Auto-pick best library per task
    
  query_strategy:
    examples:
      - "Dùng site:itviec.com hay tìm Google tổng quát?"
      - "Seed queries đã tạo, confirm để tiếp tục?"
      - "Dùng query nào cho platform này?"
    decision: Use platform-specific strategy from gather skill
    
  batch_control:
    examples:
      - "Đã có 10 items, tiếp tục thu thập không?"
      - "Thu thập thêm từ platform này không?"
      - "Batch 1 done, proceed to batch 2?"
    decision: Always continue up to target quantity
    
  retry_approval:
    examples:
      - "Fetch URL bị lỗi, thử lại không?"
      - "Timeout, retry không?"
    decision: Auto-retry up to configured max, then skip
    
  format_details:
    examples:
      - "Cỡ chữ bao nhiêu?"
      - "Font nào cho Word?"
      - "Màu gì cho chart?"
      - "Số cột trong Excel?"
    decision: Use template defaults
    
  step_approval:
    examples:
      - "Step 1 done, proceed to Step 2?"
      - "Bước thu thập hoàn tất, tiếp tục biên soạn không?"
      - "Confirm để tạo file Excel?"
    decision: Always proceed
    
  dependency_check:
    examples:
      - "Thư viện X chưa cài, install không?"
      - "Cài openpyxl trước nhé?"
    decision: Auto-install (or show one-time error if critical)
```

---

## The ONE Question Rule

```yaml
ONE_QUESTION_RULE:
  when: autonomy_mode=true
  
  allowed:
    count: 1 per pipeline run
    type: CONTENT questions only
    condition: genuinely ambiguous — output would be meaningfully different either way
    
  format:
    inline: Include question in a progress message, don't block pipeline
    default: If user doesn't respond in next message, use best assumption and proceed
    
  wording_rules:
    - Short (1 sentence)
    - Binary or multiple choice preferred (not open-ended)
    - Include the default assumption: "Nếu không trả lời tôi sẽ dùng..."
    
  example:
    BAD:  "Bạn muốn tập trung vào khía cạnh nào của thị trường lao động?"
    GOOD: "Tôi sẽ bao gồm cả công ty nước ngoài và startup. Chỉ dùng công ty Việt Nam thì nhắn lại nhé."
    
  track:
    question_asked: boolean   # set true after asking the 1 allowed question
    # Once true, NO more questions for this pipeline run
```

---

## Decision Matrix

| Question Type | autonomy_mode=false | autonomy_mode=true | silent_mode |
|--------------|--------------------|--------------------|-------------|
| Content, ambiguous | ASK | Ask once, proceed with assumption | ASSUME, skip |
| Content, inferrable | INFER | INFER | INFER |
| Technical | May ask | SUPPRESS | SUPPRESS |
| Step approval | Ask | SUPPRESS | SUPPRESS |
| Retry approval | Ask | SUPPRESS | SUPPRESS |
| Batch approval | Ask | SUPPRESS | SUPPRESS |

---

## Inferral Heuristics

Before asking ANY content question, try these inference rules:

```yaml
INFERENCE_RULES:
  format:
    if_mentioned: Use mentioned format
    if_not_mentioned: Infer from content type
      report/báo cáo → .docx
      data/dữ liệu → .xlsx
      thuyết trình/slide → .pptx
      trang web → .html
      default: .docx
      
  style:
    if_mentioned: Use mentioned style
    if_not_mentioned: Infer from context
      formal/chuyên nghiệp → corporate
      research/nghiên cứu → academic
      quick/nhanh → minimal
      tech/startup → dark-modern
      default: corporate
      
  scope:
    if_mentioned: Use mentioned scope
    if_not_mentioned: Use comprehensive depth
      length/số trang: default A4, no page limit
      time_range: default current year (2026) unless specified
      geography: default Vietnam unless specified
```
