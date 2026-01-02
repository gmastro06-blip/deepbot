#!/usr/bin/env python3
"""
Script para instalar dependencias y ejecutar el bot automáticamente
"""
import sys
import os
import subprocess

def check_and_install_dependencies():
    """Verifica e instala dependencias faltantes"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        ('opencv-python', 'cv2'),
        ('numpy', 'numpy'),
        ('mss', 'mss'),
        ('pyautogui', 'pyautogui'),
        ('colorama', 'colorama'),
        ('Pillow', 'PIL')
    ]
    
    missing_packages = []
    
    for pip_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n⚠️  Instalando {len(missing_packages)} paquetes faltantes...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Dependencias instaladas exitosamente!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            print("💡 Intenta instalar manualmente: pip install", " ".join(missing_packages))
            return False
    else:
        print("\n🎉 Todas las dependencias están instaladas!")
    
    return True

def run_bot():
    """Ejecuta el bot principal"""
    print("\n🚀 Iniciando DeepBot...")
    print("=" * 50)
    
    try:
        # Agregar directorio actual al path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Importar y ejecutar
        from main import main
        sys.exit(main())
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n💡 Posibles soluciones:")
        print("1. Verifica que todos los archivos del proyecto estén presentes")
        print("2. Reinstala dependencias: pip install -r requirements.txt")
        print("3. Verifica la estructura de carpetas")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🤖 DEEP BOT - CONFIGURACIÓN AUTOMÁTICA")
    print("=" * 50)
    
    # Paso 1: Verificar e instalar dependencias
    if not check_and_install_dependencies():
        return 1
    
    # Paso 2: Verificar estructura de archivos
    print("\n📁 Verificando estructura de archivos...")
    
    required_files = [
        'main.py',
        'core/tibia_bot.py',
        'core/screen_capturer.py',
        'core/ui_detector.py',
        'core/bot_actions.py',
        'core/bot_state.py',
        'config/settings.py',
        'config/ui_config.py',
        'detectors/health_detector.py',
        'detectors/mana_detector.py',
        'detectors/inventory_detector.py',
        'detectors/minimap_detector.py',
        'processors/color_detector.py',
        'processors/image_processor.py',
        'processors/template_matcher.py',
        'utils/logger.py',
        'utils/helpers.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Faltan {len(missing_files)} archivos importantes.")
        print("💡 Asegúrate de tener todos los archivos del proyecto.")
        return 1
    
    print("\n✅ Estructura de archivos completa!")
    
    # Paso 3: Ejecutar el bot con los argumentos pasados
    print("\n" + "=" * 50)
    print("🤖 EJECUTANDO DEEP BOT")
    print("=" * 50)
    
    # Pasar argumentos al bot
    bot_args = sys.argv[1:]  # Todos los argumentos excepto el nombre del script
    
    if bot_args:
        print(f"Argumentos: {' '.join(bot_args)}")
    
    # Agregar argumentos al sistema
    sys.argv = ['main.py'] + bot_args
    
    # Ejecutar bot
    return run_bot()

if __name__ == "__main__":
    sys.exit(main())