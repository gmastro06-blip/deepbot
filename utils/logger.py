"""
Clase AppLogger - Sistema de logging personalizado (versión sin colorama)
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

class AppLogger:
    """Logger personalizado para el bot de Tibia"""
    
    def __init__(self, name: str = "TibiaBot", log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler de consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler de archivo si se especifica
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(f"[DEBUG] {message}", *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        self.logger.info(f"[INFO] {message}", *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(f"[WARNING] {message}", *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        self.logger.error(f"[ERROR] {message}", *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(f"[CRITICAL] {message}", *args, **kwargs)
    
    def success(self, message: str, *args, **kwargs):
        self.logger.info(f"[SUCCESS] {message}", *args, **kwargs)
    
    def set_level(self, level):
        """Establece el nivel de logging"""
        # Aceptar tanto strings como objetos LogLevel
        if hasattr(level, 'value'):
            # Es un objeto LogLevel
            level_str = level.value
        else:
            # Es un string
            level_str = str(level)
        
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        level_upper = level_str.upper()
        logging_level = level_map.get(level_upper, logging.INFO)
        
        self.logger.setLevel(logging_level)
        for handler in self.logger.handlers:
            handler.setLevel(logging_level)