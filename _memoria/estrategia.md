# Estratégia

> O que importa agora. Prioridades, metas, prazos.
> O Claude usa isso pra decidir o que sugerir primeiro.

## Prioridade principal
**Escalar comercialmente a consultoria online** (o ativo de escala infinita). Aumentar e **MANTER** as conversões enquanto escala o **tráfego pago**, com **CAC sob controle**. É exatamente onde o Gabriel entra: análise de funil, CAC e estratégias de escala junto com o Henrique e a Maria (tráfego).

### Foco do Gabriel como Inside Sales (a partir de jun/2026)
Sucesso medido principalmente por **venda**. Ordem de prioridade: **1º Consultoria online, 2º Clínica presencial**. Frentes de trabalho:
1. **Atender novos leads** que entram (converter).
2. **Reativar a base parada** no Kommo (~600 leads no "Funil de vendas" parados há meses) — dinheiro na mesa.
3. **Propor melhorias no processo comercial.** ✅ Motivo de perda ligado (jun/2026, com 7 motivos sob medida). Foco real nos **2 funis vivos**: (a) aplicar a cadência de follow-up na **DEGUSTAÇÃO** (online, onde os leads respondem) e apoiar o Kanban manual que a Mari tocava; (b) **estruturar o funil da Clínica Chedid** (hoje só plugado no WhatsApp, sem estrutura). O "Funil de vendas" antigo é só **garimpo único** da base parada, não merece investimento de processo.

### Em execução (jul/2026): automação da degustação + Funil Anual
Fecha os 2 furos abertos do diagnóstico (cadência não roda; handoff degustação→anual quebrado). Escopo:
- **Esteira de áudios da degustação:** os 8 áudios do Henrique (já gravados, D0→D26) viram Salesbot automático no Kommo, tirando o follow-up manual das costas dele. Restrição: WhatsApp é API oficial → regra da janela de 24h, precisa de ~4-5 templates de texto aprovados na Meta.
- **Funil Anual** (criado ao vivo): quem termina os 30 dias entra automático e roda a esteira de conversão pro anual. **Close do anual fica humano/personalizado** (é como o Henrique converte os ~30% — não automatizar).
- Blueprint completo: `saidas/blueprint-crm-degustacao-funil-anual.md`. Templates de WhatsApp prontos: `saidas/templates-whatsapp-degustacao.md`.
- **Entregável em construção:** apresentação pro Henrique com todo o plano. **DECISÃO EM ABERTO a ser tomada junto com ele:** WhatsApp **API oficial** (escala segura, mas precisa dos templates/janela 24h) **vs. não-oficial** (simples, sem template, mas risco de banimento e não escala). Levar as duas opções lado a lado pra decidir juntos — não tratar mais como fechado.

### Aprovado na reunião com o Henrique (02/07/2026)
Ele APROVOU o plano de funis + automação (adorou). Apresentação usada: `saidas/apresentacao-funis-henrique.html` (+ versão de clique). Refinamentos e pendências que saíram da reunião:
- **Fluxo de funis FECHADO (02/07):**
  1. Lead entra no **Funil Degustação** (comercial) e roda até **comprar** o produto.
  2. Comprou → vai pro **Funil de Suporte**, marcado **CLIENTE DEGUSTAÇÃO**, **operado pela Kami** — envia os 8 áudios e responde dúvidas, **até o dia 26**.
  3. **Dia 27** → contato movido pro **Funil Anual**, onde é feita a **oferta do anual**.
  4. Comprou o anual → **volta pro Funil de Suporte**, agora marcado **CLIENTE ANUAL**.
  O Funil de Suporte é a "casa do cliente" (Kami), guarda CLIENTE DEGUSTAÇÃO e CLIENTE ANUAL por tag. Degustação e Anual são etapas comerciais transitórias. O suporte da degustação roda JUNTO com os áudios (a pessoa ainda é lead em processo de upsell).
- **WhatsApp DEFINIDO (jul/2026): 2 números, mas a AUTOMAÇÃO (esteira) roda toda no número da Kami.**
  - **Pré-compra da degustação (aquisição) = número COMERCIAL separado do Gabriel** (ele atende por WhatsApp Web). A configurar depois; **FORA do escopo da esteira/Salesbot**.
  - **Pós-compra = número da KAMI (48 99212-2712, WhatsApp Lite)** — Funil Suporte com a esteira de 8 áudios + o aquecimento do Anual. Verificado na prática: **o Lite manda áudio e roda bot**.
  - Pro cliente: fala com o comercial (Gabriel) antes de comprar, e com o número da Kami depois. **Pra missão do Salesbot, só o número da Kami importa.** Sem API, sem templates, sem chip a aquecer aqui. Manter ritmo humano nos disparos. Plano B: API já instalada no número do Henrique (48 9159-2181). Clínica no Lite = 48 99524-629.
