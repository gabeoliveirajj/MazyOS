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
- **Progresso (jul/2026): esteira de áudios CONSTRUÍDA no Salesbot** (gatilho: entra em "Onboarding D0" do Funil Suporte → 8 toques texto+nota de voz → move pro Funil Anual). **Pulo do gato do áudio:** marcar **"Converter em áudio"** no anexo faz o Salesbot mandar como **nota de voz** (senão vai como documento). Áudios em `.ogg` (`dados/audios-degustacao/ogg-prontos/`). Passo a passo completo em `saidas/passo-a-passo-salesbot-esteira.md`. **Progresso:** (1) ✅ esteira testada ponta a ponta, rodando redonda; (2) ✅ handoff de entrada CONSTRUÍDO e testado ao vivo — script `scripts/guru-para-kommo.py` acha o lead pelo telefone da venda → move pro Funil Suporte/Onboarding D0 + tag CLIENTE DEGUSTAÇÃO → esteira dispara (áudio confirmado no WhatsApp). Fase manual documentada em `saidas/runbook-handoff-degustacao.md` (gatilho = painel/app da Guru; Gabriel roda o comando por venda). **Próximo:** (a) automatizar o handoff — ✅ endpoint NO AR na Vercel (`api/handoff.py`, Python puro): `https://mazy-os-eight.vercel.app/api/handoff?key=<WEBHOOK_SECRET>`. Recebe webhook "venda aprovada" da Guru → autentica por segredo na URL (`WEBHOOK_SECRET`, guardado no `.env`) → filtra produto pelo nome (`GURU_PRODUCT_NAME_CONTAINS=degustação`) → acha o lead pelo telefone e move (ou CRIA) pro Funil Suporte. Env vars na Vercel: KOMMO_BASE_URL, KOMMO_LONG_LIVED_TOKEN, WEBHOOK_SECRET, GURU_PRODUCT_NAME_CONTAINS. Testado ao vivo: handoff move/cria e taggeia certinho. **PENDENTE (Gabriel):** plugar a URL na Guru (Config → Webhooks → aba Vendas → status Aprovada). Script manual `guru-para-kommo.py` = plano B. Guia: `saidas/guia-deploy-webhook-guru.md`.
  - **DESCOBERTA-CHAVE (limitação do WhatsApp):** a esteira só ENTREGA pra quem tem chat aberto com a Kami. Sem interação do cliente não há janela pra mandar áudio (regra do WhatsApp, não do Kommo; Lite não inicia frio e blastar frio = risco de ban). **Solução escolhida (wa.me + Lite):** compra → handoff joga o lead na etapa nova **"Aguardando ativação"** (Funil Suporte, id 108761732) + tag. Página de obrigado do checkout tem botão **wa.me** da Kami (`https://wa.me/5548992122712?text=...ativar meu acompanhamento`) → cliente manda 1ª msg → **bot "Ativar esteira" (gatilho: chat iniciado por msg de entrada na Kami, escopo etapa Aguardando ativação) move pro Onboarding D0** → esteira dispara com chat quente. **Controle de Duplicatas LIGADO** nos 2 funis (senão a msg de entrada cria lead duplicado em vez de casar pelo telefone).
  - **AINDA A VALIDAR (bloqueio aberto):** no teste com número frio, a msg de entrada criou um lead DUPLICADO ("Incoming leads" da Degustação) em vez de cair no lead em Aguardando ativação → bot de ativação não disparou. Liguei o Controle de Duplicatas pra corrigir; falta **re-testar com número frio** (ou 1º comprador real) se a msg agora cai no lead certo e a esteira entrega. Se não resolver, plano B = disparar a esteira pelo lead do chat de entrada.
  - **Verificar:** na etapa Onboarding D0 apareceram 2 bots — a esteira "DEGUSTACAI" (ok) e um "Salesbot #201855" com ⚠️ (possível resquício a limpar).
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
