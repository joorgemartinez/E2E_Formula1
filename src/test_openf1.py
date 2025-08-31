import requests
import json

# Ejemplo: vueltas del GP de Bahréin 2024 (session_key=9158)
url = "https://api.openf1.org/v1/laps?session_key=9158"

# Hacemos la llamada a la API
response = requests.get(url)
response.raise_for_status()  # lanza error si algo falla

# Parseamos la respuesta a JSON
data = response.json()

# Guardamos los datos en un archivo dentro de /data
with open("data/laps.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Descargadas {len(data)} vueltas y guardadas en data/laps.json")
