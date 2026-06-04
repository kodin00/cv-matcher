#!/usr/bin/env python3
import csv
import uuid
import sys
import time
from pathlib import Path
from typing import Optional

import requests

INPUT_CSV = Path(__file__).parent.parent.parent.parent / "Downloads" / "pairs_job_candidate.csv"
OUTPUT_CSV = Path(__file__).parent / "output" / "results.csv"
API_URL = "http://localhost:4000/api/match"
TIMEOUT = 120
MAX_RETRIES = 3
RETRY_DELAY = 3  # seconds between retries

HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "http://localhost:4000",
    "Referer": "http://localhost:4000/",
}

OUTPUT_FIELDS = ["jd_id", "candidate_name", "semantic_score", "keyword_score", "cv_text"]


def call_api(row: dict) -> Optional[dict]:
    payload = {
        "job_id": row["job_id"],
        "candidate_id": str(uuid.uuid4()),
        "candidate_name": row["candidate_name"],
        "cv_text": row["cv_text"],
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            sc = data.get("score_comparison", {})
            return {
                "jd_id": row["job_id"],
                "candidate_name": row["candidate_name"],
                "semantic_score": sc.get("semantic_score", ""),
                "keyword_score": sc.get("keyword_score", ""),
                "cv_text": row["cv_text"],
            }
        except Exception as exc:
            if attempt < MAX_RETRIES:
                print(f"  RETRY {attempt}/{MAX_RETRIES} {row['job_id']} / {row['candidate_name']}: {exc}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
            else:
                print(f"  FAILED {row['job_id']} / {row['candidate_name']}: {exc}", file=sys.stderr)
    return None


def main():
    rows = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    print(f"Loaded {len(rows)} rows. Hitting {API_URL} sequentially ...")
    start = time.time()

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    success = 0

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()

        for i, row in enumerate(rows, 1):
            result = call_api(row)
            if result:
                writer.writerow(result)
                out_f.flush()
                success += 1
            if i % 25 == 0 or i == len(rows):
                elapsed = time.time() - start
                avg = elapsed / i
                eta = avg * (len(rows) - i)
                print(f"  {i}/{len(rows)} done | {elapsed:.0f}s elapsed | ETA {eta:.0f}s")

    print(f"\nDone. {success}/{len(rows)} succeeded. Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
