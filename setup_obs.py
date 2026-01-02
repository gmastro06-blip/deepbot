# setup_obs.py
"""
Configura OBS automáticamente para el bot
"""
import json
import os

def create_obs_profile():
    """Crea un perfil de OBS para el bot"""
    
    # Ruta de perfiles de OBS (Windows)
    obs_path = os.path.expanduser("~/AppData/Roaming/obs-studio/basic/profiles")
    
    if not os.path.exists(obs_path):
        print("❌ OBS no encontrado en ruta estándar")
        return
    
    # Crear perfil para el bot
    profile_name = "TibiaBot_Profile"
    profile_path = os.path.join(obs_path, profile_name)
    
    os.makedirs(profile_path, exist_ok=True)
    
    # Configuración básica
    config = {
        "Video": {
            "Base": "1920x1080",
            "Output": "1920x1080",
            "FPS": 30
        },
        "Audio": {
            "SampleRate": 44100
        },
        "Output": {
            "Mode": "Simple",
            "FilePath": "C:/Videos/TibiaBot",
            "Format": "mp4"
        },
        "Sources": [
            {
                "name": "Tibia_Window",
                "type": "window_capture",
                "settings": {
                    "window": "Tibia"
                }
            }
        ]
    }
    
    # Guardar configuración
    config_file = os.path.join(profile_path, "basic.ini")
    
    # Crear archivo INI básico
    ini_content = """[General]
Name=TibiaBot Profile

[Video]
BaseWidth=1920
BaseHeight=1080
OutputWidth=1920
OutputHeight=1080
FPSCommon=30

[Output]
Mode=Simple
RecFormat=mp4
RecFilePath=C:/Videos/TibiaBot

[SimpleOutput]
VBitrate=2500
ABitrate=160
"""
    
    with open(config_file, 'w') as f:
        f.write(ini_content)
    
    print(f"✅ Perfil de OBS creado: {profile_name}")
    print(f"📁 Ruta: {profile_path}")
    
    # Crear script LUA para OBS
    lua_script = """-- Script LUA para OBS con TibiaBot
obs = obslua

function script_description()
    return "Integración con TibiaBot - Muestra estado del bot en OBS"
end

function script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "bot_status", "Estado del Bot", obs.OBS_TEXT_DEFAULT)
    return props
end

function script_update(settings)
    -- Actualizar texto con estado del bot
    local status = obs.obs_data_get_string(settings, "bot_status")
    print("Estado del bot actualizado: " .. status)
end

-- Función para recibir datos del bot via WebSocket
function on_bot_message(message)
    print("Mensaje del bot: " .. message)
    -- Actualizar overlay aquí
end
"""
    
    lua_path = os.path.join(profile_path, "tibia_bot_integration.lua")
    with open(lua_path, 'w') as f:
        f.write(lua_script)
    
    print(f"✅ Script LUA creado: {lua_path}")

def install_obs_websocket():
    """Guía para instalar OBS WebSocket"""
    
    print("\n📦 INSTALACIÓN DE OBS WEBSOCKET:")
    print("="*50)
    print("1. Descarga OBS WebSocket desde:")
    print("   https://github.com/obsproject/obs-websocket/releases")
    print("\n2. Instala el complemento:")
    print("   - Extrae el .zip")
    print("   - Copia data/obs-plugins/obs-websocket a tu carpeta de OBS")
    print("\n3. Configura OBS:")
    print("   - Herramientas -> obs-websocket Settings")
    print("   - Habilitar WebSocket server")
    print("   - Configurar puerto (4455 por defecto)")
    print("   - Establecer contraseña si quieres")
    print("\n4. Reinicia OBS")
    print("="*50)

if __name__ == "__main__":
    print("🎬 CONFIGURACIÓN DE OBS PARA TIBIABOT")
    print("="*50)
    
    create_obs_profile()
    install_obs_websocket()
    
    print("\n✅ Configuración completada!")
    print("\n💡 Ahora puedes:")
    print("   1. Iniciar OBS")
    print("   2. Seleccionar el perfil 'TibiaBot_Profile'")
    print("   3. Conectar tu bot usando OBSController")