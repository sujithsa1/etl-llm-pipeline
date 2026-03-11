import os
import csv
import json
import time
from groq import Groq

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

def clean_record(record: dict) -> dict:
    prompt = f"Clean this customer record:\n{json.dumps(record)}"
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    
    raw = response.choices[0].message.content.strip()
    
    # Strip markdown if model wraps in ```json
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    cleaned = json.loads(raw.strip())
    return cleaned

def clean_all(input_path: str, output_path: str):
    with open(input_path, newline="") as f:
        readers = list(csv.DictReader(f))
    
    cleaned_rows = []
    total = len(readers)
    
    for i, row in enumerate(readers):
        print(f"  Cleaning record {i+1}/{total} — {row['first_name'].strip()} {row['last_name'].strip()}")
        try:
            cleaned = clean_record(row)
            cleaned_rows.append(cleaned)
        except Exception as e:
            print(f"  ⚠️  Failed on record {row['id']}: {e}")
            cleaned_rows.append(row)  # keep original if failed
        time.sleep(0.3)  # avoid rate limits
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_rows[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    print(f"\n✅ Cleaned {len(cleaned_rows)} records → {output_path}")

if __name__ == "__main__":
    clean_all("data/raw/customers.csv", "data/cleaned/customers_cleaned.csv")