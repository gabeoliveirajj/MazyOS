# -*- coding: utf-8 -*-
# Gera 60 criativos de performance (20 por frente) em um board HTML.
import html

U = "https://images.unsplash.com/{}?w=700&q=80&auto=format&fit=crop"

clinica_imgs = [
    "photo-1490645935967-10de6ba17061","photo-1467003909585-2f8a72700288",
    "photo-1546069901-ba9599a7e63c","photo-1512621776951-a57141f2eefd",
    "photo-1498837167922-ddd27525d352","photo-1540189549336-e6e99c3679fe",
    "photo-1432139555190-58524dae6a55","photo-1547592180-85f173990554",
]
b2c_imgs = [
    "photo-1518310383802-640c2de311b2","photo-1434596922112-19c563067271",
    "photo-1538805060514-97d9cc17730c","photo-1506126613408-eca07ce68773",
    "photo-1518611012118-696072aa579a","photo-1549060279-7e168fcee0c2",
    "photo-1594381898411-846e7d193883","photo-1599058917765-a780eda07a3e",
    "photo-1545205597-3d9d02c29597","photo-1483721310020-03333e577078",
    "photo-1601422407692-ec4eeec1d9b3","photo-1571019613454-1cb2f99b2d8b",
    "photo-1534438327276-14e5300c3a48","photo-1581009146145-b5ef050c2e1e",
]
b2b_imgs = [
    "photo-1522071820081-009f0129c71c","photo-1497215728101-856f4ea42174",
    "photo-1600880292203-757bb62b4baf","photo-1556761175-b413da4baf72",
    "photo-1521737604893-d14cc237f11d","photo-1497366811353-6870744d04b2",
    "photo-1542744173-8e7e53415bb0","photo-1542744094-3a31f272c490",
    "photo-1600880292089-90a7e086ee0c",
]

