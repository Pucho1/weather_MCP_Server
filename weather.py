import sys
import json
import asyncio
from pydantic import BaseModel

initialized = False

# --------ERRORS--------

class MCPError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

        super().__init__(message)




# ---------PROMPTS----------

prompts = {
    "weather-summary": {
        "description": "Generate a weather analysis prompt",
        "arguments": [
            {
                "name": "city",
                "required": True
            }
        ],
        "template": "Analyze the weather conditions in {city}"
    }
}

#  Me dice el listado de prompts que tengo disponible.
async def list_prompts(params):

    public_prompts = {}

    for name, prompt in prompts.items():

        public_prompts[name] = {
            "description": prompt["description"],
            "arguments": prompt["arguments"]
        }

    return {
        "prompts": public_prompts
    }


# Obtinee la plantilla para el prompt solicitado.
async def get_prompt(params):

    prompt_name = params.get("name") # Obtengo el nombre del prompt.
    arguments = params.get("arguments", {}) # Obtengo los argumentos. 

    if prompt_name not in prompts:
        raise MCPError(-32601, "Prompt not found")

    prompt = prompts[prompt_name] # Obtengo todos los datos segun el nombre del prompt.

    template = prompt["template"]

    rendered_prompt = template.format(**arguments) # Cambio el parametro por su valor city --> Madrid .

    return {
        "description": prompt["description"],
        "prompt": rendered_prompt
    }





# -------RESOURCES------------

resources = {
    "weather://madrid": {
        "name": "Madrid Weather Info",
        "description": "Static weather information for Madrid",
        "content": "Madrid is usually sunny."
    }
}

# cro una lista con todos mis recursos
async def list_resources(params):

    # Creamos un diccionario vacío para exponer solo la información pública
    public_resources = {}

    # Recorremos todos los recursos disponibles (key, value)
    for uri, resource in resources.items():

        # Guardamos el nombre y la descripción del recurso en la lista pública
        public_resources[uri] = {
            "name": resource["name"],
            "description": resource["description"]
        }

    # Devolvemos el diccionario de recursos públicos al cliente
    return {
        "resources": public_resources
    }

# devuelvo el contenido de el recurso pedido
async def read_resource(params):

    # Obtenemos el URI solicitado desde los parámetros de la petición
    uri = params.get("uri")

    # Comprobamos que el recurso exista en el catálogo
    if uri not in resources:
        raise MCPError(-32601 ,"Resource not found")

    # Recuperamos el recurso completo usando el URI
    resource = resources[uri]

    # Retornamos el URI y el contenido del recurso pedido
    return {
        "uri": uri,
        "content": resource["content"]
    }




# -------TOOLS------------

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


# Metodo que me ejecuta la herramieta de obtener clima.
async def get_weather(params):
    city = params.city # Instancia tipada de Pydantic.

    if city == "Madrid":
        await asyncio.sleep(5)

    return {
        "city": city,
        "temperature": "22C"
    }


tools_publics = {
    "weather/get": {
        "description": "Get weather for a city",
        # Usamos esquemas Porque los LLMs: necesitan estructuras claras, funcionan muchísimo mejor con contratos explícitos.
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                }
            },
            "required": ["city"]
        },
    }
}

tools_runtime = {
    "weather/get": {
        "description": "Get weather for a city",
        # Usamos esquemas Porque los LLMs: necesitan estructuras claras, funcionan muchísimo mejor con contratos explícitos.
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string"
                }
            },
            "required": ["city"]
        },
        "schema": WeatherParams,# validamos los parametros.
        "handler": get_weather, # Funcion que ejecuta la herramienta.
    }
}

# Devolvemos la lista de erramientas segun los esquemas definidos.
async def list_tools(params):
    return {
        "tools": tools_publics
    }


# Ejecuta dispath de la tool dinamicamente.
async def call_tool(params):

    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name not in tools_runtime:
        raise MCPError(-32601, "Tool not found")
    
    tool = tools_runtime[tool_name]

    schema = tool["schema"]
    handler = tool["handler"]

    validated_arguments = schema(**arguments)

    result = await handler(validated_arguments)

    return result


protocol_methods  = {
    "initialize": initialize,

    # tools
    "tools/list": list_tools,
    "tools/call": None,

    # resources
    "resources/list": list_resources,
    "resources/read": read_resource,

    # prompts
    "prompts/list": list_prompts,
    "prompts/get": get_prompt,
}

protocol_methods["tools/call"] = call_tool


# Manejo la peticion.
async def handle_request(line):
    global initialized

    request = json.loads(line) # serializa el dato a json

    method_name = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    # Captura exepcones globales garantizando una respuesta el cliente
    try:

        if method_name != "initialize" and not initialized:
            raise BlockingIOError("Server not initialized")

        if method_name not in protocol_methods:
            raise NotImplementedError("Method not found")

        # Ejecuta el método correspondiente con los parámetros proporcionados y espera su resultado sin bloquear el loop
        result = await protocol_methods[method_name](params)

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

    except MCPError as e:
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": e.code,
                "message": e.message
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