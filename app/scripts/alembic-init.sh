#!/bin/bash
set -e
echo "Running alembic stamp head"
alembic stamp head
echo "Running alembic initial revision"
alembic revision --autogenerate -m "initial schema and tables migration"
echo "Running alembic migration"
alembic upgrade head
echo "Initial migration complete"
