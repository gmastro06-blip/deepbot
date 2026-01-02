# run_bot.py
"""
Script para ejecutar el bot correctamente
"""
import sys
import os
import subprocess

def check_and_fix():
    """Verifica y arregla problemas comunes"""
    
    print("🔧 Preparando entorno del bot...")
    
    # 1. Verificar que estamos en el directorio correcto
    required_files = [
        "core/tibia_bot.py",
        "core/ui_detector.py",
        "configs/default_settings.json"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Faltan archivos: {missing}")
        return False
    
    print("✅ Estructura de archivos OK")
    
    # 2. Verificar imports
    print("\n🔍 Verificando imports...")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        import cv2
        import mss
        import numpy as np
        print("✅ Dependencias básicas OK")
        
        from core.tibia_bot import TibiaBot
        print("✅ TibiaBot importado")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_bot():
    """Ejecuta el bot"""
    
    print("\n" + "="*50)
    print("🚀 EJECUTANDO TIBIABOT")
    print("="*50)
    
    if not check_and_fix():
        print("\n❌ No se pudo preparar el entorno")
        return 1
    
    try:
        # Ejecutar el bot
        from core.tibia_bot import TibiaBot
        
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        print("\n✅ Bot inicializado")
        
        # Ejecutar detección
        print("\n🔍 Ejecutando detección automática...")
        success = bot.auto_detect_ui()
        
        if success:
            print("\n🎉 ¡Todo listo!")
            print("\n💡 Comandos disponibles:")
            print("   • Ejecuta nuevamente para reiniciar")
            print("   • Modifica configs/ para ajustar")
            print("   • Crea scripts personalizados")
        else:
            print("\n⚠️  Hubo problemas con la detección")
            print("💡 Revisa que Tibia esté visible en pantalla")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    # Limpiar pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Ejecutar bot
    exit_code = run_bot()
    
    print("\n" + "="*50)
    if exit_code == 0:
        print("✅ Ejecución completada")
    else:
        print("❌ Ejecución falló")
    
    sys.exit(exit_code)