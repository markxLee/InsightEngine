# Chart Code Templates — Full Reference

## Shared Config

```python
import matplotlib
matplotlib.use('Agg')  # MUST be before any other matplotlib import
import matplotlib.pyplot as plt
import numpy as np

PALETTE = ['#2563EB', '#DC2626', '#059669', '#D97706', '#7C3AED',
           '#DB2777', '#0891B2', '#65A30D']
BACKGROUND = '#FFFFFF'
GRID_COLOR = '#E5E7EB'
TEXT_COLOR = '#1F2937'

# Apply same palette ordering across related charts in a document
# Use PALETTE[i] for series i (0-based)
```

## Bar Chart

```python
fig, ax = plt.subplots(figsize=(10, 6))
colors = PALETTE[:len(categories)]
bars = ax.bar(categories, values, color=colors, width=0.6, edgecolor='white')

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
            f'{val:,.0f}', ha='center', va='bottom', fontsize=10)

ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel(y_label, fontsize=12)
ax.grid(axis='y', alpha=0.3, color=GRID_COLOR)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=160, bbox_inches='tight')
plt.close()
```

## Line Chart

```python
fig, ax = plt.subplots(figsize=(10, 6))
for i, (series_name, series_data) in enumerate(series.items()):
    ax.plot(x_values, series_data, color=PALETTE[i],
            linewidth=2, marker='o', markersize=5, label=series_name)

ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label, fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(alpha=0.3, color=GRID_COLOR)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=160, bbox_inches='tight')
plt.close()
```

## Pie Chart

```python
fig, ax = plt.subplots(figsize=(8, 8))
colors = PALETTE[:len(labels)]
wedges, texts, autotexts = ax.pie(
    values, labels=labels, colors=colors,
    autopct='%1.1f%%', startangle=90, pctdistance=0.75,
    textprops={'fontsize': 11}
)
for at in autotexts:
    at.set_fontsize(10)
    at.set_fontweight('bold')
ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(output_path, dpi=160, bbox_inches='tight')
plt.close()
# Note: group slices beyond 8 as "Khác" to avoid clutter
```

## Radar Chart

```python
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
values_closed = values + [values[0]]
angles_closed = angles + [angles[0]]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.fill(angles_closed, values_closed, color=PALETTE[0], alpha=0.25)
ax.plot(angles_closed, values_closed, color=PALETTE[0], linewidth=2)
ax.set_xticks(angles)
ax.set_xticklabels(categories, fontsize=11)
ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(output_path, dpi=160, bbox_inches='tight')
plt.close()
```

## Scatter Plot

```python
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x_values, y_values, color=PALETTE[0], s=60, alpha=0.7, edgecolors='white')

if show_trend:
    z = np.polyfit(x_values, y_values, 1)
    p = np.poly1d(z)
    ax.plot(sorted(x_values), p(sorted(x_values)),
            color=PALETTE[1], linewidth=2, linestyle='--', label='Trend')
    ax.legend()

ax.set_title(title, fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label, fontsize=12)
ax.grid(alpha=0.3, color=GRID_COLOR)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig(output_path, dpi=160, bbox_inches='tight')
plt.close()
```

## Seaborn Usage

```python
import seaborn as sns
sns.set_theme(style='whitegrid', palette=PALETTE)
# Use for: distributions (histplot, kdeplot, boxplot, violinplot),
#          heatmaps (sns.heatmap), regression (sns.regplot)
```

## Embed Charts in Documents

```yaml
EMBED_WORD:
  from docx.shared import Inches
  doc.add_picture(chart_path, width=Inches(6.0))

EMBED_PPTX: |
  slide.addImage({path: chartPath, x: 0.5, y: 1.5, w: 9.0, h: 5.0})

EMBED_HTML: |
  import base64
  with open(chart_path, 'rb') as f:
      b64 = base64.b64encode(f.read()).decode()
  img_tag = f'<img src="data:image/png;base64,{b64}" />'

CHAIN_OUTPUT:
  return {path: str, width_px: int, height_px: int, chart_type: str}
```