- **Progresso (jul/2026): esteira de áudios CONSTRUÍDA no Salesbot** (gatilho: entra em "Onboarding D0" do Funil Suporte → 8 toques texto+nota de voz → move pro Funil Anual). **Pulo do gato do áudio:** marcar **"Converter em áudio"** no anexo faz o Salesbot mandar como **nota de voz** (senão vai como documento). Áudios em `.ogg` (`dados/audios-degustacao/ogg-prontos/`). Passo a passo completo em `saidas/passo-a-passo-salesbot-esteira.md`. **Progresso:** (1) ✅ esteira testada ponta a ponta, rodando redonda; (2) ✅ handoff de entrada CONSTRUÍDO e testado ao vivo — script `scripts/guru-para-kommo.py` acha o lead pelo telefone da venda → move pro Funil Suporte/Onboarding D0 + tag CLIENTE DEGUSTAÇÃO → esteira dispara (áudio confirmado no WhatsApp). Fase manual documentada em `saidas/runbook-handoff-degustacao.md` (gatilho = painel/app da Guru; Gabriel roda o comando por venda). **Próximo:** (a) automatizar o handoff — ✅ endpoint NO AR na Vercel (`api/handoff.py`, Python puro): `https://mazy-os-eight.vercel.app/api/handoff?key=<WEBHOOK_SECRET>`. Recebe webhook "venda aprovada" da Guru → autentica por segredo na URL (`WEBHOOK_SECRET`, guardado no `.env`) → filtra produto pelo nome (`GURU_PRODUCT_NAME_CONTAINS=degustação`) → acha o lead pelo telefone e move (ou CRIA) pro Funil Suporte. Env vars na Vercel: KOMMO_BASE_URL, KOMMO_LONG_LIVED_TOKEN, WEBHOOK_SECRET, GURU_PRODUCT_NAME_CONTAINS. Testado ao vivo: handoff move/cria e taggeia certinho. **✅ FEITO (jul/2026):** URL plugada na Guru (webhook "Handoff Degustação Kommo", filtro Todos + status Aprovada). Script manual `guru-para-kommo.py` = plano B. Guia: `saidas/guia-deploy-webhook-guru.md`.
  - **🔴 CORREÇÃO (13/08/2026) — o handoff automático NUNCA funcionou em produção.** O que estava escrito acima ("testado ao vivo, move/cria e taggeia certinho") valia só pro teste manual. Diagnóstico feito no dia 13/08: o webhook **está cadastrado e ativo** na Guru (aba **Vendas**, não Assinaturas), o segredo da URL bate com o `WEBHOOK_SECRET`, e o endpoint responde certo (`GET` health 200 · segredo errado 401 · segredo certo 200). Ele **dispara de verdade** (log de Atividades da Guru mostra várias entregas por dia). **Mas a etapa de destino "Aguardando DIETA" (id 108761732) tem ZERO leads e nunca teve nenhum.** Causa provável: o filtro `GURU_PRODUCT_NAME_CONTAINS=degustação` não bate com o nome real do produto na Guru → o endpoint responde `200 {"ignorado": "produto fora do filtro"}` e **descarta a venda em silêncio** (200, sem erro, sem alarme). Consequência: o Gabriel vinha rodando o `ativar-esteira.py` na mão a cada venda achando que a automação fazia o handoff — a assinatura disso são movimentações indo direto pro "Onboarding (D0)" sem passar por "Aguardando DIETA". **Falta pra fechar:** nome exato (ou ID) do produto de degustação na Guru. **Correção definitiva:** trocar o filtro de NOME pra **ID** (`GURU_PRODUCT_IDS`, já suportado pelo `api/handoff.py`) — nome quebra quando alguém edita a oferta/põe emoji/cria versão com desconto, ID não.
  - **DESCOBERTA-CHAVE (limitação do WhatsApp):** a esteira só ENTREGA pra quem tem chat aberto com a Kami. Sem interação do cliente não há janela pra mandar áudio (regra do WhatsApp, não do Kommo; Lite não inicia frio e blastar frio = risco de ban). **Solução escolhida (wa.me + Lite):** compra → handoff joga o lead na etapa nova **"Aguardando ativação"** (Funil Suporte, id 108761732) + tag. Página de obrigado do checkout tem botão **wa.me** da Kami (`https://wa.me/5548992122712?text=...ativar meu acompanhamento`) → cliente manda 1ª msg → **bot "Ativar esteira" (gatilho: chat iniciado por msg de entrada na Kami, escopo etapa Aguardando ativação) move pro Onboarding D0** → esteira dispara com chat quente. **Controle de Duplicatas LIGADO** nos 2 funis (senão a msg de entrada cria lead duplicado em vez de casar pelo telefone).
  - **✅ BLOQUEIO DA DUPLICATA RESOLVIDO + validado ponta a ponta (jul/2026):** com Controle de Duplicatas ligado, a msg de entrada casa no lead certo (sem duplicata nova), a ativação move pro Onboarding D0 e o áudio 1 entrega. Confirmado na API. O gatilho de ativação foi trocado pra **"Em uma mensagem recebida"** (canal 554892122712, escopo Aguardando ativação, pausa 5 min) — mais robusto que "chat iniciado", que só valia pra conversa nova e quebrava se o cliente tinha falado com a Kami nas últimas 24h.
  - **⚠️ REGRA NOVA (Kami, jul/2026) — muda o GATILHO DE LARGADA da esteira:** os 30 dias / a cadência de áudios começam **no dia da ENTREGA DA DIETA**, NÃO na compra. O cliente leva ~7 dias (variável) pra receber. Novo fluxo: compra → webhook joga o lead em **"Aguardando entrega da dieta"** (ex-"Aguardando ativação", mesmo id 108761732) e a esteira fica PARADA; a Kami entrega a dieta pelo WhatsApp e **avisa o Gabriel**, que roda `python3 scripts/ativar-esteira.py "telefone" --executar` → move pro Onboarding D0 → esteira liga (D0 = dia da entrega). Runbook: `saidas/runbook-ativar-esteira.md`. **Por causa dessa regra, o bot automático "Em uma mensagem recebida" foi DESATIVADO** (senão ligava a esteira antes da dieta chegar) — a ativação agora é **manual (Gabriel)**, no mesmo padrão do handoff. A janela do WhatsApp se resolve sozinha porque a entrega acontece por conversa ativa (rodar o comando no mesmo dia).
  - **Bot de entrada da Degustação (anúncios) corrigido (jul/2026):** o "Degustação BOT" (funil Degustação, etapa Leads Entrantes) só deixava passar quem mandava uma das 3 frases exatas dos links antigos; lead vindo de anúncio manda texto livre → não casava → morria em "Nenhuma das condições". Ligamos os becos sem saída (blocos de condição 1, 6 e 54) → qualquer msg segue o fluxo. Gatilho já era "entrada na etapa" (ok).
  - **✅ Limpo (jul/2026):** o "Salesbot #201855" (erro "Bot excluído") na Onboarding D0 era resquício órfão e foi removido; ficou só a esteira "Audios Funil Suporte".
  - IDs Kommo: Funil Degustação 13257796 (Incoming 102232080), Funil Suporte 14050808, etapas Suporte: Aguardando ativação 108761732 → Onboarding D0 108457804. Nº Kami: 48 99212-2712.
  (b) bot do Funil Anual (depende dos áudios/vídeos novos do Henrique).
