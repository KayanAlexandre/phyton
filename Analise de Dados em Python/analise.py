"""
Redes sociais no Brasil (TikTok, Instagram, WhatsApp e YouTube) com DADOS REAIS.
Gera apenas index.html (site com uma aba por rede) na pasta do script.

Instalar: pip install numpy pandas matplotlib seaborn
Rodar:    python analise_redes_sociais.py
"""
import base64
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=0.95)

REGIOES = ["Sudeste", "Nordeste", "Sul", "Norte", "Centro-Oeste"]
HORAS = ["até 9h", "9-12h", "12-13h", "13-18h", "18-20h", "20-00h", "após 0h"]
IDADE_CETIC = ["10-15", "16-24", "25-34", "35-44", "45-59", "60+"]

DR = "DataReportal, Digital 2026: Brazil (out/2025), anúncios, adultos"
C5 = "Cetic.br, TIC Domicílios 2025, tabela C5"
TC5B = "Cetic.br, TIC Domicílios 2025, tabela TC5B"
MLABS = "DataReportal Digital 2025: Brazil (Android), via mLabs"
NOTA_RS = "Proxy: % dos usuários de internet de cada região que usaram redes sociais."


def D(x, y, tipo, fonte, nota="", proxy=False, titulo=""):
    """tipo 'comp' = composicao (soma 100%); 'taxa' = % de cada grupo que usa."""
    return dict(x=x, y=np.array(y, dtype=float), tipo=tipo, fonte=fonte,
                nota=nota, proxy=proxy, titulo=titulo)


# horas por mes no app (Android): 28h34, 24h35, 23h35
TEMPO_MES = {"TikTok": 28 + 34 / 60, "WhatsApp": 24 + 35 / 60, "Instagram": 23 + 35 / 60}

REDES = {
    "TikTok": dict(cor="#e0245e", tempo=None,
        idade=D(["18-24", "25-34", "35-44", "45-54", "55+"], [24.999, 51.008, 21.871, 15.288, 16.402],
                "comp", "TikTok Ads Manager via Affect Group (abr/2026), usuários 18+"),
        sexo=D(["Feminino", "Masculino"], [41.4, 58.6], "comp", DR),
        regiao=D(REGIOES, [83, 76, 84, 81, 81], "taxa", C5, NOTA_RS, True),
        hora=D(HORAS, [9, 13, 9, 14, 24, 29, 2], "comp",
               "Opinion Box, relatório TikTok (jan/2026, n=1.066)", "Faixa do dia em que mais usa.")),
    "Instagram": dict(cor="#8a3ab9", tempo=None,
        idade=D(["18-24", "25-34", "35-44", "45-54", "55-64", "65+"], [20.2, 31.3, 20.6, 13.9, 8.3, 5.7],
                "comp", "NapoleonCat (jul/2026), usuários 18+"),
        sexo=D(["Feminino", "Masculino"], [57.1, 42.8], "comp", DR),
        regiao=D(REGIOES, [83, 76, 84, 81, 81], "taxa", C5, NOTA_RS, True),
        hora=D(HORAS, [14, 10, 10, 18, 20, 27, 1], "comp",
               "Opinion Box, relatório Instagram (dez/2025, n=1.102)", "Faixa do dia em que mais usa.")),
    "WhatsApp": dict(cor="#1f9d55", tempo=None,
        idade=D(IDADE_CETIC, [73, 95, 97, 95, 95, 83], "taxa", C5,
                "Proxy: % de cada faixa, entre usuários de internet, que mandou mensagens instantâneas.", True),
        sexo=D(["Feminino", "Masculino"], [93, 90], "taxa", C5,
               "Proxy: % dos usuários de internet que mandou mensagens instantâneas.", True),
        regiao=D(REGIOES, [94, 89, 93, 86, 92], "taxa", C5,
                 "Proxy: % dos usuários de internet que mandou mensagens instantâneas.", True),
        hora=D(["Aberto o tempo todo", "Várias vezes ao dia", "Restante"], [34, 61, 5], "comp",
               "Opinion Box, pesquisa WhatsApp (jun/2025, n=1.126)",
               "Não há dado por horário. Entre quem usa todo dia (97%); o restante é 100 - 34 - 61.",
               True, "Frequência de uso")),
    "YouTube": dict(cor="#d62d20",
        tempo=D(["Mais de 5 h/semana", "Até 5 h/semana"], [47, 53], "comp",
                "Opinion Box, via Teletime (jul/2025)", "Não há dado mensal do app; o 'até 5 h' é 100 - 47."),
        idade=D(IDADE_CETIC, [68, 67, 69, 56, 43, 15], "taxa", TC5B,
                "Proxy: % de cada faixa que assistiu vídeos em sites/apps de compartilhamento.", True),
        sexo=D(["Feminino", "Masculino"], [51.9, 48.1], "comp", DR),
        regiao=D(REGIOES, [53, 45, 56, 48, 46], "taxa", TC5B,
                 "Proxy: % da população da região que assistiu vídeos em sites/apps de compartilhamento.", True),
        hora=D(["Manhã", "Tarde", "Noite"], [22, 24, 54], "comp", "Opinion Box, via Teletime (2025)",
               "Período do dia em que mais usa.")),
}

