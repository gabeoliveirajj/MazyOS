# Tarefas pendentes — Gabriel

> Lista viva de pendências. Gabriel manda "adicionar X" e a tarefa entra aqui.
> Quando ele perguntar "tarefas pendentes", devolver a lista de abertas.
> Marcar [x] quando concluída (não apagar, pra manter histórico).

## Abertas
- [ ] Áudios degustação Eliana, Larissa, Simara, Pedro e Patrícia *(ver `saidas/checklist-audios-manuais-larissa-eliana.md`)*
- [ ] Atualizar memória do projeto
- [ ] Ajustar o fluxo dos áudios da degustação pra não atrasar mais *(causa raiz: latecomer não arrastado pra esteira automática — já 4 casos: Eliana, Larissa, Simara, Patrícia)*
- [ ] Implementar social selling
  - [ ] Trabalhar a represa: 191 leads de IG parados no "Leads de entrada" *(worklist em `saidas/social-selling-ig-represados.md`, começar pelos 60 quentes)*
  - [ ] Configurar a torneira: rotear novas DMs de IG pra cair direto no funil Social Selling / Novo *(config de chat do Kommo)*
- [ ] Decidir/gravar áudio custom pro Pedro (reta final, contexto jiu) *(antes de 01/09 — o áudio padrão fala em estética)*
- [ ] Criar automação de áudios da anamnese para clientes do plano anual — entregar pra Kami

## Concluídas
_(nada ainda)_

---
*Criada em 11/08/2026.*

---

## Automação pós-compra: "✅ receber diagnóstico" (aberta em 31/08/2026)

**O que é:** automação por conversação no Kommo. A qualquer momento depois da compra, quando o cliente mandar a frase **`✅ receber diagnóstico`**, ele recebe a mensagem de boas-vindas com o link de onboarding.

**Mensagem a enviar:**
```
Seja muito bem-vinda (o)✨🖤
Parabéns pela sua escolha!
Agora você faz parte do Team Chedid! 🔱

Clique no link abaixo para eu te explicar como vai funcionar TUDO sobre seu plano. 👇🏻

https://kommo.cc/K/WTU5GC/WQ19F0

Siga o passo a passo e bora dar o start em seu acompanhamento!

Qualquer dúvida, é só me chamar
```

**Como montar (esboço):** Salesbot próprio, gatilho de **GATILHOS DE CONVERSAÇÃO** → "Em uma mensagem recebida", com Condição `Cliente enviar · Iguais · ✅ receber diagnóstico`. Uma mensagem só, e encerra.

**Pontos a resolver antes de montar:**
- **Escopo do gatilho.** Precisa ser restrito a quem comprou, senão qualquer pessoa que mande a frase recebe o onboarding. Amarrar por etapa de funil (cliente já movido pelo webhook da Guru) ou por tag.
- **A frase tem emoji e acento.** Comparação exata (`Iguais`) pode falhar se o cliente digitar diferente. Ideal é a frase vir pronta de um botão `wa.me` na página de obrigado do checkout, igual já é feito na ativação da esteira. Vale considerar `Contém` em vez de `Iguais`, com uma palavra-chave mais robusta.
- **Link de onboarding mudou.** Antes era `form.respondi.app/sONYqCf0`, agora é `kommo.cc/K/WTU5GC/WQ19F0`. Confirmar qual é o vigente e aposentar o antigo.
- **Relação com a esteira.** Hoje a ativação da esteira é manual (`ativar-esteira.py`) e ancorada na entrega da dieta. Definir se essa automação é o gatilho de entrada dessa jornada ou um passo à parte.
