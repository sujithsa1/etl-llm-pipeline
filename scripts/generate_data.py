import csv
import random
import os

random.seed(42)

first_names = ["john","JANE","Mary ","  bob","alice","CHARLIE","diana","eve ","FRANK","grace"]
last_names = ["smith","JONES","williams ","  brown","davis","MILLER","wilson","moore ","TAYLOR","anderson"]
domains = ["gmail.com","yahoo.com","GMAIL.COM","hotmail.com","YAHOO.COM"]
streets = ["123 main st","456 ELM STREET","789 Oak Ave.","  321 Pine Rd","654 maple street"]
cities = ["new york","LOS ANGELES","Chicago ","  houston","PHOENIX"]
states = ["ny","ca","IL","tx","AZ"]

def random_phone():
    formats = [
        f"({random.randint(200,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
        f"{random.randint(200,999)}.{random.randint(100,999)}.{random.randint(1000,9999)}",
        f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        f"{random.randint(2009999100,9999999999)}",
    ]
    return random.choice(formats)

def random_email(first, last):
    first = first.strip().lower()
    last = last.strip().lower()
    patterns = [
        f"{first}.{last}@{random.choice(domains)}",
        f"{first[0]}{last}@{random.choice(domains)}",
        f"{first}_{last}@{random.choice(domains)}",
        f"INVALID_EMAIL",
        f"{first}@",
    ]
    return random.choice(patterns)

rows = []
for i in range(50):
    first = random.choice(first_names)
    last = random.choice(last_names)
    rows.append({
        "id": i + 1,
        "first_name": first,
        "last_name": last,
        "email": random_email(first, last),
        "phone": random_phone(),
        "street": random.choice(streets),
        "city": random.choice(cities),
        "state": random.choice(states),
        "zip": random.choice(["10001", "90001", "60601", "  77001", "ABCDE", ""])
    })

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Generated {len(rows)} messy customer records → data/raw/customers.csv")