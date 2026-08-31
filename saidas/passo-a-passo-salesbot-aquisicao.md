# Bot AQUISIÇÃO no Kommo · manual técnico

> Estado: **montado e rodando desde 31/08/2026**. Funil Degustação.
> A copy completa está em `comercial/fluxo-aquisicao-v2.md`.
> Este arquivo guarda o **como funciona por dentro**, as armadilhas do Salesbot que a gente
> descobriu na marra, e o que ainda falta.

---

## As 8 armadilhas do Salesbot (leia antes de mexer)

Custaram tempo. Estão aqui pra não custarem de novo.

**1. Campo de lista só grava se o valor for ESCOLHIDO da lista.**
Se você digitar o texto à mão no `Definir campo`, o bloco fica bonito no canvas, o bot executa sem erro e **não grava nada**. Falha totalmente silenciosa. Foi o que deixou OBJETIVO, TREINO e TRAVA vazios no primeiro teste completo, e o diagnóstico saiu como *"Você quer , , e o que te trava é ."*.
👉 Sempre abrir o seletor e clicar na opção.

**2. Os blocos vêm apontando pra `main contact`, não pro `lead`.**
Todo `Definir campo`, `Gerenciar tags` e `Mudar usuário resp.` nasce mirando o contato. Nossos campos vivem no **lead**. Trocar em cada bloco.

**3. Não existe botão de variável. A macro é digitada.**
Sintaxe: `{{lead.cf.ID}}`. Funciona em mensagem, validado ao vivo no Lite.
Na **pré-visualização** ela aparece como `[Lead: OBJETIVO]` porque o preview não tem lead ligado. Só a execução real mostra o valor.

**4. O editor não salva sozinho.** Botão `Salvar` no topo. Texto digitado e não salvo se perde.

**5. Bot desativado não aparece na lista do `/`.** Pra testar manualmente pelo cartão do lead, ele precisa estar ativo.

**6. Resposta de teste tem que vir do celular.**
Mensagem digitada dentro do Kommo sai como **mensagem da empresa**, não conta como "Cliente enviar", e ainda **para o bot** (gerente respondeu). O Kommo é onde você observa, não onde você responde.

**7. `Mensagem do cliente` resolve a ÚLTIMA mensagem recebida.**
Se você usar logo depois de fazer uma pergunta, vai gravar a resposta *anterior*. Precisa de um bloco de Condição no meio só pra esperar. É por isso que existe o bloco com valor `zzz` no ramo "outra" da etapa 5.

**8. WhatsApp Lite não envia lista interativa nem botão.**
O bloco `Mensagem em Lista (WhatsApp)` existe na paleta mas é recurso da API oficial. Por isso o bot usa número digitado. Número digitado funciona nos dois, então se um dia migrar pra oficial, a lista vira melhoria, não remontagem.

---

## O que o editor oferece

| Recurso | Situação |
|---|---|
| `Enviar mensagem` | tem saída de erro "Falha ao enviar a mensagem" |
| `Enviar mensagem interna` | **ainda não usado.** Candidato pra empurrar o resumo pro Gabriel |
| `Condição` | um bloco segura vários ramos, cada um com saída própria, mais "Nenhuma das condições" |
| Timeout / "sem resposta" | **não existe** no bloco de Condição. Por isso o follow-up é um bot separado |
| `Ação → Definir campo` | grava campo (ver armadilha 1) |
| `Ação → Gerenciar tags` | tags, criadas na hora em que você digita o nome |
| `Ação → Mudar o status do lead` | move de etapa |
| `Ação → Mudar usuário resp.` | atribui responsável |
| `Ação → Adicionar tarefa` | Prazo · Usuário · Tipo · Comentário. **Comentário não tem botão de variável** (macro digitada não foi testada ali) |
| Parar o bot | não existe ação. O bot encerra quando o ramo acaba sem próximo passo |
| `...` do bloco | **Duplicar** e **Iniciar pré-visualização aqui** |

---

## O gatilho

**Bot AQUISIÇÃO:**
```
Categoria:  GATILHOS DO PIPELINE
Regra:      Quando lead movido ou criado em uma etapa de funil
Status:     DEGUSTAÇÃO · Leads Entrantes
Horário:    sempre
```

Por que do pipeline e não de conversa: amarra o bot ao **funil**, não ao canal. Cliente ativo que manda mensagem pra Kami está no Funil Suporte, então não entra em Leads Entrantes e não dispara nada. O gatilho de conversa (*"quando o chat é iniciado por mensagem de entrada em qualquer canal"*) dispararia nele, porque ele também é "uma conversa nova".

> 🔴 **NUNCA marcar "Aplicar o gatilho à todos os leads já nesta etapa".**
> Se marcar, todo mundo parado em Leads Entrantes recebe *"Oi! Aqui é o Gabriel..."* de uma vez. São leads antigos, de meses atrás. Vira disparo em massa não solicitado, com risco de bloqueio no WhatsApp e de queimar a base.

