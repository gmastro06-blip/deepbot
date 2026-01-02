# check_files.py
import os
from pathlib import Path

REQUIRED_FILES = {
    'core/': ['tibia_bot.py', 'screen_capturer.py', 'ui_detector.py', 
              'bot_actions.py', 'bot_state.py'],
    'config/': ['settings.py', 'ui_config.py'],
    'detectors/': ['health_detector.py', 'mana_detector.py', 
                   'inventory_detector.py', 'minimap_detector.py'],
    'processors/': ['image_processor.py', 'color_detector.py', 'template_matcher.py'],
    'utils/': ['logger.py', 'helpers.py', 'file_manager.py', 'performance_monitor.py'],
    'configs/': ['default_settings.json']
}

print("🔍 Verificando archivos necesarios...")
print("=" * 50)

all_good = True

for folder, files in REQUIRED_FILES.items():
    print(f"\n📁 {folder}")
    for file in files:
        path = Path(folder) / file
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - FALTANTE")
            all_good = False

print("\n" + "=" * 50)
if all_good:
    print("🎉 Todos los archivos están presentes!")
else:
    print("⚠️  Faltan algunos archivos. Crea los archivos marcados con ❌")

# Verificar estructura básica
print("\n🏗️  Estructura de carpetas:")
for folder in REQUIRED_FILES.keys():
    if Path(folder).exists():
        print(f"  ✅ {folder}")
    else:
        print(f"  ❌ {folder}")