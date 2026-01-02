# quick_start.py
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Verificar que todos los archivos mínimos existen
MIN_FILES = [
    'config/settings.py',
    'config/ui_config.py',
    'core/tibia_bot.py',
    'core/screen_capturer.py',
    'core/ui_detector.py',
    'detectors/health_detector.py',
    'detectors/mana_detector.py',
    'detectors/inventory_detector.py',
    'detectors/minimap_detector.py',
    'processors/color_detector.py',
    'processors/image_processor.py',
    'processors/template_matcher.py'
]

print("🔍 Verificando archivos mínimos...")
missing = []
for file in MIN_FILES:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
        missing.append(file)

if missing:
    print(f"\n⚠️  Faltan {len(missing)} archivos. Creando versiones mínimas...")
    
    # Crear versiones mínimas de los archivos faltantes
    # ... (código para crear archivos mínimos)
    
else:
    print("\n🎉 Todos los archivos están presentes!")
    print("\n🚀 Iniciando bot...")
    
    # Importar y ejecutar
    try:
        from main import main
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()