---
name: reativar-leads
description: >
  Puxa os leads parados no CRM Kommo, prioriza pra reativação (quente → frio) e gera a lista +
  mensagens prontas pra abordar e vender. Use quando o usuário disser "reativar leads", "puxar a
  base parada", "quem tá parado no Kommo", "lista de reativação", "/reativar-leads" ou pedir pra
  trabalhar leads frios da consultoria/clínica.
---

# /reativar-leads — Reativação da base do Kommo

Skill do Inside Sales (Gabriel) pra transformar a base parada do Kommo em venda. Conecta no CRM ao vivo, prioriza os leads e entrega lista + abordagem pronta.

## Pré-requisitos

- Arquivo `.env` na raiz com `KOMMO_BASE_URL` e `KOMMO_LONG_LIVED_TOKEN` (já configurado). Nunca versionar.
- Playbook de apoio: `saidas/playbook-comercial-reativacao-team-chedid.md` (mensagens, objeções, cadência).

## Workflow

### 1. Puxar e priorizar os leads
Rodar o script (padrão = "Funil de vendas", a consultoria online, prioridade #1):
```
python3 .claude/skills/reativar-leads/puxar_leads.py
```
Pra outro funil, passar o `pipeline_id` (ex.: Clínica Chedid `13970652`, DEGUSTAÇÃO `13257796`):
```
python3 .claude/skills/reativar-leads/puxar_leads.py 13970652
```
Gera `saidas/leads-reativacao-<funil>.csv` com: prioridade, etapa, contato, telefone, dias parado, responsável e link direto pro lead no Kommo. Ordenado do mais quente pro mais frio.

### 2. Apresentar o resumo
Mostrar ao usuário a contagem por nível de prioridade (🔥 quente / 🟠 morno / 🟡 1º contato / ⚪ MQL / ❄️ frio) e recomendar começar pelos quentes/mornos (maior probabilidade de venda, menor esforço).

### 3. Entregar a abordagem
Puxar do `playbook-comercial-reativacao-team-chedid.md` a mensagem certa pro nível que o usuário vai atacar:
- **Quente** (CQA/proposta): leve "mea culpa" + reabertura.
- **Morno** (diagnóstico/follow-up): valor + pergunta de decisão.
- **Frio** (nunca triado): mensagem enxuta qualificadora.

Sempre **reconhecer o tempo parado** (não fingir contato novo) e personalizar a 1ª linha com nome + objetivo.

### 4. Apoiar o fechamento
Durante a conversa, oferecer:
- **Objeções** (sem dinheiro / cônjuge / "vou pensar") → Parte 3 do playbook.
- **Follow-up** (não respondeu / indeciso) → cadência D1–D30 da Parte 4.
- **De-risk:** online = degustação R$197 + garantia 7 dias · clínica = depósito R$50.

## Notas de manutenção
- Os IDs de etapas/funis ficam no topo do `puxar_leads.py` (dict `TIER` e `EXCLUIR`). Se o funil do Kommo mudar, atualizar lá.
- Funis atuais: Funil de vendas `12250156` · Funil de Indicação `12715659` · DEGUSTAÇÃO `13257796` · Clínica Chedid `13970652`.
- Boa prática comercial a propor: ligar o **motivo de perda** no Kommo (hoje desligado) e registrar sempre que mover lead pra Perdido.
