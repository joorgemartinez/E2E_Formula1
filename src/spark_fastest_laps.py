from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min as spark_min, udf
from pyspark.sql.types import StringType, DoubleType
import os, shutil

# === Función para formatear segundos a M:SS.mmm ===
def format_duration(seconds: float) -> str:
    if seconds is None:
        return None
    try:
        seconds = float(seconds)  # 👈 aseguramos conversión
    except:
        return None
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{secs:02d}.{millis:03d}"

format_udf = udf(format_duration, StringType())

# Sesión de Spark
spark = SparkSession.builder.appName("F1 Fastest Laps").getOrCreate()

# 1. Cargar dataset procesado
laps_df = spark.read.csv("data/processed_laps.csv", header=True, inferSchema=True)

# 👇 forzar que lap_time_seconds sea double
laps_df = laps_df.withColumn("lap_time_seconds", col("lap_time_seconds").cast(DoubleType()))

# 2. Calcular la vuelta más rápida por piloto
fastest_laps_df = laps_df.groupBy("driver_number") \
    .agg(spark_min("lap_time_seconds").alias("fastest_lap_seconds"))

# 3. Añadir formato legible
fastest_laps_df = fastest_laps_df.withColumn(
    "fastest_lap_formatted", format_udf(col("fastest_lap_seconds"))
)

print("Ejemplo de vueltas más rápidas por piloto:")
fastest_laps_df.show(10, truncate=False)

# === Guardar resultado ===
output_dir = "data/tmp_fastest_laps"
fastest_laps_df.coalesce(1).write.mode("overwrite").csv(output_dir, header=True)

for file in os.listdir(output_dir):
    if file.startswith("part") and file.endswith(".csv"):
        shutil.move(os.path.join(output_dir, file), "data/fastest_laps.csv")
        print("✅ Archivo final: data/fastest_laps.csv")

shutil.rmtree(output_dir)
spark.stop()
