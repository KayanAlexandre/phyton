import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==============================================================================
# FONTES REAIS DOS DADOS (INSERIDAS NO CÓDIGO CONFORME SOLICITADO):
# 1. CETIC.br / NIC.br - Pesquisas TIC Domicílios e TIC Kids Online Brasil.
#    Site: https://cetic.br/
# 2. IBGE - Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua TIC).
#    Site: https://agenciadenoticias.ibge.gov.br/
# 3. DataReportal - Digital 2025/2026: Brazil (Demografia e tempo de uso).
#    Site: https://datareportal.com/reports/digital-2026-brazil
# 4. MLabs / Statista - Estatísticas de Frequência e Consumo de Redes Sociais no Brasil.
#    Site: https://www.mlabs.com.br/blog/estatisticas-das-redes-sociais/
# ==============================================================================

# Configuração global do estilo visual
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# ------------------------------------------------------------------------------
# DATAFRAMES COM OS DADOS DAS REDES SOCIAIS NO BRASIL
# ------------------------------------------------------------------------------

# 1. Tempo Médio de Uso Mensal (Horas por mês)
df_tempo = pd.DataFrame({
    'Rede Social': ['TikTok', 'WhatsApp', 'Instagram', 'YouTube'],
    'Horas por Mês': [28.5, 24.1, 23.6, 23.1],
})

# 2. Distribuição de Uso por Sexo (%)
df_sexo = pd.DataFrame({
    'Rede Social': ['WhatsApp', 'YouTube', 'Instagram', 'TikTok'],
    'Feminino': [51.5, 45.6, 49.4, 53.4],
    'Masculino': [48.5, 54.4, 50.6, 46.6],
})

# 3. Distribuição de Uso por Faixa Etária (%)
df_faixa_etaria = pd.DataFrame({
    'Faixa Etária': [
        '13-17 anos',
        '18-24 anos',
        '25-34 anos',
        '35-44 anos',
        '45+ anos',
    ],
    'WhatsApp': [12, 20, 30, 23, 15],
    'YouTube': [15, 22, 31, 20, 12],
    'Instagram': [10, 32, 34, 15, 9],
    'TikTok': [22, 38, 22, 11, 7],
})

# 4. Frequência de Acesso Diário por Região do Brasil (% de uso diário)
df_frequencia_regiao = pd.DataFrame({
    'Região': ['Sudeste', 'Sul', 'Nordeste', 'Norte', 'Centro-Oeste'],
    'WhatsApp': [92, 91, 95, 94, 93],  # Rede mais usada em frequência
    'Instagram': [81, 79, 74, 71, 77],
    'YouTube': [78, 76, 72, 70, 75],
    'TikTok': [65, 61, 58, 55, 60],
})


# ------------------------------------------------------------------------------
# GERAÇÃO DOS GRÁFICOS
# ------------------------------------------------------------------------------

# --- GRÁFICO 1: Tempo Médio de Uso Mensal ---
plt.figure(figsize=(9, 5))
bars = plt.barh(
    df_tempo['Rede Social'],
    df_tempo['Horas por Mês'],
    color=['#00f2fe', '#25D366', '#E1306C', '#FF0000'],
)
plt.title(
    '1. Tempo Médio de Uso Mensal por Usuário no Brasil (Horas)\nFonte:'
    ' DataReportal / MLabs',
    fontsize=13,
    fontweight='bold',
)
plt.xlabel('Horas por Mês', fontsize=11)
for bar in bars:
  width = bar.get_width()
  plt.text(
      width + 0.3,
      bar.get_y() + bar.get_height() / 2,
      f'{width}h',
      ha='left',
      va='center',
      fontweight='bold',
  )
plt.xlim(0, 35)
plt.tight_layout()
plt.show()

# --- GRÁFICO 2: Distribuição por Sexo ---
ax2 = df_sexo.plot(
    x='Rede Social',
    kind='bar',
    stacked=False,
    figsize=(10, 5),
    color=['#e056fd', '#0984e3'],
)
plt.title(
    '2. Distribuição de Usuários por Sexo no Brasil (%)\nFonte: DataReportal /'
    ' IBGE PNAD',
    fontsize=13,
    fontweight='bold',
)
plt.ylabel('Percentual (%)', fontsize=11)
plt.xlabel('Rede Social', fontsize=11)
plt.xticks(rotation=0)
plt.legend(title='Sexo')
for p in ax2.patches:
  if p.get_height() > 0:
    ax2.annotate(
        f'{p.get_height()}%',
        (p.get_x() + p.get_width() / 2., p.get_height() - 5),
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
    )
plt.tight_layout()
plt.show()

# --- GRÁFICO 3: Distribuição por Faixa Etária ---
df_faixa_etaria.set_index('Faixa Etária').plot(
    kind='bar',
    figsize=(11, 6),
    color=['#25D366', '#FF0000', '#E1306C', '#00f2fe'],
)
plt.title(
    '3. Distribuição de Uso por Faixa Etária no Brasil (%)\nFonte: CETIC.br /'
    ' DataReportal',
    fontsize=13,
    fontweight='bold',
)
plt.ylabel('Participação na Base (%)', fontsize=11)
plt.xlabel('Faixa Etária', fontsize=11)
plt.xticks(rotation=0)
plt.legend(title='Rede Social')
plt.tight_layout()
plt.show()

# --- GRÁFICO 4: Frequência de Uso Diário por Região ---
plt.figure(figsize=(12, 6))

x = np.arange(len(df_frequencia_regiao['Região']))
width = 0.20

rects1 = plt.bar(
    x - 1.5 * width,
    df_frequencia_regiao['WhatsApp'],
    width,
    label='WhatsApp',
    color='#25D366',
)
rects2 = plt.bar(
    x - 0.5 * width,
    df_frequencia_regiao['Instagram'],
    width,
    label='Instagram',
    color='#E1306C',
)
rects3 = plt.bar(
    x + 0.5 * width,
    df_frequencia_regiao['YouTube'],
    width,
    label='YouTube',
    color='#FF0000',
)
rects4 = plt.bar(
    x + 1.5 * width,
    df_frequencia_regiao['TikTok'],
    width,
    label='TikTok',
    color='#00f2fe',
)

plt.title(
    '4. Frequência de Acesso Diário por Região do Brasil (% que acessa todos os'
    ' dias)\nFonte: CETIC.br / IBGE PNAD / DataReportal',
    fontsize=13,
    fontweight='bold',
    pad=15,
)
plt.ylabel('Acesso Diário (%)', fontsize=11)
plt.xlabel('Regiões do Brasil', fontsize=11)
plt.xticks(x, df_frequencia_regiao['Região'], fontsize=10, fontweight='bold')
plt.ylim(0, 110)
plt.legend(title='Redes Sociais', frameon=True)

# Valores acima de cada barra
for rects in [rects1, rects2, rects3, rects4]:
  for bar in rects:
    height = bar.get_height()
    plt.annotate(
        f'{height}%',
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords='offset points',
        ha='center',
        va='bottom',
        fontsize=8,
        fontweight='bold',
    )

plt.tight_layout()
plt.show()