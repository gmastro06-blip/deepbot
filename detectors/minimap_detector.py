"""
Clase MinimapDetector - Detección de minimapa
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
    """Resultado de detección de minimapa"""
    confidence: float
    region: Optional[Tuple[int, int, int, int]]
    player_position: Optional[Dict[str, int]]
    method: str

class MinimapDetector:
    """Detector especializado para minimapa"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.color_detector = ColorDetector(settings)
        self.image_processor = ImageProcessor()
    
    def detect(self, screenshot: np.ndarray) -> DetectionResult:
        """
        Detecta el minimapa en una captura
        
        Args:
            screenshot: Imagen de la pantalla completa
        
        Returns:
            Resultado de la detección
        """
        # Método 1: Por círculo (minimapa circular)
        circle_result = self._detect_by_circle(screenshot)
        if circle_result.confidence > 0.8:
            return circle_result
        
        # Método 2: Por color (verde/bosque)
        color_result = self._detect_by_color(screenshot)
        if color_result.confidence > 0.7:
            return color_result
        
        # Método 3: Por posición (esquina superior derecha)
        position_result = self._detect_by_position(screenshot)
        return position_result
    
    def _detect_by_circle(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por forma circular"""
        try:
            height, width = screenshot.shape[:2]
            
            # Buscar en esquina superior derecha (donde suele estar el minimapa)
            search_region = screenshot[50:300, width-350:width-50]
            
            if search_region.size == 0:
                return DetectionResult(0.0, None, None, "circle")
            
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
                x, y, r = circles[0][0]
                
                # Ajustar coordenadas a la pantalla completa
                x += width - 350
                y += 50
                
                region = (x - r, y - r, r * 2, r * 2)
                
                # Obtener posición del jugador
                minimap_img = screenshot[y-r:y+r, x-r:x+r]
                player_pos = self._find_player_position(minimap_img)
                
                return DetectionResult(
                    confidence=0.9,
                    region=region,
                    player_position=player_pos,
                    method="circle"
                )
            
            return DetectionResult(0.0, None, None, "circle")
            
        except Exception as e:
            print(f"Error en detección por círculo: {e}")
            return DetectionResult(0.0, None, None, "circle_error")
    
    def _detect_by_color(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por colores del minimapa (verdes, marrones)"""
        try:
            height, width = screenshot.shape[:2]
            
            # Convertir a HSV para mejor detección de color
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Rangos para colores del minimapa
            # Verde (bosque)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Marrón (caminos, montañas)
            lower_brown = np.array([10, 50, 20])
            upper_brown = np.array([25, 255, 200])
            brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
            
            # Combinar máscaras
            minimap_mask = cv2.bitwise_or(green_mask, brown_mask)
            
            # Encontrar contornos grandes
            contours, _ = cv2.findContours(minimap_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Filtrar por tamaño y posición
                large_contours = []
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 10000:  # Área mínima para minimapa
                        large_contours.append(contour)
                
                if large_contours:
                    # Tomar el contorno más grande en la esquina superior derecha
                    largest_contour = max(large_contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    
                    # Verificar que esté en posición de minimapa
                    if x > width * 0.6 and y < height * 0.4:
                        region = (x, y, w, h)
                        
                        # Obtener posición del jugador
                        minimap_img = screenshot[y:y+h, x:x+w]
                        player_pos = self._find_player_position(minimap_img)
                        
                        return DetectionResult(
                            confidence=0.8,
                            region=region,
                            player_position=player_pos,
                            method="color"
                        )
            
            return DetectionResult(0.0, None, None, "color")
            
        except Exception as e:
            print(f"Error en detección por color: {e}")
            return DetectionResult(0.0, None, None, "color_error")
    
    def _detect_by_position(self, screenshot: np.ndarray) -> DetectionResult:
        """Detección por posición común del minimapa"""
        try:
            height, width = screenshot.shape[:2]
            
            # Posición común del minimapa (esquina superior derecha)
            region_x = width - 250
            region_y = 50
            region_w = 200
            region_h = 200
            
            region = (region_x, region_y, region_w, region_h)
            
            # Obtener posición del jugador
            minimap_img = screenshot[region_y:region_y+region_h, region_x:region_x+region_w]
            player_pos = self._find_player_position(minimap_img)
            
            # Calcular confianza basada en si encontramos al jugador
            confidence = 0.7 if player_pos else 0.4
            
            return DetectionResult(
                confidence=confidence,
                region=region,
                player_position=player_pos,
                method="position"
            )
            
        except Exception as e:
            print(f"Error en detección por posición: {e}")
            return DetectionResult(0.0, None, None, "position_error")
    
    def _find_player_position(self, minimap_image: np.ndarray) -> Optional[Dict[str, int]]:
        """
        Encuentra la posición del jugador en el minimapa
        
        Args:
            minimap_image: Imagen del minimapa
        
        Returns:
            Coordenadas del jugador o None
        """
        if minimap_image is None or minimap_image.size == 0:
            return None
        
        try:
            # Método 1: Buscar punto blanco/amarillo (jugador)
            hsv = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2HSV)
            
            # Rango para color blanco/amarillo claro (jugador)
            lower_player = np.array([20, 100, 100])
            upper_player = np.array([40, 255, 255])
            
            player_mask = cv2.inRange(hsv, lower_player, upper_player)
            
            # Encontrar el punto más brillante
            moments = cv2.moments(player_mask)
            
            if moments['m00'] > 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                return {'x': cx, 'y': cy}
            
            # Método 2: Buscar punto más brillante
            gray = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar umbral para puntos brillantes
            _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            
            # Encontrar contornos de puntos brillantes
            contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Tomar el contorno más brillante y pequeño
                brightest_contour = None
                max_brightness = 0
                
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Filtrar por tamaño (el jugador es un punto pequeño)
                    if 2 < w < 10 and 2 < h < 10:
                        region = gray[y:y+h, x:x+w]
                        brightness = np.mean(region)
                        
                        if brightness > max_brightness:
                            max_brightness = brightness
                            brightest_contour = (x + w//2, y + h//2)
                
                if brightest_contour:
                    return {'x': brightest_contour[0], 'y': brightest_contour[1]}
            
            return None
            
        except Exception as e:
            print(f"Error encontrando jugador: {e}")
            return None
    
    def get_player_position(self, minimap_image: np.ndarray) -> Optional[Dict[str, int]]:
        """
        Obtiene la posición del jugador (método público)
        
        Args:
            minimap_image: Imagen del minimapa
        
        Returns:
            Coordenadas del jugador o None
        """
        return self._find_player_position(minimap_image)
    
    def get_minimap_features(self, minimap_image: np.ndarray) -> Dict[str, Any]:
        """
        Analiza características del minimapa
        
        Args:
            minimap_image: Imagen del minimapa
        
        Returns:
            Diccionario con características
        """
        if minimap_image is None or minimap_image.size == 0:
            return {"error": "Imagen vacía"}
        
        try:
            # Convertir a diferentes espacios de color
            hsv = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2HSV)
            gray = cv2.cvtColor(minimap_image, cv2.COLOR_BGR2GRAY)
            
            # Analizar colores
            color_distribution = self.color_detector.analyze_color_distribution(minimap_image)
            
            # Buscar al jugador
            player_pos = self._find_player_position(minimap_image)
            
            # Detectar bordes (estructuras, caminos)
            edges = cv2.Canny(gray, 50, 150)
            edge_percentage = cv2.countNonZero(edges) / edges.size
            
            # Detectar áreas verdes (bosque)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            green_percentage = cv2.countNonZero(green_mask) / green_mask.size
            
            # Detectar áreas azules (agua)
            lower_blue = np.array([90, 40, 40])
            upper_blue = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            blue_percentage = cv2.countNonZero(blue_mask) / blue_mask.size
            
            return {
                "player_found": player_pos is not None,
                "player_position": player_pos,
                "width": minimap_image.shape[1],
                "height": minimap_image.shape[0],
                "edge_density": edge_percentage,
                "forest_percentage": green_percentage,
                "water_percentage": blue_percentage,
                "avg_brightness": color_distribution.get('v_mean', 0),
                "avg_saturation": color_distribution.get('s_mean', 0)
            }
            
        except Exception as e:
            print(f"Error analizando minimapa: {e}")
            return {"error": str(e)}