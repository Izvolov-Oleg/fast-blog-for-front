#!/usr/bin/env sh

exec python -m alembic upgrade head &&
exec bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"