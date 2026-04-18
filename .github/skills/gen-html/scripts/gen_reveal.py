#!/usr/bin/env python3
"""Generate a reveal.js HTML presentation from JSON slide data.

Usage:
    python3 gen_reveal.py --input slides.json --output presentation.html --style corporate
"""

import argparse
import base64
import json
import sys
from html import escape
from pathlib import Path
from typing import Optional

REVEALJS_VERSION = "5.1.0"
REVEALJS_CDN = f"https://cdn.jsdelivr.net/npm/reveal.js@{REVEALJS_VERSION}"

TRANSITIONS = ["none", "slide", "fade", "convex", "concave", "zoom"]

STYLES = {
    # ── Light variants ──────────────────────────────────────────────
    "corporate": {
        "reveal_theme": "white",
        "background": "#ffffff",
        "heading_color": "#1a365d",
        "text_color": "#2d3748",
        "accent_color": "#3182ce",
        "link_hover": "#2b6cb0",
        "font_heading": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
        "font_body": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
        "table_header_bg": "#1a365d",
        "table_stripe_bg": "rgba(49,130,206,0.06)",
        "blockquote_bg": "rgba(49,130,206,0.05)",
        "code_bg": "#f7fafc",
        "default_transition": "slide",
    },
    "academic": {
        "reveal_theme": "simple",
        "background": "#fafafa",
        "heading_color": "#1a202c",
        "text_color": "#1a202c",
        "accent_color": "#744210",
        "link_hover": "#5a3510",
        "font_heading": "Georgia, 'Times New Roman', serif",
        "font_body": "Georgia, 'Times New Roman', serif",
        "table_header_bg": "#744210",
        "table_stripe_bg": "rgba(116,66,16,0.05)",
        "blockquote_bg": "rgba(116,66,16,0.04)",
        "code_bg": "#f5f0eb",
        "default_transition": "fade",
    },
    "minimal": {
        "reveal_theme": "white",
        "background": "#ffffff",
        "heading_color": "#111827",
        "text_color": "#374151",
        "accent_color": "#059669",
        "link_hover": "#047857",
        "font_heading": "'Inter', 'Helvetica Neue', Arial, sans-serif",
        "font_body": "'Inter', 'Helvetica Neue', Arial, sans-serif",
        "table_header_bg": "#059669",
        "table_stripe_bg": "rgba(5,150,105,0.05)",
        "blockquote_bg": "rgba(5,150,105,0.04)",
        "code_bg": "#f9fafb",
        "default_transition": "none",
    },
    "creative": {
        "reveal_theme": "moon",
        "background": "#fffbeb",
        "heading_color": "#8b5cf6",
        "text_color": "#1e1b4b",
        "accent_color": "#f59e0b",
        "link_hover": "#d97706",
        "font_heading": "'Poppins', 'Nunito', sans-serif",
        "font_body": "'Open Sans', 'Nunito', sans-serif",
        "table_header_bg": "#8b5cf6",
        "table_stripe_bg": "rgba(139,92,246,0.06)",
        "blockquote_bg": "rgba(245,158,11,0.08)",
        "code_bg": "#fef3c7",
        "default_transition": "zoom",
    },
    "warm-earth": {
        "reveal_theme": "simple",
        "background": "#fdf8f3",
        "heading_color": "#92400e",
        "text_color": "#451a03",
        "accent_color": "#b45309",
        "link_hover": "#92400e",
        "font_heading": "'Playfair Display', Georgia, serif",
        "font_body": "'Source Sans Pro', 'Segoe UI', sans-serif",
        "table_header_bg": "#92400e",
        "table_stripe_bg": "rgba(180,83,9,0.05)",
        "blockquote_bg": "rgba(180,83,9,0.06)",
        "code_bg": "#fef3c7",
        "default_transition": "convex",
    },
    # ── Dark variants ───────────────────────────────────────────────
    "dark-modern": {
        "reveal_theme": "night",
        "background": "#0f172a",
        "heading_color": "#6366f1",
        "text_color": "#f1f5f9",
        "accent_color": "#22d3ee",
        "link_hover": "#06b6d4",
        "font_heading": "'Inter', 'SF Pro Display', sans-serif",
        "font_body": "'Inter', 'SF Pro Text', sans-serif",
        "table_header_bg": "#4338ca",
        "table_stripe_bg": "rgba(99,102,241,0.1)",
        "blockquote_bg": "rgba(99,102,241,0.08)",
        "code_bg": "#1e293b",
        "default_transition": "fade",
    },
    "dark-neon": {
        "reveal_theme": "night",
        "background": "#0a0a0a",
        "heading_color": "#00ffc8",
        "text_color": "#e4e4e7",
        "accent_color": "#ff3cac",
        "link_hover": "#e11d9b",
        "font_heading": "'JetBrains Mono', 'Fira Code', monospace",
        "font_body": "'Inter', 'Helvetica Neue', sans-serif",
        "table_header_bg": "#18181b",
        "table_stripe_bg": "rgba(0,255,200,0.06)",
        "blockquote_bg": "rgba(255,60,172,0.08)",
        "code_bg": "#18181b",
        "default_transition": "zoom",
    },
    "dark-elegant": {
        "reveal_theme": "night",
        "background": "#1a1a2e",
        "heading_color": "#e0a458",
        "text_color": "#d4d4d8",
        "accent_color": "#e0a458",
        "link_hover": "#c88b3a",
        "font_heading": "'Playfair Display', Georgia, serif",
        "font_body": "'Lato', 'Helvetica Neue', sans-serif",
        "table_header_bg": "#16213e",
        "table_stripe_bg": "rgba(224,164,88,0.08)",
        "blockquote_bg": "rgba(224,164,88,0.06)",
        "code_bg": "#16213e",
        "default_transition": "concave",
    },
}


