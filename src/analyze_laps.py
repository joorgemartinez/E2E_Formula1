import json
from collections import Counter

def format_duration(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{secs:02d}.{millis:03d}"


# Leer el archivo que generamos en el paso 1
with open("data/laps.json", "r") as f:
    laps = json.load(f)

print(f"Total de vueltas descargadas: {len(laps)}")

# Mostrar las primeras 2 vueltas como ejemplo
print("\nEjemplo de vuelta:")
for lap in laps[:2]:
    print(lap)

# --- Estadísticas básicas ---
# 1. Número de pilotos
drivers = {lap.get("driver_number") for lap in laps}
print(f"\nNúmero de pilotos en la carrera: {len(drivers)}")
print(f"Pilotos (driver_number): {drivers}")

# 2. Vueltas por piloto
laps_per_driver = Counter([lap.get("driver_number") for lap in laps])
print("\nVueltas por piloto:")
for driver, count in laps_per_driver.items():
    print(f" Piloto {driver}: {count} vueltas")

# 3. Duración media de las vueltas

durations = [lap.get("lap_duration") for lap in laps if lap.get("lap_duration")]
avg_duration = sum(durations) / len(durations)
print(f"\nDuración media de vuelta: {format_duration(avg_duration)}")
