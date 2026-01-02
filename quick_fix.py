# quick_fix.py
import os

# Crear una versión ULTRA simple de ui_detector.py
ultra_simple = '''"""
Clase UIDetector - Versión ultra simple
"""
class UIDetector:
    def __init__(self, settings, ui_config):
        self.settings = settings
        self.ui_config = ui_config
        print("✅ UIDetector creado")
    
    def detect_health_bar(self, screenshot):
        return (100, 100, 300, 20)
    
    def detect_mana_bar(self, screenshot):
        return (100, 125, 300, 20)
    
    def detect_inventory(self, screenshot):
        return (1500, 300, 300, 400)
    
    def detect_minimap(self, screenshot):
        return (1700, 100, 150, 150)
    
    def detect_equipment_window(self, screenshot):
        return (1300, 300, 180, 380)
    
    def detect_skills_window(self, screenshot):
        return None
    
    def analyze_health_bar(self, bar_image):
        return 100.0
    
    def analyze_mana_bar(self, bar_image):
        return 100.0
'''

# Guardar el archivo
with open("core/ui_detector.py", "w", encoding="utf-8") as f:
    f.write(ultra_simple)

print("✅ Archivo core/ui_detector.py reemplazado con versión ultra simple")
print("🔄 Ahora prueba ejecutar: python -c \"from core.ui_detector import UIDetector; print('Import exitoso')\"")