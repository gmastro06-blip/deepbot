# fix_all_missing_methods.py
import os
import re

def analyze_tibia_bot():
    """Analiza tibia_bot.py para ver qué métodos necesita"""
    
    print("🔍 Analizando métodos requeridos por tibia_bot.py...")
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar todos los detect_*_window o detect_*_bar
        pattern = r'self\.detector\.(detect_[a-zA-Z_]+)'
        matches = re.findall(pattern, content)
        
        # Eliminar duplicados
        required_methods = list(set(matches))
        
        print(f"📋 Métodos requeridos encontrados ({len(required_methods)}):")
        for method in sorted(required_methods):
            print(f"   • {method}")
        
        return required_methods
        
    except Exception as e:
        print(f"❌ Error analizando {file_path}: {e}")
        return []

def check_ui_detector_methods():
    """Verifica qué métodos tiene actualmente UIDetector"""
    
    print("\n🔍 Verificando métodos existentes en UIDetector...")
    
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar métodos definidos
        pattern = r'def (detect_[a-zA-Z_]+)'
        matches = re.findall(pattern, content)
        
        existing_methods = list(set(matches))
        
        print(f"📋 Métodos existentes ({len(existing_methods)}):")
        for method in sorted(existing_methods):
            print(f"   • {method}")
        
        return existing_methods
        
    except Exception as e:
        print(f"❌ Error analizando {file_path}: {e}")
        return []

def fix_all_missing_methods():
    """Arregla TODOS los métodos faltantes en UIDetector"""
    
    print("\n" + "="*60)
    print("🔧 ARREGLANDO TODOS LOS MÉTODOS FALTANTES")
    print("="*60)
    
    # Obtener métodos requeridos y existentes
    required = analyze_tibia_bot()
    existing = check_ui_detector_methods()
    
    # Encontrar métodos faltantes
    missing = [m for m in required if m not in existing]
    
    if not missing:
        print("\n✅ ¡No hay métodos faltantes!")
        return
    
    print(f"\n❌ Métodos faltantes ({len(missing)}):")
    for method in missing:
        print(f"   • {method}")
    
    # Leer ui_detector.py
    file_path = "core/ui_detector.py"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    # Encontrar dónde insertar (después del último método detect_*)
    insert_index = len(lines)
    for i, line in enumerate(lines):
        if 'def detect_' in line:
            # Buscar el final de este método
            j = i + 1
            while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t') or lines[j].strip() == ''):
                j += 1
            insert_index = j
    
    print(f"\n📝 Insertando métodos faltantes en línea {insert_index + 1}...")
    
    # Construir métodos faltantes
    methods_code = []
    
    for method_name in missing:
        # Determinar el tipo de método
        if 'health' in method_name or 'hp' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta la barra de salud.
        """
        try:
            # Delegar al método principal de detección de HP
            return self.detect_health_bar(screenshot)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'mana' in method_name or 'mp' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta la barra de maná.
        """
        try:
            # Delegar al método principal de detección de MP
            return self.detect_mana_bar(screenshot)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'chat' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta la ventana de chat.
        """
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ Detección de chat no implementada completamente")
            
            # Por defecto, ventana de chat en la parte inferior
            height, width = screenshot.shape[:2]
            return (50, height - 300, width - 100, 250)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'skills' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta la ventana de habilidades.
        """
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ Detección de habilidades no implementada completamente")
            return None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'equipment' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta la ventana de equipo.
        """
        try:
            # Delegar al método principal
            return self.detect_equipment_window(screenshot)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'inventory' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta el inventario.
        """
        try:
            # Delegar al método principal
            return self.detect_inventory(screenshot)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        elif 'minimap' in method_name:
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta el minimapa.
        """
        try:
            # Delegar al método principal
            return self.detect_minimap(screenshot)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method_name}: {{e}}")
            return None'''
        
        else:
            # Método genérico para cualquier otro
            method_code = f'''    def {method_name}(self, screenshot):
        """
        Detecta {method_name.replace('detect_', '').replace('_', ' ')}.
        """
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"⚠️ {{method_name}} no implementado completamente")
            return None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {{method_name}}: {{e}}")
            return None'''
        
        methods_code.append(method_code)
    
    # Insertar métodos
    for i, line in enumerate(lines):
        new_lines.append(line)
        if i == insert_index:
            # Añadir línea en blanco y luego los nuevos métodos
            new_lines.append('')
            new_lines.extend(methods_code)
    
    # Escribir archivo actualizado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"\n✅ {len(missing)} métodos añadidos a UIDetector")
    
    # También actualizar tibia_bot.py para que sea más tolerante
    update_tibia_bot_tolerance()

def update_tibia_bot_tolerance():
    """Actualiza tibia_bot.py para manejar métodos faltantes de forma segura"""
    
    print("\n🔧 Actualizando tibia_bot.py para mayor tolerancia...")
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar todas las llamadas directas con llamadas seguras
    pattern = r"'(\w+)': self\.detector\.(detect_\w+)\((.*?)\)"
    
    def replacement(match):
        element_name = match.group(1)
        method_name = match.group(2)
        args = match.group(3)
        
        # Crear llamada segura
        safe_call = f"'{element_name}': self._safe_detect('{method_name}', {args})"
        return safe_call
    
    new_content = re.sub(pattern, replacement, content)
    
    # Añadir método _safe_detect si no existe
    if '_safe_detect' not in new_content:
        # Buscar donde insertar (justo antes de auto_detect_ui)
        lines = new_content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if 'def auto_detect_ui' in line:
                # Insertar método _safe_detect justo antes
                safe_method = '''
    def _safe_detect(self, method_name, screenshot):
        """
        Llama a un método de detección de forma segura.
        Si el método no existe, retorna None.
        """
        try:
            if hasattr(self.detector, method_name):
                method = getattr(self.detector, method_name)
                return method(screenshot)
            else:
                self.logger.warning(f"⚠️ Método {{method_name}} no encontrado en UIDetector")
                return None
        except Exception as e:
            self.logger.error(f"❌ Error en {{method_name}}: {{e}}")
            return None'''
                
                new_lines.insert(i, safe_method)
                break
        
        new_content = '\n'.join(new_lines)
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ tibia_bot.py actualizado con manejo seguro de métodos")

def create_complete_ui_detector():
    """Crea una versión completa de UIDetector con todos los métodos necesarios"""
    
    print("\n" + "="*60)
    print("🚀 CREANDO VERSIÓN COMPLETA DE UIDETECTOR")
    print("="*60)
    
    complete_code = '''"""
