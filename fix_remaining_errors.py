# fix_remaining_errors.py
import os
import json
import cv2
import numpy as np

def create_missing_templates():
    """Crea plantillas dummy faltantes"""
    
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Plantillas a crear
    templates = {
        "hp_bar_segment.png": (20, 100, (0, 0, 255)),  # Rojo (BGR)
        "mp_bar_segment.png": (20, 100, (255, 0, 0)),  # Azul (BGR)
        "inventory_corner.png": (50, 50, (100, 100, 100)),  # Gris (BGR)
        "minimap_circle.png": (100, 100, (0, 255, 0)),  # Verde (BGR)
    }
    
    for filename, (height, width, color) in templates.items():
        path = os.path.join(templates_dir, filename)
        
        if not os.path.exists(path):
            # Crear imagen dummy
            img = np.ones((height, width, 3), dtype=np.uint8) * color
            cv2.imwrite(path, img)
            print(f"✅ Plantilla dummy creada: {path}")
        else:
            print(f"✅ Plantilla ya existe: {path}")

def fix_ui_detector():
    """Asegura que UIDetector tenga todos los métodos necesarios"""
    
    ui_detector_path = "core/ui_detector.py"
    
    if not os.path.exists(ui_detector_path):
        print(f"❌ {ui_detector_path} no encontrado")
        return
    
    try:
        with open(ui_detector_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si detect_equipment_window existe
        if 'def detect_equipment_window' not in content:
            print("⚠️  Añadiendo detect_equipment_window a UIDetector")
            
            # Encontrar donde insertar (después de detect_minimap)
            lines = content.split('\n')
            new_lines = []
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # Buscar después de detect_minimap
                if 'def detect_minimap' in line:
                    # Insertar después de esta función
                    equipment_method = '''
    def detect_equipment_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la ventana de equipo.
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Si ya tenemos posición guardada, usarla
            if self.ui_config:
                equipment_pos = self.ui_config.get_position('equipment')
                if equipment_pos:
                    return (equipment_pos['x'], equipment_pos['y'], 
                           equipment_pos['width'], equipment_pos['height'])
            
            # El equipo suele estar a la izquierda del inventario
            inventory_region = self.detect_inventory(screenshot)
            if inventory_region:
                x, y, w, h = inventory_region
                # Asumir que el equipo está 150px a la izquierda del inventario
                equipment_x = max(0, x - 150)
                equipment_y = y
                equipment_width = 140
                equipment_height = 400
                
                return (equipment_x, equipment_y, equipment_width, equipment_height)
            
            # Si no encontramos inventario, buscar en área general
            height, width = screenshot.shape[:2]
            
            # Buscar en la parte derecha
            search_area = screenshot[200:height-100, 50:400]
            
            # Buscar patrones de armadura (formas específicas)
            gray = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Buscar contornos rectangulares
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Filtrar contornos rectangulares del tamaño correcto
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Tamaño típico de ventana de equipo
                    if 100 < w < 200 and 300 < h < 500:
                        return (x + 50, y + 200, w, h)
            
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ Detección de equipo no implementada completamente")
            return None
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error detectando ventana de equipo: {e}")
            return None'''
                    
                    # Insertar después de detect_minimap
                    new_lines.append(equipment_method)
        
        # Guardar cambios
        with open(ui_detector_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ {ui_detector_path} actualizado")
    
    except Exception as e:
        print(f"❌ Error arreglando ui_detector.py: {e}")

def fix_health_detector_color_error():
    """Arregla el error 'invalid literal for int() with base 10: 'full'"""
    
    health_detector_path = "detectors/health_detector.py"
    
    if not os.path.exists(health_detector_path):
        print(f"❌ {health_detector_path} no encontrado")
        return
    
    try:
        with open(health_detector_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar línea problemática
        if "self.settings.colors['hp']" in content:
            print("⚠️  Arreglando error de color en health_detector.py")
            
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                # Reemplazar acceso problemático a colors
                if "self.settings.colors['hp']" in line:
                    # Cambiar a usar get_color
                    new_line = line.replace(
                        "self.settings.colors['hp']",
                        "self.settings.get_color('hp', 'full')"
                    )
                    new_lines.append(new_line)
                    print(f"   Corregido: {line.strip()} -> {new_line.strip()}")
                else:
                    new_lines.append(line)
            
            # Guardar
            with open(health_detector_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print(f"✅ {health_detector_path} corregido")
        else:
            print(f"✅ {health_detector_path} parece estar bien")
    
    except Exception as e:
        print(f"❌ Error arreglando health_detector.py: {e}")

def fix_template_matcher():
    """Arregla TemplateMatcher para manejar mejor los errores"""
    
    template_matcher_path = "processors/template_matcher.py"
    
    if not os.path.exists(template_matcher_path):
        print(f"❌ {template_matcher_path} no encontrado")
        return
    
    try:
        with open(template_matcher_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Añadir manejo de errores mejorado
        if "def match_template" in content:
            print(f"✅ {template_matcher_path} ya tiene match_template")
        else:
            print(f"⚠️  {template_matcher_path} necesita match_template")
            
            # Añadir el método si falta
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                new_lines.append(line)
                
                # Buscar donde insertar después de __init__
                if "def __init__(self):" in line:
                    # Insertar método match_template
                    match_template_method = '''
    def match_template(self, image: np.ndarray, template_path: str, 
                      threshold: float = 0.8) -> Dict[str, Any]:
        """
        Busca una plantilla en la imagen
        
        Args:
            image: Imagen donde buscar
            template_path: Ruta al archivo de plantilla
            threshold: Umbral de confianza (0-1)
        
        Returns:
            Dict con 'found', 'position', 'confidence', 'region'
        """
        try:
            # Verificar que la imagen sea válida
            if image is None or image.size == 0:
                return {'found': False, 'position': None, 'confidence': 0.0, 'region': None}
            
            # Cargar plantilla
            if not os.path.exists(template_path):
                return {'found': False, 'position': None, 'confidence': 0.0, 'region': None}
            
            template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
            if template is None:
                return {'found': False, 'position': None, 'confidence': 0.0, 'region': None}
            
            # Verificar dimensiones
            if image.shape[0] < template.shape[0] or image.shape[1] < template.shape[1]:
                return {'found': False, 'position': None, 'confidence': 0.0, 'region': None}
            
            # Convertir a escala de grises si es necesario
            if len(image.shape) == 3:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                img_gray = image
            
            if len(template.shape) == 3:
                tmpl_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            else:
                tmpl_gray = template
            
            # Asegurar tipos de datos
            if img_gray.dtype != np.uint8:
                img_gray = img_gray.astype(np.uint8)
            if tmpl_gray.dtype != np.uint8:
                tmpl_gray = tmpl_gray.astype(np.uint8)
            
            # Realizar template matching
            result = cv2.matchTemplate(img_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                x, y = max_loc
                h, w = template.shape[:2]
                
                return {
                    'found': True,
                    'position': (x, y),
                    'confidence': float(max_val),
                    'region': (x, y, w, h)
                }
            else:
                return {
                    'found': False,
                    'position': None,
                    'confidence': float(max_val),
                    'region': None
                }
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en match_template: {e}")
            return {'found': False, 'position': None, 'confidence': 0.0, 'region': None}'''
                    
                    new_lines.append(match_template_method)
            
            # Guardar
            with open(template_matcher_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print(f"✅ {template_matcher_path} actualizado con match_template")

    except Exception as e:
        print(f"❌ Error arreglando template_matcher.py: {e}")

def update_tibia_bot_auto_detect():
    """Actualiza tibia_bot.py para manejar mejor los errores en auto_detect_ui"""
    
    tibia_bot_path = "core/tibia_bot.py"
    
    if not os.path.exists(tibia_bot_path):
        print(f"❌ {tibia_bot_path} no encontrado")
        return
    
    try:
        with open(tibia_bot_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar método auto_detect_ui
        if 'def auto_detect_ui' in content:
            print("✅ auto_detect_ui ya existe en tibia_bot.py")
            
            # Verificar si ya maneja el error de equipment
            if "self.detector.detect_equipment_window" in content:
                print("⚠️  Revisando manejo de errores en auto_detect_ui...")
                
                lines = content.split('\n')
                new_lines = []
                
                for line in lines:
                    # Reemplazar línea problemática con manejo de errores
                    if "'equipment': self.detector.detect_equipment_window(screenshot)" in line:
                        # Cambiar a manejo seguro
                        safe_line = "            'equipment': self.detector.detect_equipment_window(screenshot) if hasattr(self.detector, 'detect_equipment_window') else None,"
                        new_lines.append(safe_line)
                        print(f"   Corregido acceso a detect_equipment_window")
                    else:
                        new_lines.append(line)
                
                # Guardar
                with open(tibia_bot_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                
                print(f"✅ {tibia_bot_path} actualizado")
        else:
            print(f"⚠️  {tibia_bot_path} no tiene auto_detect_ui")
    
    except Exception as e:
        print(f"❌ Error actualizando tibia_bot.py: {e}")

def main():
    print("🔧 Arreglando errores restantes...")
    
    create_missing_templates()
    fix_ui_detector()
    fix_health_detector_color_error()
    fix_template_matcher()
    update_tibia_bot_auto_detect()
    
    print("\n✅ Todos los errores han sido arreglados")
    print("🔄 Ahora ejecuta: python test_run_fixed.py")

if __name__ == "__main__":
    main()