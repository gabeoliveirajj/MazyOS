# Fluxo de Aquisição v2 · Bot filtro da Consultoria Online

> Bot **AQUISIÇÃO**, montado no Kommo Salesbot e **rodando desde 31/08/2026**.
> Funil Degustação, gatilho na etapa Leads Entrantes. Quem assina: **Gabriel**, em 1ª pessoa.
> Guia técnico de montagem e manutenção: `saidas/passo-a-passo-salesbot-aquisicao.md`.
>
> ⚠️ **A fonte de verdade da copy é o bot no Kommo.** Este arquivo foi conferido contra os
> prints da montagem, mas algumas devolutivas foram reescritas pelo Gabriel direto no editor
> e aparecem truncadas nos prints. Onde houver divergência, vale o que está no Salesbot.

---

## O que este bot faz

Ele não apresenta a empresa e pede uma decisão. Ele **investiga o caso e devolve leitura**, e a oferta vira consequência do que o próprio lead contou.

A mecânica central é uma troca declarada na abertura: *"são 5 perguntas, e no final eu te devolvo uma leitura do teu caso"*. Cada número que o lead manda volta como um pedaço de diagnóstico dele, não como o próximo bloco institucional.

**Estrutura:**
```
abertura → 5 perguntas → diagnóstico → prova social + interação → oferta → link → handoff
```

**Regras fixas:**
1. Toda mensagem termina em pergunta com opções numeradas.
2. Cada resposta grava em campo do Kommo. O filtro só vale se o dado sobreviver ao bot.
3. `0` sempre disponível: falar direto com o Gabriel. Texto livre também cai no escape.
4. O preço só aparece depois do diagnóstico e da prova social.
5. Nenhuma rota termina no bot.

---

## Etapa 0 · Abertura

> Oi! Aqui é o Gabriel, do time do Nutri Chedid 🔱
>
> Antes de te passar valores, deixa eu entender teu caso. A conduta muda bastante de pessoa pra pessoa, e se eu já jogar um preço aqui vai ser igual a qualquer dieta de gaveta.

*(mensagem separada)*

> São 5 perguntas rápidas, leva uns 2 minutos. No final eu te devolvo uma leitura do teu caso e te falo qual é a melhor rota pra você.
>
> Bora?
>
> Se preferir falar comigo direto, é só mandar 0 👇

**Condição:** só `0` sai pro escape. **Qualquer outra resposta continua.** Na abertura muita gente responde "bora", "sim", "oi" em vez de digitar número, e mandar essas pessoas pro escape mataria metade dos leads na primeira mensagem.

Depois: tag `BOT-INICIADO` · `ETAPA_BOT = 0` · move pra **Apresentando**.

---

## Etapa 1 · Objetivo

> Boa. Então primeira pergunta: qual é teu objetivo hoje?
>
> 1 - Emagrecer e reduzir medidas
> 2 - Recomposição: secar gordura e ganhar músculo
> 3 - Definir e afinar a cintura, o peso já está ok
> 4 - Ganhar massa e volume em glúteo e perna

| Resp | Grava em `OBJETIVO` | Devolutiva |
|---|---|---|
| 1 | emagrecer e reduzir medidas | Entendi. Quem chega com esse objetivo quase sempre já tentou cortar comida, foi bem por um tempo e depois travou. Isso tem explicação e a gente chega nela em 2 perguntas 👇 |
| 2 | recomposição corporal | Esse é o objetivo mais comum aqui dentro e o que eu mais vejo gente errando por aí. Recomposição não se resolve comendo menos, se resolve ensinando o corpo a usar energia. Já te explico 👇 |
| 3 | definir e afinar a cintura | Aí você tá falando do Shape Slim: cintura fina, barriga seca e volume nos pontos certos 🔱 |
| 4 | ganhar massa e volume | Show. Volume não vem só do treino, vem do corpo conseguir usar o que você come pra construir músculo. Segue comigo 👇 |

Junção: `ETAPA_BOT = 1`

---

## Etapa 2 · Treino

> E hoje, como está teu treino?
>
> 1 - Musculação 3x por semana ou mais
> 2 - Treino 1 ou 2x, bem irregular
> 3 - Estou parada e quero recomeçar

| Resp | Grava em `TREINO` | Devolutiva |
|---|---|---|
| 1 | treina 3x ou mais por semana | Ótimo, então o estímulo já existe. E olha, quando a pessoa treina firme e mesmo assim não vê resultado, dificilmente o problema é o treino. Quase sempre é a alimentação que não está acompanhando. |
| 2 | treina 1 ou 2x por semana | Dá pra trabalhar bem assim. E tem uma coisa que quase ninguém liga: treino irregular costuma ser falta de energia, e falta de energia vem da comida. Ajusta um, o outro anda junto. |
| 3 | está parada no treino | Tranquilo, muita gente aqui começou parada. A dieta certa é o que devolve disposição pra você conseguir treinar sem se arrastar. |

