# Análisis Estratégico de Riesgo y Capacidad Municipal — Campeche, México

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0003--2104--6625-brightgreen.svg)](https://orcid.org/0000-0003-2104-6625)

## Descripción

Repositorio de código asociado al artículo:

> Chin Canché, G. A. (2026). De la vulnerabilidad
> a la intervención: estrategias territoriales para la reducción del riesgo de
> inundaciones en Campeche, México *Impluvium*, No. 35. Universidad Nacional Autónoma de
> México (UNAM). https://www.agua.unam.mx/impluvium.html (Pendiente de publicación)

Este proyecto integra dos índices compuestos para el análisis estratégico
del riesgo de inundación y la capacidad de respuesta institucional en los
municipios del estado de Campeche, México:

- **IVS** — Índice de Vulnerabilidad Socioterritorial: construido a partir
  del Censo de Población y Vivienda 2020 (INEGI) y el Índice de Marginación
  por Localidad 2020 (CONAPO), integrando cuatro dimensiones: Sensibilidad
  Social (SS), Exposición Física (EF), Capacidad Adaptativa (CA) y Grupos
  Vulnerables (GV).

- **ICI** — Índice de Capacidad Institucional: construido a partir del
  Presupuesto de Egresos Municipal de Campeche, integrando dos subíndices:
  Capacidad General (ICI_Gen) y Capacidad de Gestión de Riesgo (ICI_Rsg).

La integración de ambos índices permite identificar municipios en situación
de alta vulnerabilidad y baja capacidad institucional, orientando la
priorización de intervenciones de política pública.

---

## Autor de correspondencia

**Guillermo Adrián Chin Canché**
Instituto Tecnológico Superior de Calkiní (ITESCAM),
Tecnológico Nacional de México — Campeche, México
ORCID: [0000-0003-2104-6625](https://orcid.org/0000-0003-2104-6625)
Contacto y más información: [linktr.ee/guille_chin](https://linktr.ee/guille_chin)
✉️ contacto@guillermochin.com

## Coautores


---

## Marco conceptual

### Índice de Vulnerabilidad Socioterritorial (IVS)
IVS = DIM_SS×0.30 + DIM_EF×0.25 + DIM_CA×0.25 + DIM_GV×0.20

| Dimensión | Código | Peso | Justificación |
|---|---|---|---|
| Sensibilidad Social | SS | 0.30 | Cutter et al. (2003) |
| Exposición Física | EF | 0.25 | IPCC AR5 (2014) |
| Capacidad Adaptativa | CA | 0.25 | IPCC AR5 (2014) |
| Grupos Vulnerables | GV | 0.20 | Wisner et al. (2004) |

### Índice de Capacidad Institucional (ICI)
ICI_Gen  = GastoPC×0.40 + InversionPC×0.40 + Flexibilidad×0.20
ICI_Rsg  = GastoRiesgoPC×0.50 + PropFAISM×0.30 + PropPC×0.20
ICI_Comp = ICI_Gen×0.50 + ICI_Rsg×0.50

| Subíndice | Descripción | Peso |
|---|---|---|
| ICI_Gen | Capacidad presupuestal general | 0.50 |
| ICI_Rsg | Capacidad de gestión de riesgo | 0.50 |

---

## Estructura del repositorio
Analisis_Riesgo_Capacidad_Campeche/
│
├── Datos/                          # Datos de entrada (no versionados en Git)
│   ├── IML_2020.xls                # Índice de Marginación Localidad 2020 (CONAPO)
│   ├── Tabla1.xlsx                 # Tabla integrada IVS + ICI por municipio
│   └── Presupuesto de Egresos      # Presupuesto Municipal de Campeche
│       Municipales de Campeche.xlsx
│
├── Salidas/                        # Outputs generados (no versionados en Git)
│   ├── Tabla_ICI_Calculada.csv     # Tabla ICI por municipio
│   └── grafico_multipanel_final.png# Figura multipanel de resultados
│
├── calcular_ici.py                 # Cálculo del ICI desde presupuesto municipal
├── generar_graficos.py             # Generación de figura multipanel
├── auditor.py                      # Verificación matemática de consistencia
├── requirements.txt                # Dependencias Python
├── LICENSE                         # Licencia CC BY 4.0
└── README.md                       # Este archivo

---

## Flujo de análisis
IML_2020.xls ──────────────────────────────────────────┐
▼
Presupuesto_Municipal.xlsx ──► calcular_ici.py ──► Tabla_ICI_Calculada.csv
│
Tabla1.xlsx (IVS + ICI) ◄──────────────────────────────┘
│
├──► auditor.py ──► Verificación de consistencia matemática
│
└──► generar_graficos.py ──► grafico_multipanel_final.png

---

## Fuentes de datos

| Dataset | Fuente | Año | Licencia | URL |
|---|---|---|---|---|
| Índice de Marginación por Localidad | CONAPO | 2020 | Datos abiertos | https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372 |
| Presupuesto de Egresos Municipales | https://asecam.gob.mx/presupuesto-de-egresos/

> **Nota:** Los archivos de datos no se versionan en GitHub.
> Solo el código de análisis está incluido en este repositorio.

---

## Instalación y uso

```bash
# 1. Clonar el repositorio
git clone https://github.com/guillermochin/Proyecto_Recomendaciones_Inundaciones.git
cd Proyecto_Recomendaciones_Inundaciones

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Colocar los datos en la carpeta Datos/

# 5. Calcular el ICI
python calcular_ici.py

# 6. Generar gráficos
python generar_graficos.py

# 7. Verificar consistencia matemática
python auditor.py
```

---

## Descripción de los scripts

### `calcular_ici.py`
Procesa el Presupuesto de Egresos Municipal de Campeche y lo cruza con
datos de población del IML CONAPO 2020. Calcula las variables base por
habitante, aplica normalización min-max y obtiene ICI_Gen, ICI_Rsg e
ICI_Comp para cada municipio. Exporta la tabla resultante en
`Salidas/Tabla_ICI_Calculada.csv`.

### `generar_graficos.py`
Genera la figura multipanel de resultados a partir de `Datos/Tabla1.xlsx`:
- **Panel A:** Dispersión ICI vs IVS por municipio (identificación de
  cuadrantes estratégicos)
- **Panel B:** Desglose ponderado del IVS por dimensión
- **Panel C:** Desglose ponderado del ICI por subíndice

### `auditor.py`
Verifica la consistencia matemática de la tabla integrada. Recalcula IVS
e ICI desde sus componentes y detecta discrepancias superiores a 0.01.
Útil para validar la integridad de los datos antes de publicar.

---

## Outputs generados

| Archivo | Descripción |
|---|---|
| `Tabla_ICI_Calculada.csv` | ICI_Gen, ICI_Rsg e ICI_Comp por municipio |
| `grafico_multipanel_final.png` | Panel A (dispersión) + B (IVS) + C (ICI) |

---

## Licencia

Este repositorio se distribuye bajo la licencia
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

---

## Uso de inteligencia artificial

Se empleó Claude (Anthropic) como apoyo en organización del código y NotebookLM en la síntesis de la información.
La responsabilidad total del contenido, los argumentos, los datos y las conclusiones recae exclusivamente en los autores.

---

*Guillermo Adrián Chin Canché — ITESCAM, Campeche, México*
*[linktr.ee/guille_chin](https://linktr.ee/guille_chin)*
