#!/usr/bin/env python3
"""Generate professional charts from JSON data.

Usage:
    python3 gen_chart.py --input data.json --output chart.png --type bar
    python3 gen_chart.py --input data.json --output chart.png --type line --title "Revenue Trend"

JSON Input Format:
    {
        "title": "Chart Title",
        "x_label": "X Axis",
        "y_label": "Y Axis",
        "type": "bar",          // override --type flag
        "data": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "series": {
                "Revenue": [100, 150, 200, 180],
                "Cost":    [80,  90,  110, 100]
            }
        }
    }

    For scatter:
        "data": { "x": [1, 2, 3], "y": [4, 5, 6], "label": "Series" }

    For pie:
        "data": { "labels": ["A", "B", "C"], "values": [30, 50, 20] }

    For radar:
        "data": { "categories": ["Speed", "Power"], "series": { "Team A": [8, 7] } }
"""

import matplotlib
matplotlib.use('Agg')  # MUST be before any other matplotlib import

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Professional color palette ────────────────────────────────────────────────
PALETTE = [
    '#2563EB',  # Blue
    '#DC2626',  # Red
    '#059669',  # Green
    '#D97706',  # Amber
    '#7C3AED',  # Purple
    '#DB2777',  # Pink
    '#0891B2',  # Cyan
    '#65A30D',  # Lime
]
GRID_COLOR = '#E5E7EB'
TEXT_COLOR = '#1F2937'
BG_COLOR   = '#FFFFFF'

# ── Font setup for Vietnamese ──────────────────────────────────────────────────
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def _apply_base_style(ax):
    """Apply consistent base styling to any axes."""
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)


def chart_bar(data: dict, title: str, x_label: str, y_label: str) -> plt.Figure:
    labels = data['labels']
    series = data.get('series', {})

    # If only one series key named "values", treat as simple bar
    if not series and 'values' in data:
        series = {'': data['values']}

    n_series = len(series)
    x = np.arange(len(labels))
    width = 0.7 / max(n_series, 1)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    for i, (name, values) in enumerate(series.items()):
        offset = (i - n_series / 2 + 0.5) * width
        bars = ax.bar(x + offset, values, width=width * 0.9,
                      color=PALETTE[i % len(PALETTE)], label=name, edgecolor='white')
        # Value labels
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.01,
                    f'{val:,.0f}', ha='center', va='bottom', fontsize=9, color=TEXT_COLOR)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color=TEXT_COLOR)
    if x_label:
        ax.set_xlabel(x_label, fontsize=12, color=TEXT_COLOR)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12, color=TEXT_COLOR)
    if n_series > 1 or (n_series == 1 and list(series.keys())[0]):
        ax.legend(fontsize=10)
    ax.grid(axis='y', color=GRID_COLOR, linewidth=0.8)
    ax.grid(axis='x', visible=False)
    _apply_base_style(ax)
    fig.tight_layout()
    return fig


def chart_line(data: dict, title: str, x_label: str, y_label: str) -> plt.Figure:
    labels = data['labels']
    series = data.get('series', {})
    if not series and 'values' in data:
        series = {'': data['values']}

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    for i, (name, values) in enumerate(series.items()):
        ax.plot(labels, values, color=PALETTE[i % len(PALETTE)],
                linewidth=2.5, marker='o', markersize=5, label=name)

    ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color=TEXT_COLOR)
    if x_label:
        ax.set_xlabel(x_label, fontsize=12, color=TEXT_COLOR)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12, color=TEXT_COLOR)
    if len(series) > 1 or (len(series) == 1 and list(series.keys())[0]):
        ax.legend(fontsize=10)
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    _apply_base_style(ax)
    fig.tight_layout()
    return fig


def chart_pie(data: dict, title: str) -> plt.Figure:
    labels = data['labels']
    values = data['values']

    # Group small slices into "Khác" if more than 8
    if len(labels) > 8:
        sorted_pairs = sorted(zip(values, labels), reverse=True)
        top = sorted_pairs[:7]
        rest_val = sum(v for v, _ in sorted_pairs[7:])
        top_values = [v for v, _ in top]
        top_labels = [l for _, l in top]
        top_values.append(rest_val)
        top_labels.append('Khác')
        values, labels = top_values, top_labels

    colors = PALETTE[:len(labels)]
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(BG_COLOR)

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90, pctdistance=0.75,
        textprops={'fontsize': 11, 'color': TEXT_COLOR},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_color('white')

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color=TEXT_COLOR)
    fig.tight_layout()
    return fig


