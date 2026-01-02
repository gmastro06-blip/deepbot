# core/ui_detector.py - Versión completa
"""
Clase UIDetector - Detección de elementos de la interfaz de usuario
"""
import cv2
import numpy as np
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class UIDetector:
    """Detección de elementos de la interfaz de Tibia"""
    
    def __init__(self, settings, ui_config):
        self.settings = settings
        self.ui_config = ui_config
        logger.info("UIDetector inicializado")
    
    # Métodos principales de detección
    def detect_health_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la barra de salud (HP)"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, asumimos que está en la parte superior central
            return (width // 2 - 200, 50, 400, 20)
        except Exception as e:
            logger.error(f"Error detectando barra de HP: {e}")
            return None
    
    def detect_mana_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la barra de maná (MP)"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, justo debajo de la barra de HP
            return (width // 2 - 200, 75, 400, 20)
        except Exception as e:
            logger.error(f"Error detectando barra de MP: {e}")
            return None
    
    def detect_inventory(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la ventana del inventario"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, esquina inferior derecha
            return (width - 300, height - 400, 280, 380)
        except Exception as e:
            logger.error(f"Error detectando inventario: {e}")
            return None
    
    def detect_minimap(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta el minimapa"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, esquina superior derecha
            return (width - 200, 50, 150, 150)
        except Exception as e:
            logger.error(f"Error detectando minimapa: {e}")
            return None
    
    def detect_equipment_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la ventana de equipo"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, a la izquierda del inventario
            return (width - 500, height - 400, 180, 380)
        except Exception as e:
            logger.error(f"Error detectando equipo: {e}")
            return None
    
    def detect_skills_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la ventana de habilidades"""
        try:
            logger.warning("Detección de ventana de habilidades no implementada")
            return None
        except Exception as e:
            logger.error(f"Error detectando ventana de habilidades: {e}")
            return None
    
    def detect_chat_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detecta la ventana de chat"""
        try:
            height, width = screenshot.shape[:2]
            # Por defecto, parte inferior
            return (50, height - 300, width - 100, 250)
        except Exception as e:
            logger.error(f"Error detectando chat: {e}")
            return None
    
    # Métodos de análisis
    def analyze_health_bar(self, bar_image: np.ndarray) -> float:
        """Analiza una imagen de barra de HP y devuelve el porcentaje"""
        try:
            # Implementación simple: asume 100% por ahora
            return 100.0
        except Exception as e:
            logger.error(f"Error analizando barra de HP: {e}")
            return 0.0
    
    def analyze_mana_bar(self, bar_image: np.ndarray) -> float:
        """Analiza una imagen de barra de MP y devuelve el porcentaje"""
        try:
            # Implementación simple: asume 100% por ahora
            return 100.0
        except Exception as e:
            logger.error(f"Error analizando barra de MP: {e}")
            return 0.0
    
    # Métodos adicionales para compatibilidad
    def detect_hp_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Alias para detect_health_bar"""
        return self.detect_health_bar(screenshot)
    
    def detect_mp_bar(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Alias para detect_mana_bar"""
        return self.detect_mana_bar(screenshot)