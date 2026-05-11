import subprocess
import json

process = subprocess.Popen( # Crea OTRO proceso Python. El proceso padre es main.py y el proceso hijo es weather.py
    ["python", "weather.py"],
    stdin=subprocess.PIPE, # Permite enviar datos al proceso hijo a través de su entrada estándar (stdin)
    stdout=subprocess.PIPE, # Permite leer la salida del proceso hijo a través de su salida estándar (stdout)
    text=True # Indica que los datos se manejarán como texto (en lugar de bytes)
)

request = {
    "jsonrpc": "2.0",
    "id": 100,
    "method": "weather/get",
    "params": {
        "city": "Madrid"
    }
}

request2 = {
    "jsonrpc": "2.0",
    "id": 200,
    "method": "weather/get",
    "params": {
        "city": "Paris"
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()

process.stdin.write(json.dumps(request2) + "\n")
process.stdin.flush()

responses = {}

for _ in range(2):
    raw = process.stdout.readline()
    parsed =json.loads(raw)
    response_id = parsed["id"]
    responses[response_id] = parsed

print("Respuesta del servidor:")
print(json.dumps(responses, indent=2))


