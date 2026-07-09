# Blueprint CRM — Automação da Degustação + Funil Anual

> Para a reunião com o Henrique. Autor: Gabriel (Inside Sales). Jul/2026.
> Fecha os 2 furos que ainda estavam abertos no diagnóstico do funil:
> **(1)** a cadência de follow-up rodando sozinha e **(2)** o handoff degustação → anual, que hoje é manual e some sem rastro.

---

## 1. O que muda, em uma frase

Hoje o Henrique manda os áudios de acompanhamento **na mão** durante os 30 dias e tenta fechar o anual "no último dia". A proposta:

- **Degustação vira uma esteira automática de experiência** (áudios pré-gravados disparando na cadência certa) → escala sem depender do tempo do Henrique.
- **Quem termina os 30 dias cai sozinho num Funil Anual novo**, que é a máquina dedicada de converter degustação → anual (o número mais importante do negócio: os ~30%).

Resultado: o Henrique para de ser o gargalo do follow-up, e a gente passa a **medir** a conversão anual etapa por etapa em vez de "achar".

---

## 2. Arquitetura dos dois funis

```
  ┌─────────────────────── FUNIL DEGUSTAÇÃO (já existe) ───────────────────────┐
  │  Leads Entrantes → Apresentando → Follow-up → Muito quente                  │
  │        ↓ (comprou R$197)                                                    │
  │  degustação ativo  ← AQUI roda a esteira de ÁUDIOS (D0 → D24)               │
  └────────────────────────────────┬───────────────────────────────────────────┘
                                    │  ~D25-28: bot move automático
                                    ▼
  ┌──────────────────────── FUNIL ANUAL (novo — no ar) ────────────────────────┐
  │  Saiu da degustação → Aquecendo p/ oferta → Oferta anual feita              │
  │        → Negociação/objeção → Follow-up conversão                           │
  │        → Efetivou Anual (ganho)  |  Não efetivou anual (perda + motivo)     │
  └────────────────────────────────────────────────────────────────────────────┘
```

**Divisão de trabalho entre os funis:**
- **Degustação** = entregar uma experiência excelente nos 30 dias (áudios de valor, engajamento, prova social). Aqui a gente **não vende duro** — planta a semente.
- **Funil Anual** = a partir do fim da degustação, a esteira de **conversão** pro plano principal (oferta, objeção, follow-up, ganho/perda).

Isso mantém a métrica limpa: `degustação → anual` fica isolada no Funil Anual, medível etapa a etapa.

---

## 3. Cadência de áudios da DEGUSTAÇÃO (esteira automática)

> Roda no estágio **`degustação ativo`** (id `102232084`). **Os 8 áudios já existem** — o Henrique já mandou todos (transcritos em [transcricao-audios-degustacao.md](transcricao-audios-degustacao.md)). A esteira de experiência está **pronta pra programar**; é só definir o dia de cada um.

| Dia sugerido | Áudio (já gravado) | O que é | Puxa resposta? |
|---|---|---|---|
| **D0** | Áudio 1 | Boas-vindas oficial — 30 dias, experiência Team Chedid, shape slim, "confie no teu nutri", aderência | Sim |
| **D2** | Áudio 2 | Check-in dos primeiros dias — "conseguiu começar o plano? teve dúvida?" | **Sim (pergunta direta)** |
| **D5** | Áudio 3 | Dica: **sono** (recuperação, cortisol, GH, 7-9h) | Sim |
| **D7** | Áudio 4 | Reforço 7 dias — corpo já reage, menos inchaço, "não se apega à balança" | Sim |
| **D10** | Áudio 5 | **Constância** — não compensar deslize com jejum, "feito melhor que perfeito" | Sim |
| **D13** | Áudio 6 | Dica: **água** (35-40ml/kg, retenção, definição) | Sim |
| **D15** | Áudio 7 | Metade do caminho — check-in de 3 perguntas | **Sim (pergunta direta)** |
| **D26** | Áudio 8 | Reta final — pede fotos + feedback, **teasa "uma coisa especial pros próximos meses"** | **Sim (feedback)** |

Os dias são sugestão minha pra distribuir bem nos 30 dias — **o Henrique confirma o dia certo de cada um** (vários áudios citam "semana 1", então talvez ele concentre mais cedo). Depois do **Áudio 8 (D26)**, o bot **move o lead pro Funil Anual** (seção 5), onde a oferta do anual acontece.

> **Nota de qualidade da transcrição:** o modelo escreveu "Team Shady" (= Team Chedid), "Buenas/Boenas" (a saudação dele) e "renina-angiotensina" saiu torto. Conteúdo 100% legível, só revisar nomes próprios se for reaproveitar como texto.

### ⚠️ A regra dos 24h da API oficial (ponto nº1 pra validar)

Com **WhatsApp API oficial (Meta)**, só dá pra mandar mensagem livre (incluindo **áudio**) **dentro de 24h** da última mensagem que a pessoa mandou. Passou de 24h, só **template de texto aprovado** — e **template não aceita áudio**.

Como a gente resolve (sem quebrar a esteira):
1. **Todo toque tem uma micro-pergunta** ("me manda um 🔱", "como tá indo?"). Quando a pessoa responde, **reabre a janela de 24h** e o áudio flui normal.
2. Se a pessoa ficar em silêncio e a janela fechar, o bot manda primeiro um **template de texto curto** (aprovado) pra reabrir a conversa; quando ela responde, o áudio da fase dispara.
3. Comprou a degustação = acabou de interagir → **a janela do D0/D1 já está aberta**, o áudio de boas-vindas sai na hora.

