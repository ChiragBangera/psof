.PHONY: start start_build stop unit_tests check_typing

UNIT_TESTS=uv run pytest tests -vvv

start:
	@docker-compose up -d

start_build:
	@docker-compose up --build -d

stop:
	@docker-compose down

unit_tests:
	@docker-compose exec -T app-test \
	$(UNIT_TESTS)

unit_tests_local:
	@$(UNIT_TESTS)

check_typing:
	@docker-compose exec -T app-test uv run mypy .