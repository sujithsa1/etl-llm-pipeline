# ETL Pipeline with LLM-Powered Data Cleaning

![Pipeline Status](https://github.com/sujithsa1/etl-llm-pipeline/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Airflow](https://img.shields.io/badge/Airflow-2.7.2-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![LLM](https://img.shields.io/badge/LLM-Llama%203.1-green)

**An end-to-end data engineering pipeline that uses Llama 3.1 (Groq API) as an intelligent transformation step** — cleaning messy real-world customer data instead of brittle regex rules. Orchestrated with Apache Airflow, stored in PostgreSQL, fully containerized with Docker.

---

## 📸 Live Pipeline — All 4 Tasks Successful

![Airflow DAG](assets/airflow_success.png)

---

## 📊 Data Quality — Before vs After

![Quality Report](assets/quality_report.png)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Proper case names | 3 / 50 | 46 / 50 | **+43** ✅ |
| Clean whitespace | 35 / 50 | 47 / 50 | **+12** ✅ |
| Valid state codes | 0 / 50 | 50 / 50 | **+50** ✅ |
| All quality checks | ❌ | ✅ | **PASS** |

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| Orchestration | Apache Airflow 2.7 | Industry-standard DAG scheduling |
| LLM | Groq API — Llama 3.1 8B | Fast, free, production-grade LLM |
| Database | PostgreSQL 15 | Reliable relational storage |
| Infra | Docker + Compose | One-command reproducible stack |
| Language | Python 3.11 | Core pipeline logic |
| CI/CD | GitHub Actions | DAG validation on every push |

---

## 🏗️ Pipeline Flow

```
generate_raw_data  →  llm_clean_data  →  load_to_postgres  →  data_quality_check
  Creates 50            Groq/Llama 3.1      Upserts to            Asserts all
  messy records         cleans each row     PostgreSQL            50 records OK
```

---

## 🧹 What the LLM Cleans

| Problem | Raw Input | Cleaned Output |
|---------|-----------|----------------|
| Wrong case | `JANE smith` | `Jane Smith` |
| Extra spaces | `··bob·` | `Bob` |
| Invalid email | `INVALID_EMAIL` | `invalid@unknown.com` |
| Uppercase domain | `user@GMAIL.COM` | `user@gmail.com` |
| Messy zip | `··77001` | `77001` |
| Missing zip | _(empty)_ | `00000` |
| Inconsistent phone | `9541234567` | `(954) 123-4567` |
| Lowercase city | `new york` | `New York` |

---

## 📁 Project Structure

```
etl-llm-pipeline/
├── dags/
│   └── etl_pipeline_dag.py       # Airflow DAG — 4 task pipeline
├── scripts/
│   ├── generate_data.py          # Generates 50 messy customer records
│   ├── llm_cleaner.py            # Groq/Llama 3.1 with retry + logging
│   ├── db_loader.py              # Idempotent PostgreSQL loader
│   └── generate_report.py        # Before/after quality metrics
├── tests/
│   └── test_llm_cleaner.py       # 4 unit tests — all passing ✅
├── .github/workflows/ci.yml      # Validates DAG syntax on every push
├── docker-compose.yml            # Airflow + PostgreSQL services
├── Makefile                      # make start / stop / clean
├── requirements.txt
└── .env.example                  # API key template
```

---

## ⚙️ Makefile Commands

```bash
make start      # Start Airflow + PostgreSQL in Docker
make stop       # Stop all containers
make logs       # Tail live Airflow logs
make clean      # Wipe all containers, volumes, data
```

---

## 🧪 Tests

```
✅ test_valid_emails passed
✅ test_valid_zips passed
✅ test_proper_case passed
✅ test_raw_data_is_dirty passed — found 21 invalid emails in raw data
```

---

## 💡 Key Engineering Decisions

**LLM as a transformation step** — Handles ambiguous normalization that regex can't. `JANE`, `J. Smith`, `jane m` all correctly become `Jane`.

**Idempotent loading** — `ON CONFLICT DO UPDATE` so the pipeline safely reruns daily without duplicating data.

**Retry with exponential backoff** — LLM calls retry 3x with increasing delays. Failures fall back to the original record — pipeline never crashes mid-run.

**Fully containerized** — Airflow + PostgreSQL both run in Docker. Full stack up in under 2 minutes.

---

## 🔮 Roadmap

- [ ] Scale to 10,000 records using batch LLM calls
- [ ] Add Kafka for real-time streaming ingestion
- [ ] Add dbt transformation layer on PostgreSQL
- [ ] Deploy to AWS MWAA (managed Airflow)

---

Built by **Sujith** — open to Data Engineering roles. [![GitHub](https://img.shields.io/badge/GitHub-sujithsa1-black)](https://github.com/sujithsa1)
