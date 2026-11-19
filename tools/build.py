"""Gera a versão do site (index.html + assets/) a partir de entrada-bt.html.

entrada-bt.html é a fonte única do app: é o arquivo publicado no claude.ai e o
que se edita. Rode este script depois de cada alteração para atualizar o site
do GitHub Pages:

    python tools/build.py
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTE = RAIZ / "entrada-bt.html"

src = FONTE.read_text(encoding="utf-8")

css = re.search(r"<style>\n?(.*?)</style>", src, re.S).group(1)
js = re.search(r"<script>\n?(.*?)</script>", src, re.S).group(1)
corpo = re.search(r'(<div class="wrap">.*?<div class="toast" id="toast" hidden></div>)', src, re.S).group(1)
titulo = re.search(r"<title>(.*?)</title>", src).group(1)

index = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="Dimensionamento de padrão de entrada de energia em baixa tensão – Enel SP (ET 0017/0018) e CPFL (GED 13/119).">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{corpo}
<script src="assets/app.js"></script>
</body>
</html>
"""

(RAIZ / "assets").mkdir(exist_ok=True)
(RAIZ / "assets" / "style.css").write_text(css, encoding="utf-8", newline="\n")
(RAIZ / "assets" / "app.js").write_text(js, encoding="utf-8", newline="\n")
(RAIZ / "index.html").write_text(index, encoding="utf-8", newline="\n")
print(f"OK: index.html, assets/style.css ({len(css)} bytes), assets/app.js ({len(js)} bytes)")
