#!/usr/bin/env python3
"""Generate a static HTML page from Markdown or JSON content.

Usage:
    python3 gen_static.py --input content.json --output page.html --style corporate
    python3 gen_static.py --input content.md --output page.html --style minimal
"""

import argparse
import json
import sys
from html import escape
from pathlib import Path
from typing import Optional

STYLES = {
    "corporate": {
        "bg": "#ffffff",
        "text": "#2d3748",
        "heading": "#1a365d",
        "accent": "#3182ce",
        "link": "#2b6cb0",
        "border": "#e2e8f0",
        "code_bg": "#f7fafc",
        "font": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
        "max_width": "900px",
    },
    "academic": {
        "bg": "#fafafa",
        "text": "#1a202c",
        "heading": "#1a202c",
        "accent": "#744210",
        "link": "#5a3510",
        "border": "#e2e0dc",
        "code_bg": "#f5f0eb",
        "font": "Georgia, 'Times New Roman', serif",
        "max_width": "800px",
    },
    "minimal": {
        "bg": "#ffffff",
        "text": "#374151",
        "heading": "#111827",
        "accent": "#059669",
        "link": "#047857",
        "border": "#e5e7eb",
        "code_bg": "#f9fafb",
        "font": "'Inter', 'Helvetica Neue', Arial, sans-serif",
        "max_width": "780px",
    },
    "dark-modern": {
        "bg": "#0f172a",
        "text": "#f1f5f9",
        "heading": "#6366f1",
        "accent": "#22d3ee",
        "link": "#06b6d4",
        "border": "#334155",
        "code_bg": "#1e293b",
        "font": "'Inter', 'SF Pro Text', sans-serif",
        "max_width": "900px",
    },
    "creative": {
        "bg": "#fffbeb",
        "text": "#1e1b4b",
        "heading": "#8b5cf6",
        "accent": "#f59e0b",
        "link": "#d97706",
        "border": "#e5e0d5",
        "code_bg": "#fef3c7",
        "font": "'Poppins', 'Open Sans', sans-serif",
        "max_width": "860px",
    },
}


def read_content(input_path: Path) -> dict:
    """Read content from JSON or Markdown file."""
    text = input_path.read_text(encoding="utf-8")
    if input_path.suffix.lower() == ".json":
        return json.loads(text)
    # Treat as Markdown/plain text
    return {"title": input_path.stem.replace("-", " ").replace("_", " ").title(), "body_html": markdown_to_html(text)}


def markdown_to_html(md: str) -> str:
    """Minimal Markdown to HTML conversion (no external deps)."""
    lines = md.split("\n")
    html_parts = []
    in_list = False
    in_code = False
    code_lang = ""

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            if in_code:
                html_parts.append("</code></pre>")
                in_code = False
            else:
                code_lang = stripped[3:].strip()
                html_parts.append(f'<pre><code class="language-{escape(code_lang)}">')
                in_code = True
            continue
        if in_code:
            html_parts.append(escape(line))
            continue

        # Close list if needed
        if in_list and not stripped.startswith(("- ", "* ", "1.")):
            html_parts.append("</ul>")
            in_list = False

        # Headings
        if stripped.startswith("### "):
            html_parts.append(f"<h3>{escape(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{escape(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_parts.append(f"<h1>{escape(stripped[2:])}</h1>")
        # Lists
        elif stripped.startswith(("- ", "* ")):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{escape(stripped[2:])}</li>")
        # Horizontal rule
        elif stripped in ("---", "***", "___"):
            html_parts.append("<hr>")
        # Empty line
        elif not stripped:
            html_parts.append("")
        # Paragraph
        else:
            html_parts.append(f"<p>{escape(stripped)}</p>")

    if in_list:
        html_parts.append("</ul>")
    if in_code:
        html_parts.append("</code></pre>")

    return "\n".join(html_parts)


def generate_html(data: dict, style_name: str) -> str:
    """Generate a complete static HTML page."""
    s = STYLES.get(style_name, STYLES["corporate"])
    title = escape(data.get("title", "Document"))
    author = escape(data.get("author", ""))
    body = data.get("body_html", "")

    # If body is not HTML, treat sections
    if not body and "sections" in data:
        parts = []
        for sec in data["sections"]:
            sec_title = sec.get("title", "")
            sec_content = sec.get("content", "")
            if sec_title:
                parts.append(f"<h2>{escape(sec_title)}</h2>")
            if sec_content:
                for para in sec_content.split("\n\n"):
                    para = para.strip()
                    if para:
                        parts.append(f"<p>{escape(para)}</p>")
        body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="author" content="{author}">
  <title>{title}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: {s['font']};
      background: {s['bg']};
      color: {s['text']};
      line-height: 1.7;
      padding: 2rem;
    }}
    .container {{
      max-width: {s['max_width']};
      margin: 0 auto;
    }}
    h1 {{
      color: {s['heading']};
      font-size: 2.2em;
      margin: 1em 0 0.5em;
      border-bottom: 3px solid {s['accent']};
      padding-bottom: 0.3em;
    }}
    h2 {{
      color: {s['heading']};
      font-size: 1.6em;
      margin: 1.5em 0 0.5em;
      border-bottom: 1px solid {s['border']};
      padding-bottom: 0.2em;
    }}
    h3 {{
      color: {s['heading']};
      font-size: 1.3em;
      margin: 1.2em 0 0.4em;
    }}
    p {{ margin: 0.8em 0; }}
    a {{ color: {s['link']}; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    ul, ol {{ margin: 0.8em 0 0.8em 2em; }}
    li {{ margin: 0.3em 0; }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1em 0;
    }}
    th {{
      background: {s['accent']};
      color: #fff;
      padding: 0.6em 1em;
      text-align: left;
    }}
    td {{
      border: 1px solid {s['border']};
      padding: 0.5em 1em;
    }}
    tr:nth-child(even) td {{ background: rgba(0,0,0,0.02); }}
    pre {{
      background: {s['code_bg']};
      padding: 1em;
      border-radius: 6px;
      overflow-x: auto;
      margin: 1em 0;
    }}
    code {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.9em; }}
    blockquote {{
      border-left: 4px solid {s['accent']};
      padding: 0.5em 1em;
      margin: 1em 0;
      font-style: italic;
      background: rgba(0,0,0,0.02);
      border-radius: 4px;
    }}
    hr {{ border: none; border-top: 1px solid {s['border']}; margin: 2em 0; }}
    .footer {{
      margin-top: 3em;
      padding-top: 1em;
      border-top: 1px solid {s['border']};
      font-size: 0.85em;
      color: {s['text']}80;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    {body}
    <div class="footer">
      Generated by InsightEngine
    </div>
  </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate static HTML page from JSON or Markdown")
    parser.add_argument("--input", required=True, help="Path to JSON or Markdown file")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--style", choices=list(STYLES.keys()), default="corporate",
                        help="Page style (default: corporate)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    data = read_content(input_path)
    html = generate_html(data, args.style)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = output_path.stat().st_size / 1024
    print(f"✅ Saved: {output_path} ({size_kb:.1f} KB, style: {args.style})")


if __name__ == "__main__":
    main()