FONTES = [
    ("DataReportal, Digital 2026: Brazil", "https://datareportal.com/reports/digital-2026-brazil"),
    ("NapoleonCat, usuários por idade", "https://stats.napoleoncat.com/social-media-users-in-brazil/"),
    ("Affect Group, TikTok por idade", "https://affectgroup.com/blog/brazil-tiktok-audience-by-age-and-gender/"),
    ("Cetic.br, TIC Domicílios 2025 (C5)", "https://cetic.br/en/tics/domicilios/2025/individuos/C5/"),
    ("Cetic.br, TIC Domicílios 2025 (TC5B)", "https://cetic.br/en/tics/domicilios/2025/individuos/TC5B/"),
    ("Opinion Box, TikTok 2026", "https://content.app-us1.com/JY8yY/2026/03/02/80c8ddfb-d24a-4e2f-91d0-fbbc0d66a729.pdf"),
    ("Opinion Box, Instagram 2026", "https://content.app-us1.com/JY8yY/2026/07/03/4325b602-1950-454c-90d7-c127fabbca70.pdf"),
    ("Teletime, Opinion Box sobre YouTube", "https://teletime.com.br/15/07/2025/no-brasil-oito-em-cada-dez-usuarios-do-youtube-acessam-plataforma-diariamente/"),
    ("Canaltech, Opinion Box sobre WhatsApp", "https://canaltech.com.br/apps/o-que-os-brasileiros-mais-fazem-no-whatsapp-segundo-pesquisa/"),
    ("mLabs, tempo de uso", "https://www.mlabs.com.br/blog/comportamento-da-audiencia-digital/"),
]


def b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


def valores(d):
    """Normaliza composicoes para somar 100%."""
    return d["y"] / d["y"].sum() * 100 if d["tipo"] == "comp" else d["y"]


def barras(d, cor, titulo, horizontal=False):
    df = pd.DataFrame({"x": d["x"], "y": valores(d)})
    fig, ax = plt.subplots(figsize=(6, 3.6))
    rot = "% dos usuários" if d["tipo"] == "comp" else "% que usa"
    if horizontal:
        sns.barplot(data=df, y="x", x="y", color=cor, ax=ax)
        ax.set(xlabel=rot, ylabel="")
        ax.margins(x=0.15)
    else:
        sns.barplot(data=df, x="x", y="y", color=cor, ax=ax)
        ax.set(xlabel="", ylabel=rot)
        ax.margins(y=0.15)
        ax.tick_params(axis="x", labelsize=8)
    ax.bar_label(ax.containers[0], fmt="%.1f", padding=2)
    ax.set_title(titulo)
    return b64(fig)


def pizza(d, cor, titulo):
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.pie(valores(d), labels=d["x"], autopct="%.1f%%", startangle=90,
           colors=[cor, "#c9ced6"], wedgeprops=dict(edgecolor="white"))
    ax.set_title(titulo)
    return b64(fig)


def grafico_tempo(rede, p):
    if p["tempo"] is not None:
        return pizza(p["tempo"], p["cor"], "Tempo de uso por semana"), p["tempo"]
    s = pd.Series(TEMPO_MES).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 3.6))
    sns.barplot(x=s.index, y=s.values, color="#c9ced6", ax=ax)
    for patch, nome in zip(ax.patches, s.index):
        if nome == rede:
            patch.set_facecolor(p["cor"])
    ax.bar_label(ax.containers[0], labels=[f"{h:.1f} h" for h in s.values], padding=2)
    ax.set(title="Horas por mês no app (Android)", xlabel="", ylabel="Horas por mês")
    ax.margins(y=0.15)
    min_dia = np.round(TEMPO_MES[rede] * 60 / 30)
    nota = f"Média de {TEMPO_MES[rede]:.1f} h por mês, cerca de {min_dia:.0f} min por dia. YouTube fica fora: sem dado mensal."
    return b64(fig), D([], [1], "comp", MLABS, nota)


def montar_graficos(rede, p):
    saida = []
    img, d = grafico_tempo(rede, p)
    saida.append(("Tempo de uso", img, d))
    saida.append(("Faixa etária", barras(p["idade"], p["cor"], "Uso por faixa etária (anos)"), p["idade"]))
    sx = p["sexo"]
    img = pizza(sx, p["cor"], "Distribuição por sexo") if sx["tipo"] == "comp" else barras(sx, p["cor"], "Uso por sexo")
    saida.append(("Sexo", img, sx))
    saida.append(("Regiões do Brasil", barras(p["regiao"], p["cor"], "Uso por região", True), p["regiao"]))
    h = p["hora"]
    saida.append(("Horários de acesso", barras(h, p["cor"], h["titulo"] or "Horário de maior uso"), h))
    return saida


def topo(d):
    return d["x"][int(np.argmax(d["y"]))]