- **Engajamento:** cada áudio vai com **texto resumido em bullets** (feito a partir da transcrição) + **botões de interação** pra clicar e receber o áudio. Gabriel cria os resumos dos 8 áudios pra aprovação.
- **Conversão do anual:** Henrique grava **áudios NOVOS de aquecimento** + vídeos de benefício do anual; usar cupons/descontos em datas estratégicas; fechamento continua **humano**.
- **Cadência de reuniões de acompanhamento:** segundas e quintas.
- Plano: deixar degustação + anual rodando **1 mês** pra análise antes de otimizar. Estruturar o online primeiro, depois atacar o B2B.

### Novas frentes que surgiram na reunião
- **Low ticket (e-book):** e-book emocional/storytelling (R$47-67) + videoaulas, **landing separada**, seeding pra degustação com possível cashback — pra aumentar conversão degustação→anual. Henrique produz o conteúdo.
- **B2B Projeto Mais Saúde (aprofundado):** entrada via palestra + confiança do RH; taxa mensal de ativação; usar plataformas internas (Teams/feeds) no lançamento; desconto em folha 100% custeado pelo funcionário; níveis de licença **Silver/Gold/Platinum**. Concorrente principal: empresa com funding de R$180 mi, 3 anos operando no negativo. Atacar DEPOIS de estruturar o online.

Baselines reais a preservar ao escalar:
- Lead → degustação: ~40%
- Degustação → anual: ~30%
- Plano de degustação: R$197

### Em execução (ago/2026): redesenho do bot de aquisição (v2)
**Origem:** mentoria com uma expert em vendas. Diagnóstico dela: o bot de aquisição atual só entrega informação direta, não filtra nada. Resultado: lead passa pelo bot e para de responder, ou nem termina.

