# Proposta: Ligar o "Motivo de Perda" no Kommo

> Para apresentar ao Henrique. Autor: Gabriel (Inside Sales). Jun/2026.
> Melhoria de processo de baixo esforço e alto retorno — implementação em ~10 minutos.

## O problema

Hoje o motivo de perda está **desligado** no CRM (`is_loss_reason_enabled: false`). Na prática: quando um lead esfria ou é perdido, ele some do funil **sem registro do porquê**.

O resultado disso está visível na base: **~600 leads parados** no Funil de vendas, e a gente **não tem como saber** se foram embora por preço, por falta de follow-up, porque não eram o público certo, ou porque acharam caro. Sem essa informação, qualquer otimização (de copy, de oferta, de tráfego) é no escuro.

## Por que importa (o ganho)

Com o motivo de perda ligado, em 30 dias a gente passa a responder perguntas que hoje são chute:

- **Qual a objeção nº 1 que mais derruba venda?** (preço? momento? concorrente?) → ajusta o pitch e a quebra de objeção.
- **Quanto a gente perde por simples falta de follow-up?** → justifica a cadência sistemática.
- **A degustação está convertendo ou as pessoas compram e não viram anual?** → ajusta o produto/oferta.
- **O tráfego está trazendo público certo?** → feedback direto pra Maria sobre qualidade do lead.

É a diferença entre "achar" e **medir**. E mexe direto na prioridade da empresa: escalar mantendo conversão e CAC sob controle.

## Como ligar (passo a passo no Kommo)

1. **Configurações → Geral** → ativar a opção **"Motivo de perda"** (Loss reason). Isso passa a exigir um motivo sempre que um lead for movido pra etapa de perda.
2. Em cada funil (Funil de vendas, DEGUSTAÇÃO, Clínica), cadastrar a **lista de motivos** (sugestão abaixo).
3. Combinar com a equipe: **toda vez que perder/encerrar um lead, escolher o motivo** (vira regra, não opcional).

## Motivos de perda sugeridos (lista inicial enxuta)

Começar simples — lista curta é mais usada e gera dado limpo:

| Motivo | Quando usar |
|---|---|
| **Preço / sem orçamento** | Achou caro ou disse que não cabe agora |
| **Sumiu / sem resposta** | Parou de responder após a cadência completa |
| **Momento ruim** | "Deixa pra depois", viagem, vai começar mês que vem |
| **Já tem nutri / acompanhamento** | Está com outro profissional |
| **Não é o público** | Lead desqualificado (não é o perfil) |
| **Comprou degustação, não virou anual** | (só no funil) caiu na conversão degustação → anual |
| **Foi pro outro produto** | Migrou de online ↔ clínica (não é perda real) |

> Manter entre 6 e 8 motivos. Se aparecer um padrão novo recorrente, a gente adiciona.

## Esforço x retorno

- **Esforço:** ~10 min de configuração + criar o hábito na equipe.
- **Retorno:** em ~30 dias, primeiro relatório real de "por que perdemos venda" — base pra decisões de copy, oferta e tráfego.

## Conexão com os outros 2 furos do funil

Essa é uma das **3 melhorias** que identifiquei ao analisar o CRM. As outras duas (pra sequência):
1. **Rodar a cadência de follow-up de forma sistemática** (já está pronta no playbook) — é o vazamento nº 1.
2. **Conectar o "Funil de vendas" → "DEGUSTAÇÃO"** — hoje quem compra a degustação some do funil principal sem rastro; o handoff está quebrado.
