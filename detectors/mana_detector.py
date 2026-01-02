"""
Clase ManaDetector - Detección específica de barra de maná (MP) en Tibia
"""
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass

from config.settings import Settings
from processors.color_detector import ColorDetector
from processors.image_processor import ImageProcessor


@dataclass
class DetectionResult:
    """Resultado de detección de MP"""
    confidence: float
    region: Optional[Tuple[int, int, int, int]]  # (x, y, w, h)
    mp_percentage: Optional[float]
    method: str


class ManaDetector:
    """Detector especializado para barra de maná en Tibia"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.color_detector = ColorDetector(settings)
        self.image_processor = ImageProcessor()
        
        # Colores específicos de MP (azul en formato BGR)
        self.mp_colors = {
            'full': (200, 100, 50),      # Azul brillante
            'medium': (150, 80, 40),
            'low': (100, 60, 30),
            'critical': (80, 40, 20)
        }
        
        # Cache para plantilla
        self._template_cache = None
        self.template_path = "templates/mp_bar_segment.png"

    def detect(self, screenshot: np.ndarray) -> DetectionResult:
        """
        Detecta la barra de MP en una captura completa de pantalla
        """
        if screenshot is None or screenshot.size == 0:
            return DetectionResult(0.0, None, None, "no_image")

        # Método 1: Por color (más rápido y fiable en Tibia)
        color_result = self._detect_by_color(screenshot)
        if color_result.confidence > 0.8:
            return color_result
        
        # Método 2: Por plantilla
        template_result = self._detect_by_template(screenshot)
        if template_result.confidence > 0.7:
            return template_result
        
        # Método 3: Relativo a HP
        relative_result = self._detect_relative_to_hp(screenshot)
        return relative_result

    def _detect_by_color(self, screenshot: np.ndarray) -> DetectionResult:
        try:
            regions = self.color_detector.find_color_regions(
                screenshot,
                target_color=self.mp_colors['full'],
                min_width=150, max_width=400,
                min_height=8, max_height=25,
                color_tolerance=40
            )
            
            if not regions:
                return DetectionResult(0.0, None, None, "color_no_regions")
            
            best_region = self._select_best_mp_region(regions, screenshot.shape[0])
            
            mp_percentage = self._estimate_mp_from_region(screenshot, best_region)
            
            return DetectionResult(
                confidence=0.85,
                region=best_region,
                mp_percentage=mp_percentage,
                method="color"
            )
            
        except Exception as e:
            print(f"Error en detección por color: {e}")
            return DetectionResult(0.0, None, None, "color_error")

    def _detect_by_template(self, screenshot: np.ndarray) -> DetectionResult:
        try:
            template = self._load_template()
            if template is None:
                return DetectionResult(0.0, None, None, "template_not_loaded")
            
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > 0.7:
                t_h, t_w = template.shape[:2]
                x, y = max_loc
                # Estimar ancho completo de la barra (Tibia suele tener ~250-300px)
                region = (x, y, 280, t_h)
                
                return DetectionResult(
                    confidence=float(max_val),
                    region=region,
                    mp_percentage=None,
                    method="template"
                )
            
            return DetectionResult(0.0, None, None, "template_low_confidence")
            
        except Exception as e:
            print(f"Error en detección por plantilla: {e}")
            return DetectionResult(0.0, None, None, "template_error")

    def _load_template(self) -> Optional[np.ndarray]:
        """Carga plantilla con cache"""
        if self._template_cache is not None:
            return self._template_cache
        
        try:
            template = cv2.imread(self.template_path)
            if template is not None:
                self._template_cache = template
            return template
        except:
            return None

    def _detect_relative_to_hp(self, screenshot: np.ndarray) -> DetectionResult:
        try:
            hp_color = (50, 50, 200)  # Rojo típico de HP en Tibia
            hp_regions = self.color_detector.find_color_regions(
                screenshot, hp_color,
                min_width=150, max_width=400,
                min_height=8, max_height=25,
                color_tolerance=40
            )
            
            if not hp_regions:
                return DetectionResult(0.0, None, None, "relative_no_hp")
            
            hp_x, hp_y, hp_w, hp_h = hp_regions[0]
            search_y_start = hp_y + hp_h + 5
            search_y_end = search_y_start + 40
            
            if search_y_end > screenshot.shape[0]:
                return DetectionResult(0.0, None, None, "relative_out_of_bounds")
            
            search_region = screenshot[search_y_start:search_y_end, :]
            
            mp_regions = self.color_detector.find_color_regions(
                search_region, self.mp_colors['full'],
                min_width=150, max_width=400,
                min_height=8, max_height=20,
                color_tolerance=40
            )
            
            if mp_regions:
                x, y, w, h = mp_regions[0]
                region = (x, y + search_y_start, w, h)
                
                return DetectionResult(
                    confidence=0.7,
                    region=region,
                    mp_percentage=None,
                    method="relative"
                )
            
            return DetectionResult(0.0, None, None, "relative_no_mp")
            
        except Exception as e:
            print(f"Error en detección relativa: {e}")
            return DetectionResult(0.0, None, None, "relative_error")

    def _select_best_mp_region(self, regions: List[Tuple[int, int, int, int]], screen_height: int) -> Tuple[int, int, int, int]:
        """Selecciona la región más probable para la barra de MP"""
        if not regions:
            return (0, 0, 0, 0)
        
        scored_regions = []
        
        for region in regions:
            x, y, w, h = region
            
            # Aspect ratio (largo y delgado)
            aspect_ratio = w / max(h, 1)
            aspect_score = min(aspect_ratio / 15, 1.0)  # Tibia ~12-15
            
            # Dimensiones
            width_score = 1.0 if 180 < w < 350 else 0.6
            height_score = 1.0 if 10 < h < 22 else 0.6
            
            # Posición vertical (cerca de la parte superior)
            position_score = max(0.0, 1.0 - (y / screen_height))
            
            total_score = (
                aspect_score * 0.4 +
                width_score * 0.3 +
                height_score * 0.2 +
                position_score * 0.1
            )
            
            scored_regions.append((total_score, region))
        
        scored_regions.sort(reverse=True, key=lambda x: x[0])
        return scored_regions[0][1]

    def _estimate_mp_from_region(self, screenshot: np.ndarray, region: Tuple[int, int, int, int]) -> float:
        x, y, w, h = region
        if y + h > screenshot.shape[0] or x + w > screenshot.shape[1]:
            return 0.0
        
        bar_image = screenshot[y:y+h, x:x+w]
        return self.analyze(bar_image)

    def analyze(self, bar_image: np.ndarray) -> float:
        """Analiza porcentaje de MP en una imagen ya recortada de la barra"""
        if bar_image is None or bar_image.size == 0:
            return 0.0
        
        try:
            color_pct = self._analyze_by_color(bar_image)
            edge_pct = self._analyze_by_edge(bar_image)
            bright_pct = self._analyze_by_brightness(bar_image)
            
            final = (
                color_pct * 0.5 +
                edge_pct * 0.3 +
                bright_pct * 0.2
            )
            return max(0.0, min(100.0, final))
            
        except Exception as e:
            print(f"Error analizando barra: {e}")
            return 0.0

    def _analyze_by_color(self, bar_image: np.ndarray) -> float:
        mask = np.zeros(bar_image.shape[:2], dtype=np.uint8)
        for color in self.mp_colors.values():
            color_mask = self.color_detector.create_color_mask(bar_image, color, tolerance=40)
            mask = cv2.bitwise_or(mask, color_mask)
        
        pixels = cv2.countNonZero(mask)
        total = bar_image.shape[0] * bar_image.shape[1]
        return (pixels / total) * 100 if total > 0 else 0.0

    def _analyze_by_edge(self, bar_image: np.ndarray) -> float:
        gray = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
        
        h, w = thresh.shape
        right_edge = 0
        for col in range(w - 1, -1, -1):
            if cv2.countNonZero(thresh[:, col]) > h * 0.2:
                right_edge = col
                break
        
        return (right_edge / w) * 100 if w > 0 else 0.0

    def _analyze_by_brightness(self, bar_image: np.ndarray) -> float:
        gray = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)
        brightness = cv2.mean(gray)[0]
        return np.clip((brightness - 40) / 110 * 100, 0, 100)

    def validate_bar(self, bar_image: np.ndarray) -> bool:
        if bar_image is None or bar_image.size == 0:
            return False
        h, w = bar_image.shape[:2]
        if not (8 <= h <= 28 and 100 <= w <= 450):
            return False
        if self._analyze_by_color(bar_image) < 8.0:
            return False
        return True

    def calibrate(self, bar_image: np.ndarray) -> Dict[str, Any]:
        if not self.validate_bar(bar_image):
            return {"error": "Imagen no válida para calibración", "is_valid": False}
        
        avg_bgr = self.color_detector.get_dominant_color(bar_image)
        avg_hsv = self.color_detector.bgr_to_hsv(avg_bgr)
        dist = self.color_detector.analyze_color_distribution(bar_image)
        
        return {
            "avg_color_bgr": avg_bgr.tolist() if isinstance(avg_bgr, np.ndarray) else avg_bgr,
            "avg_color_hsv": avg_hsv,
            "width": bar_image.shape[1],
            "height": bar_image.shape[0],
            "current_percentage": self.analyze(bar_image),
            "brightness": dist.get('v_mean', 0),
            "saturation": dist.get('s_mean', 0),
            "is_valid": True
        }