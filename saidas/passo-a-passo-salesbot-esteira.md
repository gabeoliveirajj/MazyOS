# Passo a passo: montar a esteira de áudios no Salesbot

> Escopo: **só o número da Kami (99212-2712) / Funil Suporte.** O bot que envia os 8 áudios da degustação, D0 a D26.
> Não mexe no número comercial (aquisição) — isso é outra missão.

---

## Pré-requisitos (ter na mão antes de começar)

- [ ] Os **8 áudios em `.ogg`**: em `dados/audios-degustacao/ogg-prontos/` (1-D0-boasvindas.ogg ... 8-D26-retafinal.ogg).
  ✅ **RESOLVIDO (o pulo do gato):** pra o áudio chegar como **NOTA DE VOZ** e não como documento, dentro do passo do bot, no anexo do áudio, marcar a opção **"Converter em áudio"**. Com isso o Salesbot nativo manda nota de voz normal, sem Wazzup nem híbrido, sem custo. Usar os `.ogg` de `ogg-prontos/` e marcar **"Converter em áudio"** em CADA um dos 8. (Detalhe: `.opus` sem essa opção chega como documento.)
- [ ] Os **8 textos** (resumos): em `saidas/resumos-audios-degustacao.md`, já aprovados pelo Henrique.
- [ ] Funil **Suporte** criado ✅ (etapas: Onboarding D0 · Em acompanhamento · Reta final D26 · Cliente anual).
- [ ] WhatsApp **Lite conectado no 99212-2712** ✅ (áudio testado ✅).
- [ ] Confirmar que o teu plano do Kommo **tem Salesbot** (é recurso dos planos pagos mais altos). Se o menu de bots não aparecer, é isso.

---

## Passo 1: criar o bot

1. No Kommo: **Automações / Salesbot** (ou "Bots", no menu de automações do funil).
2. **Criar bot** novo. Nome: **Esteira Degustação**.
3. Vai abrir o editor visual (blocos que você encadeia).

## Passo 2: montar os 8 toques (a sequência)

Cada toque são 2 blocos "Enviar mensagem" (texto + áudio), seguidos de um bloco "Pausa". Repete 8 vezes com estes conteúdos e tempos:

| # | Dia | Bloco texto (resumo) | Bloco áudio | Pausa depois |
|---|---|---|---|---|
| 1 | D0 | resumo áudio 1 | Audio Chedid - 1 | 2 dias |
| 2 | D2 | resumo áudio 2 | Audio Chedid - 2 | 3 dias |
| 3 | D5 | resumo áudio 3 | Audio Chedid - 3 | 2 dias |
| 4 | D7 | resumo áudio 4 | Audio Chedid - 4 | 3 dias |
| 5 | D10 | resumo áudio 5 | Audio Chedid - 5 | 3 dias |
| 6 | D13 | resumo áudio 6 | Audio Chedid - 6 | 2 dias |
| 7 | D15 | resumo áudio 7 | Audio Chedid - 7 | 11 dias |
| 8 | D26 | resumo áudio 8 | Audio Chedid - 8 | 1 dia |

Pra cada linha:
1. Bloco **Enviar mensagem** → tipo **texto** → cola o resumo do áudio.
2. Bloco **Enviar mensagem** → tipo **arquivo/áudio** → sobe o arquivo do áudio.
3. Bloco **Pausa** → o tempo da coluna.

> Dica visual (opcional): logo após o 1º áudio, adiciona um bloco "mudar etapa" pra **Em acompanhamento**; no D26, pra **Reta final (D26)**. Ajuda a Kami a ver em que ponto cada cliente está.

## Passo 3: no fim, jogar pro Funil Anual

Depois da pausa de 1 dia do D26 (ou seja, no **D27**):
- Bloco **mudar de funil/etapa** → **Funil Anual** → etapa **Saiu da degustação**.

Isso encerra a esteira e entrega o lead pro fluxo do anual.

## Passo 4: o gatilho (quando o bot dispara)

No **Funil Suporte**, painel de automações da etapa **Onboarding (D0)**:
- **Quando o lead entra em "Onboarding (D0)" → iniciar o bot "Esteira Degustação".**
- **Condição de segurança:** só se **NÃO tiver a tag `LEGADO-MANUAL`**. (Isso blinda os 51 clientes antigos que já migramos.)

## Passo 5: a pausa no atendimento (bot não atropela a Kami)

Objetivo: se o cliente responde no meio, o áudio não cai em cima da conversa.
- Como os blocos têm **pausa de dias** entre os envios, o bot já só dispara no dia agendado (não fica mandando áudio a toda hora).
- Pra reforçar: na configuração de iniciar o bot, ver a opção **"parar o bot se o cliente responder"**. A gente decide o comportamento exato quando estiver no editor (te explico as opções na hora).

## Passo 6: testar com 1 lead antes de soltar

1. Cria um lead de teste no Funil Suporte com o **teu WhatsApp**, entrando na etapa **Onboarding (D0)**.
2. Confirma: chegou o texto 1 + o áudio 1?
3. Pra não esperar dias, dá pra encurtar as pausas (ex: minutos) num bot de teste e ver a sequência inteira rodar.
4. Deu certo? Volta as pausas pros dias reais e libera.

---

## Como a gente faz

Esse tipo de bot é mais fácil de montar junto do que lendo. Sugestão: você abre o Salesbot, e a gente vai **bloco por bloco**, você me manda print de cada tela e eu te digo exatamente onde clicar. Assim não tem erro.
</content>
