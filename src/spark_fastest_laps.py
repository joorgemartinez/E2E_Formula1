from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min as spark_min

# 1. Crear sesión de Spark
spark = SparkSession.builder \
    .appName("F1 Fastest Laps") \
    .getOrCreate()

#2. Leer JSON generado en el paso anterior 
laps_df = spark.read.json("data/laps.json")

print("Schema de los datos:")
laps_df.printSchema()

# Mostrar primeras filas para inspección
print("Ejemplo de datos:")
laps_df.show(5)

# 3. Seleccionar columnas de interés 
laps_selected = laps_df.select("driver_number", "lap_number", "lap_duration")

# 4. Calcular vuelta más rápida por piloto 
fastest_laps = laps_selected.groupBy("driver_number") \
    .agg(spark_min("lap_duration").alias("fastest_lap_time"))

# 5. Guardar resultados en CSV 
fastest_laps.coalesce(1).write.mode("overwrite").csv("data/fastest_laps", header=True)

print("✅ Archivo generado en data/fastest_laps/")
spark.stop()
