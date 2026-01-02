"""
Clase HealthDetector - Detección específica de barra de salud (HP)
"""
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any
from dataclasses import dataclass

from config.settings import Settings
from processors.color_detector import ColorDetector
from processors.image_processor import ImageProcessor

@dataclass
class DetectionResult:
    """Resultado de detección de HP"""
    confidence: float
    region: Optional[Tuple[int, int, int, int]]
    hp_percentage: Optional[float]
    method: str

class HealthDetector:
    """Detector especializado para barra de salud"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.color_detector = ColorDetector(settings)
        self.image_processor = ImageProcessor()
        
        # Colores específicos de HP (rojo en BGR)
        self.hp_colors = {
            'full': (50, 50, 200),      # Rojo brillante
            'medium': (40, 40, 150),    # Rojo medio
            'low': (30, 30, 100),       # Rojo oscuro
            'critical': (20, 20, 80)    # Rojo muy oscuro
        }
    
    def detect(self, screenshot: np.ndarray) -> DetectionResult:
        """
        Detecta la barra de HP en una captura
        
        Args:
            screenshot: Imagen de la pantalla completa
        
        Returns:
            Resultado de la detección
        """
        # Método 1: Por color
        color_result = self._detect_by_color(screenshot)
        if color_result.confidence > 0.8:
            return color_result
        
        # Método 2: Por plantilla
        template_result = self._detect_by_template(screenshot)
        if template_result.confidence > 0.7:
            return template_result
        
        # Método 3: Por patrón de barra
        pattern_result = self._detect_by_pattern(screenshot)
        return pattern_result
    
    def _detect_by_color(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección basada en color"""
        try:
            # Buscar regiones con color rojo (HP)
            regions = self.color_detector.find_color_regions(
                screenshot, self.hp_colors['full'],
                min_width=150, max_width=400,
                min_height=8, max_height=25,
                color_tolerance=40
            )
            
            if not regions:
                return DetectionResult(0.0, None, None, "color")
            
            # Seleccionar la mejor región
            best_region = self._select_best_hp_region(regions)
            
            # Calcular porcentaje de HP
            hp_percentage = self._estimate_hp_from_region(screenshot, best_region)
            
            return DetectionResult(
                confidence=0.85,
                region=best_region,
                hp_percentage=hp_percentage,
                method="color"
            )
            
        except Exception as e:
            print(f"Error en detección por color: {e}")
            return DetectionResult(0.0, None, None, "color_error")
    
    def _detect_by_template(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección basada en plantilla"""
        try:
            # Cargar plantilla de barra de HP
            template_path = "templates/hp_bar_segment.png"
            
            # Buscar coincidencia de plantilla
            result = cv2.matchTemplate(
                screenshot, 
                cv2.imread(template_path),
                cv2.TM_CCOEFF_NORMED
            )
            
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.7:  # Umbral de confianza
                template_h, template_w = cv2.imread(template_path).shape[:2]
                x, y = max_loc
                
                # La barra completa es más larga que la plantilla
                region = (x, y, 250, template_h)
                
                return DetectionResult(
                    confidence=float(max_val),
                    region=region,
                    hp_percentage=None,
                    method="template"
                )
            
            return DetectionResult(0.0, None, None, "template")
            
        except Exception as e:
            print(f"Error en detección por plantilla: {e}")
            return DetectionResult(0.0, None, None, "template_error")
    
    def _detect_by_pattern(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección basada en patrones"""
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Aplicar filtro para resaltar barras
            edges = cv2.Canny(gray, 50, 150)
            
            # Buscar líneas horizontales (bordes superior e inferior de la barra)
            lines = cv2.HoughLinesP(
                edges, 1, np.pi/180, 
                threshold=50,
                minLineLength=100,
                maxLineGap=10
            )
            
            if lines is not None:
                # Agrupar líneas por posición Y
                line_groups = {}
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    if abs(y2 - y1) < 5:  # Línea casi horizontal
                        y_avg = (y1 + y2) // 2
                        if y_avg not in line_groups:
                            line_groups[y_avg] = []
                        line_groups[y_avg].append((min(x1, x2), max(x1, x2)))
                
                # Buscar pares de líneas cercanas (bordes superior e inferior)
                for y1 in line_groups:
                    for y2 in line_groups:
                        if 5 < abs(y1 - y2) < 30:  # Altura de barra razonable
                            # Encontrar superposición en X
                            x_min = max(
                                min([x for x, _ in line_groups[y1]]),
                                min([x for x, _ in line_groups[y2]])
                            )
                            x_max = min(
                                max([x for _, x in line_groups[y1]]),
                                max([x for _, x in line_groups[y2]])
                            )
                            
                            if x_max - x_min > 100:  # Ancho mínimo
                                region = (x_min, min(y1, y2), 
                                         x_max - x_min, abs(y1 - y2))
                                
                                return DetectionResult(
                                    confidence=0.7,
                                    region=region,
                                    hp_percentage=None,
                                    method="pattern"
                                )
            
            return DetectionResult(0.0, None, None, "pattern")
            
        except Exception as e:
            print(f"Error en detección por patrón: {e}")
            return DetectionResult(0.0, None, None, "pattern_error")
    
    def _select_best_hp_region(self, regions: list) -> Tuple[int, int, int, int]:
        """Selecciona la región más probable para la barra de HP"""
        # Priorizar regiones largas y delgadas en posición superior
        scored_regions = []
        
        for region in regions:
            x, y, w, h = region
            
            # Puntuación basada en:
            # 1. Aspect ratio (debe ser largo y delgado)
            aspect_ratio = w / max(h, 1)
            aspect_score = min(aspect_ratio / 10, 1.0)
            
            # 2. Posición Y (debe estar en parte superior)
            height, _ = cv2.imread("temp").shape[:2] if False else (1080, 1920)
            position_score = 1.0 - (y / height)
            
            # 3. Ancho (debe ser razonable)
            width_score = 1.0 if 150 < w < 400 else 0.5
            
            # 4. Altura (debe ser pequeña)
            height_score = 1.0 if 8 < h < 25 else 0.5
            
            total_score = (
                aspect_score * 0.4 +
                position_score * 0.3 +
                width_score * 0.2 +
                height_score * 0.1
            )
            
            scored_regions.append((total_score, region))
        
        # Ordenar por puntuación y devolver la mejor
        scored_regions.sort(reverse=True)
        return scored_regions[0][1] if scored_regions else regions[0]
    
    def _estimate_hp_from_region(self, screenshot: np.ndarray, 
                                region: Tuple[int, int, int, int]) -> float:
        """Estima el porcentaje de HP basado en el color en la región"""
        x, y, w, h = region
        bar_image = screenshot[y:y+h, x:x+w]
        
        # Contar píxeles rojos (HP)
        hp_pixels = 0
        total_pixels = 0
        
        for color_name, color_value in self.hp_colors.items():
            mask = self.color_detector.create_color_mask(bar_image, color_value, 30)
            hp_pixels += cv2.countNonZero(mask)
        
        # Contar píxeles oscuros (HP vacío)
        gray = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)
        _, dark_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
        empty_pixels = cv2.countNonZero(dark_mask)
        
        total_pixels = bar_image.shape[0] * bar_image.shape[1]
        filled_pixels = total_pixels - empty_pixels
        
        if total_pixels > 0:
            percentage = (filled_pixels / total_pixels) * 100
            return max(0, min(100, percentage))
        
        return 0.0
    
    def analyze(self, bar_image: np.ndarray) -> float:
        """
        Analiza una imagen de barra de HP y devuelve el porcentaje
        
        Args:
            bar_image: Imagen de la barra de HP
        
        Returns:
            Porcentaje de HP (0-100)
        """
        if bar_image is None or bar_image.size == 0:
            return 0.0
        
        try:
            # Método 1: Por porcentaje de color rojo
            color_percentage = self._analyze_by_color(bar_image)
            
            # Método 2: Por posición del borde derecho
            edge_percentage = self._analyze_by_edge(bar_image)
            
            # Método 3: Por brillo promedio
            brightness_percentage = self._analyze_by_brightness(bar_image)
            
            # Combinar resultados (ponderado)
            final_percentage = (
                color_percentage * 0.5 +
                edge_percentage * 0.3 +
                brightness_percentage * 0.2
            )
            
            return max(0.0, min(100.0, final_percentage))
            
        except Exception as e:
            print(f"Error analizando barra de HP: {e}")
            return 0.0
    
    def _analyze_by_color(self, bar_image: np.ndarray) -> float:
        """Analiza por porcentaje de píxeles del color de HP"""
        # Crear máscara para color rojo (HP)
        hp_mask = np.zeros(bar_image.shape[:2], dtype=np.uint8)
        
        for color_name, color_value in self.hp_colors.items():
            color_mask = self.color_detector.create_color_mask(
                bar_image, color_value, 40
            )
            hp_mask = cv2.bitwise_or(hp_mask, color_mask)
        
        # Contar píxeles de HP
        hp_pixels = cv2.countNonZero(hp_mask)
        total_pixels = bar_image.shape[0] * bar_image.shape[1]
        
        if total_pixels > 0:
            return (hp_pixels / total_pixels) * 100
        
        return 0.0
    
    def _analyze_by_edge(self, bar_image: np.ndarray) -> float:
        """Analiza por posición del borde derecho del HP"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral para separar HP de fondo
        _, threshold = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
        
        # Encontrar el borde más a la derecha con píxeles blancos
        height, width = threshold.shape
        right_edge = 0
        
        for col in range(width - 1, -1, -1):
            column_pixels = threshold[:, col]
            if cv2.countNonZero(column_pixels) > height * 0.1:  # 10% de la columna
                right_edge = col
                break
        
        return (right_edge / width) * 100
    
    def _analyze_by_brightness(self, bar_image: np.ndarray) -> float:
        """Analiza por brillo promedio (HP lleno es más brillante)"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)
        
        # Calcular brillo promedio
        avg_brightness = cv2.mean(gray)[0]
        
        # Normalizar (asumiendo que HP lleno tiene brillo > 150, vacío < 50)
        if avg_brightness < 50:
            return 0.0
        elif avg_brightness > 150:
            return 100.0
        else:
            return ((avg_brightness - 50) / 100) * 100