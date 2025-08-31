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

## ⚙️ Pipeline de Procesamiento

### 1. Ingesta de datos
- Se descarga el archivo `laps.jsonl` desde la [API de OpenF1](https://openf1.org/).
- Se almacena en `data/raw/`.

### 2. Procesamiento inicial (`spark_process_laps.py`)
- Lee los datos crudos en formato JSONL.  
- Filtra:
  - Vueltas con valores nulos.
  - La primera vuelta de cada piloto (outlier por ser de salida de pit).  
- Convierte los tiempos de vuelta a segundos y los formatea como `M:SS.mmm`.  
- Exporta el dataset limpio a `data/processed/processed_laps.csv`.

### 3. Cálculo de vueltas rápidas (`spark_fastest_laps.py`)
- Lee el dataset procesado.  
- Calcula la **vuelta más rápida por piloto** (en segundos).  
- Añade una columna con el tiempo en formato legible `M:SS.mmm`.  
- Exporta el resultado a `data/results/fastest_laps.csv`.

---

## 📊 Ejemplo de salida

### Dataset procesado (`processed_laps.csv`)
| driver_number | lap_number | lap_time_seconds | duration_sector_1 | duration_sector_2 | duration_sector_3 | is_pit_out_lap |
|---------------|------------|------------------|-------------------|-------------------|-------------------|----------------|
| 18            | 2          | 119.436          | 29.732            | 50.693            | 39.011            | false          |
| 55            | 2          | 98.999           | 28.930            | 42.094            | 27.975            | false          |

### Vueltas rápidas (`fastest_laps.csv`)
| driver_number | fastest_lap_seconds | fastest_lap_formatted |
|---------------|---------------------|------------------------|
| 55            | 98.999              | 1:38.999               |
| 18            | 119.436             | 1:59.436               |

---

## 🚀 Requisitos

- Python 3.9+
- Apache Spark 3.x
- Dependencias:
  ```bash
  pip install -r requirements.txt
