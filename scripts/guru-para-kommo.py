#!/usr/bin/env python3
"""Handoff de entrada: venda aprovada na Guru -> move o lead pro Funil Suporte.

Dado um TELEFONE (do webhook de venda aprovada da Digital Manager Guru), acha o
lead no Kommo, move pro Funil Suporte / Onboarding (D0) e marca a tag
CLIENTE DEGUSTAÇÃO. O bot da esteira dispara sozinho na entrada da etapa.

Uso:
  python3 scripts/guru-para-kommo.py                 -> auto-teste (dry-run com um lead real)
  python3 scripts/guru-para-kommo.py "+55 48 9....." -> dry-run pra esse telefone
  python3 scripts/guru-para-kommo.py "<tel>" --executar  -> EXECUTA de verdade (move + tag)
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

PID_DEG = 13257796           # Funil Degustação
PID_SUP = 14050808           # Funil Suporte
ST_ONBOARD = 108457804       # Suporte / Onboarding (D0)
FECHADOS = {142, 143, 103047284}  # won/lost genéricos + venda perdida
TAG = "CLIENTE DEGUSTAÇÃO"

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
    """Últimos 8 dígitos (número sem país/DDD) — robusto a formatos diferentes."""
    d = norm(p)
    return d[-8:] if len(d) >= 8 else d

def buscar_lead_por_telefone(telefone):
    """Retorna (lead, contato_nome, telefone_kommo) ou (None, motivo, '')."""
    k = chave(telefone)
    if not k:
        return None, "telefone vazio/inválido", ""
    _, d = api(f'/api/v4/contacts?query={k}&with=leads&limit=50')
    contatos = (d or {}).get('_embedded', {}).get('contacts', []) if isinstance(d, dict) else []
    # confere o telefone de verdade (query é fuzzy)
    match = []
    for c in contatos:
        for f in (c.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE':
                for v in (f.get('values') or []):
                    if chave(v.get('value')) == k:
                        match.append((c, v.get('value')))
    if not match:
        return None, f"nenhum contato com o telefone (chave {k})", ""
    # entre os leads do(s) contato(s), prefere lead ABERTO no funil Degustação
    melhor = None
    for c, tel in match:
        for l in c.get('_embedded', {}).get('leads', []):
            _, ld = api(f"/api/v4/leads/{l['id']}")
            if not isinstance(ld, dict): continue
            aberto = ld['status_id'] not in FECHADOS
            no_deg = ld['pipeline_id'] == PID_DEG
            score = (2 if (no_deg and aberto) else 1 if aberto else 0, ld.get('updated_at', 0))
            if melhor is None or score > melhor[0]:
                melhor = (score, ld, c.get('name', ''), tel)
    if not melhor:
        return None, "contato achado mas sem lead", match[0][1]
    return melhor[1], melhor[2], melhor[3]

def mover_e_taguear(lead, executar=False):
    _, ld = api(f"/api/v4/leads/{lead['id']}?with=contacts")
    tags = [t['name'] for t in (ld.get('_embedded', {}).get('tags') or [])]
    if TAG not in tags: tags.append(TAG)
    body = {"pipeline_id": PID_SUP, "status_id": ST_ONBOARD,
            "_embedded": {"tags": [{"name": t} for t in tags]}}
    if not executar:
        return "DRY-RUN (nada alterado)"
    st, _ = api(f"/api/v4/leads/{lead['id']}", 'PATCH', body)
    return f"movido + tagueado (HTTP {st})"

def processar(telefone, executar=False):
    print(f"Telefone recebido: {telefone!r}  (chave de busca: {chave(telefone)})")
    lead, nome, tel = buscar_lead_por_telefone(telefone)
    if not lead:
        print(f"  ❌ {nome}")
        return
    print(f"  ✅ Lead #{lead['id']} — contato: {nome} — tel Kommo: {tel}")
    print(f"     está em pipeline {lead['pipeline_id']} / status {lead['status_id']}")
    print(f"     ação: {mover_e_taguear(lead, executar)}")

def auto_teste():
    """Pega um lead real da Degustação, lê o telefone do contato, e roda a busca (dry-run)."""
    _, d = api(f'/api/v4/leads?filter[pipeline_id]={PID_DEG}&with=contacts&limit=5')
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
            print("=== AUTO-TESTE (dry-run) com um lead real da Degustação ===")
            processar(tel, executar=False)
            return
    print("Não achei lead com telefone na Degustação pra auto-testar.")

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--executar']
    executar = '--executar' in sys.argv
    if args:
        processar(args[0], executar=executar)
    else:
        auto_teste()
