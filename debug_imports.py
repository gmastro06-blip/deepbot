# debug_imports.py
import sys
import os
import traceback

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Depurando imports...")

# 1. Verificar que podemos importar UIConfig directamente
print("\n1. Probando import directo de UIConfig:")
try:
    from config.ui_config import UIConfig
    print("   ✅ UIConfig importado directamente")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# 2. Verificar ui_detector
print("\n2. Probando import de UIDetector:")
try:
    from core.ui_detector import UIDetector
    print("   ✅ UIDetector importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# 3. Verificar tibia_bot
print("\n3. Probando import de TibiaBot:")
try:
    from core.tibia_bot import TibiaBot
    print("   ✅ TibiaBot importado")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# 4. Verificar estructura de archivos
print("\n4. Verificando estructura de archivos:")
files_to_check = [
    ("core/__init__.py", True),
    ("config/__init__.py", True),
    ("detectors/__init__.py", True),
    ("processors/__init__.py", True),
    ("utils/__init__.py", True),
    ("templates/", False),  # Directorio
]

for file_path, should_be_file in files_to_check:
    exists = os.path.exists(file_path)
    is_file = os.path.isfile(file_path) if exists else False
    is_dir = os.path.isdir(file_path) if exists else False
    
    if not exists:
        print(f"   ❌ {file_path} NO existe")
    elif should_be_file and not is_file:
        print(f"   ⚠️  {file_path} existe pero no es un archivo")
    elif not should_be_file and not is_dir:
        print(f"   ⚠️  {file_path} existe pero no es un directorio")
    else:
        print(f"   ✅ {file_path} existe")

# 5. Verificar contenido de __init__.py si existen
print("\n5. Contenido de __init__.py (si existen):")
init_files = ["core/__init__.py", "config/__init__.py"]
for init_file in init_files:
    if os.path.exists(init_file):
        print(f"\n   📄 {init_file}:")
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    print(f"   Contenido: {content[:100]}...")
                else:
                    print("   (vacío)")
        except Exception as e:
            print(f"   ❌ Error leyendo: {e}")