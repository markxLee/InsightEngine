# Speaker Notes & PDF Export — reveal.js Presentations

## Speaker Notes

reveal.js presentations support speaker notes via `<aside class="notes">`.
Notes are visible in Speaker View (press `S` during presentation).

```yaml
SPEAKER_NOTES:
  json_format:
    # Add "notes" key to any slide object:
    {"type": "content", "title": "...", "bullets": [...], "notes": "Detailed talking points here"}
    
  viewing:
    keyboard: Press "S" to open Speaker View (separate window)
    shows: Current slide, next slide, elapsed time, speaker notes
    
  generation:
    - bien-soan generates notes automatically when output is presentation
    - Notes contain expanded talking points, transitions, key insights
    - 2-4 sentences per slide, conversational tone
    
  example_json: |
    {
      "type": "content",
      "title": "Q1 Revenue",
      "bullets": ["Revenue up 15%", "Beat target by 5%"],
      "notes": "Revenue grew 15% YoY. B2B segment was the strongest driver. Note that Q4 was already a record quarter."
    }
```

---

## PDF Export

Presentations can be exported to PDF via browser print (Ctrl+P / Cmd+P).

```yaml
PDF_EXPORT:
  method: Browser print dialog (Ctrl+P / Cmd+P)
  
  print_css:
    - Each slide becomes a separate page (page-break-after: always)
    - Fragment animations resolved (all bullets visible)
    - Navigation controls hidden (slide numbers, arrows, progress bar)
    - Slides use full page width, proper spacing
    
  speaker_notes_in_pdf:
    flag: --print-notes
    behavior: |
      When --print-notes is used:
        - reveal.js showNotes = true
        - @media print CSS shows notes below each slide
        - Notes styled with border-top, italic, "Speaker Notes:" prefix
    default: Notes hidden in PDF (--print-notes not set)
    
  cli_examples:
    # Standard PDF (no notes)
    python3 gen_reveal.py --input data.json --output slides.html --style corporate
    # Then: Open in browser → Ctrl+P → Save as PDF
    
    # PDF with speaker notes visible
    python3 gen_reveal.py --input data.json --output slides.html --style corporate --print-notes
    # Then: Open in browser → Ctrl+P → Save as PDF (notes appear below each slide)
    
  layout_preservation:
    - Slide backgrounds maintained in print
    - Table and code block styling preserved
    - Images rendered at proper size
    - Typography and colors match screen version
```
