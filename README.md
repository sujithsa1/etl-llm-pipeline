
## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    Apache Airflow DAG                        │
│                  (etl_llm_customer_pipeline)                 │
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ generate_    │────▶│ llm_clean_   │────▶│ load_to_    │ │
│  │ raw_data     │     │ data         │     │ postgres    │ │
│  │              │     │              │     │             │ │
│  │ Creates 50   │     │ Groq API     │     │ PostgreSQL  │ │
│  │ messy rows   │     │ Llama 3.1    │     │ INSERT ON   │ │
│  │ of customer  │     │ normalizes   │     │ CONFLICT    │ │
│  │ CSV data     │     │ each record  │     │ DO UPDATE   │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│                                                    │        │
│                                            ┌───────▼──────┐ │
│                                            │ data_quality_│ │
│                                            │ check        │ │
│                                            │              │ │
│                                            │ Validates    │ │
│                                            │ 50 records   │ │
│                                            │ loaded OK    │ │
│                                            └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
        │                      │                    │
   ┌────▼────┐           ┌─────▼─────┐      ┌──────▼──────┐
   │  data/  │           │ Groq API  │      │ PostgreSQL  │
   │  raw/   │           │ (cloud)   │      │ (Docker)    │
   └─────────┘           └───────────┘      └─────────────┘
```
