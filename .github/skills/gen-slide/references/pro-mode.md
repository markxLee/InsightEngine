# Pro Mode — ppt-master SVG→PPTX Pipeline

Pro mode sử dụng ppt-master's multi-role pipeline để tạo bài thuyết trình chuyên nghiệp
với native DrawingML shapes — text, charts, icons là real PowerPoint objects, hoàn toàn
editable.

**ppt-master location**: `.github/skills/gen-slide/ppt-master/` (embedded trong repo này)

---

## Khi nào dùng Pro mode

- Source documents cần convert (PDF/DOCX/URL/EPUB → slides)
- Consulting-grade output (McKinsey, Google, academic styles)
- Cần visualizations phức tạp (50+ chart template types)
- Cần icon library (6700+ icons, 3 styles)
- Multi-format output (PPT 16:9, 4:3, Xiaohongshu, WeChat, Story)
- Speaker notes chuyên nghiệp với conversational narration

## So với Quick mode

| Feature | Quick (pptxgenjs) | Pro (ppt-master) |
|---------|-------------------|------------------|
| Output type | pptxgenjs objects | Native DrawingML shapes |
| Editability | Tốt | Xuất sắc (fully native) |
| Templates | 10 (light/dark) | 20+ (ngành-specific) |
| Charts | Cơ bản (bar/line/pie) | 50+ types (sankey, treemap, gantt...) |
| Icons | Không | 6700+ (3 libraries) |
| Source conversion | Không (cần thu-thap) | Built-in (PDF/DOCX/URL) |
| Speed | Nhanh | Chậm hơn (multi-step) |
| Pipeline integration | Tốt | Cần manual orchestration |

---

## Pipeline

```
Source → Project Init → Template → Strategist (8 Confirmations)
  → [Image Gen] → Executor (SVG pages) → Post-processing → Export PPTX
```

**Serial execution** — mỗi step phải hoàn thành trước khi chạy step tiếp.
**2 blocking gates**: Template Selection và Eight Confirmations.

---

## Step 1: Source Content

Nếu đã có content từ bien-soan, dùng trực tiếp. Nếu có source docs:

| Source | Command |
|--------|---------|
| PDF | `python3 .github/skills/gen-slide/ppt-master/scripts/source_to_md/pdf_to_md.py <file>` |
| DOCX | `python3 .github/skills/gen-slide/ppt-master/scripts/source_to_md/doc_to_md.py <file>` |
| PPTX | `python3 .github/skills/gen-slide/ppt-master/scripts/source_to_md/ppt_to_md.py <file>` |
| URL | `python3 .github/skills/gen-slide/ppt-master/scripts/source_to_md/web_to_md.py <URL>` |

## Step 2: Project Init

```bash
python3 .github/skills/gen-slide/ppt-master/scripts/project_manager.py init <name> --format ppt169
python3 .github/skills/gen-slide/ppt-master/scripts/project_manager.py import-sources <path> <files...> --move
```

## Step 3: Template Selection

```bash
cat .github/skills/gen-slide/ppt-master/templates/layouts/layouts_index.json
```

20+ layouts: McKinsey, Google Style, Academic Defense, AI Ops, Government (blue/red),
Medical University, Tech Blue, etc. Default: **free design** (AI tự thiết kế theo content).

## Step 4: Strategist Phase

```
read_file .github/skills/gen-slide/ppt-master/references/strategist.md
read_file .github/skills/gen-slide/ppt-master/templates/design_spec_reference.md
```

**Eight Confirmations** (trình bày gợi ý, chờ user confirm):
1. Canvas format  2. Số trang  3. Đối tượng  4. Style objective
5. Color scheme (HEX)  6. Icon approach  7. Typography  8. Image approach

Output: `<project_path>/design_spec.md`

## Step 5: Image Generation (Conditional)

```bash
python3 .github/skills/gen-slide/ppt-master/scripts/image_gen.py "prompt" --aspect_ratio 16:9 --image_size 1K -o <project_path>/images
```

## Step 6: Executor Phase

```
read_file .github/skills/gen-slide/ppt-master/references/executor-base.md
read_file .github/skills/gen-slide/ppt-master/references/executor-general.md  # hoặc consultant/consultant-top
```

**Rules**:
- SVG generation: main agent only (không delegate sub-agents)
- Generate tuần tự từng trang (không batch)
- Confirm design parameters trước trang đầu tiên

### Icons (6700+)

```xml
<use data-icon="chunk/home" x="100" y="200" width="48" height="48" fill="#005587"/>
```

| Library | Style | Count | Dùng khi |
|---------|-------|-------|----------|
| `chunk` | Fill, straight-line | 640 | **Default** |
| `tabler-filled` | Fill, smooth bezier | 1000+ | Rounded, organic feel |
| `tabler-outline` | Stroke/line art | 5000+ | Light, elegant |

Search: `ls .github/skills/gen-slide/ppt-master/templates/icons/chunk/ | grep <keyword>`

### Charts (50+)

```bash
cat .github/skills/gen-slide/ppt-master/templates/charts/charts_index.json
```

Bar, line, pie, radar, scatter, sankey, treemap, Gantt, fishbone, waterfall, funnel,
heatmap, SWOT, Porter's Five Forces, org chart, mind map, timeline, và nhiều hơn.

### SVG Constraints

**Cấm**: `mask`, `<style>`, `class`, `<foreignObject>`, `textPath`, `@font-face`,
`<animate*>`, `<script>`, `<iframe>`, `<symbol>`+`<use>`

Chi tiết: `.github/skills/gen-slide/ppt-master/references/shared-standards.md`

## Step 7: Post-processing & Export

Chạy **từng lệnh một** — không bao giờ batch:

```bash
# 7.1
python3 .github/skills/gen-slide/ppt-master/scripts/total_md_split.py <project_path>
# 7.2
python3 .github/skills/gen-slide/ppt-master/scripts/finalize_svg.py <project_path>
# 7.3
python3 .github/skills/gen-slide/ppt-master/scripts/svg_to_pptx.py <project_path> -s final
```

Output: `exports/<project_name>_<timestamp>.pptx`

---

## Thin Content Guard (áp dụng cả 2 modes)

Pro mode cũng phải kiểm tra content trước khi generate:
- **< 500 từ** cho multi-section presentation: REJECT
- **> 40% sections chỉ có 1 bullet/sentence**: REJECT
- **Không có data/examples/specifics**: REJECT
- Signal back: "❌ Content quá mỏng. Cần biên soạn lại ở mức comprehensive."

---

## Pipeline Integration

Khi gọi từ tong-hop pipeline:
- Default: **Pro mode** (mặc định cho mọi yêu cầu tạo slide)
- Chỉ dùng Quick mode khi user nói rõ "slide đơn giản", "quick", "nhanh", "prototype"
- Narrative Analysis (Step 2 trong Quick mode) vẫn áp dụng cho cả Pro mode's Strategist phase

---

## Canvas Format Quick Reference

| Format | viewBox | Use Case |
|--------|---------|----------|
| PPT 16:9 | `0 0 1280 720` | Standard |
| PPT 4:3 | `0 0 1024 768` | Legacy |
| Xiaohongshu | `0 0 1242 1660` | Social media |
| WeChat | `0 0 1080 1080` | Square |
| Story | `0 0 1080 1920` | Vertical |
