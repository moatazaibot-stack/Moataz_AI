#!/bin/sh
set -e

echo "Starting Moataz AI Platform..."

# Initialize database (create file and apply schema for SQLite)
if [ -n "$DATABASE_URL" ]; then
  echo "Initializing database..."
  # We use db push for SQLite to ensure the file is created and schema applied
  # In production with other DBs, you'd use prisma migrate deploy
  mkdir -p /app/data
  npx prisma db push --accept-data-loss
else
  echo "Warning: DATABASE_URL not set. Database initialization skipped."
fi

echo "Starting server..."
exec node server.js
