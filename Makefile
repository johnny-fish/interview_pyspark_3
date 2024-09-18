.PHONY: build-airflow
build-airflow:
	docker build -f Dockerfile.Airflow . -t airflow

.PHONY: build-spark
build-spark:
	docker build -f Dockerfile.Spark . -t spark

build: build-airflow build-spark

.PHONY: init
init:
	mkdir -p ./logs ./plugins
	docker compose -f docker-compose-airflow.yaml up airflow-init

.PHONY: up-airflow
up-airflow:
	docker compose -f docker-compose-airflow.yaml up -d

.PHONY: up-spark
up-spark:
	docker compose -f docker-compose-spark.yaml up -d

up: up-airflow up-spark

.PHONY: down-airflow
down-airflow:
	docker compose -f docker-compose-airflow.yaml down

.PHONY: down-spark
down-spark:
	docker compose -f docker-compose-spark.yaml down

down: down-airflow down-spark

.PHONY: tests
tests:
	pytest tests

.PHONY: setup-local-dev
setup-local-dev:
	poetry config virtualenvs.create false \
	&& poetry install --no-root

# Package the etl to be use for spark-submit
.PHONY: package-project
package-project:
	rm -rf dist \
	&& mkdir -p dist/algolia \
	&& cp -r etl dist/algolia \
	&& cd dist/algolia \
	&& touch __init__.py \
	&& zip -r ../algolia.zip . \
	&& cd ../.. \
	&& rm -r dist/algolia

# TODO add target to run job with docker
# Like docker exec -it agoliaassignment-spark-1 spark-submit --master spark://172.21.1.2:7077 etl/process_shopify_configuration.py
# with cluster config