# Session Summary & View Suggestions — Full Reference

## Session Summary

After every completed pipeline run, append an entry to `output/session-summary.md`.

```yaml
SESSION_SUMMARY:
  file: output/session-summary.md
  action:
    if_exists: Append new session entry at end of file
    if_missing: Create file with header + first entry

  entry_format: |
    ## Session {N} — {date}

    **Yêu cầu ban đầu:** {user_original_request}

    **Nguồn dữ liệu ({source_count}):**
    {- file/url/search per source}

    **Kết quả ({output_count} file):**
    {- path (size) per output file}

    **Thời gian xử lý:** ~{elapsed_time}

    ---

COPILOT_MUST:
  - Always create/append after pipeline completes
  - Include original user request (verbatim, first 200 chars if long)
  - List all input sources with type (file/url/web-search)
  - List all output files with full paths and sizes
  - Create output/ directory if it doesn't exist
```

---

## View Suggestions

After creating the session summary, suggest how the user can open the output file(s).

```yaml
VIEW_SUGGESTIONS:
  format: |
    ---
    📂 **Mở file đầu ra:**
    {view_suggestion_per_file}
    ---

  per_format:
    docx: |
      📝 **{filename}.docx**
      → Cài extension **"Word Document Viewer"** (vscode:extension/cweijan.vscode-office)
         hoặc tải về và mở bằng Microsoft Word / LibreOffice

    xlsx: |
      📊 **{filename}.xlsx**
      → Cài extension **"Excel Viewer"** (vscode:extension/GrapeCity.gc-excelviewer)
         Hoặc tải về và mở bằng Excel / LibreOffice Calc

    pptx: |
      📊 **{filename}.pptx**
      → Tải file về máy và mở bằng PowerPoint / LibreOffice Impress

    pdf: |
      📄 **{filename}.pdf**
      → VS Code có built-in PDF preview — click vào file để mở trực tiếp

    html: |
      🌐 **{filename}.html**
      → Mở bằng **Simple Browser** (built-in):
         Ctrl+Shift+P → "Simple Browser: Show" → nhập đường dẫn file
      → Hoặc cài **"Live Preview"** (vscode:extension/ms-vscode.live-server)

    png: |
      🖼️ **{filename}.png**
      → Click vào file trong Explorer để xem trực tiếp trong VS Code

COPILOT_MUST:
  - ALWAYS show view suggestions after pipeline completes
  - For HTML: ALWAYS mention Simple Browser (no extension needed)
  - For docx/xlsx/pptx: ALWAYS mention download option as fallback
  - Use Vietnamese for all suggestion messages
```
