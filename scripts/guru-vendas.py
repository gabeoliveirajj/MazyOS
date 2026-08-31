#!/usr/bin/env python3
"""Extrai as vendas aprovadas da Digital Manager Guru num período e monta a
linha de KPI de cada uma (nome, telefone, produto, valor, forma de pagamento,
parcelas, valor da parcela).

Precisa do token da Guru no .env:
    GURU_API_TOKEN=<token de usuário da Guru>
(Guru → menu do perfil → Configurações → Integrações → API / Token de usuário)

Uso:
  python3 scripts/guru-vendas.py 2026-08-03 2026-08-04
  python3 scripts/guru-vendas.py 2026-08-03 2026-08-04 --csv saidas/kpis-vendas.csv
  python3 scripts/guru-vendas.py 2026-08-03 2026-08-04 --raw   -> dump do JSON cru

O que a Guru NÃO responde (fica pra preencher na mão, olhando a conversa):
  - tipo de lead (novo-indicação / novo-tráfego / antigo)
  - se iniciou por bot ou por contato humano
"""
import csv, json, os, sys, urllib.request, urllib.error, urllib.parse

BASE = "https://digitalmanager.guru/api/v2"


def load_env(key):
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
        d = os.path.dirname(d)
    return os.environ.get(key)


def get(path, params, token):
    url = BASE + path + '?' + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    })
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:800]


def dig(obj, *caminhos):
    """Pega o primeiro caminho que existir. dig(t, 'payment.total', 'value')"""
    for c in caminhos:
        cur = obj
        for parte in c.split('.'):
            if isinstance(cur, dict) and parte in cur:
                cur = cur[parte]
            else:
                cur = None
                break
        if cur not in (None, '', []):
            return cur
    return ''


PAGAMENTO = {
    'credit_card': 'Cartão de crédito', 'creditcard': 'Cartão de crédito',
    'billet': 'Boleto', 'boleto': 'Boleto', 'bank_slip': 'Boleto',
    'pix': 'Pix', 'paypal': 'PayPal', 'debit_card': 'Cartão de débito',
}


def linha(t):
    metodo = str(dig(t, 'payment.method', 'payment_method', 'method') or '')
    parcelas = dig(t, 'payment.installments.quantity', 'installments',
                   'payment.installments') or 1
    if isinstance(parcelas, dict):
        parcelas = parcelas.get('quantity', 1)
    total = dig(t, 'payment.total', 'payment.value', 'value', 'total') or 0
    vparcela = dig(t, 'payment.installments.value', 'installment_value')
    try:
        if not vparcela and float(total) and int(parcelas):
            vparcela = round(float(total) / int(parcelas), 2)
    except (TypeError, ValueError):
        vparcela = ''
    return {
        'data': str(dig(t, 'dates.confirmed_at', 'dates.ordered_at',
                        'confirmed_at', 'ordered_at', 'created_at'))[:10],
        'cliente': dig(t, 'contact.name', 'customer.name', 'name'),
        'telefone': dig(t, 'contact.phone_number', 'contact.phone',
                        'customer.phone_number', 'phone'),
        'email': dig(t, 'contact.email', 'customer.email', 'email'),
        'produto': dig(t, 'product.name', 'products.0.name', 'product_name'),
        'valor_total': total,
        'forma_pagamento': PAGAMENTO.get(metodo.lower(), metodo),
        'parcelas': parcelas,
        'valor_parcela': vparcela,
        'tipo_lead': '',        # preencher na mão (conversa / origem)
        'bot_ou_humano': '',    # preencher na mão (conversa)
        'id_guru': dig(t, 'id', 'transaction_id'),
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 2:
        sys.exit(__doc__)
    ini, fim = args[0], args[1]
    token = load_env('GURU_API_TOKEN')
    if not token:
        sys.exit("ERRO: GURU_API_TOKEN não está no .env.\n"
                 "Pegue em: Guru → Configurações → Integrações → API (token de usuário)\n"
                 "e adicione a linha  GURU_API_TOKEN=<token>  no arquivo .env")

    transacoes, cursor, pagina = [], None, 1
    while True:
        params = {'ordered_at_ini': ini, 'ordered_at_end': fim,
                  'transaction_status': 'approved'}
        if cursor:
            params['cursor'] = cursor
        st, d = get('/transactions', params, token)
        if st != 200:
            sys.exit(f"ERRO {st} na API da Guru:\n{d}")
        if '--raw' in sys.argv:
            print(json.dumps(d, ensure_ascii=False, indent=2)[:6000])
            return
        lote = d.get('data', d if isinstance(d, list) else [])
        transacoes += lote
        cursor = d.get('next_cursor') if isinstance(d, dict) else None
        if not cursor or not lote:
            break
        pagina += 1
        if pagina > 20:
            break

    linhas = [linha(t) for t in transacoes]
    print(f"{len(linhas)} venda(s) aprovada(s) entre {ini} e {fim}\n")
    for l in linhas:
        print(f"{l['data']} | {l['cliente']} | {l['telefone']} | {l['produto']} | "
              f"R${l['valor_total']} | {l['forma_pagamento']} | {l['parcelas']}x "
              f"de R${l['valor_parcela']}")

    if '--csv' in sys.argv:
        destino = sys.argv[sys.argv.index('--csv') + 1]
        with open(destino, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()) if linhas else
                               ['data', 'cliente', 'telefone', 'email', 'produto',
                                'valor_total', 'forma_pagamento', 'parcelas',
                                'valor_parcela', 'tipo_lead', 'bot_ou_humano', 'id_guru'])
            w.writeheader()
            w.writerows(linhas)
        print(f"\nCSV salvo em {destino}")


if __name__ == '__main__':
    main()