def embed_image_base64(image_path: str) -> str:
    """Convert an image file to a base64 data URI."""
    path = Path(image_path)
    if not path.exists():
        return ""
    suffix = path.suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp"}
    mime = mime_map.get(suffix, "image/png")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _bg_attrs(slide: dict) -> str:
    """Build data-background-* attributes from slide's 'background' dict.

    Supported background types (detected automatically):
      - solid color:  {"color": "#1a365d"}
      - gradient:     {"gradient": "linear-gradient(135deg, #667eea, #764ba2)"}
      - image URL:    {"image": "https://example.com/bg.jpg"}
      - local image:  {"image": "/path/to/bg.png"}
      - video URL:    {"video": "https://example.com/bg.mp4"}

    Optional keys: opacity (0-1), size (cover/contain), position, repeat.
    """
    bg = slide.get("background")
    if not bg:
        return ""
    if isinstance(bg, str):
        # shorthand: just a color or gradient string
        if bg.startswith("linear-gradient") or bg.startswith("radial-gradient"):
            return f' data-background-gradient="{escape(bg)}"'
        return f' data-background-color="{escape(bg)}"'
    attrs = []
    if "color" in bg:
        attrs.append(f'data-background-color="{escape(bg["color"])}"')
    if "gradient" in bg:
        attrs.append(f'data-background-gradient="{escape(bg["gradient"])}"')
    if "image" in bg:
        img = bg["image"]
        if img.startswith(("http://", "https://")):
            attrs.append(f'data-background-image="{escape(img)}"')
        else:
            b64 = embed_image_base64(img)
            if b64:
                attrs.append(f'data-background-image="{b64}"')
    if "video" in bg:
        attrs.append(f'data-background-video="{escape(bg["video"])}"')
        attrs.append('data-background-video-muted')
    if "opacity" in bg:
        attrs.append(f'data-background-opacity="{bg["opacity"]}"')
    if "size" in bg:
        attrs.append(f'data-background-size="{escape(bg["size"])}"')
    if "position" in bg:
        attrs.append(f'data-background-position="{escape(bg["position"])}"')
    if "repeat" in bg:
        attrs.append(f'data-background-repeat="{escape(bg["repeat"])}"')
    return (" " + " ".join(attrs)) if attrs else ""


