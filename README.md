# 🏎️ End-to-End Formula 1 Data Pipeline

Este proyecto implementa un **pipeline de datos end-to-end** para analizar tiempos de vueltas de Fórmula 1 utilizando **Apache Spark**.  
El objetivo es construir un flujo reproducible desde la ingesta de datos crudos hasta la generación de datasets procesados listos para el análisis.

---

## 📂 Estructura del Proyecto
```
E2E_Formula1/

├─ data/
│  ├─ laps.json
│  ├─ laps.jsonl
│  ├─ processed_laps.csv
│  └─ fastest_laps.csv
├─ src/
│  ├─ test_openf1.py
│  ├─ json_to_jsonl.py
│  ├─ spark_process_laps.py
│  ├─ spark_fastest_laps.py
│  └─analyze_laps.py
└─ README.md
```

---

## ⚙️ Flujo del Proyecto

1. **Descarga de datos**
   - Ejecutar `test_openf1.py` para obtener datos desde la API de OpenF1.
   - Los resultados se guardan en `data/laps.json`.

2. **Conversión a JSONL**
   - Ejecutar `json_to_jsonl.py` para transformar `laps.json` a `laps.jsonl`.

3. **Procesamiento con PySpark**
   - Ejecutar `spark_process_laps.py`:
     - Filtra y limpia los datos.
     - Convierte tiempos a un formato legible (`MM:SS.mmm`).
     - Guarda el dataset como `processed_laps.csv`.

4. **Cálculo de vueltas más rápidas**
   - Ejecutar `spark_fastest_laps.py`:
     - Obtiene la vuelta más rápida de cada piloto.
     - Genera `fastest_laps.csv`.

---

## 📊 Resultados

- **`processed_laps.csv`** → Dataset con todas las vueltas (limpio y legible).  
- **`fastest_laps.csv`** → Vuelta más rápida por cada piloto.  

---

## 🚀 Tecnologías usadas

- **Python 3**
- **PySpark**
- **Requests** (para consumir la API)
