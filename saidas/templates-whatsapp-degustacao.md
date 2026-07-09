# Templates de WhatsApp — reabridores de janela (esteira da degustação + Funil Anual)

> Para submeter à aprovação da Meta (via Kommo → Modelos / WhatsApp Manager). Autor: Gabriel. Jul/2026.
>
> **Por que existem:** com API oficial, fora da janela de 24h só sai template de texto (áudio é bloqueado). Como os áudios do Henrique são espaçados (2 a 11 dias entre eles), a janela quase sempre estará fechada. Cada template abaixo **reabre a conversa** antes do áudio correspondente.
>
> **Como funciona o disparo:** o bot manda o template → a pessoa **toca no botão de resposta rápida** → isso conta como mensagem dela → **janela reabre por 24h** → o bot manda o **áudio** logo em seguida. Tocar no botão é mais fácil que digitar = mais gente reabre.

---

## Regras de preenchimento na Meta (ler antes)

- **Nome:** só minúsculas, números e `_` (já vem pronto abaixo).
- **Idioma:** Português (BR).
- **Categoria:** marquei a sugerida em cada um. **Utility** = serviço de algo que a pessoa já comprou (entrega melhor, custo menor). **Marketing** = promocional. Se a Meta reclassificar um Utility como Marketing, tudo bem — só muda o custo levemente.
- **Variável `{{1}}` = primeiro nome.** A Meta exige um **exemplo** pra aprovar → usar **`Maria`**.
- **Botão:** tipo **Resposta rápida** (Quick reply). O texto do botão é o que a pessoa "responde" ao tocar.
- Evitar CAIXA ALTA e excesso de emoji (1-2 por mensagem passa liso).

---

# PARTE 1 — Esteira da degustação (8 templates)

### 1. `degustacao_boasvindas_d0`  · Utility · precede o Áudio 1 (D0)
> Rede de segurança: no D0 a janela costuma estar aberta (acabou de comprar) e o áudio sai direto. Este template só entra se a janela já estiver fechada.

**Corpo:**
```
Buenas, {{1}}! 🔱 Seja bem-vinda ao Team Chedid. Já tô preparando as orientações dos teus primeiros 30 dias. Toca aqui embaixo que eu te mando o primeiro passo agora mesmo.
```
**Botão (resposta rápida):** `Bora começar! 🔱`

---

### 2. `degustacao_checkin_d2`  · Utility · precede o Áudio 2 (D2)
**Corpo:**
```
Oi {{1}}! Como tão sendo teus primeiros dias no plano? Gravei um retorno rápido pra ti — toca aqui que eu já te mando.
```
**Botão:** `Pode mandar 👍`

---

### 3. `degustacao_dica_sono_d5`  · Utility · precede o Áudio 3 (D5 — sono)
**Corpo:**
```
{{1}}, fechou a semana 1! 🔥 Tenho uma dica sobre uma coisa que trava muito resultado e quase ninguém cuida. Quer que eu te mande o áudio?
```
**Botão:** `Quero a dica`

---

### 4. `degustacao_progresso_d7`  · Utility · precede o Áudio 4 (D7)
**Corpo:**
```
{{1}}, 7 dias! Teu corpo já começou a responder mesmo que a balança ainda não mostre. Quero te explicar o que tá acontecendo aí dentro — toca aqui que eu te mando.
```
**Botão:** `Me explica 💪`

---

### 5. `degustacao_constancia_d10`  · Utility · precede o Áudio 5 (D10 — não compensar)
**Corpo:**
```
Oi {{1}}! Deixa eu te falar do erro nº1 que eu vejo nessa fase (e como não cair nele). É rapidinho — quer que eu te mande?
```
**Botão:** `Manda aí 👊`

---

### 6. `degustacao_dica_agua_d13`  · Utility · precede o Áudio 6 (D13 — água)
**Corpo:**
```
{{1}}, dica rápida que muda tua definição e quase todo mundo erra sem perceber. Posso te mandar o áudio?
```
**Botão:** `Pode mandar 💧`

---

### 7. `degustacao_checkin_d15`  · Utility · precede o Áudio 7 (D15 — metade)
**Corpo:**
```
Oi {{1}}! Chegamos na metade do caminho 🎯 Bora fazer um check-in rápido do teu progresso? Toca aqui que eu já te chamo.
```
**Botão:** `Bora! 🎯`

---

### 8. `degustacao_reta_final_d26`  · Marketing · precede o Áudio 8 (D26 — reta final)
> Aqui já aponta pro "algo especial pros próximos meses" (semente do anual) → sugiro Marketing.

**Corpo:**
```
{{1}}, tamo na reta final dos teus 30 dias! Quero entender tua evolução e já tô preparando uma coisa especial pros teus próximos meses. Toca aqui que eu te mando.
```
**Botão:** `Quero ver 👀`

---

# PARTE 2 — Funil Anual (3 templates)

> Entram depois que o lead migra pro Funil Anual (fim dos 30 dias). Categoria **Marketing** (é conversão/oferta).

### 9. `anual_aquecendo`  · Marketing · etapa "Aquecendo p/ oferta anual"
**Corpo:**
```
{{1}}, teus 30 dias de degustação tão fechando com chave de ouro! Antes de acabar, quero te mostrar o que muda de verdade pra quem segue os próximos meses com a gente. Posso te mandar?
```
**Botão:** `Quero saber`

---

### 10. `anual_oferta`  · Marketing · etapa "Oferta anual feita"
> Reabre a janela pra o Henrique/Gabriel fazerem o fechamento **ao vivo e personalizado** (o close humano continua sendo humano).

**Corpo:**
```
{{1}}, com base na tua evolução eu montei o plano dos teus próximos meses. Quero te apresentar pessoalmente como continuar evoluindo (e uma condição especial pra quem segue agora). Bora conversar?
```
**Botão:** `Bora! Me conta`

---

### 11. `anual_followup`  · Marketing · etapa "Follow-up conversão"
**Corpo:**
```
Oi {{1}}! Ficou alguma dúvida sobre seguir com a gente nos próximos meses? Tô por aqui pra te ajudar a decidir com calma. Toca aqui que a gente resolve rápido.
```
**Botão:** `Tenho uma dúvida`

---

## Resumo pra submissão

| # | Nome | Categoria | Botão |
|---|---|---|---|
| 1 | degustacao_boasvindas_d0 | Utility | Bora começar! 🔱 |
| 2 | degustacao_checkin_d2 | Utility | Pode mandar 👍 |
| 3 | degustacao_dica_sono_d5 | Utility | Quero a dica |
| 4 | degustacao_progresso_d7 | Utility | Me explica 💪 |
| 5 | degustacao_constancia_d10 | Utility | Manda aí 👊 |
| 6 | degustacao_dica_agua_d13 | Utility | Pode mandar 💧 |
| 7 | degustacao_checkin_d15 | Utility | Bora! 🎯 |
| 8 | degustacao_reta_final_d26 | Marketing | Quero ver 👀 |
| 9 | anual_aquecendo | Marketing | Quero saber |
| 10 | anual_oferta | Marketing | Bora! Me conta |
| 11 | anual_followup | Marketing | Tenho uma dúvida |

**Prioridade de aprovação:** submeter primeiro os **8 da Parte 1** (destravam a esteira da degustação, que é o que roda primeiro). Os 3 do Funil Anual podem ir logo em seguida — a Meta aprova cada um em minutos a ~1-2 dias.

**Todos usam 1 variável (`{{1}}` = primeiro nome), exemplo `Maria`.** Na hora de montar o bot, o Kommo preenche o `{{1}}` sozinho com o nome do lead.
</content>
