#!/usr/bin/env bash

set -e # Exit immediately if a command exits with a non-zero status.

RED='\033[0;31m'
NC='\033[0m' # No Color

# Load environment variables from .env file if present
if [ -f ".env" ]; then
  set -o allexport
  source .env
  set +o allexport
fi

CMD=$1
MSG=$2

# Default command help
function help() {
    echo "Usage: alembic.sh <command> [message]"
    echo "Commands:"
    echo "  migration \"<Message>\" - Create a new migration file (alembic revision)"
    echo "  migrate - Apply migrations to the database (alembic upgrade)"
    echo "  downgrade - Revert the last migration (alembic downgrade)"
    echo "  history - Show the migration history (alembic history)"
}

case $CMD in
migrate)
  uv run alembic upgrade head
  ;;
migration)
  if [ -z "$MSG" ]; then
    echo -e "${RED}Error: Migration message is required.${NC}"
    help
    exit 1
  fi
  uv run alembic revision --autogenerate -m "$MSG"
  ;;
downgrade)
  uv run alembic downgrade -1
  ;;
history)
  uv run alembic history --verbose
  ;;
*)
  help
  ;;
esac
