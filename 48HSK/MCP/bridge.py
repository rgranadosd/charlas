import asyncio
import os
from aiohttp import web
import obsws_python as obs

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

# --- CONFIG ---
# Load configuration from environment variables
OBS_HOST = os.getenv('OBS_HOST', 'localhost')
OBS_PORT = int(os.getenv('OBS_PORT', '4444'))
OBS_PASS = os.getenv('OBS_PASS', '')

cl = None

async def init_obs():
    global cl
    if not OBS_PASS:
        print("⚠️ WARNING: OBS_PASS not set. Please set it in .env file or environment variable.")
        return
    try:
        cl = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASS)
        print(f"✅ Connected to OBS at {OBS_HOST}:{OBS_PORT}")
    except Exception as e:
        print(f"❌ Error connecting to OBS: {e}")

async def handle_call(request):
    global cl
    cmd = request.match_info.get('command', '')
    data = await request.json()
    print(f"📞 Received command: {cmd} with data: {data}")

    if not cl:
        await init_obs()
        if not cl:
            return web.json_response({'error': 'No connection to OBS'}, status=500)

    if cmd == 'SetInputSettings':
        cl.set_input_settings(data['inputName'], data['inputSettings'], True)
        return web.json_response({'status': 'ok'})

    if cmd == 'SetSceneItemEnabled':
        try:
            # Obtener la escena actual si no se especifica
            scene_name = data.get('sceneName')
            if not scene_name:
                current_scene = cl.get_current_program_scene()
                scene_name = current_scene.datain['currentProgramSceneName']
            
            # Buscar el elemento por nombre
            scene_items = cl.get_scene_item_list(scene_name)
            item_id = None
            for item in scene_items.datain['sceneItems']:
                if item['sourceName'] == data['itemName']:
                    item_id = item['sceneItemId']
                    break
            
            if item_id is None:
                return web.json_response({'error': f"Item '{data['itemName']}' not found in scene '{scene_name}'"}, status=404)
            
            # Activar o desactivar el elemento
            cl.set_scene_item_enabled(scene_name, item_id, data['enabled'])
            return web.json_response({'status': 'ok'})
        except Exception as e:
            print(f"❌ Error en SetSceneItemEnabled: {e}")
            return web.json_response({'error': str(e)}, status=500)

    return web.json_response({'error': 'Command not implemented in bridge'}, status=400)

# --------- AÑADIR ESTO ---------
OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "OBS Direct Controller",
        "version": "1.0.0"
    },
    "paths": {
        "/call/SetInputSettings": {
            "post": {
                "operationId": "setInputSettings",
                "summary": "Cambiar propiedades de una fuente de OBS",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "inputName": {"type": "string"},
                                    "inputSettings": {"type": "object"}
                                },
                                "required": ["inputName", "inputSettings"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "OK"
                    }
                }
            }
        },
        "/call/SetSceneItemEnabled": {
            "post": {
                "operationId": "setSceneItemEnabled",
                "summary": "Activar o desactivar un elemento de escena en OBS",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "itemName": {"type": "string", "description": "Nombre del elemento (por ejemplo, Logo)"},
                                    "enabled": {"type": "boolean", "description": "true para mostrar, false para ocultar"},
                                    "sceneName": {"type": "string", "description": "Nombre de la escena (opcional, usa la escena actual si no se especifica)"}
                                },
                                "required": ["itemName", "enabled"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "OK"
                    }
                }
            }
        }
    }
}

async def get_openapi(request):
    return web.json_response(OPENAPI_SPEC)
# --------------------------------

app = web.Application()
app.add_routes([
    web.post('/call/{command}', handle_call),
    web.get('/openapi.json', get_openapi)  # <--- asegúrate de que ESTA línea está
])

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_obs())
    web.run_app(app, port=8888)
