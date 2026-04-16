# Translation Mode — Detailed Reference (US-1.2.2)

## Language Detection

```yaml
DETECT_INTENT:
  1. Determine source language:
     - Vietnamese indicators: diacritics (ă, â, đ, ê, ô, ơ, ư), common words (và, của, là, được)
     - English indicators: common words (the, is, are, with, from)
     - Mixed: treat as source language = dominant language
  2. Determine target language:
     - "dịch sang tiếng Anh" / "translate to English" → target = English
     - "dịch sang tiếng Việt" / "translate to Vietnamese" → target = Vietnamese
     - Ambiguous: ask user (interactive) or infer opposite of source (pipeline)
```

## Translation Workflow

```yaml
STEPS:
  1_PREPARE:
    - Split content into translatable sections (by heading/paragraph)
    - Non-translatable elements (preserve as-is):
      - Code blocks, URLs, file paths
      - Proper nouns / brand names
      - Technical terms → translate with original in parentheses (first occurrence)

  2_TRANSLATE_SECTIONS:
    for_each_section:
      - Translate heading text (preserve heading level)
      - Translate paragraph text naturally (not word-by-word)
      - Translate table cell content (preserve table structure)
      - Translate bullet point text (preserve list markers)
    quality_rules:
      - Natural, fluent target language (not machine-translation style)
      - Preserve meaning and tone of original
      - Consistent terminology throughout
      - Technical terms: "translated_term (original_term)" on first use only

  3_PRESERVE_FORMATTING:
    must_preserve:
      - Heading hierarchy (H1, H2, H3 levels)
      - Bold and italic markers, inline code, code blocks
      - Tables with pipe separators, numbered/bulleted lists
      - Links: translate link text, preserve URL
      - Images: translate alt text, preserve path

  4_DELIVER:
    to_user: |
      ✅ Dịch thuật hoàn tất / Translation complete:
      - Ngôn ngữ gốc / Source: {source_language}
      - Ngôn ngữ đích / Target: {target_language}
      - Số phần / Sections: {N} | Độ dài: ~{word_count} từ/words
```

## Quality Rules by Direction

```yaml
VIETNAMESE_TO_ENGLISH:
  - Use American English spelling
  - Expand Vietnamese abbreviations
  - Adapt Vietnamese-specific idioms to equivalent English expressions
  - Keep formal/informal tone matching the original

ENGLISH_TO_VIETNAMESE:
  - Use standard Vietnamese (phổ thông)
  - Technical terms: keep English original in parentheses on first use
  - Adapt English idioms to natural Vietnamese equivalents
  - Use appropriate Vietnamese pronouns and honorifics
  - Numbers and units: keep as-is (no conversion)

BILINGUAL_MODE:
  trigger: "song ngữ", "bilingual", "cả hai ngôn ngữ"
  format: |
    Each section in both languages sequentially:
    ## Heading (English) / ## Tiêu đề (Tiếng Việt)
    English paragraph... / Đoạn văn tiếng Việt...
```
