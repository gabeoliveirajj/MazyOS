#!/usr/bin/env python3
"""Webhook Guru -> Kommo: automatiza o handoff de entrada da degustação.

Recebe o POST de "venda aprovada" da Digital Manager Guru, valida que veio
mesmo da Guru (api_token) e que é o produto da DEGUSTAÇÃO, acha o lead pelo
telefone e move pro Funil Suporte / Onboarding (D0) + tag CLIENTE DEGUSTAÇÃO.
Se o comprador ainda não é lead, CRIA o lead direto no Onboarding (D0).
Em qualquer caso, a entrada na etapa dispara a esteira de áudios sozinha.

É a versão automática do fluxo manual de scripts/guru-para-kommo.py.

Deploy: função serverless Python na Vercel (arquivo em /api vira rota
/api/handoff). Config toda por variável de ambiente (ver guia de deploy).
Roda com stdlib pura — sem dependências.
"""
import json, os, re, time, urllib.request, urllib.error, urllib.parse
from http.server import BaseHTTPRequestHandler

# ---------------------------------------------------------------- config (env)
def _env(key, default=None):
    """Lê da env; se não achar, tenta um .env local (pra rodar/testar na mão)."""
    if key in os.environ:
        return os.environ[key]
    d = os.getcwd()
    for _ in range(6):
        p = os.path.join(d, '.env')
        if os.path.exists(p):
            for line in open(p, encoding='utf-8'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    if k.strip() == key:
                        return v.strip()
            break
        d = os.path.dirname(d)
    return default

BASE  = _env('KOMMO_BASE_URL')
TOKEN = _env('KOMMO_LONG_LIVED_TOKEN')
# Autenticação do webhook — dois métodos aceitos (basta um):
#  1) segredo na URL: a Guru chama .../api/handoff?key=<WEBHOOK_SECRET>  (mais simples)
#  2) api_token da Guru no corpo == GURU_API_TOKEN                        (se você tiver o token)
WEBHOOK_SECRET = _env('WEBHOOK_SECRET')
GURU_API_TOKEN = _env('GURU_API_TOKEN')
PRODUCT_IDS = {x.strip() for x in (_env('GURU_PRODUCT_IDS', '') or '').split(',') if x.strip()}
PRODUCT_NAME_CONTAINS = (_env('GURU_PRODUCT_NAME_CONTAINS', '') or '').strip().lower()

PID_DEG    = 13257796          # Funil Degustação
PID_SUP    = 14050808          # Funil Suporte
ST_ONBOARD = 108457804         # Suporte / Onboarding (D0) — onde a esteira dispara
ST_AGUARD  = 108761732         # Suporte / Aguardando ativação — landing pós-compra
# O handoff joga o lead em "Aguardando ativação" (não no Onboarding). A esteira só
# entrega com chat aberto, então o cliente manda a 1ª msg pra Kami (botão wa.me na
# página de obrigado) e uma regra no Kommo move dali pro Onboarding D0 → esteira roda.
HANDOFF_ALVO = ST_AGUARD
FECHADOS   = {142, 143, 103047284}   # won/lost genéricos + venda perdida
TAG        = "CLIENTE DEGUSTAÇÃO"

# ---------------------------------------------------------------- Kommo helpers
def api(path, method='GET', body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.status, (json.load(r) if r.status != 204 else None)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1); continue
            return e.code, e.read().decode()
    return 0, None

def norm(p):
    return re.sub(r'\D', '', p or '')

def chave(p):
    """Últimos 8 dígitos — robusto a formatos diferentes de telefone."""
    d = norm(p)
    return d[-8:] if len(d) >= 8 else d

def buscar_lead_por_telefone(telefone):
    """Retorna (lead, contato_nome, telefone_kommo) ou (None, motivo, '')."""
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
            if not isinstance(ld, dict):
                continue
            aberto = ld['status_id'] not in FECHADOS
            no_deg = ld['pipeline_id'] == PID_DEG
            score = (2 if (no_deg and aberto) else 1 if aberto else 0, ld.get('updated_at', 0))
            if melhor is None or score > melhor[0]:
                melhor = (score, ld, c.get('name', ''), tel)
    if not melhor:
        return None, "contato achado mas sem lead", match[0][1]
    return melhor[1], melhor[2], melhor[3]

def mover_e_taguear(lead, executar=True):
    _, ld = api(f"/api/v4/leads/{lead['id']}?with=contacts")
    tags = [t['name'] for t in (ld.get('_embedded', {}).get('tags') or [])]
    if TAG not in tags:
        tags.append(TAG)
    body = {"pipeline_id": PID_SUP, "status_id": HANDOFF_ALVO,
            "_embedded": {"tags": [{"name": t} for t in tags]}}
    if not executar:
        return {"acao": "mover", "lead_id": lead['id'], "executado": False}
    st, _ = api(f"/api/v4/leads/{lead['id']}", 'PATCH', body)
    return {"acao": "mover", "lead_id": lead['id'], "executado": True, "http": st}

def criar_lead(nome, telefone, executar=True):
    """Cria contato+lead novo direto no Suporte/Onboarding D0 com a tag."""
    nome = nome or "Cliente Degustação"
    body = [{
        "name": f"Degustação — {nome}",
        "pipeline_id": PID_SUP, "status_id": HANDOFF_ALVO,
        "_embedded": {
            "tags": [{"name": TAG}],
            "contacts": [{
                "name": nome,
                "custom_fields_values": [{
                    "field_code": "PHONE",
                    "values": [{"value": telefone, "enum_code": "WORK"}],
                }],
            }],
        },
    }]
    if not executar:
        return {"acao": "criar", "executado": False, "telefone": telefone}
    st, d = api('/api/v4/leads/complex', 'POST', body)
    new_id = None
    if isinstance(d, list) and d:
        new_id = d[0].get('id')
    return {"acao": "criar", "executado": True, "http": st, "lead_id": new_id}

# ---------------------------------------------------------------- webhook core
def _autorizado(payload, query):
    """Aceita o webhook se o segredo da URL OU o api_token baterem."""
    if not WEBHOOK_SECRET and not GURU_API_TOKEN:
        return False, "servidor sem segredo configurado (WEBHOOK_SECRET)"
    if WEBHOOK_SECRET and query.get('key') == WEBHOOK_SECRET:
        return True, None
    if GURU_API_TOKEN and payload.get('api_token') == GURU_API_TOKEN:
        return True, None
    return False, "não autorizado (segredo/token inválido)"

def processar_webhook(payload, query=None, executar=True):
    """Retorna (status_http_pra_responder, dict_resultado)."""
    query = query or {}
    # 1) segurança: o webhook veio mesmo da Guru?
    ok, motivo = _autorizado(payload, query)
    if not ok:
        code = 500 if 'servidor' in motivo else 401
        return code, {"erro": motivo}

    # 2) só venda aprovada
    if payload.get('status') != 'approved':
        return 200, {"ignorado": f"status={payload.get('status')}"}

    # 3) só o produto da degustação
    prod = payload.get('product') or {}
    pid = str(prod.get('id') or prod.get('marketplace_id') or '')
    pname = str(prod.get('name') or '').lower()
    if not PRODUCT_IDS and not PRODUCT_NAME_CONTAINS:
        return 200, {"ignorado": "filtro de produto não configurado (GURU_PRODUCT_IDS)"}
    ok_id = pid in PRODUCT_IDS if PRODUCT_IDS else False
    ok_name = PRODUCT_NAME_CONTAINS in pname if PRODUCT_NAME_CONTAINS else False
    if not (ok_id or ok_name):
        return 200, {"ignorado": f"produto fora do filtro (id={pid}, nome={pname!r})"}

    # 4) telefone do comprador
    contact = payload.get('contact') or {}
    numero = norm(contact.get('phone_number'))
    ddi = norm(contact.get('phone_local_code')) or '55'
    if not numero:
        return 200, {"ignorado": "venda sem telefone no contato"}
    telefone_full = f"+{ddi}{numero}"
    nome = contact.get('name') or ''

    # 5) acha o lead e move; se não existir, cria
    lead, motivo, _ = buscar_lead_por_telefone(numero)
    if lead:
        res = mover_e_taguear(lead, executar)
        res["origem"] = "lead_existente"
    else:
        res = criar_lead(nome, telefone_full, executar)
        res["origem"] = "lead_novo"
        res["motivo_busca"] = motivo
    res["telefone"] = telefone_full
    res["produto"] = pname or pid
    return 200, res

# ---------------------------------------------------------------- Vercel handler
class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # health check
        self._send(200, {"ok": True, "servico": "handoff-degustacao"})

    def do_POST(self):
        try:
            length = int(self.headers.get('content-length') or 0)
            raw = self.rfile.read(length) if length else b''
            payload = json.loads(raw or b'{}')
        except Exception as e:
            return self._send(400, {"erro": f"json inválido: {e}"})
        # segredo vem na query string da URL (?key=...)
        q = urllib.parse.urlparse(self.path).query
        query = {k: v[0] for k, v in urllib.parse.parse_qs(q).items()}
        try:
            code, result = processar_webhook(payload, query, executar=True)
        except Exception as e:
            # 500 => a Guru reenvia (não perde a venda)
            return self._send(500, {"erro": str(e)})
        self._send(code, result)


# ---------------------------------------------------------------- auto-teste local
if __name__ == '__main__':
    # Monta um payload FAKE de venda aprovada usando um lead real da Degustação
    # e roda em DRY-RUN (não altera nada). Prova que o webhook resolve o lead certo.
    WEBHOOK_SECRET = 'TESTE-LOCAL'
    PRODUCT_NAME_CONTAINS = 'degustação'

    _, d = api(f'/api/v4/leads?filter[pipeline_id]={PID_DEG}&with=contacts&limit=5')
    tel = ''
    for l in (d or {}).get('_embedded', {}).get('leads', []):
        cid = next((c['id'] for c in l.get('_embedded', {}).get('contacts', [])), None)
        if not cid:
            continue
        _, c = api(f'/api/v4/contacts/{cid}')
        for f in (c.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE' and f.get('values'):
                tel = f['values'][0].get('value', ''); break
        if tel:
            break
    fake = {
        "status": "approved", "webhook_type": "transaction",
        "product": {"id": "PROD-DEGUSTACAO", "name": "Degustação Team Chedid"},
        "contact": {"name": "Comprador Teste", "phone_local_code": "55",
                    "phone_number": norm(tel)[-11:] if tel else ""},
    }
    print("=== AUTO-TESTE (dry-run) webhook Guru->Kommo ===")
    print("payload.contact.phone_number:", fake['contact']['phone_number'])
    code, res = processar_webhook(fake, {"key": "TESTE-LOCAL"}, executar=False)
    print("resposta HTTP:", code)
    print("resultado    :", json.dumps(res, ensure_ascii=False, indent=2))