> Tradução prática pro Henrique: os áudios são a alma, mas a gente precisa aprovar **~4-5 templates de texto** na Meta pra garantir que a esteira não morra quando a pessoa some. Eu cuido dessa parte.

---

## 4. Inventário de áudios — o que já tem e o que falta

Os 8 áudios do Henrique **cobrem toda a experiência da degustação (D0→D26)**. Não falta gravar nada da esteira. O **único gap** está na hora de vender o anual:

- ✅ **Áudios 1 a 8** — esteira de experiência completa, prontos pra programar.
- ⬜ **Áudio da OFERTA do anual** — não existe. O Áudio 8 só **prepara** ("tô preparando uma coisa especial"); o fechamento hoje o Henrique faz **ao vivo, personalizado pelo feedback da pessoa** (é assim que ele converte os ~30%).

**Decisão pro Henrique (seção 7):** o fechamento do anual continua **ao vivo/personalizado** (mantém a taxa que já funciona) ou ele grava **1 áudio "coringa" de pitch do anual** pra automatizar 100%? Recomendação: **manter o close humano** — é o momento de maior valor e o áudio 8 já deixa isso claro na fala dele ("algo personalizado pros próximos meses"). O CRM automatiza tudo **até** a oferta e entrega o lead quentíssimo pro Henrique/Gabriel fecharem.

---

## 5. Funil Anual (novo — já criado no Kommo)

**Pipeline `Funil Anual` (id `14045616`).** Etapas ao vivo:

| Etapa | ID | Função |
|---|---|---|
| Saiu da degustação | `108416364` | Landing da entrada automática (fim dos 30 dias) |
| Aquecendo p/ oferta anual | `108416368` | Prova social + preparação (áudio "pré-transição") |
| Oferta anual feita | `108416372` | Pitch do anual entregue (áudio + texto: 12x R$147) |
| Negociação / objeção | `108416376` | Quebra de objeção (Playbook, Parte 3) |
| Follow-up conversão | `108416380` | Cadência pós-oferta pra quem não decidiu na hora |
| Efetivou Anual (ganho) | `142` | Fechou o anual 🎉 |
| Não efetivou anual (perda) | `143` | Não fechou → registrar **motivo de perda** |

*(Os dois últimos aparecem como "Closed - won/lost" — dá pra renomear na UI em 10s; a API trava o rename dos estágios de sistema.)*

**Gatilho de entrada (automático):** no D24-25 da degustação, o bot da degustação executa **"mudar pipeline e etapa" → Funil Anual / Saiu da degustação**. Ao entrar, um segundo bot (Digital Pipeline) começa a cadência de conversão.

**Cadência de conversão (dentro do Funil Anual):**
- **Aquecendo:** áudio de pré-transição + 1 prova social forte (resultado real de quem virou anual).
- **Oferta:** o pitch do anual (áudio "pitch do anual" + texto com a condição — 12x R$147). Move pra "Oferta anual feita".
- **Sem resposta / indeciso:** entra na cadência de follow-up (usar D1/D2/D3/D5/D7 do [playbook](playbook-comercial-reativacao-team-chedid.md), Parte 4).
- **Objeção:** move pra "Negociação/objeção", entra o **humano** (Gabriel/Henrique) com o playbook de quebra de objeção. Fechamento é humano, não bot.
- **Fechou:** move pra Efetivou Anual (ganho). **Não fechou:** move pra Não efetivou, com **motivo de perda** obrigatório (já ligado).

---

## 6. Checklist de configuração no Kommo (o que falta montar)

| # | Tarefa | Onde | Quem | Status |
|---|---|---|---|---|
| 1 | Funil Anual criado (pipeline + etapas) | API | Gabriel | ✅ feito |
| 2 | Renomear "Closed won/lost" → "Efetivou / Não efetivou" | UI | Gabriel | ⬜ 10s |
| 3 | ~~Gravar os 8 áudios~~ — **já entregues pelo Henrique** ✅ | — | Henrique | ✅ feito |
| 4 | Definir o dia de cada áudio na cadência (seção 3) | — | Henrique + Gabriel | ⬜ 5 min |
| 5 | Aprovar ~4-5 templates de texto na Meta | Kommo/Meta | Gabriel | ⬜ |
| 6 | Montar o **Salesbot da degustação** (esteira D0→D26 + move p/ Funil Anual) | UI (Salesbot) | Gabriel | ⬜ |
| 7 | Montar o **bot de conversão** do Funil Anual (Digital Pipeline) | UI | Gabriel | ⬜ |
| 8 | Testar ponta a ponta com 1 lead de teste | UI | Gabriel | ⬜ |

**Dependência crítica:** os áudios (o que costuma travar) **já estão prontos**. O gargalo agora é só a **aprovação dos templates na Meta (~1-2 dias)** — dá pra iniciar já.

---

## 7. Pra decidir na reunião

1. **Confirmar a regra dos 24h** e o uso de templates de texto pra reabrir janela (ponto técnico central).
2. **Fechar o dia de cada um dos 8 áudios** na cadência (a sugestão da seção 3 é ponto de partida).
3. **O close do anual: ao vivo ou gravado?** Único gap — o Henrique hoje fecha ao vivo, personalizado. Recomendação: manter humano e deixar o CRM entregar o lead quente na etapa "Oferta anual feita". Se ele quiser 100% automático, grava **1 áudio** de pitch do anual.
4. Onde cortar o handoff pro Funil Anual: sugestão **D26** (após o Áudio 8), com margem antes dos 30 dias acabarem.
