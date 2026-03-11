import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.generate_report import is_valid_email, is_valid_zip, is_proper_case


def test_valid_emails():
    assert is_valid_email("john.smith@gmail.com") == True
    assert is_valid_email("INVALID_EMAIL") == False
    assert is_valid_email("user@") == False
    assert is_valid_email("invalid@unknown.com") == False
    assert is_valid_email("user@GMAIL.COM") == True
    print("✅ test_valid_emails passed")


def test_valid_zips():
    assert is_valid_zip("10001") == True
    assert is_valid_zip("00000") == False
    assert is_valid_zip("  77001") == False
    assert is_valid_zip("ABCDE") == False
    assert is_valid_zip("") == False
    print("✅ test_valid_zips passed")


def test_proper_case():
    assert is_proper_case("John") == True
    assert is_proper_case("JOHN") == False
    assert is_proper_case("john") == False
    assert is_proper_case("John Smith") == True
    print("✅ test_proper_case passed")


def test_raw_data_is_dirty():
    """Confirm the raw data actually has quality issues to clean."""
    import csv
    raw_path = "data/raw/customers.csv"
    if not os.path.exists(raw_path):
        print("⚠️  Skipping test_raw_data_is_dirty — no raw data found, run generate_data.py first")
        return
    with open(raw_path) as f:
        rows = list(csv.DictReader(f))
    invalid_emails = sum(1 for r in rows if not is_valid_email(r["email"]))
    assert invalid_emails > 0, "Expected some invalid emails in raw data!"
    print(f"✅ test_raw_data_is_dirty passed — found {invalid_emails} invalid emails in raw data")


if __name__ == "__main__":
    print("\nRunning tests...\n")
    test_valid_emails()
    test_valid_zips()
    test_proper_case()
    test_raw_data_is_dirty()
    print("\n✅ All tests passed!\n")