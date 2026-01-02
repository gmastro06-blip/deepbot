# screen_capturer_obs.py
import cv2
import numpy as np
from core.screen_capturer import ScreenCapturer


class OBSScreenCapturer(ScreenCapturer):
    """Versión de ScreenCapturer que usa OBS como fuente"""
    
    def __init__(self, obs_controller=None, **kwargs):
        """
        Inicializa capturador con OBS
        
        Args:
            obs_controller: Instancia de OBSController
            **kwargs: Argumentos para ScreenCapturer padre
        """
        super().__init__(**kwargs)
        self.obs = obs_controller
    
    def capture_full_screen(self):
        """
        Captura pantalla desde OBS o método normal
        """
        if self.obs:
            # Intentar capturar desde OBS
            screenshot = self.obs.capture_game_window()
            if screenshot is not None:
                self.last_capture = screenshot
                self.capture_count += 1
                return screenshot
        
        # Si OBS falla, usar método normal
        return super().capture_full_screen()