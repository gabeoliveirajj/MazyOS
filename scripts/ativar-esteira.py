#!/usr/bin/env python3
"""Ativar a esteira: dieta entregue -> move o lead pro Onboarding D0.

Passo MANUAL do 2º gatilho da degustação. A esteira de áudios (D0->D26) tem
que começar no dia em que a DIETA é entregue (~7 dias depois da compra, e
variável), NÃO no dia da compra. Regra trazida pela Kami.

Fluxo: compra -> webhook joga o lead em "Aguardando entrega da dieta". A Kami
entrega a dieta e te avisa. Você roda este comando com o telefone do cliente:
acha o lead, move de "Aguardando entrega da dieta" -> "Onboarding (D0)" e a
esteira dispara sozinha na entrada da etapa (D0 = dia da entrega).

Uso:
  python3 scripts/ativar-esteira.py                 -> auto-teste (dry-run c/ um lead real)
  python3 scripts/ativar-esteira.py "+55 48 9...."  -> dry-run pra esse telefone
  python3 scripts/ativar-esteira.py "<tel>" --executar  -> EXECUTA de verdade (move)

Irmão do scripts/guru-para-kommo.py (o handoff da compra). Mesmos IDs, mesma
lógica de casar pelo telefone (últimos 8 dígitos).
"""
import urllib.request, json, sys, re, time, os

def load_env():
    d = os.getcwd()
    for _ in range(6):
        p = os.path.join(d, '.env')
        if os.path.exists(p):
            e = {}
            for line in open(p, encoding='utf-8'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1); e[k.strip()] = v.strip()
            return e
        d = os.path.dirname(d)
    sys.exit("ERRO: .env não encontrado.")

ENV = load_env()
BASE = ENV['KOMMO_BASE_URL']; TOKEN = ENV['KOMMO_LONG_LIVED_TOKEN']

PID_SUP = 14050808           # Funil Suporte
ST_AGUARD = 108761732        # Suporte / Aguardando entrega da dieta (landing pós-compra)
ST_ONBOARD = 108457804       # Suporte / Onboarding (D0) — onde a esteira dispara
ALVO = ST_ONBOARD            # a ativação move pra cá
FECHADOS = {142, 143, 103047284}  # won/lost genéricos + venda perdida

def api(path, method='GET', body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, (json.load(r) if r.status != 204 else None)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(1); continue
            return e.code, e.read().decode()
    return 0, None

def norm(p):
    return re.sub(r'\D', '', p or '')

def chave(p):
    """Últimos 8 dígitos — robusto a formatos diferentes de telefone."""
    d = norm(p)
    return d[-8:] if len(d) >= 8 else d

def buscar_lead_por_telefone(telefone):
    """Retorna (lead, contato_nome, telefone_kommo) ou (None, motivo, '').
    Pra ATIVAÇÃO, prefere o lead que está em Suporte / Aguardando entrega da dieta."""
    k = chave(telefone)
    if not k:
        return None, "telefone vazio/inválido", ""
    _, d = api(f'/api/v4/contacts?query={k}&with=leads&limit=50')
    contatos = (d or {}).get('_embedded', {}).get('contacts', []) if isinstance(d, dict) else []
    match = []
    for c in contatos:
        for f in (c.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE':
                for v in (f.get('values') or []):
                    if chave(v.get('value')) == k:
                        match.append((c, v.get('value')))
    if not match:
        return None, f"nenhum contato com o telefone (chave {k})", ""
    melhor = None
    for c, tel in match:
        for l in c.get('_embedded', {}).get('leads', []):
            _, ld = api(f"/api/v4/leads/{l['id']}")
            if not isinstance(ld, dict): continue
            aberto = ld['status_id'] not in FECHADOS
            no_sup = ld['pipeline_id'] == PID_SUP
            aguardando = no_sup and ld['status_id'] == ST_AGUARD
            # prioridade: aguardando entrega (3) > qualquer aberto no Suporte (2) > aberto (1) > fechado (0)
            nivel = 3 if aguardando else 2 if (no_sup and aberto) else 1 if aberto else 0
            score = (nivel, ld.get('updated_at', 0))
            if melhor is None or score > melhor[0]:
                melhor = (score, ld, c.get('name', ''), tel)
    if not melhor:
        return None, "contato achado mas sem lead", match[0][1]
    return melhor[1], melhor[2], melhor[3]

def ativar(lead, executar=False):
    if lead['pipeline_id'] == PID_SUP and lead['status_id'] == ST_ONBOARD:
        return "já está em Onboarding D0 (esteira já ativada) — nada a fazer"
    if lead['status_id'] != ST_AGUARD:
        aviso = f"⚠️ lead NÃO está em 'Aguardando entrega da dieta' (está em status {lead['status_id']}). "
    else:
        aviso = ""
    body = {"pipeline_id": PID_SUP, "status_id": ALVO}
    if not executar:
        return aviso + "DRY-RUN (nada alterado) — rode com --executar pra mover pro Onboarding D0"
    st, _ = api(f"/api/v4/leads/{lead['id']}", 'PATCH', body)
    return aviso + f"movido pro Onboarding D0 → esteira disparada (HTTP {st})"

def processar(telefone, executar=False):
    print(f"Telefone recebido: {telefone!r}  (chave de busca: {chave(telefone)})")
    lead, nome, tel = buscar_lead_por_telefone(telefone)
    if not lead:
        print(f"  ❌ {nome}")
        return
    print(f"  ✅ Lead #{lead['id']} — contato: {nome} — tel Kommo: {tel}")
    print(f"     está em pipeline {lead['pipeline_id']} / status {lead['status_id']}")
    print(f"     ação: {ativar(lead, executar)}")

def auto_teste():
    """Pega um lead em Aguardando entrega da dieta e roda a busca (dry-run)."""
    _, d = api(f'/api/v4/leads?filter[statuses][0][pipeline_id]={PID_SUP}'
               f'&filter[statuses][0][status_id]={ST_AGUARD}&with=contacts&limit=5')
    leads = (d or {}).get('_embedded', {}).get('leads', [])
    for l in leads:
        cid = next((c['id'] for c in l.get('_embedded', {}).get('contacts', [])), None)
        if not cid: continue
        _, c = api(f'/api/v4/contacts/{cid}')
        tel = ''
        for f in (c.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE' and f.get('values'):
                tel = f['values'][0].get('value', ''); break
        if tel:
            print("=== AUTO-TESTE (dry-run) com um lead em Aguardando entrega da dieta ===")
            processar(tel, executar=False)
            return
    print("Não achei lead em 'Aguardando entrega da dieta' pra auto-testar.")

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--executar']
    executar = '--executar' in sys.argv
    if args:
        processar(args[0], executar=executar)
    else:
        auto_teste()