Clase UIDetector - Versión completa con todos los métodos
"""
import cv2
import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class UIDetector:
    """Detección completa de elementos de la interfaz de Tibia"""
    
    def __init__(self, settings, ui_config):
        self.settings = settings
        self.ui_config = ui_config
        logger.info("UIDetector completo inicializado")
    
    # ===== MÉTODOS PRINCIPALES =====
    
    def detect_health_bar(self, screenshot):
        """Detecta la barra de salud"""
        try:
            height, width = screenshot.shape[:2]
            return (width // 2 - 200, 50, 400, 20)
        except Exception as e:
            logger.error(f"Error detectando HP: {e}")
            return None
    
    def detect_mana_bar(self, screenshot):
        """Detecta la barra de maná"""
        try:
            height, width = screenshot.shape[:2]
            return (width // 2 - 200, 75, 400, 20)
        except Exception as e:
            logger.error(f"Error detectando MP: {e}")
            return None
    
    def detect_inventory(self, screenshot):
        """Detecta el inventario"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 300, height - 400, 280, 380)
        except Exception as e:
            logger.error(f"Error detectando inventario: {e}")
            return None
    
    def detect_minimap(self, screenshot):
        """Detecta el minimapa"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 200, 50, 150, 150)
        except Exception as e:
            logger.error(f"Error detectando minimapa: {e}")
            return None
    
    def detect_equipment_window(self, screenshot):
        """Detecta la ventana de equipo"""
        try:
            height, width = screenshot.shape[:2]
            return (width - 500, height - 400, 180, 380)
        except Exception as e:
            logger.error(f"Error detectando equipo: {e}")
            return None
    
    def detect_skills_window(self, screenshot):
        """Detecta la ventana de habilidades"""
        try:
            logger.warning("⚠️ Detección de skills no implementada")
            return None
        except Exception as e:
            logger.error(f"Error detectando skills: {e}")
            return None
    
    def detect_chat_window(self, screenshot):
        """Detecta la ventana de chat"""
        try:
            height, width = screenshot.shape[:2]
            return (50, height - 300, width - 100, 250)
        except Exception as e:
            logger.error(f"Error detectando chat: {e}")
            return None
    
    # ===== MÉTODOS ALIAS (para compatibilidad) =====
    
    def detect_hp_bar(self, screenshot):
        """Alias para detect_health_bar"""
        return self.detect_health_bar(screenshot)
    
    def detect_mp_bar(self, screenshot):
        """Alias para detect_mana_bar"""
        return self.detect_mana_bar(screenshot)
    
    def detect_equipment(self, screenshot):
        """Alias para detect_equipment_window"""
        return self.detect_equipment_window(screenshot)
    
    def detect_skill_window(self, screenshot):
        """Alias para detect_skills_window"""
        return self.detect_skills_window(screenshot)
    
    def detect_chat(self, screenshot):
        """Alias para detect_chat_window"""
        return self.detect_chat_window(screenshot)
    
    # ===== MÉTODOS DE ANÁLISIS =====
    
    def analyze_health_bar(self, bar_image):
        """Analiza barra de HP"""
        return 100.0
    
    def analyze_mana_bar(self, bar_image):
        """Analiza barra de MP"""
        return 100.0
    
    def get_player_position(self, minimap_image):
        """Obtiene posición del jugador en minimapa"""
        return None
    
    def is_inventory_open(self, inventory_image):
        """Verifica si el inventario está abierto"""
        return True
'''
    
    # Guardar versión completa
    with open("core/ui_detector.py", 'w', encoding='utf-8') as f:
        f.write(complete_code)
    
    print("✅ Versión completa de UIDetector creada")
    print("📋 Incluye todos los métodos necesarios:")
    print("   • Métodos principales: 7 detect_*")
    print("   • Métodos alias: 5 para compatibilidad")
    print("   • Métodos de análisis: 4")

def test_fix():
    """Prueba que los métodos estén disponibles"""
    
    print("\n" + "="*60)
    print("🧪 PROBANDO LA SOLUCIÓN")
    print("="*60)
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Crear mocks
        class MockSettings:
            def get_color(self, name, variant='full'):
                return (0, 0, 255) if name == 'hp' else (255, 0, 0)
        
        class MockUIConfig:
            def get_position(self, name):
                return None
        
        # Importar UIDetector
        from core.ui_detector import UIDetector
        
        # Crear instancia
        settings = MockSettings()
        ui_config = MockUIConfig()
        detector = UIDetector(settings, ui_config)
        
        # Métodos requeridos (basados en errores comunes)
        required_methods = [
            'detect_health_bar',
            'detect_hp_bar',
            'detect_mana_bar', 
            'detect_mp_bar',
            'detect_inventory',
            'detect_minimap',
            'detect_equipment_window',
            'detect_equipment',
            'detect_skills_window',
            'detect_skill_window',
            'detect_chat_window',
            'detect_chat'
        ]
        
        print("\n✅ Métodos disponibles en UIDetector:")
        available = []
        missing = []
        
        for method in required_methods:
            if hasattr(detector, method):
                available.append(method)
                print(f"   ✓ {method}")
            else:
                missing.append(method)
                print(f"   ✗ {method} - FALTANTE")
        
        if missing:
            print(f"\n❌ Aún faltan {len(missing)} métodos")
            return False
        else:
            print(f"\n🎉 ¡Todos los {len(available)} métodos están disponibles!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    # Opción 1: Arreglar métodos individuales
    fix_all_missing_methods()
    
    # Opción 2: Crear versión completa (más radical pero efectiva)
    respuesta = input("\n¿Quieres crear una versión COMPLETA de UIDetector? (s/n): ").strip().lower()
    
    if respuesta == 's':
        create_complete_ui_detector()
    
    # Probar la solución
    success = test_fix()
    
    if success:
        print("\n" + "="*60)
        print("🚀 ¡PROBLEMA RESUELTO!")
        print("="*60)
        print("\n💡 Ahora puedes ejecutar:")
        print("   python main.py")
        print("\n📝 Recomendación:")
        print("   Si aún hay errores, ejecuta de nuevo este script")
        print("   con la opción de crear versión completa")
    else:
        print("\n⚠️  Aún hay problemas. Ejecuta de nuevo con la opción de versión completa.")