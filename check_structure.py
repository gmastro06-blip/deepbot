#!/usr/bin/env python3
"""
Verifica que todos los archivos necesarios estén presentes y tengan las clases correctas
"""
import os
import importlib.util
import sys
from pathlib import Path

def check_file_structure():
    """Verifica la estructura de archivos"""
    print("🔍 Verificando estructura de archivos...")
    print("=" * 60)
    
    required_files = {
        'core/tibia_bot.py': ['TibiaBot'],
        'core/screen_capturer.py': ['ScreenCapturer'],
        'core/ui_detector.py': ['UIDetector'],
        'core/bot_actions.py': ['BotActions'],
        'core/bot_state.py': ['BotState'],
        'config/settings.py': ['Settings'],
        'config/ui_config.py': ['UIConfig'],
        'detectors/health_detector.py': ['HealthDetector'],
        'detectors/mana_detector.py': ['ManaDetector'],
        'detectors/inventory_detector.py': ['InventoryDetector'],
        'detectors/minimap_detector.py': ['MinimapDetector'],
        'processors/color_detector.py': ['ColorDetector'],
        'processors/image_processor.py': ['ImageProcessor'],
        'processors/template_matcher.py': ['TemplateMatcher'],
        'utils/logger.py': ['AppLogger'],
        'utils/helpers.py': []  # Funciones, no clases
    }
    
    all_good = True
    
    for file_path, expected_classes in required_files.items():
        if not os.path.exists(file_path):
            print(f"❌ FALTANTE: {file_path}")
            all_good = False
            continue
        
        # Verificar que el archivo no esté vacío
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"❌ VACÍO: {file_path}")
            all_good = False
            continue
        
        print(f"✅ EXISTE: {file_path}")
        
        # Verificar clases específicas si se especifican
        for class_name in expected_classes:
            if not check_class_in_file(file_path, class_name):
                print(f"   ⚠️  Falta clase: {class_name}")
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 ¡Estructura de archivos completa!")
    else:
        print("⚠️  Faltan algunos archivos o tienen problemas")
    
    return all_good

def check_class_in_file(file_path: str, class_name: str) -> bool:
    """Verifica si una clase está definida en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"class {class_name}" in content
    except:
        return False

def check_dependencies():
    """Verifica dependencias instaladas"""
    print("\n🔧 Verificando dependencias...")
    print("=" * 60)
    
    dependencies = [
        ('opencv-python', 'cv2'),
        ('numpy', 'numpy'),
        ('mss', 'mss'),
        ('pyautogui', 'pyautogui'),
        ('colorama', 'colorama'),
        ('Pillow', 'PIL')
    ]
    
    all_installed = True
    
    for pip_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            all_installed = False
    
    print("\n" + "=" * 60)
    if all_installed:
        print("🎉 ¡Todas las dependencias están instaladas!")
    else:
        print("⚠️  Faltan algunas dependencias")
        print("\n💡 Instala las dependencias faltantes con:")
        print("   pip install opencv-python numpy mss pyautogui colorama Pillow")
    
    return all_installed

def test_imports():
    """Prueba importar los módulos principales"""
    print("\n🔄 Probando imports...")
    print("=" * 60)
    
    test_modules = [
        ('core.tibia_bot', 'TibiaBot'),
        ('core.screen_capturer', 'ScreenCapturer'),
        ('core.bot_actions', 'BotActions'),
        ('core.bot_state', 'BotState'),
        ('config.settings', 'Settings'),
        ('utils.logger', 'AppLogger')
    ]
    
    all_imported = True
    
    # Agregar directorio actual al path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    for module_path, class_name in test_modules:
        try:
            spec = importlib.util.spec_from_file_location(
                module_path.replace('.', '_'),
                module_path.replace('.', '/') + '.py'
            )
            if spec is None:
                print(f"❌ No se pudo encontrar: {module_path}")
                all_imported = False
                continue
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Verificar que la clase exista
            if hasattr(module, class_name):
                print(f"✅ {module_path}.{class_name}")
            else:
                print(f"❌ Falta clase {class_name} en {module_path}")
                all_imported = False
                
        except Exception as e:
            print(f"❌ Error importando {module_path}: {e}")
            all_imported = False
    
    print("\n" + "=" * 60)
    if all_imported:
        print("🎉 ¡Todos los imports funcionan correctamente!")
    else:
        print("⚠️  Hay problemas con algunos imports")
    
    return all_imported

def main():
    """Función principal"""
    print("🤖 DEEP BOT - VERIFICACIÓN DE ESTRUCTURA")
    print("=" * 60)
    
    # Paso 1: Verificar archivos
    files_ok = check_file_structure()
    
    # Paso 2: Verificar dependencias
    deps_ok = check_dependencies()
    
    # Paso 3: Probar imports (solo si los archivos existen)
    imports_ok = False
    if files_ok:
        imports_ok = test_imports()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    print(f"📁 Archivos: {'✅ COMPLETO' if files_ok else '❌ INCOMPLETO'}")
    print(f"🔧 Dependencias: {'✅ INSTALADAS' if deps_ok else '❌ FALTANTES'}")
    print(f"🔄 Imports: {'✅ FUNCIONALES' if imports_ok else '❌ CON ERRORES'}")
    
    print("\n" + "=" * 60)
    if files_ok and deps_ok and imports_ok:
        print("🎉 ¡TODO LISTO! Puedes ejecutar el bot:")
        print("   python main.py --auto-detect")
        return 0
    else:
        print("⚠️  Hay problemas que resolver antes de ejecutar el bot")
        return 1

if __name__ == "__main__":
    sys.exit(main())