def chart_radar(data: dict, title: str) -> plt.Figure:
    categories = data['categories']
    series = data.get('series', {})
    if not series and 'values' in data:
        series = {'': data['values']}

    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    for i, (name, values) in enumerate(series.items()):
        vals_closed = list(values) + [values[0]]
        angles_closed = angles + [angles[0]]
        ax.fill(angles_closed, vals_closed, color=PALETTE[i % len(PALETTE)], alpha=0.20)
        ax.plot(angles_closed, vals_closed, color=PALETTE[i % len(PALETTE)],
                linewidth=2, label=name)

    ax.set_xticks(angles)
    ax.set_xticklabels(categories, fontsize=11, color=TEXT_COLOR)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color=TEXT_COLOR)
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    if len(series) > 1 or (len(series) == 1 and list(series.keys())[0]):
        ax.legend(fontsize=10, loc='upper right', bbox_to_anchor=(1.3, 1.1))
    fig.tight_layout()
    return fig


def chart_scatter(data: dict, title: str, x_label: str, y_label: str,
                  show_trend: bool = False) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Support multi-series scatter
    if 'series' in data:
        for i, (name, pts) in enumerate(data['series'].items()):
            xs = pts['x']
            ys = pts['y']
            ax.scatter(xs, ys, color=PALETTE[i % len(PALETTE)],
                       s=60, alpha=0.75, edgecolors='white', label=name)
    else:
        xs = data['x']
        ys = data['y']
        label = data.get('label', '')
        ax.scatter(xs, ys, color=PALETTE[0], s=60, alpha=0.75, edgecolors='white', label=label)

        if show_trend and len(xs) > 1:
            z = np.polyfit(xs, ys, 1)
            p = np.poly1d(z)
            x_sorted = sorted(xs)
            ax.plot(x_sorted, p(x_sorted), color=PALETTE[1],
                    linewidth=2, linestyle='--', label='Trend')

    ax.set_title(title, fontsize=16, fontweight='bold', pad=15, color=TEXT_COLOR)
    if x_label:
        ax.set_xlabel(x_label, fontsize=12, color=TEXT_COLOR)
    if y_label:
        ax.set_ylabel(y_label, fontsize=12, color=TEXT_COLOR)
    # Only show legend if there are named series
    handles, lbls = ax.get_legend_handles_labels()
    if any(l for l in lbls):
        ax.legend(fontsize=10)
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    _apply_base_style(ax)
    fig.tight_layout()
    return fig


CHART_BUILDERS = {
    'bar':     chart_bar,
    'line':    chart_line,
    'pie':     chart_pie,
    'radar':   chart_radar,
    'scatter': chart_scatter,
}


def generate_chart(data: dict, chart_type: str, output_path: Path) -> None:
    title   = data.get('title', '')
    x_label = data.get('x_label', '')
    y_label = data.get('y_label', '')
    chart_data = data.get('data', data)  # fallback: data IS the chart data

    # JSON can override chart_type
    effective_type = data.get('type', chart_type)

    if effective_type not in CHART_BUILDERS:
        print(f"Error: unsupported chart type '{effective_type}'. "
              f"Choose from: {', '.join(CHART_BUILDERS.keys())}", file=sys.stderr)
        sys.exit(1)

    builder = CHART_BUILDERS[effective_type]
    if effective_type == 'pie':
        fig = builder(chart_data, title)
    elif effective_type == 'radar':
        fig = builder(chart_data, title)
    elif effective_type == 'scatter':
        fig = builder(chart_data, title, x_label, y_label)
    else:
        fig = builder(chart_data, title, x_label, y_label)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(output_path), dpi=160, bbox_inches='tight',
                facecolor=BG_COLOR, edgecolor='none')
    plt.close(fig)

    size_kb = output_path.stat().st_size / 1024
    w_px = int(fig.get_figwidth() * 160)
    h_px = int(fig.get_figheight() * 160)
    print(f"✅ Saved: {output_path} ({size_kb:.1f} KB, {effective_type}, {w_px}×{h_px}px)")


def main():
    parser = argparse.ArgumentParser(description="Generate professional chart PNG from JSON data")
    parser.add_argument("--input",  required=True,
                        help="Path to JSON file with chart data")
    parser.add_argument("--output", required=True,
                        help="Output PNG file path")
    parser.add_argument("--type",   choices=list(CHART_BUILDERS.keys()), default="bar",
                        help="Chart type (default: bar). Can also be set in JSON 'type' key.")
    parser.add_argument("--title",  default=None,
                        help="Override chart title from JSON")
    parser.add_argument("--trend",  action="store_true",
                        help="Show trend line on scatter plots")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if args.title:
        data['title'] = args.title

    generate_chart(data, args.type, Path(args.output))


if __name__ == '__main__':
    main()