# (headline, sub, cta)
clinica = [
    ("Nutrição de alta performance, no presencial.","Protocolo individual e acompanhado de perto. Agenda limitada.","Agendar consulta"),
    ("O protocolo mais preciso que você já seguiu.","Método documentado por anos, calibrado pro seu corpo.","Agendar consulta"),
    ("Resultado de verdade começa com o diagnóstico certo.","Avaliação completa e conduta sob medida.","Agendar consulta"),
    ("Atendimento presencial, agenda limitada.","Poucos dias por semana. Cada detalhe acompanhado de perto.","Agendar consulta"),
    ("Não é dieta. É um protocolo feito pra você.","Individual, preciso e ajustado ao seu dia a dia.","Agendar consulta"),
    ("Para quem cansou de tentar sozinho.","Acompanhamento profissional, do diagnóstico ao resultado.","Agendar consulta"),
    ("Cuide de você. Depois, do seu time.","O cuidado que começa no consultório transforma a sua empresa.","Quero conhecer"),
    ("A consulta que enxerga o que os exames escondem.","Avaliação aprofundada e conduta personalizada.","Agendar consulta"),
    ("Sua saúde merece mais que um plano genérico.","Protocolo individual, acompanhado de perto.","Agendar consulta"),
    ("Performance começa no prato.","Nutrição de alta performance, presencial e sob medida.","Agendar consulta"),
    ("Menos achismo. Mais método.","Conduta baseada em evidência e no seu histórico real.","Agendar consulta"),
    ("O nutricionista que vira referência dos seus resultados.","Acompanhamento próximo e ajuste constante.","Agendar consulta"),
    ("Vagas limitadas para atendimento presencial.","Agenda enxuta para cuidar de cada caso de perto.","Agendar consulta"),
    ("Líder cansado e sem energia? Comece por aqui.","Avaliação completa para empresários e executivos.","Agendar avaliação"),
    ("Seu corpo, analisado como nunca antes.","Diagnóstico aprofundado e protocolo individual.","Agendar consulta"),
    ("Saúde de alto nível pede cuidado de alto nível.","Atendimento presencial, individual e preciso.","Agendar consulta"),
    ("Resultados que cabem na sua agenda de executivo.","Protocolo prático para rotina intensa.","Agendar avaliação"),
    ("A diferença está no acompanhamento.","Não é só o plano: é o ajuste constante até o resultado.","Agendar consulta"),
    ("Invista na máquina que move tudo: você.","Nutrição de alta performance, presencial.","Agendar consulta"),
    ("Marque sua avaliação e saia com um plano.","Consulta completa e conduta personalizada.","Agendar consulta"),
]
b2c = [
    ("Seu shape slim, com dieta de vida real.","+2.000 mulheres já transformaram o corpo sem abrir mão da rotina.","Quero começar"),
    ("+2.000 mulheres já conquistaram o shape slim.","Dieta de vida real, sem dieta maluca. Agora é a sua vez.","Quero começar"),
    ("Cansada de dieta que não cabe na sua vida?","Shape slim com dieta de vida real, do seu jeito.","Quero experimentar"),
    ("Barriga seca e cintura fina, sem passar fome.","Dieta de vida real, feita pra sua rotina.","Quero meu shape"),
    ("Comece pela degustação, por R$190.","O método completo na prática, do seu jeito.","Quero começar"),
    ("Sozinha você para. Com a comunidade certa, você evolui.","Entre pro Team Chedid e conquiste seu shape.","Entrar pra comunidade"),
    ("Shape slim sem abrir mão da vida social.","Dieta de vida real que cabe no rolê e na rotina.","Quero começar"),
    ("O método que já mudou +2.000 corpos.","Shape slim com dieta de vida real. Comece hoje.","Quero começar"),
    ("Glúteos e pernas definidos, com plano feito pra você.","Dieta de vida real, sem fórmula genérica.","Quero meu shape"),
    ("Você já se esforça. Falta o método certo.","Shape slim com acompanhamento que funciona.","Quero começar"),
    ("Sua transformação começa por R$190.","Experimente o método. Dieta de vida real, do seu jeito.","Quero experimentar"),
    ("Magra, definida e com energia lá em cima.","Shape slim com dieta de vida real.","Quero começar"),
    ("Pare de recomeçar toda segunda.","Dieta de vida real e uma comunidade que não te deixa parar.","Entrar pra comunidade"),
    ("Dieta de vida real, resultado de verdade.","+2.000 mulheres já provaram. Comece pela degustação.","Quero começar"),
    ("Seu shape dos sonhos cabe na sua rotina.","Plano flexível, sem passar fome.","Quero meu shape"),
    ("Resultado sem terrorismo nutricional.","Shape slim com leveza e dieta de vida real.","Quero começar"),
    ("20 países, +3.000 pacientes, um método.","Conquiste seu shape slim. Comece agora.","Quero começar"),
    ("Foco no shape, sem viver de salada triste.","Dieta de vida real e gostosa. Comece pela degustação.","Quero experimentar"),
    ("A virada que você adia desde janeiro.","Shape slim com dieta de vida real. Bora começar?","Quero começar"),
    ("Entre pra comunidade que transforma corpos.","Team Chedid: método, acompanhamento e resultado.","Entrar pra comunidade"),
]
b2b = [
    ("A saúde do seu time pode ser o próximo salto da empresa.","Uma empresa em Floripa bateu recorde de faturamento.","Vamos conversar"),
    ("Cultura forte começa por gente que se cuida.","Time com mais energia, sono melhor e menos ansiedade.","Vamos conversar"),
    ("Você cuida da sua saúde. E da do seu time?","Levamos o cuidado nutricional pra dentro da sua empresa.","Conhecer o projeto"),
    ("Quando o time se cuida, a empresa inteira sente.","Mais energia, menos faltas, mais resultado.","Vamos conversar"),
    ("Saúde como benefício que dá retorno.","Cuidado nutricional, pessoa por pessoa, na sua empresa.","Conhecer o projeto"),
    ("O case que bateu recorde de faturamento.","Veja o que aconteceu quando o time começou a se cuidar.","Ver o case"),
    ("Seu time merece mais que vale-refeição.","Acompanhamento nutricional de verdade, dentro da empresa.","Vamos conversar"),
    ("Energia que aparece nos resultados.","Quando as pessoas se cuidam, o trabalho rende mais.","Vamos conversar"),
    ("Saúde não é custo. É cultura.","Leve o Projeto Mais Saúde pra sua empresa.","Conhecer o projeto"),
    ("O benefício que seus colaboradores realmente usam.","Cuidado nutricional individual, com método.","Vamos conversar"),
    ("Gente saudável constrói empresa forte.","Vamos conversar sobre a cultura do seu time?","Vamos conversar"),
    ("Da mesa de reunião pro prato de cada um.","Cuidado nutricional pessoa por pessoa.","Conhecer o projeto"),
    ("Menos lezeira, mais foco.","Alimentação que muda o clima e o rendimento da equipe.","Vamos conversar"),
    ("Um programa de saúde que o RH ama mostrar.","Resultados que aparecem e o time sente.","Conhecer o projeto"),
    ("Comece com uma conversa, sem compromisso.","A gente entende a sua empresa antes de propor.","Vamos conversar"),
    ("A saúde do time é decisão de liderança.","Leve o cuidado nutricional pra dentro da empresa.","Conhecer o projeto"),
    ("Performance começa pelo bem-estar de quem entrega.","Cuidado nutricional, pessoa por pessoa.","Vamos conversar"),
    ("O diferencial que retém talento.","Saúde de verdade como parte da cultura.","Conhecer o projeto"),
    ("Transforme a saúde do time e veja o reflexo nos números.","Inspirado num case real em Floripa.","Ver o case"),
    ("Sua empresa pode ser o próximo case.","Vamos conversar sobre o Projeto Mais Saúde?","Vamos conversar"),
]