**Solução desenhada (24/08/2026):** transformar o bot num **filtro que coleta o caso enquanto conduz pra oferta**. Mecânica central = **troca a cada toque**: contrato declarado na abertura ("6 perguntas, no final eu te devolvo uma leitura do teu caso") e cada número que o lead manda volta como um pedaço de diagnóstico dele, não como bloco institucional.
- **5 perguntas** (após a virada de 25/08): objetivo → treino → o que trava → sintomas → condição de saúde. A urgência foi removida.
- Os **3 pilares** saíram do monólogo e viraram **resposta** ao que trava o lead. Os **12 protocolos** são nomeados na etapa de sintomas (é o que prova individualização).
- **Preço só na etapa 7**, depois do mini diagnóstico. No v1 ele aparecia na msg 6, antes do lead falar qualquer coisa de si.
- **Rota única (desde 25/08):** todo lead recebe anual → mensal → cupom, nessa ordem. As duas rotas por urgência foram descartadas.
- **6 campos por lead no Kommo** (OBJETIVO, TREINO, TRAVA, SINTOMAS, CONDICAO, URGENCIA + ETAPA_BOT). É o ganho que existe mesmo sem venda: o Gabriel abre o cartão sabendo tudo antes de dar bom dia, e a base fica segmentável pra reativação.
- **Rotas de escape obrigatórias:** texto livre nunca mata o fluxo (bug do bot antigo), `0` chama o Gabriel, e nenhuma rota termina no bot.
- **Follow-up de abandono** retomando da etapa exata (+40min, D+1, D+3, D+7).
- **Métrica:** quantos chegam na etapa 7 vs. quantos chegavam na msg 8 do v1.

**Decisões fechadas (24/08/2026):** semestral fica FORA do bot (só atendimento humano) · quem assina é o Gabriel em 1ª pessoa · links de checkout plugados.

### 🔄 VIRADA DE OFERTA (25/08/2026) — ancoragem e produto de entrada
Muda o que o bot vende e como.

- **A urgência saiu do filtro.** A pergunta "quando você quer começar?" foi removida, e com ela o roteamento por temperatura. O filtro agora tem **5 perguntas** (objetivo · treino · trava · sintoma · condição de saúde), não 6. ⚠️ A mensagem de abertura prometia "6 perguntas" e precisa dizer **5**.
- **Todo lead recebe a mesma sequência de oferta**, em 3 mensagens: (1) o **Anual** (12x R$147), (2) o **Mensal** de 30 dias, (3) o **cupom de 24h** que derruba o mensal pra R$197.
- **A ancoragem é o ponto.** O anual entra primeiro pra estabelecer o valor de referência; o mensal chega depois parecendo barato em comparação. Não é para vender o anual.
- **O objetivo real é vender o MENSAL**, que tem a menor barreira de entrada. O anual é âncora.
- **Depois que o lead vira cliente do mensal, o objetivo passa a ser o upsell pro anual.** Isso reforça o papel do Funil Anual como máquina de conversão.
- **"Plano Degustação" morreu como nome.** Agora é **Acompanhamento Mensal** com cupom de boas-vindas. Deixa de soar como amostra grátis e passa a soar como produto.
- **Fechamento:** o bot espera o lead escolher anual ou mensal e manda o link correspondente. Cupom `BEMVINDO150` para o mensal. PIX (chave 10366978942) fora do checkout.

**Entregáveis:** `comercial/fluxo-aquisicao-v2.md` (copy pronta pro Salesbot) + página visual `saidas/fluxo-aquisicao-v2.html` (artifact `77a27815-bd88-4b9e-8dde-6d83616a0f6b`).
**Próximo passo:** montar no Kommo Salesbot. Dependência: o **número comercial de aquisição do Gabriel ainda não está configurado** (o bot v2 roda nele, não no da Kami). O bot atual a ser substituído é o "Degustação BOT" (funil Degustação, etapa Leads Entrantes).

## Segunda frente: estruturar o B2B (Projeto Mais Saúde)
- Destravar o pipeline (30+ empresas, ~8 quentes) com a **abordagem comercial certa**.
- O decisor entra mais por **cultura e storytelling** do que por venda dura.
- Usar o **consultório presencial como porta de entrada** (atrair empresários — CFO, RH, financeiro — que levam ao decisor).
- Alavancar o case de Floripa (prova social gravada).

## Clínica presencial
- Manter agenda cheia, **subir ticket médio**. Sem expandir dias (Henrique fica em até 2 dias/semana).
- Tratar como **boca do funil B2B**.

## Métricas que importam
- Conversão lead → degustação
- Conversão degustação → anual
- CAC vs. break-even
- Empresas qualificadas no pipe B2B
- Nº de ativos na consultoria (~200)

## Em aberto / próximos
- **Rebranding:** nome definitivo da marca + do "Projeto Mais Saúde" + identidade visual.
- Começar a **divulgar o uso de IA** no sistema (quando o público amadurecer).
- Construir o **hub/gamificação** do B2B.
