"""
llm_cleaner.py
--------------
Uses Groq API (Llama 3.1) to clean messy customer records.
Reads from data/raw/customers.csv → writes to data/cleaned/customers_cleaned.csv
"""

import os
import csv
import json
import time
import logging
from groq import Groq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a data cleaning assistant.
Given a dirty customer record, return a cleaned version as JSON.

Rules:
- Proper case for first_name and last_name (e.g. "john" → "John")
- Remove all leading/trailing spaces from every field
- Lowercase and validate email (mark as "invalid@unknown.com" if broken)
- Normalize phone to format: (XXX) XXX-XXXX. If ungrouped digits, format them.
- Proper case for street and city
- Uppercase state abbreviation (2 letters)
- Zip should be 5 digits only, strip spaces. If missing or invalid use "00000"

Return ONLY a valid JSON object, no explanation, no markdown."""


def clean_record(record: dict, retries: int = 3) -> dict:
    """
    Send a single customer record to Groq LLM for cleaning.
    Retries up to 3 times on failure before returning original record.
    """
    prompt = f"Clean this customer record:\n{json.dumps(record)}"

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
            )

            raw = response.choices[0].message.content.strip()

            # Strip markdown fences if model wraps in ```json
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            return json.loads(raw.strip())

        except Exception as e:
            logger.warning(f"Attempt {attempt}/{retries} failed for record {record['id']}: {e}")
            if attempt < retries:
                time.sleep(1 * attempt)  # exponential backoff
            else:
                logger.error(f"All retries failed for record {record['id']}, keeping original")
                return record


def clean_all(input_path: str, output_path: str) -> dict:
    """
    Clean all records in a CSV file using LLM.
    Returns a metrics dict with before/after statistics.
    """
    logger.info(f"Reading raw data from {input_path}")
    with open(input_path, newline="") as f:
        raw_rows = list(csv.DictReader(f))

    total = len(raw_rows)
    logger.info(f"Found {total} records to clean")

    cleaned_rows = []
    failed = 0

    for i, row in enumerate(raw_rows):
        logger.info(f"Cleaning record {i+1}/{total} — {row['first_name'].strip()} {row['last_name'].strip()}")
        cleaned = clean_record(row)

        # Track if record was actually changed
        if cleaned == row:
            failed += 1

        cleaned_rows.append(cleaned)
        time.sleep(0.3)  # rate limit protection

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="