efault: help
.PHONY: help migration migrate downgrade history

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
