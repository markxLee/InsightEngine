#!/usr/bin/env python3
"""Detect duplicate and near-duplicate paragraphs in Markdown content.

Usage:
    python3 deduplicate.py --input content.md
    python3 deduplicate.py --input content.md --threshold 0.8 --output report.json

Compares all paragraph pairs using word-level Jaccard similarity.
Reports pairs above the threshold (default 0.75) as potential duplicates.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_paragraphs(text: str) -> list[dict]:
    """Split Markdown text into paragraphs, ignoring headings and short lines."""
    paragraphs = []
    current = []
    for line in text.split("\n"):
        stripped = line.strip()
        # Skip headings, horizontal rules, empty lines as separators
        if stripped.startswith("#") or stripped == "---" or stripped == "":
            if current:
                para_text = " ".join(current)
                if len(para_text.split()) >= 5:  # Skip very short fragments
                    paragraphs.append({"text": para_text, "line_start": len(paragraphs) + 1})
                current = []
        else:
            current.append(stripped)
    if current:
        para_text = " ".join(current)
        if len(para_text.split()) >= 5:
            paragraphs.append({"text": para_text, "line_start": len(paragraphs) + 1})
    return paragraphs


def normalize(text: str) -> set[str]:
    """Normalize text to a set of lowercase words for comparison."""
    words = re.findall(r"\w+", text.lower())
    return set(words)


def jaccard_similarity(a: set, b: set) -> float:
    """Compute Jaccard similarity between two word sets."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_duplicates(paragraphs: list[dict], threshold: float) -> list[dict]:
    """Find duplicate/near-duplicate paragraph pairs above threshold."""
    word_sets = [normalize(p["text"]) for p in paragraphs]
    duplicates = []

    for i in range(len(paragraphs)):
        for j in range(i + 1, len(paragraphs)):
            sim = jaccard_similarity(word_sets[i], word_sets[j])
            if sim >= threshold:
                duplicates.append({
                    "paragraph_a": i + 1,
                    "paragraph_b": j + 1,
                    "similarity": round(sim, 3),
                    "preview_a": paragraphs[i]["text"][:100] + ("..." if len(paragraphs[i]["text"]) > 100 else ""),
                    "preview_b": paragraphs[j]["text"][:100] + ("..." if len(paragraphs[j]["text"]) > 100 else ""),
                })

    duplicates.sort(key=lambda x: x["similarity"], reverse=True)
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Detect duplicate paragraphs in Markdown")
    parser.add_argument("--input", required=True, help="Input Markdown file")
    parser.add_argument("--threshold", type=float, default=0.75,
                        help="Similarity threshold (0-1, default 0.75)")
    parser.add_argument("--output", help="Output JSON report path (optional, prints to stdout if omitted)")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    paragraphs = extract_paragraphs(text)
    duplicates = find_duplicates(paragraphs, args.threshold)

    report = {
        "source": args.input,
        "total_paragraphs": len(paragraphs),
        "threshold": args.threshold,
        "duplicates_found": len(duplicates),
        "duplicates": duplicates,
    }

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ Dedup report: {args.output} ({len(paragraphs)} paragraphs, "
              f"{len(duplicates)} duplicate pairs found, threshold={args.threshold})")
    else:
        # Print summary to stdout
        print(f"📊 Duplicate Detection Report")
        print(f"   Source: {args.input}")
        print(f"   Paragraphs: {len(paragraphs)}")
        print(f"   Threshold: {args.threshold}")
        print(f"   Duplicates found: {len(duplicates)}")
        if duplicates:
            print(f"\n   Top duplicates:")
            for d in duplicates[:5]:
                print(f"   ¶{d['paragraph_a']} ↔ ¶{d['paragraph_b']} "
                      f"(similarity: {d['similarity']:.1%})")
                print(f"     A: {d['preview_a']}")
                print(f"     B: {d['preview_b']}")
                print()


if __name__ == "__main__":
    main()
