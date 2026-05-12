import subprocess
import json

process = subprocess.Popen( # Crea OTRO proceso Python. El proceso padre es main.py y el proceso hijo es weather.py
    ["python", "weather.py"],
    stdin=subprocess.PIPE, # Permite enviar datos al proceso hijo a través de su entrada estándar (stdin)
    stdout=subprocess.PIPE, # Permite leer la salida del proceso hijo a través de su salida estándar (stdout)
    text=True # Indica que los datos se manejarán como texto (en lugar de bytes)
)

requests = [
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "client": "miguel-agent"
        }
    },

   {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    },

    # {
    #     "jsonrpc": "2.0",
    #     "id": 2,
    #     "method": "weather/get",
    #     "params": {
    #         "city": {}
    #     }
    # },
]


for request in requests:
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()



init_response = process.stdout.readline()

print("INITIALIZE RESPONSE")
print(json.dumps(json.loads(init_response), indent=2))

tools_list = process.stdout.readline()

print("tools/list RESPONSE")
print(json.dumps(json.loads(tools_list), indent=2))


# weather_response = process.stdout.readline()

# print("WEATHER RESPONSE")
# print(json.dumps(json.loads(weather_response), indent=2))

# responses = {}

# for _ in range(2):
#     raw = process.stdout.readline()
#     parsed =json.loads(raw)
#     response_id = parsed["id"]
#     responses[response_id] = parsed

# print("Respuesta del servidor:")
# print(json.dumps(responses, indent=2))


