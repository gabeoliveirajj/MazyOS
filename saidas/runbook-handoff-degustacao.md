# Runbook: handoff de entrada da degustação (fase manual)

> **O que é:** quando alguém compra a degustação (R$197), o lead precisa ir pro
> **Funil Suporte / Onboarding (D0)** com a tag **CLIENTE DEGUSTAÇÃO**. Assim que
> entra nessa etapa, a **esteira de 8 áudios** dispara sozinha.
> **Fase atual:** manual (você aciona). Automação via webhook da Guru fica pra depois.

---

## O gatilho: painel/app da Guru

Você acompanha as vendas no **painel/app da Guru**. Quando entrar uma venda
aprovada da **degustação**, pegue o **telefone do comprador** (o mesmo que ele
usou no cadastro/WhatsApp) — é a chave que liga a venda ao lead no Kommo.

> 💡 Só faça o handoff pra vendas da **degustação**. Outros produtos não entram nessa esteira.

---

## O comando (o handoff em si)

No terminal, dentro da pasta do projeto:

```bash
# 1) Confere ANTES (dry-run — não altera nada, só mostra qual lead vai mexer):
python3 scripts/guru-para-kommo.py "TELEFONE_DO_COMPRADOR"

# 2) Se o lead certo apareceu, EXECUTA de verdade:
python3 scripts/guru-para-kommo.py "TELEFONE_DO_COMPRADOR" --executar
```

Exemplos de telefone que funcionam (o script normaliza sozinho): `48 99805-5599`,
`+55 48 99805-5599`, `5548998055599`. Ele casa pelos **últimos 8 dígitos**, então
formato não importa muito.

### O que o script faz
1. Acha o contato pelo telefone e escolhe o **melhor lead** (prioriza lead **aberto no Funil Degustação**).
2. Move pro **Funil Suporte → Onboarding (D0)**.
3. Adiciona a tag **CLIENTE DEGUSTAÇÃO** (sem apagar as tags que já existem).
4. A entrada na etapa Onboarding (D0) **dispara a esteira** automaticamente.

### Como ler a saída
```
✅ Lead #54219013 — contato: Fulano — tel Kommo: +554899805599
   está em pipeline 13257796 / status 143
   ação: movido + tagueado (HTTP 200)
```
- `✅` + `HTTP 200` = deu certo, lead movido e tagueado.
- `❌ nenhum contato com o telefone` = o telefone da venda não bate com nenhum lead
  no Kommo. Ver seção "Quando dá ruim".

---

## Confirmar que funcionou

No Kommo, abra o **Funil Suporte**: o lead deve estar em **Onboarding (D0)**, com a
tag **CLIENTE DEGUSTAÇÃO**, e a conversa da esteira começando no WhatsApp da Kami.

---

## Quando dá ruim

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `❌ nenhum contato com o telefone` | O comprador usou um telefone diferente do que está no lead, ou o lead nunca foi criado | Buscar o lead no Kommo pelo nome/e-mail e mover **na mão** (arrastar pra Onboarding D0 + tag) |
| Achou o lead **errado** (homônimo/telefone repetido) | Dois contatos com final de número parecido | Não rodar `--executar`; mover o lead certo na mão no Kommo |
| `HTTP` diferente de 200/204 | Token do Kommo expirado ou instabilidade | Rodar de novo; se persistir, checar o `KOMMO_LONG_LIVED_TOKEN` no `.env` |

**Plano B sempre disponível:** fazer o handoff **na mão** no Kommo — arrastar o lead
pro Funil Suporte / Onboarding (D0) e adicionar a tag CLIENTE DEGUSTAÇÃO. O efeito é
idêntico (a esteira dispara na entrada da etapa).

---

## Próximo passo (automação — depois)

Trocar o acionamento manual por: **webhook de venda aprovada da Guru → endpoint
hospedado que roda essa mesma lógica**. Aí o handoff acontece sozinho, sem você
tocar. Fica pra quando a fase manual estiver rodando redonda.
