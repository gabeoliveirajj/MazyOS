# Esboço das automações no Kommo (3 funis, número comum)

> Rascunho pra Gabriel entender o desenho antes de montar. Não é pra aprovar com o Henrique (é execução interna).
> Base: WhatsApp **número comum** (chip virtual novo), sem API.

---

## Contexto técnico (o que o número comum muda)

- Sem API significa **sem janela de 24h e sem templates**. A esteira vira simples: o bot manda **texto + áudio** direto, no dia certo. Sem burocracia de reabertura.
- **Sem botões interativos.** Integração não-oficial não dispara botão nativo. Então a pessoa não precisa "clicar pra receber": o bot já manda o texto (resumo) e o áudio em sequência.
- O bot **pausa sozinho quando a pessoa responde** (pra Kami dar suporte) e **retoma** a esteira depois.

---

## Visão geral: os 3 funis e as passagens

```
[FUNIL DEGUSTAÇÃO]  aquisição (comercial)
   Leads → Apresentando → Follow-up
        │ (pagou o R$197)
        ▼  automático: move + tag CLIENTE DEGUSTAÇÃO
[FUNIL SUPORTE]  operado pela Kami · esteira de áudios
   Recebe os 8 áudios (texto + áudio), D0 a D26, + suporte inline
        │ (D27)
        ▼  automático: move pro Anual
[FUNIL ANUAL]  conversão (comercial)
   Aquecimento → Oferta → (fechamento humano do Gabriel)
        │ (comprou o anual)
        ▼  automático: volta pro Suporte + troca tag p/ CLIENTE ANUAL
[FUNIL SUPORTE]  agora como CLIENTE ANUAL (suporte contínuo)
```

---

## Os números (DEFINIDO)

**2 números, mas a automação (esteira) roda TODA no número da Kami.**

- **Pré-compra da degustação (aquisição):** número **comercial separado do Gabriel** (ele atende por WhatsApp Web). A configurar depois. **Fora do escopo desta missão do Salesbot** (não precisa mexer nele agora).
- **Pós-compra (Funil Suporte + esteira de áudios + aquecimento do Anual):** número da **Kami (48 99212-2712, WhatsApp Lite)**. Verificado: manda áudio e roda bot. **É aqui que o Salesbot vive.**
- O cliente passa do comercial (Gabriel) pra Kami ao comprar a degustação.
- A Kami segue atendendo pelo **WhatsApp Web**; o Kommo dispara os áudios e enxerga as mensagens (pausa o bot quando o cliente responde; retomada por tempo).
- **Ban:** número antigo e estabelecido resiste bem, volume ~50/mês é baixo. Ritmo humano, nunca disparo em massa a frio.
- **Plano B:** API oficial já instalada no número do Henrique (48 9159-2181), se precisar escalar.

---

## Bot 1 · Funil Degustação (aquisição)

- **Entrada:** lead novo cai no funil (do tráfego / bot de qualificação que o Henrique vai ativar).
- **Miolo:** apresentação + follow-up até vender a degustação (parte comercial, pode ter bot de qualificação + humano).
- **Gatilho de saída (o mais importante):** **pagamento do R$197 confirmado** → automação move o contato pro Funil Suporte e aplica a tag **CLIENTE DEGUSTAÇÃO**.
- **Dependência:** como o Kommo fica sabendo do pagamento? Via **página de obrigado / webhook do checkout**, integração do gateway, ou marcação manual. Precisa definir (é o gatilho que liga a esteira).

---

## Bot 2 · Funil Suporte (a esteira de áudios) — o coração

- **Entrada:** contato entrou com a tag **CLIENTE DEGUSTAÇÃO** → dispara o Salesbot da esteira.
- **Passo-tipo (repete 8 vezes, um por áudio):**
  1. Enviar **mensagem de texto** (o resumo do áudio N).
  2. Aguardar uns 30 a 60 segundos.
  3. Enviar o **áudio N**.
  4. Aguardar até o próximo dia da cadência.
- **Cadência aprovada:** D0, D2, D5, D7, D10, D13, D15, D26.
- **Regra de pausa (suporte):** se o cliente **responder** durante a espera → o bot **pausa** (a Kami atende pelo WhatsApp Web como sempre). A esteira **retoma por tempo**, no próximo dia da cadência, sem depender da Kami mexer no Kommo.
- **Gatilho de saída:** no **D27**, automação move o contato pro **Funil Anual**.

---

## Bot 3 · Funil Anual (conversão)

- **Entrada:** contato chegou do Suporte no D27.
- **Aquecimento (automático):** áudios **novos** + vídeos de benefício do anual (Henrique vai gravar).
- **Oferta:** bot manda a oferta e **cria uma tarefa pro Gabriel** fechar. O **fechamento é humano** (do jeito que converte os ~30%).
- **Resultado:**
  - Comprou → automação move de volta pro **Funil Suporte** e troca a tag pra **CLIENTE ANUAL**.
  - Não comprou → **Não efetivou**, com **motivo de perda** registrado (caro / resultado abaixo / sumiu / vai pensar).

---

## Gatilhos automáticos (resumo)

| Evento | Ação automática |
|---|---|
| Pagou a degustação | Move p/ Suporte + tag CLIENTE DEGUSTAÇÃO + liga a esteira |
| Cliente responde durante a esteira | Pausa bot + tarefa pra Kami |
| Chegou o D27 | Move p/ Funil Anual |
| Entrou no Anual | Dispara aquecimento + oferta + tarefa pro Gabriel |
| Comprou o anual | Volta p/ Suporte + troca tag p/ CLIENTE ANUAL |
| Não fechou o anual | Não efetivou + motivo de perda |

---

## Dependências pra ligar (checklist técnico)

- [ ] **Confirmar a integração de WhatsApp não-oficial** escolhida suporta: (a) automação via Salesbot, (b) envio de **áudio**, (c) estabilidade. Nem todo widget faz isso.
- [ ] **Ativar e AQUECER o chip novo** antes de disparar volume. Número novo mandando automação em massa é o que mais toma ban. Aquecer aos poucos (conversas reais, volume crescente) por alguns dias.
- [ ] **Definir a detecção de pagamento** (checkout / webhook / manual) da degustação e do anual.
- [ ] Áudios da degustação: prontos ✅. Áudios + vídeos do anual: Henrique a gravar.
- [ ] Bater a decisão dos números (seção acima).

## Ordem sugerida de implementação

1. Ativar + aquecer o chip novo.
2. Montar o **Funil Suporte** + o bot da esteira (já temos áudios e resumos).
3. **Testar com 1 lead** ponta a ponta.
4. Ligar a **detecção de pagamento** e as movimentações automáticas.
5. Montar o **Funil Anual** quando o Henrique entregar os áudios/vídeos.
</content>
