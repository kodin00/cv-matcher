"""
Fine-tuning script for the CV-JD semantic matching model.
Uses the sentence-transformers v3+ SentenceTransformerTrainer API.

Usage (run from the backend/ directory):

    # With validation split (saves best checkpoint by eval loss):
    python train.py --train ../data/train_pairs.csv --val ../data/val_pairs.csv

    # Full dataset, no validation split (saves final epoch):
    python train.py --train ../data/all_pairs.csv

Optional arguments:
    --val     Path to val_pairs.csv (omit to train on full dataset)
    --output  Path to save the model  (default: ../models/finetuned)
    --epochs  Number of training epochs (default: 4)
    --batch   Training batch size       (default: 16)

The script uses CosineSimilarityLoss with continuous labels in [0.0, 1.0].
When --val is provided, eval loss is reported each epoch and the best
checkpoint is saved automatically. When --val is omitted, the final
epoch model is saved.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))


def load_pairs_as_dataset(path: str):
    """Load a CV-JD pairs CSV into a HuggingFace Dataset with sentence1/sentence2/label columns."""
    from datasets import Dataset

    rows = {"sentence1": [], "sentence2": [], "label": []}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows["sentence1"].append(row["cv_text"])
            rows["sentence2"].append(row["jd_text"])
            rows["label"].append(float(row["label"]))
    return Dataset.from_dict(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune the CV-JD embedding model.")
    parser.add_argument("--train",  required=True,                 help="Path to train CSV (cv_text, jd_text, label)")
    parser.add_argument("--val",    default=None,                  help="Path to val CSV (omit for full-dataset mode)")
    parser.add_argument("--output", default="../models/finetuned", help="Directory to save the model")
    parser.add_argument("--epochs", type=int, default=4,           help="Number of training epochs")
    parser.add_argument("--batch",  type=int, default=16,          help="Training batch size")
    args = parser.parse_args()

    from sentence_transformers import SentenceTransformer
    from sentence_transformers.sentence_transformer.losses import CosineSimilarityLoss
    from sentence_transformers.sentence_transformer.trainer import SentenceTransformerTrainer
    from sentence_transformers.sentence_transformer.training_args import SentenceTransformerTrainingArguments
    from config import MODEL_NAME

    print(f"Loading base model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Loading training pairs from: {args.train}")
    train_dataset = load_pairs_as_dataset(args.train)

    val_dataset = None
    if args.val:
        print(f"Loading validation pairs from: {args.val}")
        val_dataset = load_pairs_as_dataset(args.val)
        print(f"Train: {len(train_dataset)} pairs  |  Val: {len(val_dataset)} pairs")
    else:
        print(f"Train: {len(train_dataset)} pairs  |  Val: none (full-dataset mode)")

    loss = CosineSimilarityLoss(model)

    # Steps per epoch for logging/saving cadence
    steps_per_epoch = max(1, len(train_dataset) // args.batch)

    training_args = SentenceTransformerTrainingArguments(
        output_dir=args.output,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch,
        warmup_ratio=0.1,
        # Evaluate and save once per epoch (or never if no val)
        eval_strategy="epoch" if val_dataset else "no",
        save_strategy="epoch" if val_dataset else "no",
        load_best_model_at_end=bool(val_dataset),
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        logging_steps=steps_per_epoch,
        fp16=False,
        bf16=False,
        dataloader_num_workers=0,
    )

    trainer = SentenceTransformerTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        loss=loss,
    )

    print(f"\nStarting training ({args.epochs} epochs, batch {args.batch})...")
    trainer.train()

    # Save the final model (Trainer saves best-by-eval when val is provided;
    # for full-dataset mode we save manually here)
    model.save_pretrained(args.output)
    print(f"\nModel saved to: {args.output}")


if __name__ == "__main__":
    main()
