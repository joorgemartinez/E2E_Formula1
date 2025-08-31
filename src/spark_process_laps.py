import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round, udf
from pyspark.sql.types import StringType

# === Función para formatear segundos a M:SS.mmm ===
def format_duration(seconds: float) -> str:
    if seconds is None:
        return None
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{secs:02d}.{millis:03d}"

# Registrar UDF
format_udf = udf(format_duration, StringType())

# Sesión de Spark
spark = SparkSession.builder \
    .appName("F1 Curated Laps") \
    .getOrCreate()

# Leer JSONL
laps_df = spark.read.json("data/laps.jsonl")

# Seleccionar columnas relevantes
laps_selected_df = laps_df.select(
    col("driver_number"),
    col("lap_number"),
    round(col("lap_duration"), 3).alias("lap_time_seconds"),
    col("duration_sector_1"),
    col("duration_sector_2"),
    col("duration_sector_3"),
    col("is_pit_out_lap")
)

# Filtrar nulos y vuelta 1 (Outlier Nulo)
laps_clean_df = laps_selected_df.filter(
    (col("lap_time_seconds").isNotNull()) & (col("lap_number") > 1)
)

# 👉 En vez de sobrescribir, añadimos una columna nueva
laps_formatted_df = laps_clean_df.withColumn(
    "lap_time_formatted", format_udf(col("lap_time_seconds"))
)

print("Ejemplo de datos transformados:")
laps_formatted_df.show(10, truncate=False)

# Guardar en carpeta temporal
output_dir = "data/processed_laps"
laps_formatted_df.coalesce(1).write.mode("overwrite").csv(output_dir, header=True)

# Buscar el archivo que empieza con "part"
for file in os.listdir(output_dir):
    if file.startswith("part") and file.endswith(".csv"):
        part_file = os.path.join(output_dir, file)
        final_file = "data/processed_laps.csv"
        shutil.move(part_file, final_file)
        print(f"✅ Archivo final renombrado a {final_file}")

# (Opcional) borrar la carpeta sobrante
shutil.rmtree(output_dir)

print("🎉 Curated dataset listo en data/curated_laps.csv")
spark.stop()
