#!/usr/bin/env python3
"""KPI diário: fecha o dia do funil DEGUSTAÇÃO e devolve tudo em JSON.

Quem consome é o Google Apps Script preso na planilha de KPIs, que roda
todo dia às 23h, chama esse endpoint e escreve as linhas.

    GET /api/kpi-diario?key=<WEBHOOK_SECRET>&data=2026-08-05

Sem `data`, fecha o dia de hoje (fuso -03).

De onde vem cada número:
  - leads novos ......... eventos `lead_added` do Kommo no funil Degustação
                          (inclui a fila de entrada, que o /leads normal esconde)
  - receberam proposta .. entraram na etapa "Apresentando" (o bot move sozinho)
  - compraram ........... venda aprovada na Guru; o Kommo entra como conferência
  - perdidos ............ entraram em "venda perdida" + motivo de perda
  - dados de venda ...... transações aprovadas na Guru (7 campos financeiros)

Campos que ficam em branco de propósito (decisão de ago/2026): tipo de lead e
bot-vs-humano. O Kommo não tem esse dado hoje — o widget de WhatsApp registra
as mensagens todas como bot e nenhum lead tem origem gravada. Preencher na mão
até existir tag pra isso.

Rodar local:  python3 api/kpi-diario.py 2026-08-05
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler

TZ = timezone(timedelta(hours=-3))


# ---------------------------------------------------------------- config (env)
def _env(key, default=None):
    if key in os.environ:
        return os.environ[key]
    d = os.path.dirname(os.path.abspath(__file__))
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
SECRET = _env('WEBHOOK_SECRET')
GURU_TOKEN = _env('GURU_API_TOKEN')
GURU_BASE = 'https://digitalmanager.guru/api/v2'

PID_DEG = 13257796               # funil DEGUSTAÇÃO
ST_APRESENTANDO = 102232088      # "recebeu proposta" — o bot move sozinho
ST_PERDIDO = {103047284, 143}    # venda perdida
# Só o MOMENTO DA COMPRA. "Onboarding (D0)" fica de fora de propósito: é a
# ativação da esteira quando a dieta é entregue, dias depois da venda — contar
# ali faria o mesmo cliente aparecer duas vezes, em dois dias diferentes.
ST_COMPROU = {102232084, 142,    # degustação ativo / efetivou consultoria
              108761732}         # Suporte / Aguardando DIETA (destino do webhook)


# ---------------------------------------------------------------- Kommo
def kommo(path):
    req = urllib.request.Request(BASE + path, headers={
        'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.status, (json.load(r) if r.status != 204 else None)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1); continue
            return e.code, None
        except Exception:
            return 0, None
    return 0, None


def eventos(tipo, ini, fim):
    """Todos os eventos de um tipo na janela, paginando até acabar."""
    out, page = [], 1
    while page <= 10:
        st, d = kommo(f'/api/v4/events?filter[type][]={tipo}'
                      f'&filter[created_at][from]={ini}&filter[created_at][to]={fim}'
                      f'&limit=250&page={page}')
        if st != 200 or not isinstance(d, dict):
            break
        lote = d.get('_embedded', {}).get('events', [])
        out += lote
        if len(lote) < 250:
            break
        page += 1
    return out


_cache_lead = {}


def lead(lid):
    if lid not in _cache_lead:
        st, d = kommo(f'/api/v4/leads/{lid}?with=contacts')
        _cache_lead[lid] = d if st == 200 and isinstance(d, dict) else {}
    return _cache_lead[lid]


def contato_do_lead(lid):
    """(nome, telefone) do contato principal do lead."""
    l = lead(lid)
    for c in l.get('_embedded', {}).get('contacts', []):
        st, ct = kommo(f"/api/v4/contacts/{c['id']}")
        if st != 200 or not isinstance(ct, dict):
            continue
        tel = ''
        for f in (ct.get('custom_fields_values') or []):
            if f.get('field_code') == 'PHONE' and f.get('values'):
                tel = f['values'][0].get('value', '')
                break
        return ct.get('name', ''), tel
    return '', ''


def status_depois(ev):
    try:
        return ev['value_after'][0]['lead_status']['id']
    except (KeyError, IndexError, TypeError):
        return None


def motivos_perda():
    st, d = kommo('/api/v4/leads/loss_reasons')
    if st != 200 or not isinstance(d, dict):
        return {}
    return {x['id']: x['name'] for x in d.get('_embedded', {}).get('loss_reasons', [])}


# ---------------------------------------------------------------- Guru
PAGAMENTO = {
    'credit_card': 'Cartão de crédito', 'creditcard': 'Cartão de crédito',
    'billet': 'Boleto', 'boleto': 'Boleto', 'bank_slip': 'Boleto',
    'pix': 'Pix', 'paypal': 'PayPal', 'debit_card': 'Cartão de débito',
}


def dig(obj, *caminhos):
    for c in caminhos:
        cur = obj
        for parte in c.split('.'):
            if isinstance(cur, dict) and parte in cur:
                cur = cur[parte]
            elif isinstance(cur, list) and parte.isdigit() and len(cur) > int(parte):
                cur = cur[int(parte)]
            else:
                cur = None
                break
        if cur not in (None, '', []):
            return cur
    return ''


def vendas_guru(dia):
    """Transações aprovadas do dia. Retorna (linhas, alerta_ou_None)."""
    if not GURU_TOKEN:
        return [], "GURU_API_TOKEN não configurado — bloco de vendas veio vazio"
    linhas, cursor, pagina = [], None, 1
    while pagina <= 20:
        params = {'ordered_at_ini': dia, 'ordered_at_end': dia,
                  'transaction_status': 'approved'}
        if cursor:
            params['cursor'] = cursor
        url = f'{GURU_BASE}/transactions?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {GURU_TOKEN}', 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.load(r)
        except urllib.error.HTTPError as e:
            return linhas, f"Guru respondeu {e.code}"
        except Exception as e:
            return linhas, f"Guru indisponível: {e}"
        lote = d.get('data', d if isinstance(d, list) else [])
        linhas += [_linha_venda(t) for t in lote]
        cursor = d.get('next_cursor') if isinstance(d, dict) else None
        if not cursor or not lote:
            break
        pagina += 1
    return linhas, None


def _linha_venda(t):
    metodo = str(dig(t, 'payment.method', 'payment_method', 'method') or '')
    # a Guru manda 'qty' (confirmado no payload real de 13/08/2026), não 'quantity'
    parcelas = dig(t, 'payment.installments.qty', 'payment.installments.quantity',
                   'installments') or 1
    if isinstance(parcelas, dict):
        parcelas = parcelas.get('qty', parcelas.get('quantity', 1))
    total = dig(t, 'payment.total', 'payment.value', 'value', 'total') or 0
    vparcela = dig(t, 'payment.installments.value', 'installment_value')
    try:
        if not vparcela and float(total) and int(parcelas):
            vparcela = round(float(total) / int(parcelas), 2)
    except (TypeError, ValueError):
        vparcela = ''
    ddi = str(dig(t, 'contact.phone_local_code') or '55')
    fone = str(dig(t, 'contact.phone_number', 'contact.phone', 'phone') or '')
    # Assinatura recorrente: ciclo 1 = cliente NOVO entrando; ciclo >1 = mensalidade
    # de quem já é cliente. Só o ciclo 1 conta como venda nova no KPI do dia.
    ciclo = dig(t, 'invoice.cycle', 'subscription.charged_times') or 1
    try:
        ciclo = int(ciclo)
    except (TypeError, ValueError):
        ciclo = 1
    return {
        'nome': dig(t, 'contact.name', 'customer.name', 'name'),
        'telefone': f'+{ddi}{fone}' if fone and not fone.startswith('+') else fone,
        'produto': dig(t, 'product.name', 'products.0.name', 'product_name'),
        'valor_total': total,
        'forma_pagamento': PAGAMENTO.get(metodo.lower(), metodo),
        'parcelas': parcelas,
        'valor_parcela': vparcela,
        'tipo_lead': '',       # em branco por decisão — não existe no dado hoje
        'bot_ou_humano': '',   # idem
        'ciclo': ciclo,
        'venda_nova': ciclo <= 1,
        'id_guru': dig(t, 'id', 'transaction_id'),
    }


# ---------------------------------------------------------------- núcleo
def fechar_dia(dia):
    """dia = 'YYYY-MM-DD'. Devolve o dict de KPIs."""
    d0 = datetime.strptime(dia, '%Y-%m-%d').replace(tzinfo=TZ)
    ini, fim = int(d0.timestamp()), int((d0 + timedelta(days=1)).timestamp()) - 1
    alertas = []

    # --- leads novos: eventos de criação, filtrados pelo funil Degustação
    novos = []
    for ev in eventos('lead_added', ini, fim):
        lid = ev.get('entity_id')
        if lead(lid).get('pipeline_id') == PID_DEG:
            novos.append(lid)
    novos = sorted(set(novos))

    # --- mudanças de etapa do dia
    proposta, comprou, perdeu = set(), set(), set()
    for ev in eventos('lead_status_changed', ini, fim):
        lid, novo = ev.get('entity_id'), status_depois(ev)
        if novo == ST_APRESENTANDO:
            proposta.add(lid)
        elif novo in ST_COMPROU:
            comprou.add(lid)
        elif novo in ST_PERDIDO and lead(lid).get('pipeline_id') == PID_DEG:
            perdeu.add(lid)

    # --- perdidos: quem é e por quê
    nomes_motivo = motivos_perda()
    perdidos = []
    for lid in sorted(perdeu):
        nome, tel = contato_do_lead(lid)
        mid = lead(lid).get('loss_reason_id')
        perdidos.append({'lead_id': lid, 'nome': nome, 'telefone': tel,
                         'motivo': nomes_motivo.get(mid, '')})
    sem_motivo = sum(1 for p in perdidos if not p['motivo'])
    if sem_motivo:
        alertas.append(f"{sem_motivo} lead(s) perdido(s) sem motivo preenchido no Kommo")

    # --- vendas (Guru manda; Kommo confere)
    vendas, erro_guru = vendas_guru(dia)
    if erro_guru:
        alertas.append(erro_guru)
    if not erro_guru and len(vendas) != len(comprou):
        alertas.append(f"divergência: Guru registrou {len(vendas)} venda(s) e o Kommo "
                       f"moveu {len(comprou)} lead(s) — conferir se o webhook disparou")

    return {
        'data': dia,
        'gerado_em': datetime.now(TZ).strftime('%Y-%m-%d %H:%M'),
        'aquisicao': {
            'leads_novos': len(novos),
            'receberam_proposta': len(proposta),
            'compraram': len(vendas) if not erro_guru else len(comprou),
            'perdidos': len(perdidos),
            'perdidos_detalhe': perdidos,
            # coorte: dos que chegaram HOJE, quantos já andaram hoje mesmo
            'coorte_novos_com_proposta': len(set(novos) & proposta),
            'coorte_novos_que_compraram': len(set(novos) & comprou),
        },
        'vendas': vendas,
        'alertas': alertas,
    }


# ---------------------------------------------------------------- Vercel handler
class handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        q = urllib.parse.urlparse(self.path).query
        query = {k: v[0] for k, v in urllib.parse.parse_qs(q).items()}
        if not SECRET or query.get('key') != SECRET:
            return self._send(401, {'erro': 'não autorizado'})
        dia = query.get('data') or datetime.now(TZ).strftime('%Y-%m-%d')
        try:
            datetime.strptime(dia, '%Y-%m-%d')
        except ValueError:
            return self._send(400, {'erro': 'data inválida, use YYYY-MM-DD'})
        try:
            self._send(200, fechar_dia(dia))
        except Exception as e:
            self._send(500, {'erro': str(e)})


# ---------------------------------------------------------------- teste local
if __name__ == '__main__':
    dia = sys.argv[1] if len(sys.argv) > 1 else datetime.now(TZ).strftime('%Y-%m-%d')
    print(json.dumps(fechar_dia(dia), ensure_ascii=False, indent=2))
