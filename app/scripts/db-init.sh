#!/bin/bash
set -e

echo "Creating schema..."
psql -d ${POSTGRES_DB} -a -U${POSTGRES_USER} -f /schema.sql
