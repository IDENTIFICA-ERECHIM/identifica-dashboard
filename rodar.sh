#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! sudo docker network inspect identifica > /dev/null 2>&1; then
    echo "Rede 'identifica' nao encontrada."
    echo "Suba o MySQL no identifica-etl primeiro (docker compose up -d mysql)."
    exit 1
fi

sudo docker compose up --build -d

trap "docker compose down" EXIT

echo "Tentando rodar dashboard..."
tentativas=0
until curl -fs http://localhost:8501/_stcore/health > /dev/null; do
    tentativas=$((tentativas + 1))
    if [ "$tentativas" -ge 60 ]; then
        echo "Dashboard nao respondeu em 60s. Logs:"
        sudo docker compose logs dashboard
        exit 1
    fi
    sleep 1
done

xdg-open http://localhost:8501 > /dev/null 2>&1
sudo docker compose logs -f dashboard
