# replace_ui_detector.py
import os

def replace_ui_detector():
    """Reemplaza ui_detector.py con una versión corregida"""
    
    backup_path = "core/ui_detector.py.backup"
    original_path = "core/ui_detector.py"
    
    # Hacer backup
    if os.path.exists(original_path):
        import shutil
        shutil.copy2(original_path, backup_path)
        print(f"✅ Backup creado en: {backup_path}")
    
    # Crear la versión corregida
    corrected_code = '''"""
Clase UIDetector - Detección de elementos de la interfaz de usuario
"""
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import pytesseract
import logging

from config.settings import Settings
from config.ui_config import UIConfig
from detectors.health_detector import HealthDetector
from detectors.mana_detector import ManaDetector
from detectors.inventory_detector import InventoryDetector
from detectors.minimap_detector import MinimapDetector
from processors.image_processor import ImageProcessor
from processors.color_detector import ColorDetector
from processors.template_matcher import TemplateMatcher

logger = logging.getLogger(__name__)

@dataclass
class DetectionResult:
    """Resultado de una detección"""
    element_name: str
    confidence: float
    region: Optional[Tuple[int, int, int, int]] = None
    data: Optional[Any] = None
    method: str = "unknown"
    
    @property
    def success(self) -> bool:
        """Indica si la detección fue exitosa"""
        return self.confidence >= 0.7 and self.region is not None
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return {
            'element': self.element_name,
            'confidence': self.confidence,
            'region': self.region,
            'method': self.method,
            'success': self.success
        }

class UIDetector:
    """Detección de elementos de la interfaz de Tibia"""
    
    def __init__(self, settings: Settings, ui_config: UIConfig):
        """
        Inicializa el detector de UI
        
        Args:
            settings: Configuración del bot
            ui_config: Configuración de la UI
        """
        self.settings = settings
        self.ui_config = ui_config
        
        # Inicializar detectores específicos
        self.health_detector = HealthDetector(settings)
        self.mana_detector = ManaDetector(settings)
        self.inventory_detector = InventoryDetector(settings)
        self.minimap_detector = MinimapDetector(settings)
        
        # Inicializar procesadores
        self.image_processor = ImageProcessor()
        self.color_detector = ColorDetector(settings)
        self.template_matcher = TemplateMatcher()
        
        # Configurar Tesseract si está disponible
        try:
            pytesseract.get_tesseract_version()
            self.ocr_available = True
        except:
            self.ocr_available = False
            logger.warning("Tesseract OCR no disponible. La detección de texto será limitada.")
    
    def detect_health_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la barra de salud (HP)
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Método 1: Usar detector específico
            result = self.health_detector.detect(screenshot)
            if result and result.confidence > 0.8:
                return result.region
            
            # Método 2: Búsqueda por color
            hp_color = self.settings.get_color('hp', 'full')
            
            regions = self.color_detector.find_color_regions(
                screenshot, hp_color, 
                min_width=150, max_width=400,
                min_height=10, max_height=30
            )
            
            if regions:
                # Seleccionar la región más probable (la más larga y delgada)
                best_region = max(regions, key=lambda r: r[2] / max(r[3], 1))
                return best_region
            
            # Método 3: Búsqueda por plantilla
            template_path = "templates/hp_bar_segment.png"
            template_result = self.template_matcher.match_template(screenshot, template_path)
            if template_result and template_result.get('found'):
                return template_result.get('region')
            
            return None
            
        except Exception as e:
            logger.error(f"Error detectando barra de HP: {e}")
            return None
    
    def detect_mana_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la barra de maná (MP)
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Método 1: Usar detector específico
            result = self.mana_detector.detect(screenshot)
            if result and result.confidence > 0.8:
                return result.region
            
            # Método 2: Buscar cerca de la barra de HP
            hp_region = self.ui_config.get_position('hp_bar')
            if hp_region:
                # La barra de MP suele estar justo debajo de la de HP
                search_y = hp_region['y'] + hp_region['height'] + 5
                search_height = 30
                
                # Crear región de búsqueda
                search_region = screenshot[search_y:search_y+search_height, :]
                
                # Buscar color azul
                mp_color = self.settings.get_color('mp', 'full')
                
                mp_regions = self.color_detector.find_color_regions(
                    search_region, mp_color,
                    min_width=150, max_width=400,
                    min_height=10, max_height=20
                )
                
                if mp_regions:
                    # Ajustar coordenadas a la pantalla completa
                    x, y, w, h = mp_regions[0]
                    return (x, y + search_y, w, h)
            
            # Método 3: Búsqueda por plantilla
            template_path = "templates/mp_bar_segment.png"
            template_result = self.template_matcher.match_template(screenshot, template_path)
            if template_result and template_result.get('found'):
                return template_result.get('region')
            
            return None
            
        except Exception as e:
            logger.error(f"Error detectando barra de MP: {e}")
            return None
    
    def detect_inventory(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la ventana del inventario
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Método 1: Usar detector específico
            result = self.inventory_detector.detect(screenshot)
            if result and result.confidence > 0.7:
                return result.region
            
            # Método 2: Buscar en esquina derecha (posición común)
            height, width = screenshot.shape[:2]
            
            # El inventario suele estar en la parte derecha-central
            right_region = screenshot[200:height-100, width-400:width-50]
            
            # Buscar patrones de slots (cuadrícula)
            gray = cv2.cvtColor(right_region, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Buscar líneas horizontales y verticales
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, 
                                   minLineLength=30, maxLineGap=10)
            
            if lines is not None:
                # Agrupar líneas por posición
                horizontal_lines = []
                vertical_lines = []
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    
                    # Determinar si es línea horizontal o vertical
                    if abs(y2 - y1) < abs(x2 - x1):
                        # Más horizontal que vertical
                        horizontal_lines.append((min(y1, y2), max(y1, y2)))
                    else:
                        vertical_lines.append((min(x1, x2), max(x1, x2)))
                
                # Si encontramos varias líneas paralelas, podría ser el inventario
                if len(horizontal_lines) >= 3 and len(vertical_lines) >= 3:
                    # Calcular bounding box aproximado
                    min_y = min([h[0] for h in horizontal_lines])
                    max_y = max([h[1] for h in horizontal_lines])
                    min_x = min([v[0] for v in vertical_lines])
                    max_x = max([v[1] for v in vertical_lines])
                    
                    # Ajustar coordenadas a la pantalla completa
                    return (min_x + (width-400), min_y + 200, 
                            max_x - min_x, max_y - min_y)
            
            # Método 3: Buscar por plantilla de esquina
            template_path = "templates/inventory_corner.png"
            template_result = self.template_matcher.match_template(screenshot, template_path)
            if template_result and template_result.get('found'):
                region = template_result.get('region')
                if region:
                    x, y, w, h = region
                    # El inventario es más grande que la esquina
                    return (x, y, 300, 400)
            
            return None
            
        except Exception as e:
            logger.error(f"Error detectando inventario: {e}")
            return None
    
    def detect_minimap(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta el minimapa
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Método 1: Usar detector específico
            result = self.minimap_detector.detect(screenshot)
            if result and result.confidence > 0.7:
                return result.region
            
            # Método 2: Buscar área circular en esquina superior derecha
            height, width = screenshot.shape[:2]
            
            # Buscar en esquina superior derecha
            search_region = screenshot[50:300, width-350:width-50]
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(search_region, cv2.COLOR_BGR2GRAY)
            
            # Buscar círculos
            circles = cv2.HoughCircles(
                gray, cv2.HOUGH_GRADIENT, 
                dp=1, minDist=50,
                param1=50, param2=30,
                minRadius=80, maxRadius=120
            )
            
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for circle in circles[0, :]:
                    x, y, r = circle
                    
                    # Ajustar coordenadas a la pantalla completa
                    x += width - 350
                    y += 50
                    
                    return (x - r, y - r, r * 2, r * 2)
            
            # Método 3: Buscar por color (verde/bosque)
            # El minimapa suele tener tonos verdes y marrones
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Rango para verdes (bosque)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Encontrar contornos grandes
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Filtrar por tamaño y posición
                large_contours = [c for c in contours 
                                 if cv2.contourArea(c) > 10000]
                
                for contour in large_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Verificar que esté en esquina superior derecha
                    if x > width * 0.6 and y < height * 0.4:
                        # Verificar que sea aproximadamente cuadrado/circular
                        aspect_ratio = w / h
                        if 0.7 < aspect_ratio < 1.3:
                            return (x, y, w, h)
            
            return None
            
        except Exception as e:
            logger.error(f"Error detectando minimapa: {e}")
            return None
    
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
            
            logger.warning("⚠️ Detección de equipo no implementada completamente")
            return None
            
        except Exception as e:
            logger.error(f"Error detectando ventana de equipo: {e}")
            return None
    
    def detect_skills_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la ventana de habilidades.
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Si ya tenemos posición guardada, usarla
            if self.ui_config:
                skills_pos = self.ui_config.get_position('skills')
                if skills_pos:
                    return (skills_pos['x'], skills_pos['y'], 
                           skills_pos['width'], skills_pos['height'])
            
            # Por ahora, retornar None ya que no está implementado
            logger.warning("⚠️ Detección de ventana de habilidades no implementada")
            return None
            
        except Exception as e:
            logger.error(f"Error detectando ventana de habilidades: {e}")
            return None
    
    def analyze_health_bar(self, bar_image: np.ndarray) -> float:
        """
        Analiza una imagen de barra de HP y devuelve el porcentaje
        
        Args:
            bar_image: Imagen de la barra de HP
        
        Returns:
            Porcentaje de HP (0-100)
        """
        return self.health_detector.analyze(bar_image)
    
    def analyze_mana_bar(self, bar_image: np.ndarray) -> float:
        """
        Analiza una imagen de barra de MP y devuelve el porcentaje
        
        Args:
            bar_image: Imagen de la barra de MP
        
        Returns:
            Porcentaje de MP (0-100)
        """
        return self.mana_detector.analyze(bar_image)
    
    def is_inventory_open(self, inventory_image: np.ndarray) -> bool:
        """
        Determina si el inventario está abierto
        
        Args:
            inventory_image: Imagen de la región del inventario
        
        Returns:
            True si el inventario está abierto
        """
        return self.inventory_detector.is_open(inventory_image)
    
    def get_player_position(self, minimap_image: np.ndarray) -> Optional[Dict[str, int]]:
        """
        Obtiene la posición del jugador en el minimapa
        
        Args:
            minimap_image: Imagen del minimapa
        
        Returns:
            Diccionario con coordenadas x, y o None
        """
        return self.minimap_detector.get_player_position(minimap_image)
    
    def detect_all_elements(self, screenshot: np.ndarray) -> Dict[str, DetectionResult]:
        """
        Detecta todos los elementos de la UI
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Diccionario con resultados de detección
        """
        elements = {
            'hp_bar': self.detect_health_bar,
            'mp_bar': self.detect_mana_bar,
            'inventory': self.detect_inventory,
            'minimap': self.detect_minimap,
            'equipment': self.detect_equipment_window,
            'skills': self.detect_skills_window
        }
        
        results = {}
        
        for name, detector_func in elements.items():
            try:
                region = detector_func(screenshot)
                if region:
                    confidence = self._calculate_confidence(region, name)
                    results[name] = DetectionResult(
                        element_name=name,
                        confidence=confidence,
                        region=region,
                        method=detector_func.__name__
                    )
                else:
                    results[name] = DetectionResult(
                        element_name=name,
                        confidence=0.0,
                        region=None,
                        method=detector_func.__name__
                    )
            except Exception as e:
                logger.error(f"Error detectando {name}: {e}")
                results[name] = DetectionResult(
                    element_name=name,
                    confidence=0.0,
                    region=None,
                    method="error"
                )
        
        return results
    
    def _calculate_confidence(self, region: Tuple[int, int, int, int], 
                            element_type: str) -> float:
        """
        Calcula la confianza de una detección
        
        Args:
            region: Región detectada
            element_type: Tipo de elemento
        
        Returns:
            Nivel de confianza (0-1)
        """
        x, y, w, h = region
        
        # Verificar tamaño razonable
        if w <= 0 or h <= 0:
            return 0.0
        
        # Confianza basada en proporciones esperadas
        if element_type in ['hp_bar', 'mp_bar']:
            # Las barras son largas y delgadas
            aspect_ratio = w / h
            if 5 < aspect_ratio < 20:
                return 0.9
            elif 3 < aspect_ratio < 30:
                return 0.7
            else:
                return 0.4
        
        elif element_type == 'minimap':
            # El minimapa es aproximadamente cuadrado
            aspect_ratio = w / h
            if 0.8 < aspect_ratio < 1.2:
                return 0.9
            elif 0.6 < aspect_ratio < 1.5:
                return 0.7
            else:
                return 0.4
        
        elif element_type in ['inventory', 'equipment', 'skills']:
            # El inventario/equipo/habilidades es rectangular
            aspect_ratio = w / h
            if 0.6 < aspect_ratio < 1.0:
                return 0.8
            else:
                return 0.5
        
        return 0.5
    
    def calibrate_detector(self, screenshot: np.ndarray, 
                          element_name: str, 
                          manual_region: Tuple[int, int, int, int]):
        """
        Calibra el detector para un elemento específico
        
        Args:
            screenshot: Captura de pantalla
            element_name: Nombre del elemento
            manual_region: Región seleccionada manualmente
        """
        # Extraer la región
        x, y, w, h = manual_region
        element_image = screenshot[y:y+h, x:x+w]
        
        # Guardar como plantilla para futuras detecciones
        import os
        template_path = f"templates/{element_name}_calibrated.png"
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        cv2.imwrite(template_path, element_image)
        
        logger.info(f"Calibración completada para {element_name}")
        logger.info(f"Plantilla guardada en: {template_path}")'''
    
    # Escribir el archivo corregido
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(corrected_code)
    
    print(f"✅ {original_path} reemplazado con versión corregida")
    print("📋 Métodos incluidos:")
    print("   • detect_health_bar")
    print("   • detect_mana_bar")
    print("   • detect_inventory")
    print("   • detect_minimap")
    print("   • detect_equipment_window")
    print("   • detect_skills_window")

if __name__ == "__main__":
    replace_ui_detector()