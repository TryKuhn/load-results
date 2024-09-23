mount:
	docker container exec -it mr-web bash

build:
	docker build -t load-results:latest -f Dockerfile .

clean-up:
	docker rm -f mr-web
	docker rm -f mr-mysql
	docker rm -f mr-clickhouse

clean-up-test:
	docker rm -f mr-test
	docker rm -f mr-test-mysql
	docker rm -f mr-test-clickhouse

clean-up-all: clean-up clean-up-test

prepare: clean-up
	docker compose up -d mysql clickhouse
	sleep 20
	docker compose up migrator
	docker rm mr-migrator

prepare-test: clean-up-test
	docker compose up -d test-mysql test-clickhouse

prepare-all: prepare prepare-test

make-migrations:
	docker compose up migrations-maker
	docker rm -f mr-migrations-maker

migrate:
	docker compose up migrator
	docker rm -f mr-migrator

check-pep8:
	docker compose up check-pep8
	docker rm -f mr-check-pep8

test:
	docker compose up test

run:
	docker compose up --force-recreate -d web