fronts = [
    {"key":"clinica","pill":"Clínica · Presencial","title":"Clínica presencial",
     "tone":"Autoridade e exclusividade · porta do funil B2B","brand":"Nutri Chedid",
     "cta":"gold","imgs":clinica_imgs,"items":clinica},
    {"key":"b2c","pill":"Consultoria online · B2C","title":"Consultoria online (Team Chedid)",
     "tone":"Shape slim + dieta de vida real · público feminino, compra emocional","brand":"Team Chedid",
     "cta":"gold","imgs":b2c_imgs,"items":b2c},
    {"key":"b2b","pill":"Projeto Mais Saúde · B2B","title":"Projeto Mais Saúde",
     "tone":"Storytelling e cultura · sem venda dura","brand":"Nutri Chedid",
     "cta":"white","imgs":b2b_imgs,"items":b2b},
]

def card(it, idx, f):
    head, sub, cta = it
    img = f["imgs"][idx % len(f["imgs"])]
    cls = "gold" if f["cta"] == "gold" else ""
    return f'''
      <div class="ad">
        <div class="bg"><img src="{U.format(img)}" alt="" loading="lazy" /></div>
        <div class="scrim"></div>
        <div class="ad-top"><div class="ad-brand"><span class="mark">🔱</span><b>{f["brand"]}</b></div><span class="vnum">{idx+1:02d}</span></div>
        <div class="ad-body">
          <h3 class="ad-head">{html.escape(head)}</h3>
          <p class="ad-sub">{html.escape(sub)}</p>
          <span class="ad-cta {cls}">{html.escape(cta)}</span>
        </div>
      </div>'''

sections = ""
for f in fronts:
    cards = "".join(card(it, i, f) for i, it in enumerate(f["items"]))
    sections += f'''
  <section class="front">
    <div class="wrap">
      <div class="front-head">
        <span class="pill">{f["pill"]}</span>
        <h2>{f["title"]}</h2>
        <span class="tone">Tom: {f["tone"]} · 20 variações</span>
      </div>
      <div class="board">{cards}
      </div>
    </div>
  </section>'''

