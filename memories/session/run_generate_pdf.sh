#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -f package.json ]; then
  echo "package.json não encontrado"
  exit 1
fi

echo "Instalando dependências..."
npm install --no-audit --no-fund --silent

echo "Gerando PDF..."
npm run generate-pdf

echo "PDF gerado em: $(pwd)/apresentacao-nutri-chedid.pdf"
