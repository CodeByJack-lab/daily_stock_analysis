#!/usr/bin/env python3
"""Convert Simplified Chinese in strategies/ and apps/dsa-web/src/ to Traditional (s2twp).

Usage:
    python3 scripts/convert_simp_to_trad.py --dry-run    # preview only
    python3 scripts/convert_simp_to_trad.py              # write changes
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent

INCLUDE_GLOBS = [
    "strategies/*.yaml",
    "strategies/*.yml",
    "strategies/README.md",
]

WEB_SRC = ROOT / "apps" / "dsa-web" / "src"
WEB_EXCLUDE_DIRS = {"node_modules", "dist", "__tests__"}
WEB_EXTS = {".ts", ".tsx"}


def collect_files() -> list[Path]:
    files: list[Path] = []
    for pattern in INCLUDE_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))
    if WEB_SRC.exists():
        for dirpath, dirnames, filenames in os.walk(WEB_SRC):
            dirnames[:] = [d for d in dirnames if d not in WEB_EXCLUDE_DIRS]
            for name in filenames:
                if Path(name).suffix in WEB_EXTS:
                    files.append(Path(dirpath) / name)
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="preview without writing")
    args = parser.parse_args()

    # s2hk = Simplified → Hong Kong Traditional (character-level only).
    # Avoid s2twp because its phrase table mis-translates financial terms
    # (e.g. 回調 → 回撥 changes "pullback" into "callback / refund").
    cc = OpenCC("s2hk")

    # Post-conversion fixes. Two categories:
    # (a) cosmetic — both forms are valid traditional; keep the original.
    # (b) semantic — OpenCC HK rule is contextually wrong; restore correct character.
    REVERT_PAIRS = {
        "拉昇": "拉升",   # (a) cosmetic
        "説": "說",       # (a) cosmetic
        "隻": "只",       # (b) "only" misconverted to animal measure word
    }

    def _post_process(text: str) -> str:
        for new, keep in REVERT_PAIRS.items():
            text = text.replace(new, keep)
        return text

    files = collect_files()
    changed = 0
    total_diff_chars = 0
    samples: list[str] = []

    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"skip {path}: {exc}", file=sys.stderr)
            continue
        converted = _post_process(cc.convert(original))
        if converted == original:
            continue
        changed += 1
        diff_chars = sum(1 for a, b in zip(original, converted) if a != b)
        total_diff_chars += diff_chars
        rel = path.relative_to(ROOT)
        if args.dry_run and len(samples) < 5:
            samples.append(f"\n--- {rel} ({diff_chars} chars changed) ---")
            for orig_line, new_line in zip(original.splitlines(), converted.splitlines()):
                if orig_line != new_line:
                    samples.append(f"- {orig_line}")
                    samples.append(f"+ {new_line}")
                    if len(samples) > 30:
                        break
        if not args.dry_run:
            path.write_text(converted, encoding="utf-8")

    print(f"Scanned {len(files)} files, would change {changed} files")
    print(f"Total character substitutions: {total_diff_chars}")
    if args.dry_run and samples:
        print("\n=== Sample diff (first ~30 lines from up to 5 files) ===")
        print("\n".join(samples))
    if args.dry_run:
        print("\n(dry-run — no files written; rerun without --dry-run to apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
