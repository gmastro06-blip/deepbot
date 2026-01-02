# main_with_obs.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🤖 TibiaBot + OBS Integration")
    print("="*50)
    
    try:
        # Importar componentes
        from core.tibia_bot import TibiaBot
        from obs_integration import OBSController
        
        # Inicializar OBS
        print("\n🔗 Conectando con OBS...")
        obs = OBSController(
            host='localhost',
            port=4455,
            password=''  # Deja vacío si no usas contraseña
        )
        
        if obs.client:
            print("✅ Conectado a OBS")
            
            # Iniciar grabación automática
            obs.start_recording()
            
            # Crear overlay del bot
            bot_info = {
                "hp": 100,
                "mp": 100, 
                "state": "Calibrando"
            }
            obs.create_scene_with_overlay(bot_info)
        
        # Inicializar bot
        print("\n🤖 Inicializando TibiaBot...")
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        # Usar OBS como fuente de captura si está disponible
        if obs.client:
            print("🎬 Usando OBS como fuente de captura")
            # Aquí modificarías el bot para usar OBS en lugar de captura directa
        
        # Ejecutar bot normal
        print("\n🔍 Ejecutando detección...")
        bot.auto_detect_ui()
        
        # Monitoreo con OBS
        print("\n👁️  Iniciando monitoreo con OBS...")
        try:
            while True:
                # Actualizar overlay de OBS
                if obs.client:
                    # Obtener estado actual del bot
                    current_hp = 85  # Esto vendría del análisis real
                    current_mp = 70
                    
                    obs.show_bot_alert(f"HP: {current_hp}% | MP: {current_mp}%", 2)
                
                # Lógica de monitoreo normal
                # ... (tu código existente)
                
                import time
                time.sleep(1)  # Intervalo de monitoreo
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoreo detenido")
            if obs.client:
                obs.stop_recording()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()