#!/bin/bash
export PORT=${PORT:-8080}
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
