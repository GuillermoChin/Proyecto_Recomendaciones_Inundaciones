import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from adjustText import adjust_text
import matplotlib.cm as cm # Para generar colores únicos
import numpy as np

# 1. Crear carpeta Salidas si no existe
os.makedirs('Salidas', exist_ok=True)

# 2. Cargar los datos
try:
    df = pd.read_excel('Datos/Tabla1.xlsx')
except FileNotFoundError:
    print("Error: No se encontró el archivo. Asegúrate de que exista la carpeta 'Datos' y el archivo 'Tabla1.xlsx'")
    exit()

df.columns = df.columns.str.strip()
df['Municipio'] = df['Municipio'].astype(str).str.strip()

# Preparación de datos para barras
ss_p, ef_p, ca_p, gv_p = df['DIM_SS']*0.30, df['DIM_EF']*0.25, df['DIM_CA']*0.25, df['DIM_GV']*0.20
gen_p, rsg_p = df['ICI_Gen']*0.50, df['ICI_Rsg']*0.50

# --- CONFIGURACIÓN DE FIGURA ---
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
fig = plt.figure(figsize=(20, 16)) # Un poco más ancho para la leyenda
fig.suptitle('ANÁLISIS ESTRATÉGICO DE RIESGO Y CAPACIDAD MUNICIPAL', 
             fontsize=26, weight='bold', y=0.98)

# Ajustamos los márgenes para que quepa la leyenda del Panel A
gs = GridSpec(2, 2, width_ratios=[1.2, 1], height_ratios=[1, 1], wspace=0.4, hspace=0.3)

ax1 = fig.add_subplot(gs[:, 0]) 
ax2 = fig.add_subplot(gs[0, 1]) 
ax3 = fig.add_subplot(gs[1, 1]) 

# =========================================================
# PANEL A: DISPERSIÓN POR MUNICIPIO (COLORES ÚNICOS)
# =========================================================
# Generamos una paleta de colores con tantos colores como municipios haya
colores = cm.get_cmap('tab20', len(df))
textos = []

for i, row in df.iterrows():
    color_muni = colores(i)
    # Dibujamos el punto. Reducimos un poco la opacidad (alpha) 
    # para que el nombre sea más fácil de leer si queda encima.
    ax1.scatter(row['ICI_Comp'], row['IVS'], color=color_muni, s=300, 
                edgecolors='black', zorder=3, alpha=0.7)
    
    # Colocamos el nombre justo en la coordenada del punto
    # 'ha' y 'va' al centro aseguran que esté justo "sobre" el punto
    t = ax1.text(row['ICI_Comp'], row['IVS'], row['Municipio'], 
                 fontsize=10, weight='bold', ha='center', va='center')
    textos.append(t)

# Usamos adjust_text para evitar que los nombres se encimen entre sí,
# pero configuramos para que se mantengan lo más cerca posible de los puntos.
adjust_text(textos, ax=ax1, 
            only_move={'points':'y', 'text':'y'}, # Prioriza movimiento vertical si hay choque
            force_text=0.5,
            expand_points=(1.2, 1.2),
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.4))

# Líneas de medianas de referencia
ax1.axhline(0.459, color='black', linestyle=':', lw=1.5, alpha=0.5)
ax1.axvline(0.361, color='black', linestyle=':', lw=1.5, alpha=0.5)

# Zoom dinámico con margen
m_x, m_y = (df['ICI_Comp'].max()-df['ICI_Comp'].min())*0.15, (df['IVS'].max()-df['IVS'].min())*0.15
ax1.set_xlim(df['ICI_Comp'].min()-m_x, df['ICI_Comp'].max()+m_x)
ax1.set_ylim(df['IVS'].min()-m_y, df['IVS'].max()+m_y)

ax1.set_title('A. RELACIÓN CAPACIDAD (ICI) vs. RIESGO (IVS)', fontsize=18, weight='bold', pad=20)
ax1.set_xlabel('Índice de Capacidad Institucional (ICI_Comp)', fontsize=14, weight='bold')
ax1.set_ylabel('Índice de Vulnerabilidad Social (IVS)', fontsize=14, weight='bold')

# =========================================================
# PANELES B Y C (Siguen igual, consistentes con la tabla)
# =========================================================
y_pos = range(len(df))
# Panel B
ax2.barh(y_pos, ss_p, color='#a50026', label='Sensibilidad (30%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, ef_p, left=ss_p, color='#f46d43', label='Exposición (25%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, ca_p, left=ss_p+ef_p, color='#fee090', label='Cap. Adaptativa (25%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, gv_p, left=ss_p+ef_p+ca_p, color='#4575b4', label='Grupos Vuln. (20%)', edgecolor='black', lw=0.5)
ax2.set_title('B. DESGLOSE PONDERADO DEL IVS', fontsize=16, weight='bold')
ax2.set_yticks(y_pos); ax2.set_yticklabels(df['Municipio'])
ax2.invert_yaxis(); ax2.legend(loc='lower right', fontsize=9)

# Panel C
ax3.barh(y_pos, gen_p, color='#313695', label='Cap. General (50%)', edgecolor='black', lw=0.5)
ax3.barh(y_pos, rsg_p, left=gen_p, color='#fdae61', label='Cap. Riesgo (50%)', edgecolor='black', lw=0.5)
ax3.set_title('C. DESGLOSE PONDERADO DEL ICI', fontsize=16, weight='bold')
ax3.set_yticks(y_pos); ax3.set_yticklabels(df['Municipio'])
ax3.invert_yaxis(); ax3.legend(loc='lower right', fontsize=9)

plt.tight_layout(rect=[0, 0, 0.95, 0.95]) # Ajuste para que no se corte la leyenda derecha
plt.savefig('Salidas/grafico_multipanel_final_v2.png', dpi=300, bbox_inches='tight')
print("Éxito: Imagen generada con leyenda lateral.")
plt.show()