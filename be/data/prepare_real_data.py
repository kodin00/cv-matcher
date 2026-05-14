#!/usr/bin/env python3
"""
Convert the human-annotated CV-JD pairs into train_pairs.csv and val_pairs.csv.

Source:
    tmp/anotasi final dokumentasi.xlsx - annotations.csv

Label:
    mean(a1_aggregate, a2_aggregate, a3_aggregate) as a float in [0.0, 1.0].
    Aggregates use a comma as the decimal separator — this is handled automatically.

Split:
    Stratified 80/20 by consensus_label (Cocok / Tidak Cocok), seed=42.

Output:
    data/train_pairs.csv       — 80% (~240 rows)  cv_text, jd_text, label
    data/val_pairs.csv         — 20% (~60 rows)   cv_text, jd_text, label
    data/train_pairs_index.csv — pair_id, cv_id, jd_id, label
    data/val_pairs_index.csv   — pair_id, cv_id, jd_id, label

Run from project root:
    python data/prepare_real_data.py
"""

import csv
import random
from pathlib import Path

SEED = 42
ANNOTATIONS = Path("tmp/anotasi final dokumentasi.xlsx - annotations.csv")
CV_TEXTS    = Path("tmp/cv_texts.csv")
JD_TEXTS    = Path("tmp/jd_texts.csv")
OUT_DIR     = Path("data")


def parse_agg(value: str) -> float | None:
    """Parse a comma-decimal aggregate string like '0,45' → 0.45."""
    s = value.strip().replace(",", ".")
    return float(s) if s else None


def load_lookup(path: Path, id_col: str, text_col: str) -> dict[str, str]:
    with open(path, newline="", encoding="utf-8") as f:
        return {row[id_col]: row[text_col] for row in csv.DictReader(f)}


def main() -> None:
    cv_texts = load_lookup(CV_TEXTS, "cv_id", "raw_text")
    jd_texts = load_lookup(JD_TEXTS, "jd_id", "raw_text")

    rows_cocok: list[dict] = []
    rows_tidak: list[dict] = []
    skipped = 0

    with open(ANNOTATIONS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cv_id   = row["cv_id"].strip()
            jd_id   = row["jd_id"].strip()
            label_s = row["consensus_label"].strip()

            if not cv_id or not jd_id or label_s not in ("Cocok", "Tidak Cocok"):
                skipped += 1
                continue

            if cv_id not in cv_texts:
                print(f"  WARNING: {cv_id} not in cv_texts.csv – skipping {row['pair_id']}")
                skipped += 1
                continue
            if jd_id not in jd_texts:
                print(f"  WARNING: {jd_id} not in jd_texts.csv – skipping {row['pair_id']}")
                skipped += 1
                continue

            # Continuous label: mean of available annotator aggregates
            agg_vals = [parse_agg(row[f"a{i}_aggregate"]) for i in [1, 2, 3]]
            agg_vals = [v for v in agg_vals if v is not None]
            label = round(sum(agg_vals) / len(agg_vals), 6) if agg_vals else (1.0 if label_s == "Cocok" else 0.0)

            entry = {
                "cv_text":  cv_texts[cv_id],
                "jd_text":  jd_texts[jd_id],
                "label":    label,
                "_pair_id": row["pair_id"],
                "_cv_id":   cv_id,
                "_jd_id":   jd_id,
            }
            if label_s == "Cocok":
                rows_cocok.append(entry)
            else:
                rows_tidak.append(entry)

    rng = random.Random(SEED)
    rng.shuffle(rows_cocok)
    rng.shuffle(rows_tidak)

    # Stratified 80/20 split
    def split80(lst: list) -> tuple[list, list]:
        n = int(len(lst) * 0.8)
        return lst[:n], lst[n:]

    train_cocok, val_cocok = split80(rows_cocok)
    train_tidak, val_tidak = split80(rows_tidak)

    train_rows = train_cocok + train_tidak
    val_rows   = val_cocok   + val_tidak

    rng.shuffle(train_rows)
    rng.shuffle(val_rows)

    # Write output
    text_fields  = ["cv_text", "jd_text", "label"]
    index_fields = ["_pair_id", "_cv_id", "_jd_id", "label"]

    def write(path: Path, data: list[dict], fields: list[str]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(data)

    OUT_DIR.mkdir(exist_ok=True)
    write(OUT_DIR / "train_pairs.csv",       train_rows, text_fields)
    write(OUT_DIR / "val_pairs.csv",         val_rows,   text_fields)
    write(OUT_DIR / "train_pairs_index.csv", train_rows, index_fields)
    write(OUT_DIR / "val_pairs_index.csv",   val_rows,   index_fields)

    total = len(train_rows) + len(val_rows)
    print(f"\nSource rows : {total + skipped}  (skipped {skipped})")
    print(f"Usable pairs: {total}")
    print(f"  Train : {len(train_rows)}  (Cocok={len(train_cocok)}, Tidak={len(train_tidak)})")
    print(f"  Val   : {len(val_rows)}   (Cocok={len(val_cocok)}, Tidak={len(val_tidak)})")
    print(f"\nLabel stats (train):")
    labels = [r["label"] for r in train_rows]
    print(f"  min={min(labels):.3f}  max={max(labels):.3f}  mean={sum(labels)/len(labels):.3f}")
    print(f"\nFiles written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
