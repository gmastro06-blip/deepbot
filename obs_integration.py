# obs_integration.py
"""
Integración con OBS - Versión actualizada para OBS 30+ (2026)
"""
import sys
import os
import time

# Añadir directorio actual al path (por si ejecutas desde otro lugar)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_obs():
    """Configura y conecta a OBS WebSocket (protocolo v5)"""
    print("🎥 Configurando integración con OBS (WebSocket v5)...")
    
    try:
        from obswebsocket import obsws, requests
        print("✅ obs-websocket-py importado correctamente")
    except ImportError:
        print("❌ obs-websocket-py no está instalado")
        print("💡 Instala con: pip install obs-websocket-py")
        return None

    # Configuración actual para OBS 28+
    host = "localhost"
    port = 4455        # Puerto por defecto en versiones modernas
    password = ""      # Pon aquí tu contraseña si la configuraste en OBS

    try:
        client = obsws(host, port, password)
        client.connect()
        print("✅ Conectado a OBS WebSocket")

        # Obtener versión (en v5 se llama obsVersion)
        response = client.call(requests.GetVersion())
        print(f"✅ OBS versión: {response.getObsVersion()}")
        print(f"   WebSocket versión: {response.getObsWebsocketVersion()}")

        return client

    except Exception as e:
        print(f"❌ Error conectando a OBS: {e}")
        print("💡 Verifica que:")
        print("   1. OBS esté abierto")
        print("   2. WebSocket esté habilitado (Herramientas → WebSockets Server Settings)")
        print("   3. Puerto sea 4455 y contraseña correcta")
        return None

def update_text_source(client, source_name: str, text: str = "¡Alerta!"):
    """Actualiza o crea una fuente de texto en la escena actual"""
    try:
        from obswebsocket import requests

        # Intentar actualizar texto existente
        client.call(requests.SetInputSettings(
            inputName=source_name,
            inputSettings={"text": text}
        ))
        print(f"✅ Texto actualizado en fuente: {source_name}")
        return True

    except Exception as e:
        print(f"⚠️ Fuente no existe aún, intentando crearla: {e}")
        try:
            # Crear nueva fuente de texto (v5 usa inputKind "text_gdiplus_v2" en Windows)
            client.call(requests.CreateInput(
                sceneName="Escena",  # Cambia por el nombre real de tu escena
                inputName=source_name,
                inputKind="text_gdiplus_v2",
                inputSettings={
                    "text": text,
                    "font": {"face": "Arial", "flags": 0, "size": 72},
                    "color": 0xFF0000FF  # Rojo con alpha (ARGB)
                }
            ))
            print(f"✅ Fuente de texto creada: {source_name}")
            return True
        except Exception as create_error:
            print(f"❌ Error creando fuente: {create_error}")
            return False

def main():
    print("🎬 Integración OBS para DEEPBOT - Tibia")
    print("=" * 50)

    obs_client = setup_obs()

    if not obs_client:
        print("\n⚠️ No se pudo conectar a OBS → Modo sin overlay")
        # Aquí iría tu bot sin OBS
        return

    print("\n✅ Integración OBS activada")

    # Ejemplo: actualizar una fuente de texto
    update_text_source(obs_client, "AlertaBot", "¡HP Bajo! Usa potion!")

    # Aquí integrarías con tu bot principal
    # Por ejemplo: cuando detectes low HP/mana → update_text_source(...)

    try:
        print("\n🤖 Manteniendo conexión OBS... (Ctrl+C para salir)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Desconectando de OBS...")
        obs_client.disconnect()

if __name__ == "__main__":
    main()