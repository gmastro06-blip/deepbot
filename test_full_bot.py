# test_full_bot.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_full_bot():
    print("🤖 Probando bot completo...")
    
    try:
        from core.tibia_bot import TibiaBot
        
        # Crear bot
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        print("✅ Bot creado correctamente")
        print(f"📊 Estado: {bot.show_status() if hasattr(bot, 'show_status') else 'N/A'}")
        
        # 1. Detección automática
        print("\n🔍 Ejecutando detección automática...")
        success = bot.auto_detect_ui()
        
        if success:
            print("✅ Detección automática exitosa!")
            
            # Mostrar posiciones detectadas
            if hasattr(bot, 'ui_config'):
                ui_config = bot.ui_config
                print(f"\n🗺️  Elementos detectados ({len(ui_config.elements)}):")
                for name, element in ui_config.elements.items():
                    print(f"   • {name}: ({element.x}, {element.y}) {element.width}x{element.height}")
                
                # Guardar configuración
                ui_config.save_to_file()
        else:
            print("⚠️  Detección automática falló o incompleta")
        
        # 2. Monitoreo de salud/mana (si se detectaron)
        print("\n❤️💙 Probando monitoreo de HP/MP...")
        if hasattr(bot, 'start_monitoring'):
            try:
                # Monitorear por 3 segundos
                import threading
                import time
                
                monitoring = True
                
                def monitor():
                    count = 0
                    while monitoring and count < 6:  # 6 iteraciones = 3 segundos aprox.
                        if hasattr(bot, 'check_health') and callable(bot.check_health):
                            hp = bot.check_health()
                            print(f"   HP: {hp}%" if hp else "   No se pudo leer HP")
                        
                        if hasattr(bot, 'check_mana') and callable(bot.check_mana):
                            mp = bot.check_mana()
                            print(f"   MP: {mp}%" if mp else "   No se pudo leer MP")
                        
                        time.sleep(0.5)
                        count += 1
                
                print("   Iniciando monitoreo (3 segundos)...")
                monitor_thread = threading.Thread(target=monitor)
                monitor_thread.start()
                monitor_thread.join()
                
                # Detener
                monitoring = False
                
            except Exception as e:
                print(f"   ❌ Error en monitoreo: {e}")
        
        print("\n🎉 Prueba completada!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_bot()
    if success:
        print("\n✅ ¡El bot funciona! Ejecuta: python main.py")
    else:
        print("\n💥 Algo salió mal. Revisa los errores arriba.")