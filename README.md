<div align="center">

# 🚀 ETL Pipeline with LLM-Powered Data Cleaning

<p>
  <img src="https://github.com/sujithsa1/etl-llm-pipeline/actions/workflows/ci.yml/badge.svg"/>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Airflow-2.7.2-017CEE?style=flat&logo=apacheairflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLM-Llama%203.1-10B981?style=flat"/>
</p>

<p><strong>Apache Airflow pipeline that uses Llama 3.1 (Groq) as an intelligent data transformation step</strong><br/>
Cleans messy customer records · Loads to PostgreSQL · Fully containerized with Docker</p>

</div>

---

## ✅ Live Pipeline — All Tasks Successful

![Airflow DAG](assets/airflow_success.png)

---

## 📊 Data Quality Results

<div align="center">
<img src="assets/quality_report.png" width="600"/>
</div>

| Metric | Before | After | Improvement |
|--------|:------:|:-----:|:-----------:|
| Proper case names | 3 / 50 | 46 / 50 | 🟢 **+43** |
| Clean whitespace | 35 / 50 | 47 / 50 | 🟢 **+12** |
| Valid state codes | 0 / 50 | 50 / 50 | 🟢 **+50** |
| Quality checks | ❌ Fail | ✅ Pass | 🟢 **PASS** |

---

## 🏗️ Pipeline Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ generate_       │───▶│ llm_clean_      │───▶│ load_to_        │───▶│ data_quality_   │
│ raw_data        │    │ data            │    │ postgres        │    │ check           │
│                 │    │                 │    │                 │    │                 │
│ 50 messy CSV    │    │ Groq / Llama3.1 │    │ Upsert to DB    │    │ Assert 50 rows  │
│ customer rows   │    │ cleans each row │    │ ON CONFLICT     │    │ all valid ✅    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| 🎯 Orchestration | Apache Airflow 2.7 | DAG scheduling & monitoring |
| 🤖 LLM | Groq API — Llama 3.1 8B | Intelligent data transformation |
| 🗄️ Database | PostgreSQL 15 | Cleaned data storage |
| 🐳 Infra | Docker + Compose | One-command reproducible stack |
| 🐍 Language | Python 3.11 | Core pipeline logic |
| ⚙️ CI/CD | GitHub Actions | DAG validation on every push |

---

## 🧹 What the LLM Fixes

| Problem | Raw Input | Cleaned Output |
|---------|-----------|----------------|
| Wrong case | `JANE smith` | `Jane Smith` |
| Extra spaces | `··bob·` | `Bob` |
| Invalid email | `INVALID_EMAIL` | `invalid@unknown.com` |
| Uppercase domain | `user@GMAIL.COM` | `user@gmail.com` |
| Bad zip | `··77001` | `77001` |
| Missing zip | _(empty)_ | `00000` |
| Unformatted phone | `9541234567` | `(954) 123-4567` |
| Lowercase city | `new york` | `New York` |

---

## 📁 Project Structure

```
etl-llm-pipeline/
├── 📂 dags/
│   └── etl_pipeline_dag.py       # Airflow DAG — 4 task pipeline
├── 📂 scripts/
│   ├── generate_data.py          # Generates 50 messy customer records
│   ├── llm_cleaner.py            # Groq/Llama 3.1 with retry + logging
│   ├── db_loader.py              # Idempotent PostgreSQL loader
│   └── generate_report.py        # Before/after quality metrics
├── 📂 tests/
│   └── test_llm_cleaner.py       # 4 unit tests ✅
├── 📂 .github/workflows/
│   └── ci.yml                    # Validates DAG on every push
├── docker-compose.yml            # Airflow + PostgreSQL services
├── Makefile                      # make start / stop / clean
├── requirements.txt
└── .env.example                  # API key template (safe to commit)
```

---

## ⚙️ Commands

```bash
make start      # Start Airflow + PostgreSQL in Docker
make stop       # Stop all containers
make logs       # Tail live Airflow logs
make clean      # Wipe containers, volumes and data
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

## 💡 Engineering Decisions

> **LLM as a transformation step** — Handles ambiguous normalization that regex can't. `JANE`, `J. Smith`, `jane m` all correctly become `Jane`.

> **Idempotent loading** — `ON CONFLICT DO UPDATE` so the pipeline safely reruns daily without duplicating records.

> **Retry with exponential backoff** — LLM calls retry 3x. Failures fall back to the original record — pipeline never crashes mid-run.

> **Fully containerized** — Airflow + PostgreSQL in Docker. Full stack up in under 2 minutes with `make start`.

---

<div align="center">

Built by **Sujith** · Open to Data Engineering roles

[![GitHub](https://img.shields.io/badge/GitHub-sujithsa1-181717?style=flat&logo=github)](https://github.com/sujithsa1)

</div>
