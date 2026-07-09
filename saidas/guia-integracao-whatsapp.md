# Guia: deixar a integração de WhatsApp certinha

> Objetivo: dois números de WhatsApp comum (não-oficial) conectados ao Kommo, prontos pra rodar a esteira.
> Mapa: **número atual da Kami** = Funil Suporte (dispara áudios, ela atende no WhatsApp Web) · **chip novo** = Funil Degustação + Anual (comercial, Gabriel).

---

## Passo 1 (FAZER PRIMEIRO): descobrir o que já está conectado

Hoje a Kami já usa um WhatsApp plugado no Kommo, com bot rodando. Antes de contratar qualquer coisa:

1. No Kommo: **Configurações → Integrações** (ou o painel de "Chats" / canais). Veja **qual widget de WhatsApp** está conectado hoje.
2. Teste o item que decide tudo: **essa integração manda ÁUDIO** (nota de voz)? Manda um áudio de teste por ela.
   - **Se manda áudio E funciona com Salesbot:** ótimo, reaproveita ela pro número da Kami. Só falta adicionar o número comercial novo.
   - **Se NÃO manda áudio:** troca por uma que mande (ver Passo 3). Áudio é inegociável, é a alma da esteira.

Anota o nome do widget atual pra gente saber com o que está lidando.

---

## Passo 2: a porta de entrada vai mudar de número (planejar)

Hoje os leads chegam no número da Kami. No plano novo, quem recebe lead novo é o **chip comercial**. Então:

- O número que aparece nos **anúncios, landing page, bio do Instagram e link do WhatsApp** precisa virar o **chip novo comercial**.
- O número da Kami deixa de ser a porta de entrada e vira **só suporte** (clientes que já compraram).
- Combinar com a **Maria (tráfego)** e quem mexe na landing/bio pra trocar o número no dia da virada.

> Detalhe bom: assim a automação pesada (áudios) fica no número antigo e estabelecido da Kami (aguenta melhor ban), e o chip novo cuida da entrada, que é mais conversa humana.

---

## Passo 3: escolher a integração (se precisar trocar)

Precisa ser um widget de **WhatsApp Web (QR)**, não a integração oficial (API). Ele TEM que fazer os 5:

1. Conectar número comum por **QR code** (não API).
2. **Enviar áudio** (nota de voz tocável). ← o teste decisivo
3. Rodar com o **Salesbot** do Kommo (automação).
4. **Capturar as mensagens que o cliente manda** (pro bot pausar).
5. Deixar a **Kami seguir usando o WhatsApp Web** normal enquanto está conectada (coexistência).

Candidata mais comum pra Kommo + WhatsApp por QR + Salesbot + mídia: **Wazzup**. Existem outras no marketplace do Kommo. Pega o **trial** e testa os 5 pontos antes de pagar.

---

## Passo 4: preparar e AQUECER o chip novo (começar já, leva dias)

Número novo que já começa disparando automação toma ban na hora. Antes de conectar na esteira:

1. Ativar o chip (eSIM virtual ou físico).
2. Instalar **WhatsApp Business** e preencher o perfil (nome, foto, infos) pra parecer legítimo.
3. **Aquecer por 1 a 2 semanas:** conversas reais, salvar contatos, receber e responder mensagens, volume crescendo aos poucos. Só depois plugar automação.

---

## Passo 5: conectar os dois números no Kommo

1. Instalar/abrir o widget escolhido.
2. Conectar o **número da Kami** por QR.
3. Conectar o **chip comercial** por QR.
4. Definir o **responsável** de cada canal: comercial → Gabriel; suporte → Kami.
5. Rotear a **entrada de conversa nova** do número comercial pro **Funil Degustação**. (As passagens entre funis são por automação, não por entrada.)

---

## Passo 6: testar os 4 pontos críticos antes de montar o bot

Com um número de teste seu:

- [ ] Mandar um **áudio** pela integração. Chega como nota de voz tocável?
- [ ] **Cliente responde** uma mensagem. Aparece no Kommo?
- [ ] O **Salesbot** consegue disparar por esse canal?
- [ ] A **Kami abre o WhatsApp Web** dela. Funciona junto com a integração conectada?

Se algum falhar, resolve antes de seguir pro bot.

---

## Ordem sugerida

1. **Passo 1** (checar o que já existe) + **Passo 4** (comprar e aquecer o chip) em paralelo, hoje.
2. Passo 2 (alinhar a troca do número com a Maria).
3. Passo 3 (trocar de widget só se o atual não mandar áudio).
4. Passo 5 (conectar) + Passo 6 (testar).
5. Aí sim: montar o bot da esteira.
</content>
