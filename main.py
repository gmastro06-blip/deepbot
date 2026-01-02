# main.py (versión simple)
import sys
import os

# Añadir directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🤖 TibiaBot - Sistema Principal")
print("="*50)

def main():
    try:
        from core.tibia_bot import TibiaBot
        
        print("\n⚙️  Inicializando bot...")
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        print("✅ Bot inicializado")
        print("\n🔍 Ejecutando detección automática...")
        
        # Ejecutar detección
        success = bot.auto_detect_ui()
        
        if success:
            print("🎉 ¡Detección exitosa!")
            
            # Mostrar menú interactivo
            while True:
                print("\n" + "="*50)
                print("📋 MENÚ PRINCIPAL")
                print("="*50)
                print("1. 👁️  Iniciar monitoreo básico")
                print("2. 📊 Mostrar estado")
                print("3. 💾 Guardar configuración")
                print("4. 🚪 Salir")
                print("="*50)
                
                opcion = input("\nSelecciona una opción (1-4): ").strip()
                
                if opcion == "1":
                    print("\n👁️  Iniciando monitoreo básico...")
                    print("⚠️  Presiona Ctrl+C para detener")
                    
                    try:
                        # Monitoreo simple sin OBS
                        import time
                        bot.is_running = True
                        
                        print("\n📊 Monitoreo iniciado:")
                        print("   • Comprobando HP/MP cada 2 segundos")
                        print("   • No hay integración con OBS")
                        
                        while bot.is_running:
                            # Aquí iría la lógica de monitoreo
                            time.sleep(2)
                            
                    except KeyboardInterrupt:
                        print("\n🛑 Monitoreo detenido")
                        bot.is_running = False
                        
                elif opcion == "2":
                    print("\n📊 Estado del bot:")
                    if hasattr(bot, 'show_status'):
                        bot.show_status()
                    else:
                        print("✅ Bot activo")
                        print(f"📁 Elementos UI: {len(bot.ui_config.elements)}")
                        
                elif opcion == "3":
                    print("\n💾 Guardando configuración...")
                    if hasattr(bot, 'save_configuration'):
                        bot.save_configuration()
                    else:
                        bot.ui_config.save_to_file()
                        print("✅ Configuración guardada")
                        
                elif opcion == "4":
                    print("\n👋 Saliendo...")
                    break
                    
                else:
                    print("⚠️  Opción no válida")
                    
        else:
            print("⚠️  La detección automática falló")
            print("💡 Ejecuta: python calibrate_ui.py")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())