Junção: `ETAPA_BOT = 2`

---

## Etapa 3 · O que trava

A pergunta mais importante do filtro. É onde os 3 pilares do método entram **aplicados ao caso**, em vez de apresentados soltos.

> Agora vem a que mais me ajuda a entender teu caso.
>
> O que costuma acontecer quando você tenta?
>
> 1 - Já fiz dieta, funcionou um tempo e voltou tudo
> 2 - Treino certinho mas o corpo não muda
> 3 - Usei caneta e travei ou voltei a engordar
> 4 - Nunca fiz nada estruturado, sempre no achismo
> 5 - Já passei por vários nutris e não engatei

| Resp | Grava em `TRAVA` | Devolutiva |
|---|---|---|
| 1 | o efeito sanfona | Clássico. E não é falta de força de vontade, viu. Chama adaptação metabólica: o corpo se ajusta à restrição e para de responder. Por isso aqui a gente não corta comida, a gente reorganiza. Esse é o pilar da **Sincronia Metabólica**. |
| 2 | treinar e o corpo não mudar | Isso tem nome: falta de **responsividade fisiológica**. Quando intestino, inflamação e eixos hormonais estão desregulados, o corpo simplesmente não responde ao estímulo, por melhor que seja o treino. Fazer ele voltar a responder é o primeiro pilar do método. |
| 3 | o rebote da caneta | A caneta tira a fome, só que não ensina nada pro teu corpo. Quando ela sai, o corpo volta pro que era, muitas vezes com menos músculo do que antes. Tem um Protocolo Canetas Emagrecedoras justamente pra essa transição. |
| 4 | nunca ter tido um plano estruturado | Então tenho uma boa notícia: você nunca teve um plano de verdade. Quem chega assim costuma ter o resultado mais rápido, porque tem muita coisa simples pra organizar antes de precisar de estratégia fina. |
| 5 | não engatar com nutri nenhum | Olha, na maioria das vezes o problema não foi o nutri. Foi a dieta não caber na vida da pessoa. Quando ela briga com a rotina, com o trabalho e com a comida da casa, ninguém desiste da dieta, desiste do processo todo. Dieta boa é a que você consegue sustentar. |

Junção: `ETAPA_BOT = 3`

---

## Etapa 4 · Sintomas

Escolha única. O Salesbot não tem múltipla escolha de verdade, e uma dor nomeada já prova individualização.

> E além do shape, o que mais te incomoda hoje?
>
> 1 - Inchaço e retenção
> 2 - Ansiedade e compulsão à noite
> 3 - Cansaço, acordo sem disposição
> 4 - Intestino irregular, gases
> 5 - TPM forte, oscilação hormonal
> 6 - Nenhum desses, é o shape mesmo

| Resp | Grava em `SINTOMA` | Devolutiva |
|---|---|---|
| 1 | inchaço e retenção | Inchaço costuma ser dos primeiros a melhorar, e é o que mais muda a foto. Podemos montar um planejamento contra inchaço e retenção específico pro seu caso. |
| 2 | ansiedade e compulsão à noite | Esse é o que mais derruba dieta, e não tem nada a ver com força de vontade. Podemos montar um planejamento focado em zerar esses sintomas, que mexe em comida, horário e no que sustenta teu humor. |
| 3 | cansaço | Cansaço quase sempre é o corpo recebendo energia na hora errada. Podemos montar um planejamento focado na sua disposição e energia pra você se livrar dessa sensação. |
| 4 | intestino irregular | Intestino é base de tudo, porque se ele não vai bem você não absorve direito o que come. Podemos montar um planejamento focado em regular seu intestino. |
| 5 | TPM forte | TPM forte mexe direto com fome, retenção e humor, e isso atrapalha o shape o mês inteiro. Esse é um cenário que resolvemos todos os dias por aqui. |
| 6 | nenhum | Beleza, então a gente foca 100% no shape e no que sustenta ele. |

> 📌 **Decisão de 25/08/2026:** os **nomes dos protocolos saíram** das devolutivas e a mensagem comum *"São 12 protocolos no total..."* foi removida. O texto passou a falar em "planejamento" em vez de "protocolo" e "conduta".
> Trade-off registrado: nomear o protocolo era a prova mais concreta de individualização do fluxo. "Podemos montar um planejamento focado em" é mais suave e mais genérico.

Junção: `ETAPA_BOT = 4`

---

## Etapa 5 · Condição de saúde

> Tem alguma dessas condições?
>
> 1 - Hipotireoidismo ou Hashimoto
> 2 - Resistência à insulina ou pré-diabetes
> 3 - Uso anticoncepcional
> 4 - Lipedema
> 5 - Nenhuma delas
> 6 - Outra (me conta qual)