def resumo(rede, p):
    if rede in TEMPO_MES:
        h = TEMPO_MES[rede]
        tempo = f"{int(h)}h{int(round((h % 1) * 60)):02d} por mês"
    else:
        tempo = "47% passam mais de 5 h/semana"
    return [("Tempo", tempo), ("Faixa etária líder", topo(p["idade"])), ("Sexo líder", topo(p["sexo"])),
            ("Região líder", topo(p["regiao"])), ("Pico", str(topo(p["hora"])))]


def tabela_dados():
    linhas = []
    for rede, p in REDES.items():
        for ind in ["idade", "sexo", "regiao", "hora"]:
            d = p[ind]
            for x, y in zip(d["x"], d["y"]):
                linhas.append(dict(rede=rede, indicador=ind, categoria=x, valor=y, tipo=d["tipo"],
                                   proxy=d["proxy"], fonte=d["fonte"]))
    return pd.DataFrame(linhas)


HTML = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Redes sociais no Brasil: análise de dados</title>
<style>
:root{--bg:#f5f6f8;--card:#fff;--tx:#1b1f27;--mut:#5d6675;--bd:#dfe3ea;box-sizing:border-box;
padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14171c;--card:#1d222a;--tx:#eef0f4;--mut:#a3acba;--bd:#2c333e}}
:root[data-theme="dark"]{--bg:#14171c;--card:#1d222a;--tx:#eef0f4;--mut:#a3acba;--bd:#2c333e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font-family:"Segoe UI",system-ui,Arial,sans-serif;line-height:1.5}
header,main,footer{max-width:1100px;margin:0 auto;padding:0 20px}
header{padding-top:32px}
h1{font-size:clamp(1.6rem,4vw,2.4rem);margin:0 0 6px}
header p{color:var(--mut);margin:0 0 20px;max-width:75ch}
nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}
nav button{font:inherit;font-weight:600;padding:10px 18px;border-radius:999px;border:2px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer}
nav button.on{background:var(--c);border-color:var(--c);color:#fff}
nav button:focus-visible{outline:3px solid var(--c);outline-offset:2px}
.panel{display:none}.panel.on{display:block}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:18px}
.stat{background:var(--card);border:1px solid var(--bd);border-left:5px solid var(--c);border-radius:8px;padding:10px 14px}
.stat span{display:block;color:var(--mut);font-size:.85rem}.stat b{font-size:1.05rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:16px}
figure{margin:0;background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:14px}
figure h2{font-size:1.05rem;margin:0 0 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.tag{font-size:.72rem;font-weight:600;padding:2px 8px;border-radius:999px;border:1px solid var(--bd);color:var(--mut)}
.tag.proxy{border-color:#b7791f;color:#b7791f}
.img{background:#fff;border-radius:6px;overflow-x:auto}
img{display:block;max-width:100%;height:auto;margin:0 auto}
figcaption{color:var(--mut);font-size:.88rem;margin-top:8px}
footer{color:var(--mut);font-size:.88rem;padding-top:24px;padding-bottom:32px}
footer a{color:inherit}
</style></head><body>
<header><h1>Redes sociais no Brasil</h1>
<p>Análise com dados reais de pesquisas publicadas até out/2026. Cada gráfico traz sua fonte.</p>
<nav role="tablist">__TABS__</nav></header>
<main>__PANELS__</main>
<footer><b>Fontes</b><ul>__FONTES__</ul>
Estimativas de alcance publicitário e pesquisas online não medem a população inteira. Dados de períodos diferentes não são diretamente comparáveis.</footer>
<script>
document.querySelectorAll("nav button").forEach(function(b){b.addEventListener("click",function(){
document.querySelectorAll("nav button,.panel").forEach(function(e){e.classList.remove("on")});
b.classList.add("on");document.getElementById(b.dataset.t).classList.add("on");b.setAttribute("aria-selected","true")})});
</script></body></html>"""


def montar_site():
    abas, paineis = "", ""
    for i, (rede, p) in enumerate(REDES.items()):
        on = " on" if i == 0 else ""
        abas += f'<button role="tab" class="{on.strip()}" data-t="p-{rede}" style="--c:{p["cor"]}">{rede}</button>'
        stats = "".join(f"<div class='stat'><span>{k}</span><b>{v}</b></div>" for k, v in resumo(rede, p))
        figs = ""
        for titulo, img, d in montar_graficos(rede, p):
            legenda = f"Fonte: {d['fonte']}."
            figs += (f"<figure><h2>{titulo}</h2><div class='img'><img alt='Gráfico: {titulo} no {rede}' "
                     f"src='data:image/png;base64,{img}'></div><figcaption>{legenda}</figcaption></figure>")
        paineis += (f'<section id="p-{rede}" class="panel{on}" style="--c:{p["cor"]}" role="tabpanel">'
                    f'<div class="stats">{stats}</div><div class="grid">{figs}</div></section>')
    fontes = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in FONTES)
    return HTML.replace("__TABS__", abas).replace("__PANELS__", paineis).replace("__FONTES__", fontes)


if __name__ == "__main__":
    pasta = Path(__file__).parent
    df = tabela_dados()
    print(df.groupby(["rede", "indicador"])["valor"].agg(["count", "sum"]).round(1))
    (pasta / "index.html").write_text(montar_site(), encoding="utf-8")
    print("Site gerado em", pasta / "index.html")
