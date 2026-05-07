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
df['Municipio'] = df['Municipio'].astype(str).str.strip()

# --- LÓGICA DE AJUSTE (SIN NORMALIZACIÓN) ---
# Como tu tabla ya está matemáticamente perfecta, usamos los datos directos
ss_p = df['DIM_SS'] * 0.30
ef_p = df['DIM_EF'] * 0.25
ca_p = df['DIM_CA'] * 0.25
gv_p = df['DIM_GV'] * 0.20

gen_p = df['ICI_Gen'] * 0.50
rsg_p = df['ICI_Rsg'] * 0.50

# --- CONFIGURACIÓN VISUAL ---
plt.rcParams['font.sans-serif'] = ['Arial', 'Liberation Sans', 'DejaVu Sans']
fig = plt.figure(figsize=(18, 16))
fig.suptitle('ANÁLISIS DE RIESGO E INDICADORES DE CAPACIDAD\nMunicipios de Campeche, México', 
             fontsize=24, weight='bold', y=0.97)

gs = GridSpec(2, 2, width_ratios=[1.1, 1], height_ratios=[1, 1], wspace=0.28, hspace=0.3)

ax1 = fig.add_subplot(gs[:, 0]) # Dispersión
ax2 = fig.add_subplot(gs[0, 1]) # IVS
ax3 = fig.add_subplot(gs[1, 1]) # ICI

# =========================================================
# PANEL A: DISPERSIÓN (MEJORADO CON ZOOM Y LEYENDA)
# =========================================================
colores_c = {'I': '#d73027', 'II': '#f46d43', 'III': '#fee090', 'IV': '#1a9850'}
textos = []

for i, row in df.iterrows():
    color = colores_c.get(str(row['C']).strip(), 'gray')
    ax1.scatter(row['ICI_Comp'], row['IVS'], color=color, s=200, edgecolors='black', zorder=5)
    
    # Quitamos el número de cuadrante del texto para que sea más limpio
    t = ax1.text(row['ICI_Comp'], row['IVS'], f"{row['Municipio']}", fontsize=13, weight='bold')
    textos.append(t)

# Acomodo automático de textos
adjust_text(textos, 
            ax=ax1, 
            force_text=(0.8, 1.5),      
            force_points=(0.8, 1.5),    
            expand_points=(1.5, 1.5),   
            max_iterations=2000,        
            arrowprops=dict(arrowstyle='-', color='gray', lw=0.8, alpha=0.7))

# Líneas de medianas
ax1.axhline(0.459, color='black', linestyle='--', lw=2, alpha=0.6, zorder=1)
ax1.axvline(0.361, color='black', linestyle='--', lw=2, alpha=0.6, zorder=1)

# ZOOM DINÁMICO: Dejamos que Pandas calcule el min/max y le damos un 10% de margen
margen_x = (df['ICI_Comp'].max() - df['ICI_Comp'].min()) * 0.10
margen_y = (df['IVS'].max() - df['IVS'].min()) * 0.10
ax1.set_xlim(df['ICI_Comp'].min() - margen_x, df['ICI_Comp'].max() + margen_x)
ax1.set_ylim(df['IVS'].min() - margen_y, df['IVS'].max() + margen_y)

# Títulos y ejes
ax1.set_title('A. CUADRANTES DE PRIORIZACIÓN', fontsize=18, weight='bold', pad=15)
ax1.set_xlabel('Capacidad Institucional (ICI Compuesto)', fontsize=15, weight='bold')
ax1.set_ylabel('Vulnerabilidad Social (IVS)', fontsize=15, weight='bold')
ax1.grid(True, ls=':', alpha=0.5)
ax1.tick_params(labelsize=13)

# Textos de las líneas de corte (ahora dinámicos según el zoom)
xmin, xmax = ax1.get_xlim()
ymin, ymax = ax1.get_ylim()
ax1.text(xmin + 0.005, 0.459 + 0.003, 'MEDIANA IVS (0.459)', fontsize=11, weight='bold', color='black')
ax1.text(0.361 + 0.005, ymin + 0.005, 'MEDIANA ICI (0.361)', fontsize=11, weight='bold', color='black', rotation=90)

# NUEVO: Leyenda de colores del Panel A
elementos_leyenda = [
    Line2D([0], [0], marker='o', color='w', label='I (Alta Prioridad)', markerfacecolor='#d73027', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='II (Media-Alta)', markerfacecolor='#f46d43', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='III (Media-Baja)', markerfacecolor='#fee090', markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label='IV (Baja Prioridad)', markerfacecolor='#1a9850', markersize=12, markeredgecolor='black')
]
ax1.legend(handles=elementos_leyenda, loc='lower left', title='Cuadrantes', fontsize=11, title_fontsize=13, framealpha=0.9)

# =========================================================
# PANEL B: IVS (BARRAS APILADAS)
# =========================================================
y_pos = range(len(df))
ax2.barh(y_pos, ss_p, color='#a50026', label='Sensibilidad (30%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, ef_p, left=ss_p, color='#f46d43', label='Exposición (25%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, ca_p, left=ss_p+ef_p, color='#fee090', label='Cap. Adaptativa (25%)', edgecolor='black', lw=0.5)
ax2.barh(y_pos, gv_p, left=ss_p+ef_p+ca_p, color='#4575b4', label='Grupos Vuln. (20%)', edgecolor='black', lw=0.5)

ax2.set_title('B. COMPOSICIÓN DEL IVS', fontsize=16, weight='bold')
ax2.set_xlabel('IVS TOTAL', fontsize=13, weight='bold')
ax2.set_yticks(y_pos); ax2.set_yticklabels(df['Municipio'], fontsize=12)
ax2.invert_yaxis()
ax2.legend(loc='lower right', fontsize=10)

# =========================================================
# PANEL C: ICI (BARRAS APILADAS)
# =========================================================
ax3.barh(y_pos, gen_p, color='#313695', label='Cap. General (50%)', edgecolor='black', lw=0.5)
ax3.barh(y_pos, rsg_p, left=gen_p, color='#fdae61', label='Cap. Riesgo (50%)', edgecolor='black', lw=0.5)

ax3.set_title('C. COMPOSICIÓN DEL ICI', fontsize=16, weight='bold')
ax3.set_xlabel('ICI COMPUESTO TOTAL', fontsize=13, weight='bold')
ax3.set_yticks(y_pos); ax3.set_yticklabels(df['Municipio'], fontsize=12)
ax3.invert_yaxis()
ax3.legend(loc='lower right', fontsize=10)

# Guardar y mostrar
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Salidas/grafico_multipanel_final.png', dpi=300, bbox_inches='tight')
print("Éxito: Imagen generada en 'Salidas/grafico_multipanel_final.png'")
plt.show()