| Resp | Grava em `CONDICAO` |
|---|---|
| 1 | hipotireoidismo ou Hashimoto |
| 2 | resistência à insulina |
| 3 | uso de anticoncepcional |
| 4 | lipedema |
| 5 | nenhuma |
| 6 | outra |

**Ramos 1 a 4 convergem numa devolutiva só:**
> Esse é o tipo de coisa que derruba dieta genérica.
>
> Aqui o seu planejamento é montado considerando isso, e se você tiver exames recentes eles entram na leitura do teu caso.

**Ramo 5:**
> Beleza, isso simplifica bastante o planejamento.

**Ramo 6 é o único com mecânica própria:**
```
1. grava CONDICAO = outra
2. Enviar mensagem: "Me conta rapidinho qual é?"
3. Condição de espera (valor impossível, tipo "zzz")   ← segura o fluxo
4. grava CONDICAO_OUTRA = Mensagem do cliente
```
O bloco 3 não testa nada. Ele existe só pra o bot esperar a pessoa escrever. **Sem ele, o `CONDICAO_OUTRA` gravaria o "6"**, porque "Mensagem do cliente" resolve a última mensagem recebida.

Junção: `ETAPA_BOT = 5`

---

## Diagnóstico

Mensagem única, igual pra todo mundo, montada com macro:

> Fechado, já consigo te dar uma leitura 👇
>
> Você quer `{{lead.cf.3909605}}`, `{{lead.cf.3909607}}`, e o que te trava é `{{lead.cf.3909609}}`.
>
> Pelo que você me contou, o que falta não é esforço, é direção. A parte difícil você já faz. Falta o corpo receber o estímulo certo, na ordem certa.
>
> Com um planejamento montado pro teu caso, o que costuma acontecer nas primeiras 4 a 8 semanas:
>
> ✅ 2 a 5 cm a menos de cintura
> ✅ desinchaço forte já nas primeiras semanas
> ✅ mais disposição e menos compulsão à noite
> ✅ corpo mais leve e mais seco no espelho
>
> São mais de 3.000 pacientes em mais de 20 países e 86% de renovação. As pessoas ficam porque funciona 🔱

Usa **só OBJETIVO, TREINO e TRAVA**. O SINTOMA e a CONDICAO ficaram de fora de propósito: quem responde "nenhum" e "nenhuma" faria a frase sair quebrada, e aí precisaria de duas versões e uma condição extra.

Depois: `ETAPA_BOT = 6`

---

## Prova social e interação

Acrescentado em 31/08/2026 para quebrar a sequência de mensagens e cobrar um micro compromisso antes do preço.

> E antes de falar de valores, quero te mostrar uma coisa.
>
> Essa é uma paciente que chegou com um quadro bem parecido com o teu 👇

*(imagem de antes e depois anexada)*

> Resultado assim não é sorte, é método aplicado no caso certo.
>
> Faz sentido pra você chegar nisso?
>
> 1 - Faz sentido, quero saber como
> 2 - Faz, mas tenho receio de não funcionar pra mim

**Ramo 1** → segue direto pra oferta.
**Ramo 2** → recebe antes:
> Esse receio é o mais comum que eu escuto aqui, e é exatamente por isso que existe uma opção de entrada. Já te explico 👇

Essa frase transforma a objeção em ponte pro mensal, que é o produto que a gente quer vender.

---

## A oferta

Rota única, três mensagens em sequência. **A ordem é a estratégia:** o anual entra primeiro como âncora de valor, o mensal chega depois parecendo leve por comparação.

**1. O anual (âncora):**
> Pro teu caso o caminho certo é o Acompanhamento Anual. São 12 protocolos, um pra cada fase do teu processo, com atualização completa a cada 8 semanas e acompanhamento diário com o Nutri e com o time no WhatsApp.
>
> 12x R$147 ou à vista com 5% de desconto
>
> Um ano inteiro com nutricionista só seu, levando em conta o teu objetivo de `{{lead.cf.3909605}}`, por menos de uma coxinha por dia 😄

**2. O mensal (o que a gente quer vender):**
> Como você nunca testou a metodologia, é normal aquele medinho de dar o primeiro passo e se comprometer com um planejamento anual sem ter certeza de que vai funcionar.
>
> Por isso temos uma opção de entrada que só vale na primeira compra: o Acompanhamento Mensal, por 30 dias, de R$347.
>
> Mesmo Diagnóstico, mesmo protocolo feito pelo Chedid, mesma profundidade. Muda só o tempo.
>
> É pra você testar por 30 dias, sentir os resultados na pele, e depois decidir como quer seguir!

