import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from adjustText import adjust_text

# 1. Crear carpeta Salidas si no existe
os.makedirs('Salidas', exist_ok=True)

# 2. Cargar los datos
try:
    df = pd.read_excel('Datos/Tabla1.xlsx')
except FileNotFoundError:
    print("Error: No se encontró el archivo. Asegúrate de que exista la carpeta 'Datos' y el archivo 'Tabla1.xlsx'")
    exit()

df.columns = df.columns.str.strip()

# 3. Configurar la figura (Más vertical, menos horizontal)
fig = plt.figure(figsize=(16, 14))
fig.suptitle('ANÁLISIS COMPARATIVO DE RIESGO (IVS) Y CAPACIDAD (ICI) POR MUNICIPIO DE CAMPECHE', fontsize=20, weight='bold')

gs = GridSpec(2, 2, width_ratios=[1.2, 1], height_ratios=[1, 1])
gs.update(wspace=0.20, hspace=0.35)

ax1 = fig.add_subplot(gs[:, 0])    
ax2 = fig.add_subplot(gs[0, 1])    
ax3 = fig.add_subplot(gs[1, 1])    

# ---------------------------------------------------------
# PANEL A: Análisis Sintético de Priorización (Dispersión)
# ---------------------------------------------------------
median_ivs = 0.459
median_ici_comp = 0.361
colores_cuadrante = {'I': 'red', 'II': 'orange', 'III': 'gold', 'IV': 'green'}
df['C'] = df['C'].astype(str).str.strip() 

textos = [] # Lista para guardar las etiquetas y acomodarlas luego

for i, row in df.iterrows():
    color = colores_cuadrante.get(row['C'], 'gray')
    ax1.scatter(row['ICI_Comp'], row['IVS'], color=color, s=150, edgecolors='black', zorder=3)
    
    # Crear el texto pero guardarlo en la lista en lugar de fijarlo
    t = ax1.text(row['ICI_Comp'], row['IVS'], f"{row['Municipio']} ({row['C']})", fontsize=12, weight='bold')
    textos.append(t)

# Acomodar los textos automáticamente para que no se encimen (usa adjustText)
adjust_text(texts, 
            ax=ax1, 
            force_text=(0.5, 1.5),      # Aumenta la repulsión entre las etiquetas
            force_points=(0.5, 1.5),    # Aumenta la repulsión entre etiqueta y punto
            expand_points=(1.5, 1.5),   # Crea un "colchón" invisible alrededor de los puntos
            expand_text=(1.5, 1.5),     # Crea un "colchón" invisible alrededor de los textos
            max_iterations=2000,        # Le da a la computadora más intentos para acomodarlos
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.8, alpha=0.7))

ax1.axhline(y=median_ivs, color='black', linestyle='--', zorder=1)
ax1.axvline(x=median_ici_comp, color='black', linestyle='--', zorder=1)

ax1.set_title('A. ANÁLISIS SINTÉTICO DE PRIORIZACIÓN', fontsize=16, weight='bold')
ax1.set_xlabel('ÍNDICE DE CAPACIDAD INSTITUCIONAL COMPUESTO (ICI_Comp)', fontsize=14, weight='bold')
ax1.set_ylabel('ÍNDICE DE VULNERABILIDAD SOCIAL (IVS)', fontsize=14, weight='bold')
ax1.set_xlim(0, 1.0)
ax1.set_ylim(0, 0.8)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.tick_params(axis='both', labelsize=12)

ax1.text(0.02, median_ivs + 0.01, f'MEDIANA DE CORTE IVS ({median_ivs})', fontsize=12, weight='bold')
ax1.text(median_ici_comp + 0.01, 0.02, f'MEDIANA DE CORTE\nICI_Comp ({median_ici_comp})', fontsize=12, weight='bold')

# ---------------------------------------------------------
# PANEL B: Diagnóstico de Riesgo (Fórmula IVS)
# IVS = SS × 0.30 + EF × 0.25 + CA × 0.25 + GV × 0.20
# ---------------------------------------------------------
municipios = df['Municipio']

# Aplicando las ponderaciones indicadas
dim_ss_w = df['DIM_SS'] * 0.30
dim_ef_w = df['DIM_EF'] * 0.25
dim_ca_w = df['DIM_CA'] * 0.25
dim_gv_w = df['DIM_GV'] * 0.20

p1 = ax2.barh(municipios, dim_ss_w, color='#a50026', edgecolor='white')
p2 = ax2.barh(municipios, dim_ef_w, left=dim_ss_w, color='#f46d43', edgecolor='white')
p3 = ax2.barh(municipios, dim_ca_w, left=dim_ss_w+dim_ef_w, color='#fee090', edgecolor='white')
p4 = ax2.barh(municipios, dim_gv_w, left=dim_ss_w+dim_ef_w+dim_ca_w, color='#4575b4', edgecolor='white')

ax2.set_title('B. COMPOSICIÓN DEL IVS (VALORES PONDERADOS)', fontsize=14, weight='bold')
ax2.set_xlabel('IVS TOTAL', fontsize=12, weight='bold')
ax2.invert_yaxis() 
ax2.tick_params(axis='both', labelsize=11)
ax2.legend((p1[0], p2[0], p3[0], p4[0]), 
           ('Sensibilidad Social (30%)', 'Exposición Física (25%)', 'Capacidad Adaptativa (25%)', 'Grupos Vulnerables (20%)'), 
           loc='lower right', fontsize=10)

# ---------------------------------------------------------
# PANEL C: Diagnóstico de Capacidad (Fórmula ICI_Comp)
# ICI_Comp = ICI_Gen × 0.50 + ICI_Rsg × 0.50
# ---------------------------------------------------------

# Aplicando las ponderaciones indicadas
ici_gen_w = df['ICI_Gen'] * 0.50
ici_rsg_w = df['ICI_Rsg'] * 0.50

p5 = ax3.barh(municipios, ici_gen_w, color='#313695', edgecolor='white')
p6 = ax3.barh(municipios, ici_rsg_w, left=ici_gen_w, color='#fdae61', edgecolor='white')

ax3.set_title('C. COMPOSICIÓN DEL ICI_COMP (VALORES PONDERADOS)', fontsize=14, weight='bold')
ax3.set_xlabel('ICI COMPUESTO', fontsize=12, weight='bold')
ax3.invert_yaxis()
ax3.tick_params(axis='both', labelsize=11)
ax3.legend((p5[0], p6[0]), ('ICI General (50%)', 'ICI Riesgo (50%)'), loc='lower right', fontsize=10)

# Ajustar el diseño y guardar en la carpeta Salidas
plt.tight_layout()
plt.subplots_adjust(top=0.93) 
plt.savefig('Salidas/grafico_multipanel.png', dpi=300, bbox_inches='tight')
print("¡Gráfico generado exitosamente y guardado en 'Salidas/grafico_multipanel.png'!")
plt.show()