def render_slide(slide: dict, fragments: bool = True) -> str:
    """Render a single slide dict to a <section> HTML block.
    
    Per-slide transition: add "transition" key to slide dict.
    Fragment animations: bullets appear one-by-one when fragments=True.
    """
    slide_type = slide.get("type", "content")
    notes = slide.get("notes", "")
    notes_html = f'<aside class="notes">{escape(notes)}</aside>' if notes else ""
    bg = _bg_attrs(slide)
    
    # Per-slide transition override
    trans = slide.get("transition", "")
    trans_attr = f' data-transition="{escape(trans)}"' if trans else ""

    if slide_type == "title":
        title = escape(slide.get("title", ""))
        subtitle = escape(slide.get("subtitle", ""))
        sub_html = f"<h3>{subtitle}</h3>" if subtitle else ""
        return f'<section data-state="title-slide"{bg}{trans_attr}><h1>{title}</h1>{sub_html}{notes_html}</section>'

    if slide_type == "section":
        title = escape(slide.get("title", ""))
        return f'<section{bg}{trans_attr}><h2>{title}</h2>{notes_html}</section>'

    if slide_type == "content":
        title = escape(slide.get("title", ""))
        bullets = slide.get("bullets", [])
        text = slide.get("text", "")
        body = ""
        if bullets:
            frag_class = ' class="fragment"' if fragments else ""
            items = "".join(f"<li{frag_class}>{escape(b)}</li>" for b in bullets)
            body = f"<ul>{items}</ul>"
        elif text:
            body = f"<p>{escape(text)}</p>"
        return f"<section{bg}{trans_attr}><h3>{title}</h3>{body}{notes_html}</section>"

    if slide_type == "image":
        title = escape(slide.get("title", ""))
        image_path = slide.get("image_path", "")
        caption = escape(slide.get("caption", ""))
        src = embed_image_base64(image_path) if image_path else ""
        img_tag = f'<img src="{src}" alt="{caption}" style="max-height:60vh;">' if src else f"<p><em>{caption}</em></p>"
        cap_html = f"<p><small>{caption}</small></p>" if caption else ""
        return f"<section{bg}{trans_attr}><h3>{title}</h3>{img_tag}{cap_html}{notes_html}</section>"

    if slide_type == "quote":
        text = escape(slide.get("text", ""))
        author = escape(slide.get("author", ""))
        cite = f"<cite>— {author}</cite>" if author else ""
        return f"<section{bg}{trans_attr}><blockquote><p>{text}</p>{cite}</blockquote>{notes_html}</section>"

    if slide_type == "code":
        title = escape(slide.get("title", ""))
        lang = slide.get("language", "")
        code = escape(slide.get("code", ""))
        return f'<section{bg}{trans_attr}><h3>{title}</h3><pre><code data-trim data-noescape class="language-{lang}">{code}</code></pre>{notes_html}</section>'

    if slide_type == "table":
        title = escape(slide.get("title", ""))
        headers = slide.get("headers", [])
        rows = slide.get("rows", [])
        th = "".join(f"<th>{escape(h)}</th>" for h in headers)
        tr_list = []
        for row in rows:
            tds = "".join(f"<td>{escape(str(c))}</td>" for c in row)
            tr_list.append(f"<tr>{tds}</tr>")
        tbody = "".join(tr_list)
        return f"<section{bg}{trans_attr}><h3>{title}</h3><table><thead><tr>{th}</tr></thead><tbody>{tbody}</tbody></table>{notes_html}</section>"

    if slide_type == "closing":
        title = escape(slide.get("title", "Cảm ơn!"))
        subtitle = escape(slide.get("subtitle", ""))
        sub_html = f"<p>{subtitle}</p>" if subtitle else ""
        return f'<section data-state="closing-slide"{bg}{trans_attr}><h2>{title}</h2>{sub_html}{notes_html}</section>'

    # Fallback: treat as content
    return render_slide({**slide, "type": "content"}, fragments=fragments)


