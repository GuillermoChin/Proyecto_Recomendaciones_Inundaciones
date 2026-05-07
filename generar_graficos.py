import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

# 1. Cargar los datos
# Asegúrate de que el archivo se llame exactamente así y esté en formato CSV.
# Si es Excel, usa pd.read_excel('Datos/Tabla1.xlsx')
try:
    df = pd.read_csv('Datos/Tabla1.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo. Asegúrate de que exista la carpeta 'Datos' y el archivo 'Tabla1.csv'")
    exit()

# Limpiar posibles espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# 2. Configurar la figura y la cuadrícula (Layout)
fig = plt.figure(figsize=(20, 10))
fig.suptitle('ANÁLISIS COMPARATIVO DE RIESGO (IVS) Y CAPACIDAD (ICI) POR MUNICIPIO DE CAMPECHE', fontsize=18, weight='bold')

# GridSpec permite hacer el Panel A más grande (ocupa la columna izquierda) y B/C apilados en la derecha
gs = GridSpec(2, 2, width_ratios=[1.2, 1], height_ratios=[1, 1])
gs.update(wspace=0.15, hspace=0.3)

ax1 = fig.add_subplot(gs[:, 0])    # Panel A: Izquierda, ocupa ambas filas
ax2 = fig.add_subplot(gs[0, 1])    # Panel B: Derecha, fila superior
ax3 = fig.add_subplot(gs[1, 1])    # Panel C: Derecha, fila inferior

# ---------------------------------------------------------
# PANEL A: Análisis Sintético de Priorización (Dispersión)
# ---------------------------------------------------------
median_ivs = 0.459
median_ici_comp = 0.361

# Diccionario de colores para los cuadrantes
colores_cuadrante = {'I': 'red', 'II': 'orange', 'III': 'gold', 'IV': 'green'}
# Limpiar la columna C de espacios extras por si acaso
df['C'] = df['C'].astype(str).str.strip() 

for i, row in df.iterrows():
    color = colores_cuadrante.get(row['C'], 'gray')
    ax1.scatter(row['ICI_Com'], row['IVS'], color=color, s=100, edgecolors='black', zorder=3)
    # Etiquetar cada punto
    ax1.annotate(f"{row['Municipio']} ({row['C']})", 
                 (row['ICI_Com'], row['IVS']), 
                 textcoords="offset points", 
                 xytext=(10,-5), 
                 ha='left', fontsize=10)

# Líneas de corte (Medianas)
ax1.axhline(y=median_ivs, color='black', linestyle='--', zorder=1)
ax1.axvline(x=median_ici_comp, color='black', linestyle='--', zorder=1)

ax1.set_title('A. ANÁLISIS SINTÉTICO DE PRIORIZACIÓN: IVS vs. ICI_COMPUESTO', weight='bold')
ax1.set_xlabel('ÍNDICE DE CAPACIDAD INSTITUCIONAL COMPUESTO (ICI_Comp)', weight='bold')
ax1.set_ylabel('ÍNDICE DE VULNERABILIDAD SOCIAL (IVS) - RIESGO', weight='bold')
ax1.set_xlim(0, 1.0)
ax1.set_ylim(0, 0.8)
ax1.grid(True, linestyle=':', alpha=0.6)

# Anotaciones de las medianas
ax1.text(0.01, median_ivs + 0.01, f'MEDIANA DE CORTE IVS ({median_ivs})', weight='bold')
ax1.text(median_ici_comp + 0.01, 0.02, f'MEDIANA DE CORTE\nICI_Comp ({median_ici_comp})', weight='bold')

# ---------------------------------------------------------
# PANEL B: Diagnóstico de Componentes de Riesgo (Barras Apiladas)
# ---------------------------------------------------------
municipios = df['Municipio']
dim_ss = df['DIM_SS']
dim_ef = df['DIM_EF']
dim_ca = df['DIM_CA']
dim_gv = df['DIM_GV']

# Crear barras apiladas
p1 = ax2.barh(municipios, dim_ss, color='#a50026', edgecolor='white')
p2 = ax2.barh(municipios, dim_ef, left=dim_ss, color='#f46d43', edgecolor='white')
p3 = ax2.barh(municipios, dim_ca, left=dim_ss+dim_ef, color='#fee090', edgecolor='white')
p4 = ax2.barh(municipios, dim_gv, left=dim_ss+dim_ef+dim_ca, color='#4575b4', edgecolor='white')

ax2.set_title('B. DIAGNÓSTICO DE COMPONENTES DE RIESGO (DIMENSIONES DEL IVS)', weight='bold')
ax2.set_xlabel('IVS COMPUESTO', weight='bold')
ax2.invert_yaxis() # Para que el primer municipio salga arriba
ax2.legend((p1[0], p2[0], p3[0], p4[0]), ('Sensibilidad Social (DIM_SS)', 'Exposición Física (DIM_EF)', 'Capacidad Adaptativa (DIM_CA)', 'Grupos Vulnerables (DIM_GV)'), loc='lower right', fontsize=8)

# ---------------------------------------------------------
# PANEL C: Diagnóstico de Componentes de Capacidad (Barras Apiladas)
# ---------------------------------------------------------
# Nota: Apilar índices puede sumar > 1, es importante interpretar el total correctamente.
ici_gen = df['ICI_Gen']
ici_rsg = df['ICI_Rsg']
ici_com = df['ICI_Com']

p5 = ax3.barh(municipios, ici_gen, color='#313695', edgecolor='white')
p6 = ax3.barh(municipios, ici_rsg, left=ici_gen, color='#fdae61', edgecolor='white')
p7 = ax3.barh(municipios, ici_com, left=ici_gen+ici_rsg, color='#74add1', edgecolor='white')

ax3.set_title('C. DIAGNÓSTICO DE COMPONENTES DE CAPACIDAD (COMPOSICIÓN DEL ICI)', weight='bold')
ax3.set_xlabel('SUMA DE ÍNDICES ICI', weight='bold')
ax3.invert_yaxis()
ax3.legend((p5[0], p6[0], p7[0]), ('ICI General (ICI_Gen)', 'ICI Riesgo (ICI_Rsg)', 'ICI Compuesto (ICI_Com)'), loc='lower right', fontsize=8)

# Ajustar el diseño y guardar la imagen
plt.tight_layout()
plt.subplots_adjust(top=0.92) # Dar espacio al título principal
plt.savefig('grafico_multipanel.png', dpi=300, bbox_inches='tight')
print("¡Gráfico generado exitosamente y guardado como 'grafico_multipanel.png'!")
plt.show()