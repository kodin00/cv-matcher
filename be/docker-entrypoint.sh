#!/bin/sh
set -e

DB_FILE="${DATABASE_URL#sqlite:///}"
DB_FILE="${DB_FILE#sqlite:////}"   # strip absolute sqlite:////path form too

# Resolve relative path relative to /app
case "$DB_FILE" in
    /*) : ;;             # already absolute
    *)  DB_FILE="/app/$DB_FILE" ;;
esac

DB_DIR="$(dirname "$DB_FILE")"
mkdir -p "$DB_DIR"

if [ ! -s "$DB_FILE" ]; then
    echo "[entrypoint] Initialising database at $DB_FILE"
    sqlite3 "$DB_FILE" < /app/seed/schema.sql

    if [ -f /app/seed/jobs_seed.sql ]; then
        sqlite3 "$DB_FILE" < /app/seed/jobs_seed.sql
    else
        echo "[entrypoint] Warning: /app/seed/jobs_seed.sql not found, skipping seed data."
    fi

    echo "[entrypoint] Database ready."
fi

exec "$@"
