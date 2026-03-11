.PHONY: start stop restart logs clean run-local

start:
	docker-compose up -d
	@echo "✅ Airflow UI: http://localhost:8080 (admin/admin)"

stop:
	docker-compose down

restart:
	docker-compose down && docker-compose up -d

logs:
	docker logs etl_airflow -f

clean:
	docker-compose down -v
	rm -rf data/raw/* data/cleaned/* logs/*

run-local:
	python3 scripts/generate_data.py
	python3 scripts/llm_cleaner.py
	python3 scripts/db_loader.py
	@echo "✅ Pipeline complete!"
