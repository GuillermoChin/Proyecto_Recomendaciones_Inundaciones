import os
import unicodedata
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Crear carpeta Salidas si no existe
os.makedirs('Salidas', exist_ok=True)

# =========================================================
# FUNCIÓN DE AYUDA PARA CRUZAR TABLAS
# =========================================================
def limpiar_texto(columna):
    """Quita acentos, espacios extra y convierte a mayúsculas para evitar errores al cruzar datos"""
    return columna.astype(str).apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8')).str.strip().str.upper()

# =========================================================
# 2. PROCESAR POBLACIÓN (IML 2020)
# =========================================================
try:
    # Lee el archivo Excel original y especifica la hoja exacta
    df_pob = pd.read_excel('Datos/IML_2020.xls', sheet_name='IML_2020_AGS-MEX')
except FileNotFoundError:
    print("Error: No se encontró el archivo de población 'IML_2020.xls' en la carpeta 'Datos'.")
    exit()
except ValueError:
    print("Error: No se encontró la hoja 'IML_2020_AGS-MEX' dentro del archivo. Verifica el nombre de la pestaña en tu Excel.")
    exit()

# Filtrar solo el estado de Campeche
df_pob['NOM_ENT_CLEAN'] = limpiar_texto(df_pob['NOM_ENT'])
df_campeche = df_pob[df_pob['NOM_ENT_CLEAN'] == 'CAMPECHE'].copy()

# Asegurar que la población sea un número (a veces INEGI usa caracteres para datos faltantes)
df_campeche['POB_TOT'] = pd.to_numeric(df_campeche['POB_TOT'], errors='coerce').fillna(0)

# Agrupar por municipio y sumar la población de todas sus localidades
df_campeche['Municipio_Join'] = limpiar_texto(df_campeche['NOM_MUN'])
pob_municipal = df_campeche.groupby('Municipio_Join')['POB_TOT'].sum().reset_index()
pob_municipal.rename(columns={'POB_TOT': 'Poblacion_Total'}, inplace=True)

# =========================================================
# 3. PROCESAR PRESUPUESTOS Y CRUZAR DATOS
# =========================================================
try:
    df_presupuesto = pd.read_excel('Datos/Presupuesto de Egresos Municipales de Campeche.xlsx')
except FileNotFoundError:
    print("Error: No se encontró el CSV de presupuestos.")
    exit()

df_presupuesto.columns = df_presupuesto.columns.str.strip()

# Limpiar los nombres de municipios en la tabla de presupuesto para que el cruce sea exacto
col_municipio = 'Municipio' # Cambia esto si en tu CSV se llama diferente
df_presupuesto['Municipio_Join'] = limpiar_texto(df_presupuesto[col_municipio])

# ¡El Cruce Maestro! Unimos la tabla de presupuestos con la de población
df = pd.merge(df_presupuesto, pob_municipal, on='Municipio_Join', how='left')

# Verificación de seguridad
if df['Poblacion_Total'].isnull().any():
    faltantes = df[df['Poblacion_Total'].isnull()]['Municipio'].unique()
    print(f"ADVERTENCIA: No se encontró población para estos municipios (revisa cómo están escritos): {faltantes}")

# =========================================================
# 4. MAPEO DE COLUMNAS DE PRESUPUESTO
# Reemplaza los valores con los nombres EXACTOS de tus columnas en el CSV
# =========================================================
col_municipio = 'Municipio'
col_gasto_total = 'Presupuesto_Total' 
col_cap1000 = 'Cap1000'
col_cap2000 = 'Cap2000'
col_cap3000 = 'Cap3000'
col_cap6000 = 'Cap6000'
col_pc = 'FC_ProteccionCivil'
col_agua = 'AguaPotable_Dir'
col_obras = 'ObrasPublicas_Dir'
col_faism = 'FAISM'

# =========================================================
# 4.5 LIMPIEZA DE DATOS FINANCIEROS (NUEVO)
# Quitamos signos $, comas y convertimos texto a números
# =========================================================
cols_financieras = [col_gasto_total, col_cap1000, col_cap2000, col_cap3000, 
                    col_cap6000, col_pc, col_agua, col_obras, col_faism]

for col in cols_financieras:
    # 1. Convertimos a texto por si acaso, 2. Borramos $ y comas, 3. Convertimos a número
    df[col] = df[col].astype(str).str.replace(r'[\$,\s]', '', regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# =========================================================
# 5. CÁLCULO DE VARIABLES BASE
# =========================================================
# Usamos la nueva columna cruzada 'Poblacion_Total'
df['GastoPC'] = df[col_gasto_total] / df['Poblacion_Total']
df['InversionPC'] = df[col_cap6000] / df['Poblacion_Total']
df['Gasto_Corriente'] = df[col_cap1000] + df[col_cap2000] + df[col_cap3000]
df['Prop_Gasto_Corriente'] = df['Gasto_Corriente'] / df[col_gasto_total]
df['Flexibilidad'] = 1 - df['Prop_Gasto_Corriente']

df['GastoRiesgo_Total'] = df[col_pc] + df[col_agua] + (0.30 * df[col_obras])
df['GastoRiesgoPC'] = df['GastoRiesgo_Total'] / df['Poblacion_Total']
df['PropFAISM'] = df[col_faism] / df[col_gasto_total]
df['PropPC'] = df[col_pc] / df[col_gasto_total]

# =========================================================
# 6. NORMALIZACIÓN MIN-MAX [0,1]
# =========================================================
scaler = MinMaxScaler()
variables_a_normalizar = ['GastoPC', 'InversionPC', 'Flexibilidad', 
                          'GastoRiesgoPC', 'PropFAISM', 'PropPC']

# Rellenar posibles NaNs con 0 por seguridad antes de normalizar
df[variables_a_normalizar] = df[variables_a_normalizar].fillna(0)
df[variables_a_normalizar] = scaler.fit_transform(df[variables_a_normalizar])

# =========================================================
# 7. CÁLCULO DE ÍNDICES (FÓRMULAS)
# =========================================================
df['ICI_Gen'] = (df['GastoPC'] * 0.40) + (df['InversionPC'] * 0.40) + (df['Flexibilidad'] * 0.20)
df['ICI_Rsg'] = (df['GastoRiesgoPC'] * 0.50) + (df['PropFAISM'] * 0.30) + (df['PropPC'] * 0.20)
df['ICI_Comp'] = (df['ICI_Gen'] * 0.50) + (df['ICI_Rsg'] * 0.50)

# =========================================================
# 8. PROMEDIO MULTIANUAL POR MUNICIPIO
# =========================================================
df_final = df.groupby(col_municipio)[['ICI_Gen', 'ICI_Rsg', 'ICI_Comp']].mean().reset_index()

# Guardar la tabla final correcta
df_final.to_csv('Salidas/Tabla_ICI_Calculada.csv', index=False)
print("¡Cálculo completado! La tabla cruzada con CONAPO se guardó en 'Salidas/Tabla_ICI_Calculada.csv'")