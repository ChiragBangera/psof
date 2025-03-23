.PHONY: start start_build stop unit_tests check_typing

start:
	docker-compose up -d

start_build:
	docker-compose up --build -d

stop:
	docker-compose down

unit_tests:
	docker-compose exec -T app-test uv run pytest tests

check_typing:
	docker-compose exec -T app-test uv run mypy .