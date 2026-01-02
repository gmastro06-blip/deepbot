# diagnose_ui_detector.py
import os
import sys

def check_ui_detector():
    """Verifica el archivo ui_detector.py"""
    
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return
    
    print(f"🔍 Analizando {file_path}...")
    
    try:
        # Intentar abrir y compilar el archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Intentar compilar para detectar errores de sintaxis
        compile(content, file_path, 'exec')
        print("✅ Sintaxis correcta")
        
        # Verificar que tenga la clase UIDetector
        if 'class UIDetector' in content:
            print("✅ Clase UIDetector encontrada")
        else:
            print("❌ Clase UIDetector NO encontrada en el archivo")
            
        # Verificar imports
        if 'import cv2' in content:
            print("✅ Import cv2 encontrado")
        else:
            print("❌ Import cv2 NO encontrado")
            
        # Contar líneas
        lines = content.split('\n')
        print(f"📄 Total de líneas: {len(lines)}")
        
    except SyntaxError as e:
        print(f"❌ ERROR DE SINTAXIS: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
        
        # Mostrar contexto del error
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            start = max(0, e.lineno - 3)
            end = min(len(lines), e.lineno + 2)
            print(f"\n📝 Contexto del error (líneas {start+1}-{end}):")
            for i in range(start, end):
                prefix = ">>> " if i == e.lineno - 1 else "    "
                print(f"{prefix}{i+1}: {lines[i].rstrip()}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def fix_common_errors():
    """Corrige errores comunes en ui_detector.py"""
    
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Corrigiendo errores comunes...")
        
        # 1. Reemplazar caracteres problemáticos
        content = content.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        
        # 2. Corregir imports faltantes
        if 'import numpy as np' not in content:
            print("⚠️  Añadiendo import numpy as np")
            # Añadir después de import cv2
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if 'import cv2' in line:
                    new_lines.append('import numpy as np')
            content = '\n'.join(new_lines)
        
        # 3. Verificar que todos los imports estén presentes
        required_imports = [
            'from typing import',
            'from dataclasses import',
            'import logging'
        ]
        
        for imp in required_imports:
            if imp not in content:
                print(f"⚠️  Añadiendo {imp}")
                lines = content.split('\n')
                new_lines = []
                added = False
                for line in lines:
                    new_lines.append(line)
                    if not added and 'import cv2' in line:
                        if 'from typing import' not in content:
                            new_lines.append('from typing import Dict, List, Optional, Tuple, Any')
                        if 'from dataclasses import' not in content:
                            new_lines.append('from dataclasses import dataclass')
                        if 'import logging' not in content:
                            new_lines.append('import logging')
                        added = True
                content = '\n'.join(new_lines)
        
        # 4. Guardar archivo corregido
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 5. Probar si ahora se puede importar
        print("\n🧪 Probando importación después de correcciones...")
        try:
            # Añadir directorio al path
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            
            # Eliminar módulo de la caché si existe
            if 'core.ui_detector' in sys.modules:
                del sys.modules['core.ui_detector']
            
            from core.ui_detector import UIDetector
            print("✅ ¡Importación exitosa después de correcciones!")
            
            # También guardar la versión corregida como el archivo principal
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Archivo corregido guardado: {file_path}")
            print(f"📦 Backup guardado: {backup_path}")
            
        except Exception as e:
            print(f"❌ Aún hay errores: {e}")
            print("\n🔄 Creando versión mínima funcional...")
            create_minimal_ui_detector()
            
    except Exception as e:
        print(f"❌ Error durante la corrección: {e}")
        create_minimal_ui_detector()

def create_minimal_ui_detector():
    """Crea una versión mínima y funcional de UIDetector"""
    
    minimal_code = '''"""
Clase UIDetector - Versión mínima para resolver errores de importación
"""
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class UIDetector:
    """Detección de elementos de la interfaz de Tibia"""
    
    def __init__(self, settings, ui_config):
        """
        Inicializa el detector de UI
        """
        self.settings = settings
        self.ui_config = ui_config
        logger.info("UIDetector inicializado (versión mínima)")
    
    def detect_health_bar(self, screenshot):
        """Detecta la barra de salud"""
        try:
            height, width = screenshot.shape[:2]
            return (width // 2 - 200, 50, 400, 20)  # Posición por defecto
        except Exception as e:
            logger.error(f"Error detectando HP: {e}")
            return None
    
    def detect_mana_bar(self, screenshot):
        """Detecta la barra de maná"""
        try:
            height, width = screenshot.shape[:2]
            return (width // 2 - 200, 75, 400, 20)  # Posición por defecto
        except Exception as e:
            logger.error(f"Error detectando MP: {e}")
            return None
    
    def detect_inventory(self, screenshot):
        """Detecta el inventario"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 300, height - 400, 280, 380)  # Posición por defecto
        except Exception as e:
            logger.error(f"Error detectando inventario: {e}")
            return None
    
    def detect_minimap(self, screenshot):
        """Detecta el minimapa"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 200, 50, 150, 150)  # Posición por defecto
        except Exception as e:
            logger.error(f"Error detectando minimapa: {e}")
            return None
    
    def detect_equipment_window(self, screenshot):
        """Detecta la ventana de equipo"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 500, height - 400, 180, 380)  # Posición por defecto
        except Exception as e:
            logger.error(f"Error detectando equipo: {e}")
            return None
    
    def detect_skills_window(self, screenshot):
        """Detecta la ventana de habilidades"""
        try:
            logger.warning("Detección de skills no implementada")
            return None
        except Exception as e:
            logger.error(f"Error detectando skills: {e}")
            return None
    
    def analyze_health_bar(self, bar_image):
        """Analiza barra de HP"""
        return 100.0  # Placeholder
    
    def analyze_mana_bar(self, bar_image):
        """Analiza barra de MP"""
        return 100.0  # Placeholder
'''
    
    file_path = "core/ui_detector.py"
    
    # Hacer backup del archivo actual
    backup_path = file_path + ".old"
    try:
        import shutil
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backup del archivo original: {backup_path}")
    except:
        pass
    
    # Guardar versión mínima
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(minimal_code)
    
    print(f"✅ Versión mínima creada: {file_path}")
    
    # Verificar que funciona
    try:
        if 'core.ui_detector' in sys.modules:
            del sys.modules['core.ui_detector']
        
        from core.ui_detector import UIDetector
        print("✅ ¡Versión mínima importada correctamente!")
        return True
    except Exception as e:
        print(f"❌ Error con versión mínima: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Diagnóstico de UIDetector...")
    check_ui_detector()
    print("\n" + "="*50 + "\n")
    fix_common_errors()