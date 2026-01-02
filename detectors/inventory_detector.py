"""
Clase InventoryDetector - Detección de ventana de inventario
"""
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

from config.settings import Settings
from processors.color_detector import ColorDetector
from processors.image_processor import ImageProcessor
from processors.template_matcher import TemplateMatcher

@dataclass
class DetectionResult:
    """Resultado de detección de inventario"""
    confidence: float
    region: Optional[Tuple[int, int, int, int]]
    is_open: Optional[bool]
    method: str

class InventoryDetector:
    """Detector especializado para ventana de inventario"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.color_detector = ColorDetector(settings)
        self.image_processor = ImageProcessor()
        self.template_matcher = TemplateMatcher()
    
    def detect(self, screenshot: np.ndarray) -> DetectionResult:
        """
        Detecta la ventana del inventario
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Resultado de la detección
        """
        # Método 1: Por plantilla (esquina del inventario)
        template_result = self._detect_by_template(screenshot)
        if template_result.confidence > 0.8:
            return template_result
        
        # Método 2: Por color y patrones
        color_result = self._detect_by_color_pattern(screenshot)
        if color_result.confidence > 0.7:
            return color_result
        
        # Método 3: Buscar en posición común (esquina superior derecha)
        position_result = self._detect_by_position(screenshot)
        return position_result
    
    def _detect_by_template(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por plantilla de esquina de inventario"""
        try:
            template_path = "templates/inventory_corner.png"
            result = self.template_matcher.match(screenshot, template_path, threshold=0.7)
            
            if result:
                x, y, w, h = result
                # El inventario completo es más grande que la esquina
                inventory_width = 300
                inventory_height = 400
                region = (x, y, inventory_width, inventory_height)
                
                # Verificar si está abierto
                inventory_img = screenshot[y:y+inventory_height, x:x+inventory_width]
                is_open = self._check_if_open(inventory_img)
                
                return DetectionResult(
                    confidence=0.9,
                    region=region,
                    is_open=is_open,
                    method="template"
                )
            
            return DetectionResult(0.0, None, None, "template")
            
        except Exception as e:
            print(f"Error en detección por plantilla: {e}")
            return DetectionResult(0.0, None, None, "template_error")
    
    def _detect_by_color_pattern(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por patrones de color y bordes"""
        try:
            height, width = screenshot.shape[:2]
            
            # Buscar en la parte derecha de la pantalla (donde suele estar el inventario)
            right_region = screenshot[200:height-100, width-400:width-50]
            
            if right_region.size == 0:
                return DetectionResult(0.0, None, None, "color_pattern")
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(right_region, cv2.COLOR_BGR2GRAY)
            
            # Buscar bordes
            edges = cv2.Canny(gray, 50, 150)
            
            # Buscar líneas (bordes de slots del inventario)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, 
                                   minLineLength=30, maxLineGap=10)
            
            if lines is not None and len(lines) > 5:
                # Encontrar límites de las líneas
                min_x = width
                max_x = 0
                min_y = height
                max_y = 0
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    min_x = min(min_x, x1, x2)
                    max_x = max(max_x, x1, x2)
                    min_y = min(min_y, y1, y2)
                    max_y = max(max_y, y1, y2)
                
                # Ajustar coordenadas a la pantalla completa
                region_x = min_x + (width - 400)
                region_y = min_y + 200
                region_w = max_x - min_x
                region_h = max_y - min_y
                
                region = (region_x, region_y, region_w, region_h)
                
                # Verificar si está abierto
                inventory_img = screenshot[region_y:region_y+region_h, region_x:region_x+region_w]
                is_open = self._check_if_open(inventory_img)
                
                return DetectionResult(
                    confidence=0.7,
                    region=region,
                    is_open=is_open,
                    method="color_pattern"
                )
            
            return DetectionResult(0.0, None, None, "color_pattern")
            
        except Exception as e:
            print(f"Error en detección por patrón: {e}")
            return DetectionResult(0.0, None, None, "pattern_error")
    
    def _detect_by_position(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por posición común del inventario"""
        try:
            height, width = screenshot.shape[:2]
            
            # Posición común del inventario (esquina superior derecha)
            region_x = width - 350
            region_y = 200
            region_w = 300
            region_h = 400
            
            region = (region_x, region_y, region_w, region_h)
            
            # Verificar si hay contenido en esta región
            inventory_img = screenshot[region_y:region_y+region_h, region_x:region_x+region_w]
            is_open = self._check_if_open(inventory_img)
            
            # Calcular confianza basada en contenido
            confidence = 0.5 if is_open else 0.3
            
            return DetectionResult(
                confidence=confidence,
                region=region,
                is_open=is_open,
                method="position"
            )
            
        except Exception as e:
            print(f"Error en detección por posición: {e}")
            return DetectionResult(0.0, None, None, "position_error")
    
    def _check_if_open(self, inventory_image: np.ndarray) -> bool:
        """
        Determina si el inventario está abierto
        
        Args:
            inventory_image: Imagen de la región del inventario
        
        Returns:
            True si el inventario está abierto
        """
        if inventory_image is None or inventory_image.size == 0:
            return False
        
        try:
            # Método 1: Verificar brillo promedio
            gray = cv2.cvtColor(inventory_image, cv2.COLOR_BGR2GRAY)
            avg_brightness = cv2.mean(gray)[0]
            
            # Si está muy oscuro, probablemente cerrado
            if avg_brightness < 50:
                return False
            
            # Método 2: Verificar variación de color (inventario abierto tiene más variación)
            color_std = np.std(inventory_image)
            if color_std < 20:  # Muy poca variación
                return False
            
            # Método 3: Buscar bordes (slots del inventario crean bordes)
            edges = cv2.Canny(gray, 50, 150)
            edge_percentage = cv2.countNonZero(edges) / (edges.shape[0] * edges.shape[1])
            
            if edge_percentage > 0.05:  # Más del 5% de bordes
                return True
            
            # Método 4: Verificar colores característicos del inventario
            inventory_colors = self.settings.colors.inventory_colors
            color_matches = 0
            
            for color in inventory_colors:
                mask = self.color_detector.create_color_mask(inventory_image, color, 40)
                match_percentage = cv2.countNonZero(mask) / mask.size
                if match_percentage > 0.1:  # Más del 10% de coincidencia
                    color_matches += 1
            
            return color_matches >= 2  # Al menos 2 colores coinciden
            
        except Exception as e:
            print(f"Error verificando inventario: {e}")
            return False
    
    def is_open(self, inventory_image: np.ndarray) -> bool:
        """
        Determina si el inventario está abierto (método público)
        
        Args:
            inventory_image: Imagen de la región del inventario
        
        Returns:
            True si el inventario está abierto
        """
        return self._check_if_open(inventory_image)
    
    def get_slots(self, inventory_image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Intenta identificar los slots del inventario
        
        Args:
            inventory_image: Imagen del inventario
        
        Returns:
            Información sobre slots o None
        """
        if not self.is_open(inventory_image):
            return None
        
        try:
            gray = cv2.cvtColor(inventory_image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar umbral para encontrar slots (normalmente más oscuros)
            _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            slots = []
            slot_size = 32  # Tamaño aproximado de un slot en píxeles
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 800 < area < 1200:  # Área típica de un slot
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Verificar proporciones (los slots son aproximadamente cuadrados)
                    aspect_ratio = w / h
                    if 0.8 < aspect_ratio < 1.2:
                        slots.append({
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'area': area
                        })
            
            if slots:
                return {
                    'slot_count': len(slots),
                    'slots': slots,
                    'estimated_rows': min(4, len(slots) // 5),
                    'estimated_columns': min(5, len(slots) // 4)
                }
            
            return None
            
        except Exception as e:
            print(f"Error detectando slots: {e}")
            return None