#!/usr/bin/env python3
"""
Output consistency check (Section 3.6.2).

Compares generated outputs from C2/C3/C4/C5 against C1 reference outputs.
Reports exact match, character-level diff stats, and minor/major classification.

Usage:
    python3 consistency_check.py \
        --reference /path/to/C1_results/outputs \
        --compare /path/to/C2_results/outputs \
        --output consistency_report.csv
"""

import argparse
import csv
import difflib
import os
import sys
from pathlib import Path


def load_outputs(output_dir: str) -> dict:
    """
    Load all generated text files from a results/outputs directory.
    Returns: { "model_id/prompt_id": text, ... }
    Averages across runs by taking the first non-warmup run found.
    """
    outputs = {}
    base = Path(output_dir)
    if not base.exists():
        print(f"ERROR: Directory not found: {output_dir}")
        sys.exit(1)

    for model_dir in sorted(base.iterdir()):
        if not model_dir.is_dir():
            continue
        model_id = model_dir.name
        for txt_file in sorted(model_dir.glob("*.txt")):
            # e.g., P01_run2.txt
            prompt_id = txt_file.stem.split("_run")[0]
            key = f"{model_id}/{prompt_id}"
            # Take the first (lowest run number) file found
            if key not in outputs:
                outputs[key] = txt_file.read_text(encoding="utf-8").strip()

    return outputs


def classify_divergence(ref_text: str, cmp_text: str) -> dict:
    """
    Compare two outputs and classify divergence.
    Returns: {
        exact_match: bool,
        similarity_ratio: float (0-1),
        classification: 'match' | 'minor' | 'major',
        char_diff_count: int,
        word_diff_count: int,
    }
    """
    if ref_text == cmp_text:
        return {
            "exact_match": True,
            "similarity_ratio": 1.0,
            "classification": "match",
            "char_diff_count": 0,
            "word_diff_count": 0,
        }

    # Character-level similarity
    sm = difflib.SequenceMatcher(None, ref_text, cmp_text)
    sim_ratio = sm.ratio()

    # Word-level diff
    ref_words = ref_text.split()
    cmp_words = cmp_text.split()
    word_diff = sum(1 for op, i1, i2, j1, j2
                    in difflib.SequenceMatcher(None, ref_words, cmp_words).get_opcodes()
                    if op != "equal")

    # Classification thresholds
    # > 0.95 similarity = minor (wording variation)
    # <= 0.95 similarity = major (semantically different)
    if sim_ratio > 0.95:
        classification = "minor"
    else:
        classification = "major"

    return {
        "exact_match": False,
        "similarity_ratio": round(sim_ratio, 4),
        "classification": classification,
        "char_diff_count": len(ref_text) + len(cmp_text) - 2 * int(sim_ratio * max(len(ref_text), len(cmp_text))),
        "word_diff_count": word_diff,
    }


def run_consistency_check(reference_dir: str, compare_dir: str, output_csv: str):
    """Run the full consistency check and save results."""

    ref_outputs = load_outputs(reference_dir)
    cmp_outputs = load_outputs(compare_dir)

    print(f"Reference outputs: {len(ref_outputs)} entries")
    print(f"Compare outputs:   {len(cmp_outputs)} entries")

    results = []
    exact_matches = 0
    minor_mismatches = 0
    major_mismatches = 0
    missing = 0

    for key in sorted(ref_outputs.keys()):
        model_id, prompt_id = key.split("/")

        if key not in cmp_outputs:
            results.append({
                "model_id": model_id,
                "prompt_id": prompt_id,
                "exact_match": False,
                "similarity_ratio": 0.0,
                "classification": "missing",
                "char_diff_count": -1,
                "word_diff_count": -1,
            })
            missing += 1
            continue

        comparison = classify_divergence(ref_outputs[key], cmp_outputs[key])
        comparison["model_id"] = model_id
        comparison["prompt_id"] = prompt_id
        results.append(comparison)

        if comparison["exact_match"]:
            exact_matches += 1
        elif comparison["classification"] == "minor":
            minor_mismatches += 1
        else:
            major_mismatches += 1

    # Write CSV
    fields = ["model_id", "prompt_id", "exact_match", "similarity_ratio",
              "classification", "char_diff_count", "word_diff_count"]
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    # Summary
    total = len(results)
    print(f"\n{'=' * 50}")
    print(f"  Consistency Check Summary")
    print(f"{'=' * 50}")
    print(f"  Total comparisons: {total}")
    print(f"  Exact matches:     {exact_matches} ({exact_matches/max(total,1)*100:.1f}%)")
    print(f"  Minor mismatches:  {minor_mismatches} ({minor_mismatches/max(total,1)*100:.1f}%)")
    print(f"  Major mismatches:  {major_mismatches} ({major_mismatches/max(total,1)*100:.1f}%)")
    print(f"  Missing outputs:   {missing}")
    print(f"\n  Report saved to: {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Output consistency check")
    parser.add_argument("--reference", required=True, help="Path to C1 reference outputs directory")
    parser.add_argument("--compare", required=True, help="Path to comparison outputs directory")
    parser.add_argument("--output", default="consistency_report.csv", help="Output CSV path")
    args = parser.parse_args()

    run_consistency_check(args.reference, args.compare, args.output)


if __name__ == "__main__":
    main()
