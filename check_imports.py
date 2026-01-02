# check_imports.py
import sys
import os

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_imports():
    print("🔍 Verificando imports...")
    
    try:
        from config.ui_config import UIConfig
        print("✅ UIConfig importado correctamente")
        
        # Verificar que no haya auto-import
        import config.ui_config as ui_config_module
        if hasattr(ui_config_module, '__file__'):
            with open(ui_config_module.__file__, 'r') as f:
                content = f.read()
                if 'from config.ui_config import UIConfig' in content:
                    print("❌ ERROR: Importación circular detectada en ui_config.py")
                    print("   Elimina esta línea: 'from config.ui_config import UIConfig'")
                else:
                    print("✅ No hay importación circular en ui_config.py")
        
        # Verificar otros imports importantes
        imports_to_check = [
            ('core.ui_detector', 'UIDetector'),
            ('processors.template_matcher', 'TemplateMatcher'),
            ('config.settings', 'Settings'),
        ]
        
        for module_name, class_name in imports_to_check:
            try:
                module = __import__(module_name, fromlist=[class_name])
                if hasattr(module, class_name):
                    print(f"✅ {module_name}.{class_name} disponible")
                else:
                    print(f"❌ {class_name} no encontrado en {module_name}")
            except ImportError as e:
                print(f"❌ Error importando {module_name}: {e}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_imports()