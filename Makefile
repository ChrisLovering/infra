.PHONY: lock
lock:
	poetry lock
	poetry export --only main --output requirements.txt
	poetry install --no-root --sync

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: precommit
precommit:
	poetry run pre-commit install
