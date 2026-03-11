import csv
import os

def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1] and "unknown" not in email

def is_valid_zip(zip_code):
    return zip_code.isdigit() and len(zip_code) == 5 and zip_code != "00000"

def is_proper_case(name):
    return name == name.title()

def generate_report(raw_path, cleaned_path):
    raw = load_csv(raw_path)
    cleaned = load_csv(cleaned_path)

    print("\n" + "="*55)
    print("       DATA QUALITY REPORT — ETL LLM PIPELINE")
    print("="*55)

    metrics = [
        ("Valid emails",
            sum(1 for r in raw if is_valid_email(r["email"])),
            sum(1 for r in cleaned if is_valid_email(r["email"]))),
        ("Valid zip codes",
            sum(1 for r in raw if is_valid_zip(r["zip"].strip())),
            sum(1 for r in cleaned if is_valid_zip(r["zip"].strip()))),
        ("Proper case names",
            sum(1 for r in raw if is_proper_case(r["first_name"].strip())),
            sum(1 for r in cleaned if is_proper_case(r["first_name"].strip()))),
        ("No whitespace in fields",
            sum(1 for r in raw if r["first_name"] == r["first_name"].strip()),
            sum(1 for r in cleaned if r["first_name"] == r["first_name"].strip())),
    ]

    total = len(raw)
    print(f"\n{'Metric':<25} {'Before':>8} {'After':>8} {'Improvement':>12}")
    print("-"*55)
    for label, before, after in metrics:
        improvement = after - before
        sign = "+" if improvement >= 0 else ""
        print(f"{label:<25} {before:>6}/{total} {after:>6}/{total} {sign}{improvement:>+10}")

    print("="*55)
    print(f"Total records processed: {total}")
    print("="*55 + "\n")

if __name__ == "__main__":
    generate_report("data/raw/customers.csv", "data/cleaned/customers_cleaned.csv")