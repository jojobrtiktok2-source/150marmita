"""Gera /1, /2, /3, /4 e /g: cópias de index.html que mudam só os checkouts.

Preencha os links em VARIACOES e rode:
    python tools/gerar_variacoes.py
"""
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Checkouts da página principal (/)
COMPLETO = "https://pay.wiapy.com/0IyEFtOa6kiN"  # 150 Almoços Fitness COMPLETO R$ 29,00
BASICO = "https://pay.wiapy.com/WSMiDkueHtaW"    # Oferta Básica R$ 18,00

VARIACOES = {
    "1": {"completo": "https://pay.cakto.com.br/59w8hya?src=checkout1", "basico": "https://pay.cakto.com.br/3bo9nuh_1284129?src=checkout1", "pixel": False},
    "2": {"completo": "https://pay.cakto.com.br/59w8hya?src=checkout2", "basico": "https://pay.cakto.com.br/3bo9nuh_1284152?src=checkout2", "pixel": False},
    "3": {"completo": "https://pay.cakto.com.br/59w8hya?src=checkout3", "basico": "https://pay.cakto.com.br/3bo9nuh_1284151?src=checkout3", "pixel": False},
    "4": {"completo": COMPLETO, "basico": BASICO, "pixel": False},
    "g": {"completo": "https://pay.cakto.com.br/59w8hya_1284532", "basico": "https://pay.cakto.com.br/3bo9nuh_1284530", "pixel": False, "gtm": True},  # Google Ads
}

# Google Tag Manager, só no /g (entra logo depois do <meta charset>)
GTM = """
  <!-- Google Tag Manager -->
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-KCZ5XCJT"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  </script>
  <!-- /Google Tag Manager -->"""
CHARSET = '<meta charset="UTF-8" />'

# Pixel da Meta (fbq) e o s.js da Tajokefy, que também liga o Pixel pela configuração do painel
PIXEL = [
    re.compile(r'\n  <!-- Pixel da Meta deste domínio.*?</script>\n', re.S),
    re.compile(r'  <script src="https://painel\.tajokefy\.online/s\.js[^"]*" async></script>\n'),
]


def main():
    base = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
    assert base.count(f'href="{COMPLETO}"') == 1 and base.count(f'href="{BASICO}"') == 1

    # arquivos locais passam a apontar um nível acima
    html = re.sub(r'(src|href)="(?!https?:|data:|mailto:|#|/|\.\./)', r'\1="../', base)

    for pasta, links in VARIACOES.items():
        h = html.replace(f'href="{COMPLETO}"', f'href="{links["completo"]}"')
        h = h.replace(f'href="{BASICO}"', f'href="{links["basico"]}"')
        if not links["pixel"]:
            for padrao in PIXEL:
                h, n = padrao.subn("\n" if padrao is PIXEL[0] else "", h)
                assert n == 1, padrao.pattern
            assert "fbq" not in h and "tajokefy.online/s.js" not in h
        if links.get("gtm"):
            assert h.count(CHARSET) == 1
            h = h.replace(CHARSET, CHARSET + GTM)
        os.makedirs(os.path.join(RAIZ, pasta), exist_ok=True)
        with open(os.path.join(RAIZ, pasta, "index.html"), "w", encoding="utf-8") as f:
            f.write(h)
        print(f"/{pasta}: completo={links['completo']} basico={links['basico']} pixel={links['pixel']}")


if __name__ == "__main__":
    main()
