# quick_diagnostic.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Diagnóstico rápido del sistema...")

# 1. Verificar archivos críticos
print("\n1. Archivos críticos:")
critical_files = [
    "core/tibia_bot.py",
    "core/ui_detector.py", 
    "core/screen_capturer.py",
    "config/settings.py",
    "config/ui_config.py",
    "configs/default_settings.json"
]

for file in critical_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} - FALTANTE")

# 2. Verificar directorios
print("\n2. Directorios necesarios:")
directories = ["templates", "configs", "logs"]
for dir in directories:
    if os.path.exists(dir):
        print(f"   ✅ {dir}/")
    else:
        print(f"   ❌ {dir}/ - FALTANTE")

# 3. Verificar UIDetector
print("\n3. Métodos de UIDetector:")
try:
    from core.ui_detector import UIDetector
    
    # Métodos que tibia_bot.py necesita
    required_methods = [
        'detect_health_bar',
        'detect_mana_bar',
        'detect_inventory',
        'detect_minimap', 
        'detect_equipment_window',
        'detect_skills_window',
        'detect_chat_window'
    ]
    
    # Crear instancia dummy
    class Dummy: pass
    detector = UIDetector(Dummy(), Dummy())
    
    for method in required_methods:
        if hasattr(detector, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} - FALTANTE")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

# 4. Verificar TibiaBot
print("\n4. Creando TibiaBot...")
try:
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(debug_mode=True)
    print("   ✅ TibiaBot creado exitosamente")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Diagnóstico completado!")