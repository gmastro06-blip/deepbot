# verify_structure.py
import os
from pathlib import Path

print("🔍 Verificando estructura del proyecto...")

REQUIRED = {
    'detectors/': ['health_detector.py', 'mana_detector.py', 
                   'inventory_detector.py', 'minimap_detector.py'],
    'processors/': ['color_detector.py', 'image_processor.py', 'template_matcher.py'],
    'core/': ['tibia_bot.py', 'screen_capturer.py', 'ui_detector.py'],
    'config/': ['settings.py', 'ui_config.py']
}

all_good = True

for folder, files in REQUIRED.items():
    print(f"\n📁 {folder}")
    for file in files:
        path = Path(folder) / file
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            all_good = False

if all_good:
    print("\n🎉 ¡Estructura completa! Puedes ejecutar:")
    print("   python main.py --auto-detect")
else:
    print("\n⚠️  Faltan archivos. Crea los archivos marcados con ❌")

# Verificar archivos de plantilla
print("\n🖼️  Plantillas (opcionales pero recomendadas):")
templates = ['hp_bar_segment.png', 'mp_bar_segment.png', 
             'inventory_corner.png', 'minimap_circle.png']
for template in templates:
    path = Path('templates') / template
    if path.exists():
        print(f"  ✅ {template}")
    else:
        print(f"  ⚠️  {template} (puedes crearlo más tarde)")