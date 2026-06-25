#!/usr/bin/env python3
"""
Puxa leads do Kommo, prioriza pra reativação e exporta CSV.
Uso: python3 puxar_leads.py [pipeline_id]
  - sem argumento: usa o "Funil de vendas" (consultoria online, padrão).
Lê credenciais do .env na raiz do workspace.
"""
import urllib.request, urllib.error, json, os, sys, time, csv
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=-3))
FUNIL_VENDAS = 12250156  # consultoria online (padrão)

def load_env():
    # procura .env subindo a partir do diretório atual
    d = os.getcwd()
    for _ in range(6):
        p = os.path.join(d, '.env')
        if os.path.exists(p):
            env = {}
            for line in open(p, encoding='utf-8'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
            return env
        d = os.path.dirname(d)
    sys.exit("ERRO: .env não encontrado. Rode a partir do workspace.")

ENV = load_env()
BASE = ENV['KOMMO_BASE_URL']
TOKEN = ENV['KOMMO_LONG_LIVED_TOKEN']

def get(path):
    req = urllib.request.Request(BASE + path, headers={'Authorization': f'Bearer {TOKEN}'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as r:
                return None if r.status == 204 else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 204: return None
            if e.code == 429: time.sleep(1); continue
            raise
    return None

def paginate(path, key):
    items, page = [], 1
    sep = '&' if '?' in path else '?'
    while True:
        d = get(f'{path}{sep}limit=250&page={page}')
        if not d: break
        batch = d.get('_embedded', {}).get(key, [])
        if not batch: break
        items.extend(batch)
        if 'next' not in d.get('_links', {}): break
        page += 1; time.sleep(0.12)
    return items

# tiers de prioridade por etapa (Funil de vendas). Ajuste se mudar o funil.
TIER = {
    94667143: (1, '🔥 Quente — pediu/pronto pra call (CQA)'),
    97793367: (1, '🔥 Quente — proposta já enviada'),
    97793375: (2, '🟠 Morno — estava em Follow-up 2'),
    97793371: (2, '🟠 Morno — estava em Follow-up 1'),
    94667139: (2, '🟠 Morno — diagnóstico iniciado'),
    94667135: (3, '🟡 Teve 1º contato do vendedor'),
    94667131: (3, '🟡 SQL qualificado'),
    94667123: (4, '⚪ MQL (lead novo, nunca trabalhado a fundo)'),
    98528608: (5, '❄️ Frio — entrou e nunca foi triado'),
    94666848: (5, '❄️ Frio — leads de entrada'),
}
# etapas fechadas (won/lost/cliente/perdido) — fora da reativação
EXCLUIR = {97793379, 97793383, 142, 143}

def main():
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else FUNIL_VENDAS
    pipes = get('/api/v4/leads/pipelines')['_embedded']['pipelines']
    pipe_name = {p['id']: p['name'] for p in pipes}
    status_name, status_sort = {}, {}
    for p in pipes:
        for s in p['_embedded']['statuses']:
            status_name[(p['id'], s['id'])] = s['name']
            status_sort[(p['id'], s['id'])] = s['sort']
    users = {u['id']: u['name'] for u in get('/api/v4/users')['_embedded']['users']}

    print("Puxando contatos..."); contacts = paginate('/api/v4/contacts', 'contacts')
    cmap = {}
    for c in contacts:
        phone = ''
        for f in (c.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE' and f.get('values'):
                phone = f['values'][0].get('value', ''); break
        cmap[c['id']] = (c.get('name', '') or '', phone)

    print("Puxando leads..."); leads = paginate('/api/v4/leads?with=contacts', 'leads')
    now = time.time(); rows = []
    for l in leads:
        if l['pipeline_id'] != pid: continue
        sid = l['status_id']
        if sid in EXCLUIR: continue
        tier, label = TIER.get(sid, (6, status_name.get((pid, sid), '?')))
        cid = next((ct['id'] for ct in l.get('_embedded', {}).get('contacts', []) if ct.get('is_main')), None)
        if cid is None and l.get('_embedded', {}).get('contacts'):
            cid = l['_embedded']['contacts'][0]['id']
        cnome, ctel = cmap.get(cid, ('', ''))
        dias = round((now - l['updated_at']) / 86400)
        rows.append({
            'tier': tier, 'prioridade': label,
            'etapa': status_name.get((pid, sid), '?'),
            'contato': cnome or l.get('name', ''), 'telefone': ctel,
            'dias_parado': dias,
            'ultima_atividade': datetime.fromtimestamp(l['updated_at'], TZ).strftime('%d/%m/%Y'),
            'criado_em': datetime.fromtimestamp(l['created_at'], TZ).strftime('%d/%m/%Y'),
            'responsavel': users.get(l['responsible_user_id'], ''),
            'lead_id': l['id'], 'link': f"{BASE}/leads/detail/{l['id']}",
        })
    rows.sort(key=lambda r: (r['tier'], r['dias_parado']))

    slug = pipe_name.get(pid, str(pid)).lower().replace(' ', '-')
    os.makedirs('saidas', exist_ok=True)
    out = f'saidas/leads-reativacao-{slug}.csv'
    cols = ['prioridade', 'etapa', 'contato', 'telefone', 'dias_parado',
            'ultima_atividade', 'criado_em', 'responsavel', 'lead_id', 'link']
    with open(out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader(); [w.writerow(r) for r in rows]

    from collections import Counter
    print(f"\n✅ {out} — {len(rows)} leads ({pipe_name.get(pid)})")
    tc = Counter((r['tier'], r['prioridade']) for r in rows)
    for (_, label), n in sorted(tc.items()):
        print(f"  {label}: {n}")

if __name__ == '__main__':
    main()