CSS = """
  :root { --accent:#c8a86a; --accent-soft:#e3c48f; --accent-deep:#b9975b; --text:#f5efe5; --muted:#c2b39f; --muted-2:#9a8c79; --line:rgba(255,255,255,0.10); }
  *{box-sizing:border-box;}
  body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;background:radial-gradient(900px 500px at 10% -8%,rgba(200,168,106,0.16),transparent 55%),linear-gradient(180deg,#130d09,#0c0805);color:var(--text);min-height:100vh;-webkit-font-smoothing:antialiased;}
  .example-banner{background:#211b13;color:var(--accent-soft);text-align:center;font-size:13px;padding:8px;letter-spacing:0.06em;}
  .wrap{max-width:1320px;margin:0 auto;padding:0 26px;}
  header.page{text-align:center;padding:52px 0 6px;}
  header.page .eyebrow{color:var(--accent);font-size:13px;letter-spacing:0.20em;text-transform:uppercase;font-weight:700;}
  header.page h1{font-family:Georgia,serif;font-size:clamp(32px,4vw,50px);margin:14px 0 0;letter-spacing:-0.02em;}
  header.page h1 em{color:var(--accent);font-style:italic;}
  header.page p{color:var(--muted);font-size:18px;max-width:700px;margin:14px auto 0;line-height:1.6;}
  .front{padding:42px 0 6px;}
  .front-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:26px;}
  .front-head h2{font-family:Georgia,serif;font-size:clamp(22px,2.4vw,30px);margin:0;color:#fff;}
  .front-head .tone{color:var(--muted-2);font-size:13px;}
  .front-head .pill{font-size:11px;letter-spacing:0.10em;text-transform:uppercase;font-weight:700;color:var(--accent);border:1px solid rgba(200,168,106,0.35);padding:5px 11px;border-radius:999px;}
  .board{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding-bottom:22px;}
  .ad{position:relative;aspect-ratio:4/5;border-radius:18px;overflow:hidden;border:1px solid var(--line);box-shadow:0 20px 46px rgba(0,0,0,0.40);display:flex;flex-direction:column;justify-content:space-between;isolation:isolate;}
  .ad .bg{position:absolute;inset:0;z-index:-2;}
  .ad .bg img{width:100%;height:100%;object-fit:cover;display:block;}
  .ad .scrim{position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(15,10,7,0.70) 0%,rgba(15,10,7,0.10) 30%,rgba(15,10,7,0.55) 60%,rgba(15,10,7,0.95) 100%);}
  .ad-top{display:flex;align-items:center;justify-content:space-between;padding:13px 14px;}
  .ad-brand{display:inline-flex;align-items:center;gap:7px;}
  .ad-brand .mark{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;background:rgba(200,168,106,0.18);border:1px solid rgba(255,255,255,0.14);font-size:14px;}
  .ad-brand b{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:#fff;}
  .vnum{font-size:10px;font-weight:700;color:#20180c;background:linear-gradient(160deg,var(--accent-soft),var(--accent-deep));padding:3px 7px;border-radius:999px;}
  .ad-body{padding:16px 16px 18px;display:grid;gap:9px;}
  .ad-head{font-family:Georgia,serif;font-size:clamp(16px,1.25vw,20px);line-height:1.13;color:#fff;margin:0;text-shadow:0 2px 16px rgba(0,0,0,0.55);}
  .ad-sub{margin:0;font-size:12.5px;line-height:1.45;color:#eae0d0;text-shadow:0 1px 10px rgba(0,0,0,0.5);}
  .ad-cta{display:inline-flex;align-items:center;justify-content:center;width:fit-content;margin-top:3px;background:#fff;color:#20180c;font-weight:800;font-size:12px;padding:9px 15px;border-radius:10px;}
  .ad-cta.gold{background:linear-gradient(160deg,var(--accent-soft),var(--accent-deep));}
  footer{text-align:center;color:var(--muted-2);font-size:13px;padding:26px 0 54px;}
  @media (max-width:1100px){.board{grid-template-columns:repeat(3,1fr);}}
  @media (max-width:820px){.board{grid-template-columns:repeat(2,1fr);}}
  @media (max-width:520px){.board{grid-template-columns:1fr;max-width:420px;margin:0 auto;}}
"""

doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>60 criativos de performance | Nutri Chedid</title>
<style>{CSS}</style>
</head>
<body>
<div class="example-banner">★ MATERIAL DE EXEMPLO · 60 criativos de performance (20 por frente) · copy e imagens ilustrativas</div>
<header class="page">
  <div class="wrap">
    <span class="eyebrow">Performance · Nutri Chedid 🔱</span>
    <h1>Variações de criativos <em>por frente</em></h1>
    <p>20 variações para cada frente da empresa, prontas para teste em escala. Cada card traz um ângulo diferente, no tom calibrado por público.</p>
  </div>
</header>
{sections}
<footer>Material de exemplo · formato feed 4:5 (1080×1350) · 60 variações (20 por frente) · copy e imagens ilustrativas.</footer>
</body>
</html>'''

with open("/Users/gabrieloliveira/Desktop/nutri-chedid/memories/session/exemplo-criativos-60.html","w",encoding="utf-8") as fh:
    fh.write(doc)
print("OK - 60 criativos gerados:", clinica.__len__()+b2c.__len__()+b2b.__len__(), "cards")
