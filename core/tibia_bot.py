"""
Clase principal TibiaBot - Versión simplificada y funcional
"""
import time
import logging
from typing import Dict, Optional, Any

from core.screen_capturer import ScreenCapturer
from core.ui_detector import UIDetector
from core.bot_actions import BotActions
from core.bot_state import BotState
from config.settings import Settings
from config.ui_config import UIConfig

class TibiaBot:
    """Bot principal para automatizar tareas en Tibia"""
    
    def __init__(self, config_path: str = 'configs/default_settings.json', 
                 debug_mode: bool = False, logger: Optional[Any] = None):
        """
        Inicializa el bot
        
        Args:
            config_path: Ruta al archivo de configuración
            debug_mode: Modo de depuración
            logger: Logger personalizado (opcional)
        """
        # Configurar logging
        self.logger = logger or self._setup_logger(debug_mode)
        
        # Cargar configuración
        self.settings = Settings(config_path)
        self.ui_config = UIConfig()
        
        # Inicializar componentes
        self.capturer = ScreenCapturer(self.settings.monitor_index)
        self.detector = UIDetector(self.settings, self.ui_config)
        self.actions = BotActions(self.settings, self.ui_config)
        self.state = BotState()
        
        self.logger.info("[INFO] 🤖 TibiaBot inicializado correctamente")
        self.is_running = False
    
    def _setup_logger(self, debug_mode: bool) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger('TibiaBot')
        logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        # Handler para consola
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        return logger
    
    def auto_detect_ui(self) -> bool:
        """
        Detecta automáticamente los elementos de la UI
        
        Returns:
            True si la detección fue exitosa
        """
        self.logger.info("[INFO] 🔍 Iniciando detección automática de UI...")
        
        try:
            # Capturar pantalla
            screenshot = self.capturer.capture_full_screen()
            
            # Diccionario para almacenar posiciones detectadas
            detected_positions = {}
            
            # Lista de elementos a detectar
            elements_to_detect = {
                'hp_bar': 'detect_health_bar',
                'mp_bar': 'detect_mana_bar',
                'inventory': 'detect_inventory',
                'minimap': 'detect_minimap',
                'equipment': 'detect_equipment_window',
                'skills': 'detect_skills_window',
                'chat': 'detect_chat_window'
            }
            
            # Detectar cada elemento
            for element_name, method_name in elements_to_detect.items():
                try:
                    # Obtener método de detección
                    if hasattr(self.detector, method_name):
                        method = getattr(self.detector, method_name)
                        position = method(screenshot)
                        
                        if position:
                            detected_positions[element_name] = {
                                'x': position[0],
                                'y': position[1],
                                'width': position[2],
                                'height': position[3],
                                'confidence': 0.8,
                                'method': 'auto_detect'
                            }
                            self.logger.info(f"✅ {element_name} detectado: {position}")
                        else:
                            self.logger.warning(f"⚠️ {element_name} no detectado")
                    else:
                        self.logger.warning(f"⚠️ Método {method_name} no disponible")
                        
                except Exception as e:
                    self.logger.error(f"❌ Error detectando {element_name}: {e}")
            
            # Actualizar configuración
            if detected_positions:
                self.ui_config.update_positions(detected_positions)
                self.ui_config.save_to_file()
                
                self.logger.info(f"[INFO] ✅ Detección completada: {len(detected_positions)} elementos")
                return True
            else:
                self.logger.error("[ERROR] ❌ No se detectó ningún elemento")
                return False
                
        except Exception as e:
            self.logger.error(f"[ERROR] ❌ Error en detección automática: {e}")
            return False
    
    def start_monitoring(self):
        """Inicia el monitoreo automático"""
        self.logger.info("[INFO] 👁️ Iniciando monitoreo...")
        self.is_running = True
        
        try:
            while self.is_running:
                # Aquí iría la lógica de monitoreo
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("[INFO] 🛑 Monitoreo detenido por usuario")
        except Exception as e:
            self.logger.error(f"[ERROR] ❌ Error en monitoreo: {e}")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.logger.info("[INFO] ⏹️ Deteniendo monitoreo...")
        self.is_running = False
    
    def emergency_stop(self):
        """Detención de emergencia"""
        self.logger.warning("[WARNING] 🚨 Detención de emergencia!")
        self.stop_monitoring()
    
    def save_configuration(self):
        """Guarda la configuración actual"""
        try:
            self.ui_config.save_to_file()
            self.logger.info("[INFO] 💾 Configuración guardada")
        except Exception as e:
            self.logger.error(f"[ERROR] ❌ Error guardando configuración: {e}")
    
    def show_status(self):
        """Muestra el estado actual del bot"""
        print("\n" + "="*50)
        print("🤖 ESTADO DEL TIBIABOT")
        print("="*50)
        print(f"📊 Monitoreo activo: {'✅' if self.is_running else '❌'}")
        print(f"🖥️  Monitor: {self.settings.monitor_index}")
        print(f"📁 Elementos configurados: {len(self.ui_config.elements)}")
        
        if self.ui_config.elements:
            print("\n📋 Elementos detectados:")
            for name, element in self.ui_config.elements.items():
                print(f"   • {name}: {element.width}x{element.height} en ({element.x}, {element.y})")
        
        print("="*50)
