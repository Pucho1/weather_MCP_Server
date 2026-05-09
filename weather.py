import sys
import json



def get_weather(params):
    city = params.get("city")

    return {
        "city": city,
        "temperature": "22C"
    }

methods = {
    "weather/get": get_weather
}

# Escucha mensajes entrantes
for line in sys.stdin:
    request = json.loads(line) # Parsea el mensaje recibido como JSON

    # print("Mensaje recibido:", request, flush=True)

    method_name = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")


    if method_name not in methods:
        error_response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }

        print(json.dumps(error_response), flush=True)
        continue

    result = methods[method_name](params)

    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }

    # Responde por stdout sin flush:true el clinte puede buferisarce y no recibir la respuesta inmediatamente
    print(json.dumps(response), flush=True) 