def generate_html(data: dict, style_name: str, global_background: Optional[str] = None,
                   transition: Optional[str] = None, fragments: bool = True,
                   show_notes_in_print: bool = False) -> str:
    """Generate complete reveal.js HTML from slide data and style.

    Args:
        data: Slide data dict with 'title', 'author', 'slides' keys.
        style_name: Name of the style from STYLES dict.
        global_background: Optional global background override. Can be:
            - color: "#1a365d"
            - gradient: "linear-gradient(135deg, #667eea, #764ba2)"
            - image URL: "https://example.com/bg.jpg"
        transition: Transition type (none, slide, fade, convex, concave, zoom).
                    Falls back to style default, then 'slide'.
        show_notes_in_print: If True, speaker notes are visible in print/PDF output.
        fragments: Enable fragment animations for bullet points (default: True).
    """
    style = STYLES.get(style_name, STYLES["corporate"])
    title = escape(data.get("title", "Presentation"))
    author = escape(data.get("author", ""))
    slides = data.get("slides", [])

    # Resolve transition: CLI flag > JSON data > style default > 'slide'
    effective_transition = (
        transition
        or data.get("transition")
        or style.get("default_transition", "slide")
    )
    if effective_transition not in TRANSITIONS:
        effective_transition = "slide"

    # Resolve fragments: CLI flag > JSON data > default True
    effective_fragments = data.get("fragments", fragments)

    slides_html = "\n        ".join(render_slide(s, fragments=effective_fragments) for s in slides)

    # Determine effective background for Reveal.initialize
    bg_color = style["background"]
    parallax_cfg = ""
    if global_background:
        if global_background.startswith(("linear-gradient", "radial-gradient")):
            bg_color = "transparent"
            # Gradient applied via CSS on .reveal
            parallax_cfg = ""
        elif global_background.startswith(("http://", "https://")):
            parallax_cfg = f"""
      parallaxBackgroundImage: '{global_background}',
      parallaxBackgroundSize: '2560px 1440px',"""
        else:
            bg_color = global_background

    global_bg_css = ""
    if global_background and global_background.startswith(("linear-gradient", "radial-gradient")):
        global_bg_css = f"""
      .reveal {{ background: {global_background}; }}
      .reveal .slide-background {{ background: transparent !important; }}"""

    custom_css = f"""
      .reveal {{
        font-family: {style['font_body']};
        color: {style['text_color']};
      }}
      .reveal h1, .reveal h2, .reveal h3 {{
        font-family: {style['font_heading']};
        color: {style['heading_color']};
        text-transform: none;
      }}
      .reveal a {{ color: {style['accent_color']}; text-decoration: none; }}
      .reveal a:hover {{ color: {style.get('link_hover', style['accent_color'])}; text-decoration: underline; }}
      .reveal blockquote {{
        border-left: 4px solid {style['accent_color']};
        padding: 0.5em 1em;
        font-style: italic;
        background: {style.get('blockquote_bg', 'rgba(0,0,0,0.03)')};
        border-radius: 4px;
      }}
      .reveal table {{
        border-collapse: collapse;
        margin: 0 auto;
      }}
      .reveal table th {{
        background: {style.get('table_header_bg', style['accent_color'])};
        color: #fff;
        padding: 0.5em 1em;
      }}
      .reveal table td {{
        border: 1px solid rgba(128,128,128,0.25);
        padding: 0.5em 1em;
      }}
      .reveal table tr:nth-child(even) td {{
        background: {style.get('table_stripe_bg', 'rgba(0,0,0,0.03)')};
      }}
      .reveal ul, .reveal ol {{
        text-align: left;
        display: block;
        margin-left: 1em;
      }}
      .reveal li {{
        margin-bottom: 0.4em;
        line-height: 1.5;
      }}
      .reveal pre {{
        width: 90%;
        font-size: 0.65em;
        background: {style.get('code_bg', '#f7fafc')};
        border-radius: 6px;
      }}
      .reveal code {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
      }}
      .reveal .slide-number {{
        color: {style['text_color']};
        font-size: 0.6em;
      }}
    """

    # showNotes: controls whether speaker notes appear in print/PDF
    show_notes_cfg = "true" if show_notes_in_print else "false"

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="author" content="{author}">
  <title>{title}</title>
  <link rel="stylesheet" href="{REVEALJS_CDN}/dist/reveal.css">
  <link rel="stylesheet" href="{REVEALJS_CDN}/dist/theme/{style['reveal_theme']}.css">
  <link rel="stylesheet" href="{REVEALJS_CDN}/plugin/highlight/monokai.css">
  <style>{custom_css}{global_bg_css}

      /* ── Print / PDF export styles (US-4.5.2) ─────────────── */
      @media print {{
        .reveal .slides section {{
          page-break-after: always;
          page-break-inside: avoid;
          min-height: 100vh;
          box-sizing: border-box;
          padding: 2em;
        }}
        .reveal .slides section .fragment {{
          opacity: 1 !important;
          visibility: visible !important;
        }}
        .reveal .slide-number,
        .reveal .controls,
        .reveal .progress {{
          display: none !important;
        }}
        .reveal {{
          overflow: visible !important;
        }}
        .reveal .slides {{
          position: static !important;
          width: 100% !important;
          height: auto !important;
          overflow: visible !important;
          transform: none !important;
        }}
        .reveal .slides section {{
          position: relative !important;
          width: 100% !important;
          height: auto !important;
          transform: none !important;
          left: 0 !important;
          top: 0 !important;
        }}
        aside.notes {{
          display: block !important;
          margin-top: 1.5em;
          padding: 0.8em 1em;
          border-top: 2px solid {style['accent_color']};
          font-size: 0.75em;
          color: {style.get('text_color', '#333')};
          font-style: italic;
          background: {style.get('blockquote_bg', 'rgba(0,0,0,0.03)')};
        }}
        aside.notes::before {{
          content: "Speaker Notes: ";
          font-weight: bold;
          font-style: normal;
        }}
      }}
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      {slides_html}
    </div>
  </div>
  <script src="{REVEALJS_CDN}/dist/reveal.js"></script>
  <script src="{REVEALJS_CDN}/plugin/notes/notes.js"></script>
  <script src="{REVEALJS_CDN}/plugin/highlight/highlight.js"></script>
  <script>
    Reveal.initialize({{
      hash: true,
      slideNumber: true,
      showNotes: {show_notes_cfg},
      transition: '{effective_transition}',
      backgroundColor: '{bg_color}',{parallax_cfg}
      plugins: [RevealNotes, RevealHighlight]
    }});
  </script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate reveal.js HTML presentation from JSON data")
    parser.add_argument("--input", required=True, help="Path to JSON file with slide data")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument("--style", choices=list(STYLES.keys()), default="corporate",
                        help="Presentation style (default: corporate)")
    parser.add_argument("--background", default=None,
                        help="Global background: color (#hex), gradient (linear-gradient(...)), or image URL")
    parser.add_argument("--transition", choices=TRANSITIONS, default=None,
                        help="Slide transition type (overrides style default)")
    parser.add_argument("--no-fragments", action="store_true",
                        help="Disable fragment animations (bullets appear all at once)")
    parser.add_argument("--print-notes", action="store_true",
                        help="Include speaker notes in print/PDF output")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_html(data, args.style, args.background,
                         transition=args.transition,
                         fragments=not args.no_fragments,
                         show_notes_in_print=args.print_notes)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = output_path.stat().st_size / 1024
    slide_count = len(data.get("slides", []))
    print(f"✅ Saved: {output_path} ({size_kb:.1f} KB, {slide_count} slides, style: {args.style})")


if __name__ == "__main__":
    main()
