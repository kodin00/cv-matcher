"""
Comparative evaluation script — base model vs fine-tuned model.

Runs both models against the same labeled dataset and prints a side-by-side
Precision / Recall / F1 table. Use this for the thesis Bab IV comparison.

Usage (run from the backend/ directory):
    python compare.py --dataset ../data/val_pairs.csv

The dataset file must have columns: cv_text, jd_text, label
  label: continuous float in [0.0, 1.0]; values >= 0.5 are treated as Relevant.

Environment variables (read from backend/.env or passed inline):
  MODEL_NAME   — base model name or path  (default: paraphrase-multilingual-MiniLM-L12-v2)
  FINETUNED    — fine-tuned model path     (default: ../models/finetuned)

Example:
    python compare.py --dataset ../data/val_pairs.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

# Similarity threshold for predicting "Relevant" (cosine is 0–1 range)
COSINE_THRESHOLD = 0.5
# Label binarisation threshold
LABEL_THRESHOLD  = 0.5


def _load_pairs(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return [
            {
                "cv_text": row["cv_text"],
                "jd_text": row["jd_text"],
                "label":   1 if float(row["label"]) >= LABEL_THRESHOLD else 0,
            }
            for row in csv.DictReader(f)
        ]


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return round(p, 4), round(r, 4), round(f, 4)


def _evaluate_semantic(pairs: list[dict], model_name: str) -> tuple[float, float, float]:
    """Encode all texts, compute cosine similarity, threshold → P/R/F1."""
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    print(f"  Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    cv_texts = [p["cv_text"] for p in pairs]
    jd_texts = [p["jd_text"] for p in pairs]
    labels   = [p["label"]   for p in pairs]

    print(f"  Encoding {len(pairs)} pairs …")
    cv_embs = model.encode(cv_texts, batch_size=16, show_progress_bar=False)
    jd_embs = model.encode(jd_texts, batch_size=16, show_progress_bar=False)

    tp = fp = fn = 0
    for cv_e, jd_e, label in zip(cv_embs, jd_embs, labels):
        sim = float(cosine_similarity([cv_e], [jd_e])[0][0])
        pred = 1 if sim >= COSINE_THRESHOLD else 0
        if pred == 1 and label == 1:
            tp += 1
        elif pred == 1 and label == 0:
            fp += 1
        elif pred == 0 and label == 1:
            fn += 1

    return _prf(tp, fp, fn)


def _evaluate_tfidf(pairs: list[dict]) -> tuple[float, float, float]:
    """TF-IDF cosine similarity baseline (matches baseline_service logic)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    tp = fp = fn = 0
    for p in pairs:
        vec = TfidfVectorizer().fit([p["cv_text"], p["jd_text"]])
        tfs = vec.transform([p["cv_text"], p["jd_text"]])
        sim = float(cosine_similarity(tfs[0], tfs[1])[0][0])
        pred  = 1 if sim >= COSINE_THRESHOLD else 0
        label = p["label"]
        if pred == 1 and label == 1:
            tp += 1
        elif pred == 1 and label == 0:
            fp += 1
        elif pred == 0 and label == 1:
            fn += 1

    return _prf(tp, fp, fn)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare base vs fine-tuned model.")
    parser.add_argument("--dataset",   default="../data/val_pairs.csv",
                        help="Labeled CSV with cv_text, jd_text, label columns")
    parser.add_argument("--base",      default=os.getenv("MODEL_NAME",
                        "paraphrase-multilingual-MiniLM-L12-v2"),
                        help="Base model name or HF Hub ID")
    parser.add_argument("--finetuned", default=os.getenv("FINETUNED",
                        "../models/finetuned"),
                        help="Path to fine-tuned model directory")
    args = parser.parse_args()

    pairs = _load_pairs(args.dataset)
    total = len(pairs)
    pos   = sum(p["label"] for p in pairs)
    print(f"\nDataset : {args.dataset}")
    print(f"Pairs   : {total}  (relevant={pos}, not-relevant={total - pos})")
    print(f"Threshold (cosine ≥ {COSINE_THRESHOLD} → Relevant)\n")

    # ── TF-IDF baseline (model-independent) ──────────────────────────────────
    print("[ TF-IDF Baseline ]")
    tp, tr, tf = _evaluate_tfidf(pairs)
    print(f"  Precision={tp:.4f}  Recall={tr:.4f}  F1={tf:.4f}\n")

    # ── Base semantic model ───────────────────────────────────────────────────
    print(f"[ Semantic — Base Model: {args.base} ]")
    bp, br, bf = _evaluate_semantic(pairs, args.base)
    print(f"  Precision={bp:.4f}  Recall={br:.4f}  F1={bf:.4f}\n")

    # ── Fine-tuned model ──────────────────────────────────────────────────────
    print(f"[ Semantic — Fine-Tuned: {args.finetuned} ]")
    fp_, fr, ff = _evaluate_semantic(pairs, args.finetuned)
    print(f"  Precision={fp_:.4f}  Recall={fr:.4f}  F1={ff:.4f}\n")

    # ── Summary table ─────────────────────────────────────────────────────────
    print("=" * 62)
    print(f"{'Model':<32} {'Precision':>9} {'Recall':>7} {'F1':>7}")
    print("-" * 62)
    print(f"{'TF-IDF Baseline':<32} {tp:>9.4f} {tr:>7.4f} {tf:>7.4f}")
    print(f"{'Semantic (Base)':<32} {bp:>9.4f} {br:>7.4f} {bf:>7.4f}")
    print(f"{'Semantic (Fine-Tuned)':<32} {fp_:>9.4f} {fr:>7.4f} {ff:>7.4f}")
    print("=" * 62)


if __name__ == "__main__":
    main()