**3. O cupom e a escolha:**
> E além disso, eu tenho direito a liberar um cupom de desconto por 24h para novos contatos! Seu cupom de primeira compra derruba o preço de R$347 pra R$197 😁
>
> Qual faz mais sentido pra você?
>
> 1 - Quero o Anual, 12x R$147
> 2 - Quero começar pelo Mensal, R$197

---

## Fechamento

**Ramo 1, anual:**
> Boa escolha 🔱 Segue teu link:
> https://clkdmg.site/pay/consultoria-team-chedid-d-shape-slim-anual

**Ramo 2, mensal:**
> Perfeito, bora começar 🔱 Segue teu link:
> https://clkdmg.site/pay/acompanhamento-online-chedid-mensal
>
> Na hora de pagar, aplica o cupom **BEMVINDO150** que derruba pra R$197.

**Nos dois ramos, na sequência:**
```
Mudar o status do lead   → DEGUSTAÇÃO · Muito quente
Mudar usuário resp.      → no lead
Adicionar tarefa         Imediatamente · Usuário responsável atual · Acompanhar
                         "Lead recebeu o link, acompanhar"
```
> Te mandei o link aqui em cima 🎯
>
> Assim que você confirmar eu já começo teu onboarding e teu caso entra na fila do Chedid. Qualquer dúvida no meio do caminho é só me chamar aqui mesmo.

O bot encerra aqui.

---

## Escape

Uma cadeia só, para onde todas as etapas apontam (blocos 12 a 15):

```
Gerenciar tags       → no LEAD: FALAR-COM-HUMANO
Mudar usuário resp.  → no LEAD
Adicionar tarefa     Imediatamente · Acompanhar
                     "Lead saiu do bot. Assumir a conversa agora."
Enviar mensagem      "Pode deixar comigo, eu te respondo aqui direto 👋"
(encerra)
```

Cai aqui quem digita `0`, quem escreve texto livre e quem manda um número fora da lista. **Nunca responder "opção inválida"**: texto livre não é erro do lead, é sinal de que ele quer falar com gente.

---

## Follow-up de quem abandona (bot separado)

Segundo Salesbot, **`AQUISIÇÃO Follow-up`**.

**Gatilho:** `3 horas após a última mensagem recebida`, para leads com Status = **DEGUSTAÇÃO · Apresentando** (quem terminou já foi pra "Muito quente" e não é pego). Excluir quem tem a tag `FALAR-COM-HUMANO`, que não abandonou, pediu atendimento.

```
1. Mudar o status do lead → DEGUSTAÇÃO · Follow-up
2. cutucão 1
3. Pausar 1 dia
4. cutucão 2
5. Pausar 3 dias
6. cutucão 3
```

Ligar **"parar o bot se o cliente responder"**. Sem isso, quem responde o primeiro ainda recebe os outros dois.

**Cutucão 1:**
> Oi! Ficou pela metade aqui 😅
>
> Faltavam poucas perguntas pra eu fechar a leitura do teu caso. Quer terminar? Leva menos de um minuto.

**Cutucão 2:**
> Passando aqui de novo 👋
>
> Teu diagnóstico ficou pronto pela metade. Se quiser, é só me responder que eu retomo de onde a gente parou.

**Cutucão 3:**
> Última vez que te chamo por aqui, prometo 😄
>
> Ainda faz sentido pra você mudar o corpo esse mês, ou deixamos pro próximo?

**Limitação assumida:** ele **não retoma o questionário**. Quando a pessoa responde, quem continua é o Gabriel, na mão. O `ETAPA_BOT` no cartão diz onde ela parou.

---

## Campos no Kommo

| Campo | id | Tipo |
|---|---|---|
| OBJETIVO | 3909605 | lista |
| TREINO | 3909607 | lista |
| TRAVA | 3909609 | lista |
| SINTOMA | 3909611 | lista |
| CONDICAO | 3909621 | lista |
| CONDICAO_OUTRA | 3909623 | texto |
| ETAPA_BOT | 3909617 | numérico |
| URGENCIA | 3909615 | lista · **sem uso** desde a virada de oferta |

Macro nas mensagens: `{{lead.cf.ID}}`, digitada na mão (não existe botão de variável).

**Tags:** `BOT-INICIADO` · `FALAR-COM-HUMANO` · `RECEIO` (opcional, no ramo 2 da prova social)

**Etapas do funil Degustação:**
```
Leads Entrantes  → entra, dispara o bot
Apresentando     → bot rodando
Follow-up        → abandonou no meio
Muito quente     → recebeu o link
degustação ativo → comprou
venda perdida    → com motivo de perda
```

---

## Como medir

O número principal é **quantos chegam na oferta**, comparado com quantos chegavam na mensagem 8 do bot v1. Se uma etapa concentrar o abandono, é aquela pergunta que muda, não o fluxo inteiro.

Depois: conversão oferta → compra, separada por **anual** e **mensal**. Como o objetivo declarado é vender o mensal, o mensal é o placar.
