"""
Fine-tuning script for the CV-JD semantic matching model.

Usage (run from the backend/ directory):
    python train.py --train ../data/train_pairs.csv --val ../data/val_pairs.csv

Optional arguments:
    --output  Path to save the best model (default: ../models/finetuned)
    --epochs  Number of training epochs            (default: 4)
    --batch   Training batch size                  (default: 16)

The script uses CosineSimilarityLoss with continuous labels in [0.0, 1.0].
Pearson/Spearman correlation on the validation set is reported after every
evaluation_steps batches, and the best checkpoint is saved automatically.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

# Allow `from config import MODEL_NAME` when run from backend/
sys.path.insert(0, os.path.dirname(__file__))


def load_pairs(path: str):
    """Load (cv_text, jd_text, label) triples from a CSV file."""
    from sentence_transformers import InputExample

    examples = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            examples.append(
                InputExample(
                    texts=[row["cv_text"], row["jd_text"]],
                    label=float(row["label"]),
                )
            )
    return examples


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune the CV-JD embedding model.")
    parser.add_argument("--train",  required=True,              help="Path to train_pairs.csv")
    parser.add_argument("--val",    required=True,              help="Path to val_pairs.csv")
    parser.add_argument("--output", default="../models/finetuned", help="Directory to save the best model")
    parser.add_argument("--epochs", type=int, default=4,        help="Number of training epochs")
    parser.add_argument("--batch",  type=int, default=16,       help="Training batch size")
    args = parser.parse_args()

    from sentence_transformers import SentenceTransformer, losses, evaluation
    from torch.utils.data import DataLoader
    from config import MODEL_NAME

    print(f"Loading base model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Loading training pairs from: {args.train}")
    train_examples = load_pairs(args.train)

    print(f"Loading validation pairs from: {args.val}")
    val_examples = load_pairs(args.val)

    print(f"Train: {len(train_examples)} pairs  |  Val: {len(val_examples)} pairs")

    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=args.batch)
    train_loss = losses.CosineSimilarityLoss(model)

    # Reports Pearson & Spearman correlation against val labels after each eval step
    val_evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(
        val_examples, name="val"
    )

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        evaluator=val_evaluator,
        epochs=args.epochs,
        evaluation_steps=50,
        output_path=args.output,
        save_best_model=True,
        show_progress_bar=True,
    )

    print(f"\nBest model saved to: {args.output}")


if __name__ == "__main__":
    main()
