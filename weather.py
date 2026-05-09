import sys
import json
import asyncio # concurrencia cooperativa lib de python


async def get_weather(params):
    city = params.get("city")

    if city  == "Madrid":
        # SIMULA una operación asíncrona, no detiene el programa sino que cede el hilo a otra tarea
        await asyncio.sleep(5)  
    
    return {
        "city": city,
        "temperature": "22C"
    }

methods = {
    "weather/get": get_weather
}

async def  handle_request(line):
    request = json.loads(line) # Parsea el mensaje recibido como JSON

    method_name = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")


    # Captura exepcones globales garantizando una respuesta el cliente
    try:
        # Ejecuta el método correspondiente con los parámetros proporcionados y espera su resultado sin bloquear el loop
        result = await methods[method_name](params)

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
    print(json.dumps(response), flush=True)
    

async def main():

    while True:
        line = await asyncio.to_thread(sys.stdin.readline)

        if not line:
            break

        asyncio.create_task(handle_request(line))
    


# Crea event loop, ejecuta main, destruye loop al terminar
asyncio.run(main())
