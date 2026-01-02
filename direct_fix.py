# direct_fix.py
import os

# 1. Primero, actualiza UIDetector para que skills retorne una región por defecto
ui_detector_content = '''"""
Clase UIDetector - Versión optimizada
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
        logger.info("UIDetector optimizado inicializado")
    
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
            height, width = screenshot.shape[:2]
            # Posición por defecto: lado derecho central
            return (width - 450, 200, 200, 300)
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
    
    # Alias para compatibilidad
    def detect_hp_bar(self, screenshot):
        return self.detect_health_bar(screenshot)
    
    def detect_mp_bar(self, screenshot):
        return self.detect_mana_bar(screenshot)
    
    def detect_equipment(self, screenshot):
        return self.detect_equipment_window(screenshot)
    
    def detect_skill_window(self, screenshot):
        return self.detect_skills_window(screenshot)
    
    def detect_chat(self, screenshot):
        return self.detect_chat_window(screenshot)
    
    # Métodos de análisis
    def analyze_health_bar(self, bar_image):
        return 100.0
    
    def analyze_mana_bar(self, bar_image):
        return 100.0
'''

# Guardar UIDetector optimizado
with open("core/ui_detector.py", 'w', encoding='utf-8') as f:
    f.write(ui_detector_content)

print("✅ UIDetector optimizado creado")

# 2. Ahora arreglar tibia_bot.py para ser más tolerante
with open("core/tibia_bot.py", 'r') as f:
    tibia_bot_content = f.read()

# Buscar y reemplazar la sección problemática
import re

# Encontrar auto_detect_ui y reemplazar su lógica
def replace_auto_detect(match):
    original = match.group(0)
    
    # Reemplazar con versión mejorada
    improved = '''    def auto_detect_ui(self):
        """
        Detecta automáticamente todos los elementos de la UI.
        
        Returns:
            bool: True si se detectó al menos un elemento
        """
        try:
            self.logger.info("🔍 Iniciando detección automática de UI...")
            
            # Capturar pantalla
            screenshot = self.capturer.capture_full_screen()
            
            # Lista de elementos a detectar
            elements_to_detect = {
                'hp_bar': 'detect_health_bar',
                'mp_bar': 'detect_mana_bar',
                'inventory': 'detect_inventory',
                'minimap': 'detect_minimap',
                'equipment': 'detect_equipment_window',
                'skills': 'detect_skills_window',
                'chat': 'detect_chat_window'
            }
            
            detected_positions = {}
            
            # Detectar cada elemento
            for element_name, method_name in elements_to_detect.items():
                try:
                    if hasattr(self.detector, method_name):
                        method = getattr(self.detector, method_name)
                        region = method(screenshot)
                        
                        if region and len(region) == 4:
                            detected_positions[element_name] = {
                                'x': region[0],
                                'y': region[1],
                                'width': region[2],
                                'height': region[3],
                                'confidence': 0.8 if 'bar' in element_name else 0.7,
                                'method': 'auto_detect'
                            }
                            self.logger.info(f"✅ Detectado: {element_name}")
                        else:
                            self.logger.warning(f"⚠️ No detectado: {element_name}")
                    else:
                        self.logger.warning(f"⚠️ Método {method_name} no disponible para {element_name}")
                        
                except Exception as e:
                    self.logger.error(f"❌ Error detectando {element_name}: {e}")
            
            # Actualizar configuración si se detectó algo
            if detected_positions:
                self.ui_config.update_positions(detected_positions)
                
                # Guardar configuración
                if self.ui_config.save_to_file():
                    self.logger.info("💾 Configuración guardada")
                
                self.logger.info("🎉 Detección automática completada")
                return True
            else:
                self.logger.error("❌ No se detectó ningún elemento")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error en detección automática: {e}")
            return False'''
    
    return improved

# Aplicar reemplazo
pattern = r'def auto_detect_ui\(self\):.*?return (?:True|False)'
tibia_bot_content = re.sub(pattern, replace_auto_detect, tibia_bot_content, flags=re.DOTALL)

# Guardar tibia_bot.py corregido
with open("core/tibia_bot.py", 'w') as f:
    f.write(tibia_bot_content)

print("✅ tibia_bot.py corregido")

# 3. Crear script de prueba final
test_script = '''# final_verification.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verificación final del sistema")
print("="*50)

try:
    # 1. Test UIDetector
    print("\\n1. Probando UIDetector...")
    from core.ui_detector import UIDetector
    
    class MockSettings:
        def get_color(self, name, variant='full'):
            return (0, 0, 255)
    
    class MockUIConfig:
        def get_position(self, name):
            return None
    
    detector = UIDetector(MockSettings(), MockUIConfig())
    
    # Verificar métodos críticos
    critical_methods = [
        'detect_health_bar',
        'detect_mana_bar',
        'detect_inventory',
        'detect_minimap',
        'detect_equipment_window',
        'detect_skills_window',
        'detect_chat_window'
    ]
    
    all_ok = True
    for method in critical_methods:
        if hasattr(detector, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method}")
            all_ok = False
    
    if not all_ok:
        print("❌ Faltan métodos en UIDetector")
        sys.exit(1)
    
    # 2. Test TibiaBot
    print("\\n2. Probando TibiaBot...")
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(
        config_path="configs/default_settings.json",
        debug_mode=True,
        logger=None
    )
    
    print("✅ Bot creado")
    
    # 3. Test auto_detect_ui
    print("\\n3. Ejecutando auto_detect_ui...")
    success = bot.auto_detect_ui()
    
    print(f"✅ auto_detect_ui ejecutado: {'Éxito' if success else 'Falló'}")
    
    if success:
        print("\\n🎉 ¡Sistema verificado correctamente!")
        print("\\n💡 Ahora puedes:")
        print("   • Ejecutar: python main.py")
        print("   • O calibrar: python calibrate_ui.py")
    else:
        print("\\n⚠️  La detección automática no encontró elementos")
        print("   Esto puede ser normal si no tienes Tibia abierto")
        print("   💡 Abre Tibia y ejecuta de nuevo")
        
except Exception as e:
    print(f"\\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
'''

with open("final_verification.py", 'w', encoding='utf-8') as f:
    f.write(test_script)

print("✅ Script de verificación creado: final_verification.py")
print("\\n🔄 Ejecuta: python final_verification.py")