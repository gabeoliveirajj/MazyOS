# Guia: subir o webhook do handoff (Guru → Kommo) na Vercel

> Automatiza o handoff de entrada: **venda aprovada da degustação → lead entra
> no Funil Suporte / Onboarding D0 + tag → esteira dispara**, sem toque humano.
> Código: [`api/handoff.py`](../api/handoff.py). Roda sem dependências (Python puro).
> Substitui o passo manual do [runbook](runbook-handoff-degustacao.md).

---

## Visão geral (o que vai acontecer)

1. Você conecta este repositório à **Vercel** (1x).
2. Configura 4 **variáveis de ambiente** (segredos ficam só lá, nunca no GitHub).
3. A Vercel te dá uma **URL** (ex: `https://mazyos.vercel.app/api/handoff`).
4. Você cola essa URL na **Guru** (webhook de transação, status "aprovada").
5. Testa com 1 venda de teste. Pronto — roda sozinho.

---

## Parte 1 — Deploy na Vercel

1. Entra em **vercel.com** e loga (dá pra logar com a conta do GitHub).
2. **Add New → Project → Import** o repositório **MazyOS**.
3. Framework: **Other** (ela detecta o Python pela pasta `/api` + `requirements.txt`).
4. Antes de clicar em Deploy, abre **Environment Variables** e adiciona as 4 abaixo.
5. **Deploy.** No fim, a URL do webhook é: `https://SEU-PROJETO.vercel.app/api/handoff`.

> Teste rápido: abre essa URL no navegador (GET). Tem que responder
> `{"ok": true, "servico": "handoff-degustacao"}`. Se responder isso, tá no ar.

### As 4 variáveis de ambiente

| Variável | O que é | Valor |
|---|---|---|
| `KOMMO_BASE_URL` | URL base da conta Kommo | importar do seu `.env` local |
| `KOMMO_LONG_LIVED_TOKEN` | token de longa duração do Kommo | importar do seu `.env` local |
| `WEBHOOK_SECRET` | segredo que autentica o webhook (vai na URL) | um segredo forte gerado pra você (guardar) |
| `GURU_PRODUCT_NAME_CONTAINS` | filtra só o produto da degustação pelo nome | `degustação` |

> **Autenticação (WEBHOOK_SECRET):** a URL do webhook na Guru leva o segredo no final
> (`.../api/handoff?key=SEU_SEGREDO`). Só quem tem a URL completa consegue acionar —
> bloqueia acesso indevido sem precisar caçar o token da Guru.
>
> **Filtro de produto (obrigatório):** `GURU_PRODUCT_NAME_CONTAINS=degustação` faz o
> webhook processar só vendas cujo nome do produto contém "degustação" e ignorar o
> resto. (Alternativa: `GURU_PRODUCT_IDS` com o id exato, separado por vírgula.)

---

## Parte 2 — Configurar o webhook na Guru

1. Painel da Guru → **Configurações → Webhooks** → aba **Vendas** → **Adicionar Webhook**.
2. **URL:** cola a URL da Vercel **com o segredo no final**:
   `https://SEU-PROJETO.vercel.app/api/handoff?key=SEU_WEBHOOK_SECRET`
3. **Status:** marca **Aprovada** (`approved`). *(Só esse — o resto o endpoint ignora sozinho, mas melhor nem mandar.)*
4. **Ativo:** sim. Salva.

---

## Parte 3 — Testar ponta a ponta

**Opção A (recomendada) — venda de teste real na Guru:**
1. Gera um link de teste/checkout da degustação com valor simbólico (ou usa o modo teste da Guru, se tiver).
2. Compra usando um **telefone de teste seu** (o mesmo do teste da esteira).
3. Confere no Kommo: o lead entrou no **Funil Suporte / Onboarding D0** com a tag
   **CLIENTE DEGUSTAÇÃO**, e o **áudio 1** chegou no WhatsApp.
4. Limpa o lead de teste depois (lixeira no Kommo).

**Opção B — só validar o endpoint (sem mexer no Kommo):**
- Abre a URL no navegador (GET) e confirma o `{"ok": true}`.
- O disparo real a gente confirma com a Opção A.

---

## Como saber se funcionou (logs)

Na Vercel: projeto → **Logs** (ou Deployments → Functions). Cada venda que
chega aparece ali com o resultado, ex:
- `{"acao":"mover","origem":"lead_existente","http":200}` → achou e moveu o lead.
- `{"acao":"criar","origem":"lead_novo","http":200}` → comprador novo, criou o lead.
- `{"ignorado":"produto fora do filtro..."}` → era outra venda, ignorou (esperado).
- `{"erro":"api_token inválido"}` → alguém/algo bateu na URL sem ser a Guru (bloqueado).

---

## Segurança (já embutida)

- Só processa se o `api_token` do webhook bater com `GURU_API_TOKEN` → ninguém de
  fora consegue mover leads batendo na URL.
- Só dispara em `status == approved` **e** produto no filtro **e** com telefone.
- Erro no servidor responde 500 → a Guru **reenvia** depois (não perde a venda).

---

## Quando algo dá ruim

| Sintoma | Causa | O que fazer |
|---|---|---|
| GET não responde `{"ok":true}` | Deploy falhou ou runtime Python não detectado | Ver Logs da Vercel; confirmar que `requirements.txt` e `/api/handoff.py` estão no repo |
| Log mostra `api_token inválido` numa venda real | `GURU_API_TOKEN` na Vercel ≠ o da Guru | Copiar de novo o `api_token` do painel da Guru pra variável da Vercel |
| Venda da degustação vira `ignorado: produto fora do filtro` | `GURU_PRODUCT_IDS` errado | Conferir o id real do produto no log (`id=...`) e ajustar a variável |
| Lead não entrou na esteira mesmo movido | O gatilho do Salesbot pode não disparar em lead **criado** na etapa | Confirmar no teste; se for o caso, a gente troca "criar na etapa" por "criar + mover" |

---

## Manual continua valendo

O [runbook manual](runbook-handoff-degustacao.md) (`scripts/guru-para-kommo.py`)
segue funcionando como **plano B** — se a Vercel/Guru cair, você roda o handoff na
mão pelo terminal. Mesma lógica, mesmos IDs.
