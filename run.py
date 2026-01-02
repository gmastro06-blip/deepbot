# run.py - Versión simplificada
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Instalar dependencias faltantes automáticamente
def install_dependencies():
    required = ['opencv-python', 'numpy', 'mss', 'pyautogui', 'colorama']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  Instalando dependencias faltantes: {missing}")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)

try:
    # Intentar importar
    from main import main
    sys.exit(main())
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("🔧 Intentando instalar dependencias...")
    
    install_dependencies()
    
    # Intentar de nuevo
    try:
        from main import main
        print("✅ Dependencias instaladas. Iniciando bot...")
        sys.exit(main())
    except Exception as e2:
        print(f"❌ Error crítico: {e2}")
        import traceback
        traceback.print_exc()