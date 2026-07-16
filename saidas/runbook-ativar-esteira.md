# Runbook: ativar a esteira (dieta entregue → Onboarding D0)

> **O que é:** o **2º gatilho manual** da degustação. A esteira de 8 áudios (D0→D26)
> tem que começar **no dia em que a dieta é entregue** — não no dia da compra.
> Regra trazida pela Kami: o cliente leva ~7 dias (variável) pra receber a dieta,
> e os áudios só fazem sentido depois disso (o áudio 2 já pergunta "conseguiu
> começar o plano?").

---

## O fluxo completo (onde este passo entra)

```
1. Compra aprovada na Guru
      ↓ (automático — webhook)
2. Lead cai em "Aguardando entrega da dieta" (Funil Suporte). Esteira PARADA.
      ↓ (Henrique produz + Kami ENTREGA a dieta pelo WhatsApp — ~7 dias, variável)
3. Kami te avisa "entreguei pra fulano (telefone X)"
      ↓ (MANUAL — você roda o comando abaixo)
4. Lead move pra "Onboarding (D0)" → esteira dispara (D0 = dia da entrega) ✅
```

> **Por que manual:** o sistema não sabe quando a dieta foi entregue (é um passo
> humano do Henrique/Kami). Então você marca a entrega rodando o comando.

---

## O comando (a ativação em si)

No terminal, dentro da pasta do projeto:

```bash
# 1) Confere ANTES (dry-run — não altera nada, só mostra qual lead vai mexer):
python3 scripts/ativar-esteira.py "TELEFONE_DO_CLIENTE"

# 2) Se o lead certo apareceu, ATIVA de verdade:
python3 scripts/ativar-esteira.py "TELEFONE_DO_CLIENTE" --executar
```

Telefone em qualquer formato (`48 99943-7241`, `+55 48 99943-7241`, `5548999437241`) —
o script casa pelos **últimos 8 dígitos**.

### O que o script faz
1. Acha o contato pelo telefone e escolhe o **melhor lead** (prioriza o que está em
   **Suporte / Aguardando entrega da dieta**).
2. Move pro **Funil Suporte → Onboarding (D0)**.
3. A entrada no Onboarding (D0) **dispara a esteira** automaticamente.

### Como ler a saída
```
✅ Lead #64101555 — contato: Fulano — tel Kommo: +554899805599
   está em pipeline 14050808 / status 108761732
   ação: movido pro Onboarding D0 → esteira disparada (HTTP 200)
```
- `✅` + `HTTP 200` = deu certo, esteira ligada.
- `já está em Onboarding D0` = a esteira desse lead já foi ativada (não roda de novo).
- `⚠️ lead NÃO está em 'Aguardando entrega da dieta'` = confere se é o lead certo antes de `--executar`.
- `❌ nenhum contato com o telefone` = o telefone não bate com nenhum lead. Ver "Quando dá ruim".

---

## A janela do WhatsApp (por que rodar no dia da entrega)

A esteira só **entrega** o áudio se a conversa com a Kami estiver **aberta** (regra do
WhatsApp). Como a **entrega da dieta acontece pelo WhatsApp** (a Kami manda, o cliente
responde), a janela está aberta **no mesmo dia**. Por isso: **rode o comando logo após
a Kami confirmar a entrega**, com a conversa quente. Se rodar dias depois, sem o cliente
ter interagido, o áudio D0 pode não sair.

---

## Quando dá ruim

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `❌ nenhum contato com o telefone` | Telefone diferente do lead, ou lead não existe | Buscar no Kommo pelo nome e mover **na mão** (arrastar pro Onboarding D0) |
| `⚠️ lead NÃO está em 'Aguardando entrega da dieta'` | Lead noutra etapa (homônimo, ou já ativado) | Confirmar o lead certo antes de `--executar` |
| Esteira não entregou o áudio mesmo movido | Janela do WhatsApp fechada | Pedir pra Kami trocar 1 msg com o cliente e rodar de novo, ou reativar quando o cliente responder |

**Plano B (na mão):** arrastar o lead de *Aguardando entrega da dieta* → *Onboarding (D0)*
no Kanban do Kommo. Efeito idêntico (a esteira dispara na entrada da etapa).

---

## Contexto técnico

- Funil Suporte: `14050808` · Aguardando entrega da dieta: `108761732` · Onboarding D0: `108457804`.
- Irmão deste runbook: `runbook-handoff-degustacao.md` (o 1º gatilho, compra → Suporte, hoje automático via webhook).
- **Importante:** o bot automático *"Em uma mensagem recebida"* (que ligava a esteira quando o
  cliente mandava msg) foi **desativado** — senão a esteira ligaria antes da dieta chegar.
  Agora quem liga é este comando manual, na entrega.
