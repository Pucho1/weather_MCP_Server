import subprocess
import json

process = subprocess.Popen( # Crea OTRO proceso Python. El proceso padre es main.py y el proceso hijo es weather.py
    ["python", "weather.py"],
    stdin=subprocess.PIPE, # Permite enviar datos al proceso hijo a través de su entrada estándar (stdin)
    stdout=subprocess.PIPE, # Permite leer la salida del proceso hijo a través de su salida estándar (stdout)
    text=True # Indica que los datos se manejarán como texto (en lugar de bytes)
)


# INICIAL CALL HAND_CHAKE

initial_call = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "client": "miguel-agent"
    }
}

process.stdin.write(json.dumps(initial_call) + "\n")
process.stdin.flush()


init_response = process.stdout.readline()

print("INITIALIZE RESPONSE")
print(json.dumps(json.loads(init_response), indent=2))



# GET TOOL LIST

get_tool_list_call = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}

process.stdin.write(json.dumps(get_tool_list_call) + "\n")
process.stdin.flush()


tools_list      = process.stdout.readline()
tools_data      = json.loads(tools_list)

available_tools = tools_data["result"]["tools"]

tool_name = list(available_tools.keys())[0]

print("tools/list RESPONSE")
print(json.dumps(available_tools, indent=2))




tool_call_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": tool_name,
        "arguments": {
        "city": "Madrid"
        }
    }
}

process.stdin.write(json.dumps(tool_call_request) + "\n")
process.stdin.flush()

tool_result = process.stdout.readline()
tool_result_data = json.loads(tool_result)

print("tools RESPONSE")
print(json.dumps(tool_result_data, indent=2))




# -------RESOURCES----------


resources_list_request = {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "resources/list",
    "params": {}
}

process.stdin.write(json.dumps(resources_list_request) + "\n")
process.stdin.flush()


resources_response = process.stdout.readline()
resources_data = json.loads(resources_response)


available_resources = resources_data["result"]["resources"]

print("RESOURCES")
print(json.dumps(available_resources, indent=2))


resource_uri = next(iter(available_resources.keys()))
# resource_uri = list(available_resources.keys())[0]

resource_read_request = {
    "jsonrpc": "2.0",
    "id": 5,
    "method": "resources/read",
    "params": {
        "uri": "toma//toma"
    }
}

process.stdin.write(json.dumps(resource_read_request) + "\n")
process.stdin.flush()



resource_content = process.stdout.readline()

resource_data = json.loads(resource_content)

print("RESOURCE CONTENT")
print(json.dumps(resource_data, indent=2))