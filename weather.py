import sys
import json
import asyncio
from pydantic import BaseModel

initialized = False

# Digo el tipo de datos del cual sera el parametro.
# describe exactamente qué falla
class WeatherParams(BaseModel):
    city: str

async def initialize(params):
    global initialized

    initialized = True

    return {
        "server": "weather-server",
        "version": "1.0",
        "capabilities": {
            "tools": True
        }
    }


async def get_weather(params):
    validated = WeatherParams(**params)

    city = validated.city

    if city == "Madrid":
        await asyncio.sleep(5)

    return {
        "city": city,
        "temperature": "22C"
    }

#  usamos esquemas Porque los LLMs: necesitan estructuras claras, funcionan muchísimo mejor con contratos explícitos
tools = {
    "weather/get": {
        "description": "Get weather for a city",
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                }
            },
            "required": ["city"]
        }
    }
}

async def list_tools(params):
    return {
        "tools": tools
    }

tool_handlers = {
    "weather/get": get_weather
}

methods = {
    "initialize": initialize,
    "tools/list": list_tools,
    "tools/call": None,
}


# Manejo la peticion.
async def handle_request(line):
    global initialized

    request = json.loads(line)

    method_name = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    # Captura exepcones globales garantizando una respuesta el cliente
    try:

        if method_name != "initialize" and not initialized:
            raise Exception("Server not initialized")

        if method_name not in methods:
            raise Exception("Method not found")

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