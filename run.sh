#!/usr/bin/env bash
# Start, stop or update the dashboard demo server (Docker). See demo/README.md.
#
#   ./run.sh [start]   build and start on $FIF_PORT (default 5187), wait until healthy
#   ./run.sh update    git pull, then start
#   ./run.sh stop | restart | logs | status
#
# Env: FIF_PORT (5187), FIF_BIND (0.0.0.0; use 127.0.0.1 behind nginx/Caddy).
set -euo pipefail
cd "$(dirname "$0")"

export FIF_PORT="${FIF_PORT:-5187}"
export FIF_BIND="${FIF_BIND:-0.0.0.0}"
compose() { docker compose "$@"; }

port_owner() {
    command -v ss >/dev/null || return 0
    ss -Htlnp "sport = :$FIF_PORT" 2>/dev/null
}

start() {
    command -v docker >/dev/null || { echo "docker is not installed"; exit 1; }
    # Our own container holding the port is fine (compose replaces it); anything else is a conflict.
    if [ -z "$(compose ps -q demo 2>/dev/null)" ] && [ -n "$(port_owner)" ]; then
        echo "Port $FIF_PORT is already in use:"; port_owner
        echo "Stop that process (e.g. the old Flask run.py) or pick another port: FIF_PORT=5188 ./run.sh"
        exit 1
    fi
    compose up -d --build
    echo -n "Waiting for the server"
    for _ in $(seq 60); do
        if curl -fsS "http://127.0.0.1:$FIF_PORT/api/health" >/dev/null 2>&1; then
            echo; echo "Up: http://$(hostname -f 2>/dev/null || hostname):$FIF_PORT  (bound to $FIF_BIND)"
            return 0
        fi
        echo -n .; sleep 2
    done
    echo; echo "No answer from /api/health after 2 minutes. Last logs:"; compose logs --tail 40 demo; exit 1
}

case "${1:-start}" in
    start)   start ;;
    update)  git pull --ff-only && start ;;
    stop)    compose down ;;
    restart) compose down && start ;;
    logs)    compose logs -f demo ;;
    status)  compose ps; curl -fsS "http://127.0.0.1:$FIF_PORT/api/health" && echo ;;
    *)       sed -n 2,7p "$0"; exit 1 ;;
esac