> ⚠️ **"movido ou criado"**: arrastar um lead pra Leads Entrantes na mão **roda o bot nele**. É útil pra reprocessar alguém de propósito, e é um tiro no pé se for sem querer.

**Bot AQUISIÇÃO Follow-up:**
```
Categoria:  GATILHOS DE CONVERSAÇÃO
Regra:      3 horas após a última mensagem recebida
Status:     DEGUSTAÇÃO · Apresentando
Excluir:    leads com a tag FALAR-COM-HUMANO
Opção:      "parar o bot se o cliente responder" LIGADA
```

---

## Estrutura de blocos

```
Iniciar robô
  └ 18/19  abertura (2 mensagens)
     └ 20  Condição: só "0" sai · qualquer outra coisa continua
        └ 22 tag BOT-INICIADO · 23 ETAPA_BOT=0 · 24 move p/ Apresentando
           └ 25/26  etapa 1 OBJETIVO   → 35 ETAPA_BOT=1
              └ 43/44 etapa 2 TREINO   → 53 ETAPA_BOT=2
                 └ etapa 3 TRAVA (57)  → 71 ETAPA_BOT=3
                    └ 75/76 etapa 4 SINTOMA → 84 ETAPA_BOT=4
                       └ 92/99 etapa 5 CONDICAO → 114 ETAPA_BOT=5
                          └ 119 diagnóstico → 124 ETAPA_BOT=6
                             └ prova social + pergunta + Condição
                                └ 125/126/127 oferta → 128 Condição
                                   ├ 129 link anual ┐
                                   └ 131 link mensal┴→ 133/135/136/137 handoff

Escape (cadeia solta, todas as etapas apontam pra ela)
  12 tag → 13 responsável → 14 tarefa → 15 mensagem → fim
```

**Mapa dos blocos de gravação** (útil quando um campo parar de gravar):
```
OBJETIVO  27 (ramo1) · 36 (ramo2) · 30 (ramo3) · 31 (ramo4)
TREINO    45 · 47 · 48
TRAVA     58 (r1) · 60 (r2) · 66 (r3) · 59 (r4) · 62 (r5)
SINTOMA   93 · 94 · 95 · 96 · 97 · 98
CONDICAO  100 · 102 · 103 · 104 · 105 · 106   ·   CONDICAO_OUTRA 117
```
Os números não seguem ordem lógica porque o Kommo numera na ordem de criação e os ramos foram duplicados. **Confie no texto do bloco, não no número.**

---

## Como testar

1. Cria um **lead novo** (não reaproveita, senão sobra valor da rodada anterior e você não sabe o que é novo)
2. Abre o cartão do lead, clica no campo de mensagem, digita `/` e escolhe **AQUISIÇÃO**
3. Responde **pelo celular**, no WhatsApp (armadilha 6)
4. Confere o cartão no fim

**Checklist:**
```
[ ] OBJETIVO, TREINO, TRAVA, SINTOMA e CONDICAO preencheram?
[ ] ETAPA_BOT parou no número certo?
[ ] No ramo "outra", CONDICAO_OUTRA guardou o texto e não o "6"?
[ ] O diagnóstico veio com as palavras da lead?
[ ] A frase ficou legível, sem maiúscula no meio nem concordância quebrada?
[ ] Lead foi pra "Muito quente" e gerou tarefa?
[ ] Os dois links abrem e o cupom BEMVINDO150 funciona no checkout?
```

**Conferir pela API** (mais rápido que abrir o cartão):
```bash
set -a; . ./.env; set +a
curl -s -H "Authorization: Bearer $KOMMO_LONG_LIVED_TOKEN" \
  "$KOMMO_BASE_URL/api/v4/leads/<ID_DO_LEAD>"
```

---

## Pendências

**Bloqueia a operação de verdade**
1. **Número comercial de aquisição.** Hoje o bot roda no número da Kami (48 99212-2712), o mesmo dos clientes ativos.
2. **Recortar o `Canais: Todos`** dos blocos de mensagem pro canal de aquisição, quando existir.

**Melhora muito e é rápido**
3. **Usuário do Gabriel no Kommo.** Só o Henrique existe como responsável, então toda tarefa do bot cai nele. Os blocos usam `Usuário responsável atual`, então isso se corrige sozinho no dia em que o usuário existir.
4. **`Enviar mensagem interna` com o resumo do diagnóstico.** Como o Gabriel atende pelo WhatsApp Web e não abre o Kommo, o diagnóstico fica preso num cartão que ninguém lê. O resumo precisa ser **empurrado**, não consultado.

**Depois**
5. **Follow-up que retoma da pergunta exata** usando o `ETAPA_BOT`. Hoje ele só traz a pessoa de volta e entrega pro humano.
6. **Melhorias de copy** que o Gabriel deixou pro segundo momento.
7. **Desligar de vez o "Degustação BOT" antigo**, se ainda estiver ativo.
8. Campo `URGENCIA` ficou órfão depois da virada de oferta. Manter ou apagar.
