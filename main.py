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
    "id": 1,
    "method": "weather/get",
    "params": {
        "city": "Madrid"
    }
}

process.stdin.write(json.dumps(request) + "\n")
process.stdin.flush()


response = process.stdout.readline()

parsed =json.loads(response)

print("Respuesta del servidor:")
print(json.dumps(parsed, indent=2))


