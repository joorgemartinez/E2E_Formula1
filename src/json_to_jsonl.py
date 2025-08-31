import json

# Leer archivo JSON (array)
with open("data/laps.json", "r") as f:
    laps = json.load(f)

# Guardar como JSONL (una línea = una vuelta)
with open("data/laps.jsonl", "w") as f:
    for lap in laps:
        f.write(json.dumps(lap) + "\n")

print(f"✅ Convertido {len(laps)} registros a data/laps.jsonl")
