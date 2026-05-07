import pandas as pd
import numpy as np

# Lee tu nueva tabla (ajusta el nombre si es necesario)
df = pd.read_excel('Datos/Tabla1.xlsx')
df.columns = df.columns.str.strip()

print("--- INICIANDO AUDITORÍA MATEMÁTICA ---")

# 1. Verificar IVS
ivs_calculado = (df['DIM_SS']*0.30 + df['DIM_EF']*0.25 + df['DIM_CA']*0.25 + df['DIM_GV']*0.20)
diferencia_ivs = np.abs(df['IVS'] - ivs_calculado)

if (diferencia_ivs > 0.01).any():
    print("❌ AÚN HAY ERRORES EN EL IVS. Revisa estas filas:")
    print(df[diferencia_ivs > 0.01][['Municipio', 'IVS']])
else:
    print("✅ EL IVS ES PERFECTAMENTE CONSISTENTE.")

# 2. Verificar ICI
ici_calculado = (df['ICI_Gen']*0.50 + df['ICI_Rsg']*0.50)
diferencia_ici = np.abs(df['ICI_Comp'] - ici_calculado)

if (diferencia_ici > 0.01).any():
    print("❌ AÚN HAY ERRORES EN EL ICI. Revisa estas filas:")
    print(df[diferencia_ici > 0.01][['Municipio', 'ICI_Comp']])
else:
    print("✅ EL ICI ES PERFECTAMENTE CONSISTENTE.")