efault: help
.PHONY: help env test test-cov test-cov-o clean migration migrate downgrade history

## This help screen
help:
	@printf "Available targets:\n\n"
	@awk '/^[a-zA-Z\-\_0-9%:\\ ]+/ { \
	  helpMessage = match(lastLine, /^## (.*)/); \
	  if (helpMessage) { \
	    helpCommand = $$1; \
	    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
	    gsub("\\\\", "", helpCommand); \
	    gsub(":+$$", "", helpCommand); \
	    printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
	  } \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@printf "\n"


## Make .env from the .env.ini template
env:
	@echo "Creating .env from .env.ini template"
	@./scripts/env.sh
	@echo "Done"


## Test
test:
	@uv run pytest

## Test with coverage
test-cov:
	@uv run pytest --cov=apps --cov-report=term-missing --cov-report=html

## Test with coverage and open the report in browser
test-cov-o:
	@uv run pytest --cov=apps --cov-report=term-missing --cov-report=html && open htmlcov/index.html

## Cleanup the code base (remove the tests and coverage files)
clean:
	@echo "Cleaning up the code base"
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@find . -name ".coverage" -delete
	@find . -name ".pytest_cache" -delete
	@find . -name "htmlcov" -type d -exec rm -rf {} +
	@echo "Done"

## Create a alembic revision
migration:
	@./scripts/alembic.sh migration "$msg"


## Apply alembic migrations
migrate:
	@./scripts/alembic.sh migrate


## Revert alembic migrations
downgrade:
	@./scripts/alembic.sh downgrade

## Alembic History
history:
	@./scripts/alembic.sh history



# Prevent Make from treating extra words as targets
%:
	@:
