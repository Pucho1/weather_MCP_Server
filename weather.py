import sys
import json



async def get_weather(params):
    city = params.get("city")

    if city  == "crash":
        1 / 0  # Simula un error dividiendo por cero

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

    method_name = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")


    #  Verifica si el método solicitado existe en el diccionario de métodos
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

    # Ejecuta el método y maneja cualquier error que pueda ocurrir 
    try:
        result = methods[method_name](params)

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

    except Exception as e:
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }

    # Responde por stdout sin flush:true el clinte puede buferisarce y no recibir la respuesta inmediatamente
    print(json.dumps(response), flush=True)