"""
Clase ColorDetector - Detección de colores específicos
"""
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

class ColorDetector:
    """Detección de colores en imágenes"""
    
    def __init__(self, settings):
        """
        Inicializa el detector de colores
        
        Args:
            settings: Configuración del bot
        """
        self.settings = settings
        
        # Configuración de tolerancia de color
        self.color_tolerance = getattr(settings, 'color_tolerance', 30)
        self.min_region_area = getattr(settings, 'min_region_area', 100)
        
        # Rangos de color predefinidos
        self.predefined_ranges = self._create_predefined_ranges()
    
    def _create_predefined_ranges(self) -> Dict[str, Dict[str, Tuple]]:
        """
        Crea rangos de color predefinidos desde settings
        
        Returns:
            Diccionario con rangos de color
        """
        ranges = {}
        
        # Si settings.colors existe
        if hasattr(self.settings, 'colors') and self.settings.colors:
            colors = self.settings.colors
            
            # Procesar cada color
            for color_name, color_info in colors.items():
                if isinstance(color_info, dict):
                    # Si es diccionario con variantes
                    for variant, bgr_color in color_info.items():
                        if isinstance(bgr_color, (list, tuple)) and len(bgr_color) == 3:
                            key = f"{color_name}_{variant}"
                            ranges[key] = self._create_color_range(bgr_color, self.color_tolerance)
                elif isinstance(color_info, (list, tuple)) and len(color_info) == 3:
                    # Si es directamente un color BGR
                    ranges[color_name] = self._create_color_range(color_info, self.color_tolerance)
        
        # Si no hay colores en settings, crear algunos por defecto
        if not ranges:
            ranges = {
                'hp_full': self._create_color_range((50, 50, 200), 40),
                'mp_full': self._create_color_range((200, 50, 50), 40),
                'green': self._create_color_range((50, 200, 50), 40),
                'yellow': self._create_color_range((50, 200, 200), 40),
            }
        
        return ranges
    
    def _create_color_range(self, bgr_color: Tuple[int, int, int], 
                           tolerance: int = 30) -> Dict[str, np.ndarray]:
        """
        Crea un rango de color HSV desde un color BGR
        
        Args:
            bgr_color: Color en formato BGR (Blue, Green, Red)
            tolerance: Tolerancia para el rango
        
        Returns:
            Diccionario con lower y upper bounds en HSV
        """
        # Convertir BGR a HSV
        bgr_array = np.uint8([[list(bgr_color)]])
        hsv_color = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)[0][0]
        
        # Crear rango (usar int para evitar overflow)
        lower = np.array([
            max(0, int(hsv_color[0]) - tolerance),
            max(0, int(hsv_color[1]) - tolerance),
            max(0, int(hsv_color[2]) - tolerance)
        ], dtype=np.int32)
        
        upper = np.array([
            min(179, int(hsv_color[0]) + tolerance),
            min(255, int(hsv_color[1]) + tolerance),
            min(255, int(hsv_color[2]) + tolerance)
        ], dtype=np.int32)
        
        return {'lower': lower, 'upper': upper}
    
    def create_color_mask(self, image: np.ndarray, target_color: Tuple[int, int, int],
                         tolerance: int = None) -> np.ndarray:
        """
        Crea una máscara para un color específico
        
        Args:
            image: Imagen en formato BGR
            target_color: Color objetivo en formato BGR
            tolerance: Tolerancia de color (None = usar default)
        
        Returns:
            Máscara binaria (blanco donde está el color)
        """
        if tolerance is None:
            tolerance = self.color_tolerance
        
        # Crear rango para este color específico
        color_range = self._create_color_range(target_color, tolerance)
        
        # Convertir imagen a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crear máscara
        mask = cv2.inRange(hsv, color_range['lower'], color_range['upper'])
        
        return mask
    
    def find_color_regions(self, image: np.ndarray, target_color: Tuple[int, int, int],
                          min_width: int = 10, max_width: int = 1000,
                          min_height: int = 10, max_height: int = 1000,
                          color_tolerance: int = None) -> List[Tuple[int, int, int, int]]:
        """
        Encuentra regiones de un color específico
        
        Args:
            image: Imagen donde buscar
            target_color: Color a buscar en formato BGR
            min_width: Ancho mínimo de región
            max_width: Ancho máximo de región
            min_height: Alto mínimo de región
            max_height: Alto máximo de región
            color_tolerance: Tolerancia de color
        
        Returns:
            Lista de regiones (x, y, ancho, alto)
        """
        # Crear máscara
        mask = self.create_color_mask(image, target_color, color_tolerance)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        
        for contour in contours:
            # Obtener bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtrar por tamaño
            if (min_width <= w <= max_width and 
                min_height <= h <= max_height and
                w * h >= self.min_region_area):
                
                regions.append((x, y, w, h))
        
        # Ordenar por área (mayor primero)
        regions.sort(key=lambda r: r[2] * r[3], reverse=True)
        
        return regions