# config/settings.py
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

@dataclass
class Settings:
    """Configuración general del bot"""
    
    # Ruta al archivo de configuración
    config_path: str = "configs/default_settings.json"
    
    # Configuración de logging
    log_level: str = "INFO"
    log_file: str = "logs/tibia_bot.log"
    log_to_console: bool = True
    color_tolerance: int = 30  # Tolerancia para detección de colores
    min_region_area: int = 100  # Área mínima para considerar una región
    
    # Configuración de captura de pantalla
    monitor_index: int = 1
    capture_fps: int = 5
    capture_quality: int = 80
    
    # Configuración de detección
    detection_confidence: float = 0.7
    detection_interval: float = 0.5  # segundos
    
    # Configuración de colores
    colors: Dict[str, Any] = field(default_factory=lambda: {
        'hp': {
            'full': (50, 50, 200),      # Rojo brillante (BGR)
            'medium': (40, 40, 150),    # Rojo medio
            'low': (30, 30, 100),       # Rojo oscuro
            'critical': (20, 20, 80)    # Rojo muy oscuro
        },
        'mp': {
            'full': (200, 50, 50),      # Azul brillante (BGR)
            'medium': (150, 40, 40),    # Azul medio
            'low': (100, 30, 30),       # Azul oscuro
            'critical': (80, 20, 20)    # Azul muy oscuro
        }
    })
    
    # Configuración de acciones
    emergency_hp_threshold: int = 30  # % de HP para emergencia
    emergency_mp_threshold: int = 20  # % de MP para emergencia
    auto_heal_enabled: bool = True
    auto_mana_enabled: bool = True
    
    def __post_init__(self):
        """Validación y carga de configuración desde archivo"""
        self.load_from_file(self.config_path)
    
    def load_from_file(self, config_path: str = None) -> bool:
        """
        Carga configuración desde archivo JSON
        
        Args:
            config_path: Ruta al archivo de configuración
        
        Returns:
            True si se cargó exitosamente
        """
        if config_path is None:
            config_path = self.config_path
        
        config_path = Path(config_path)
        if not config_path.exists():
            print(f"⚠️ Archivo de configuración no encontrado: {config_path}")
            print("   Usando valores por defecto")
            return False
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Actualizar atributos desde el archivo
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            
            print(f"✅ Configuración cargada desde {config_path}")
            return True
            
        except Exception as e:
            print(f"⚠️ Error cargando configuración: {e}")
            print("   Usando valores por defecto")
            return False
    
    def save_to_file(self, config_path: str = None) -> bool:
        """
        Guarda configuración en archivo JSON
        
        Args:
            config_path: Ruta donde guardar
        
        Returns:
            True si se guardó exitosamente
        """
        if config_path is None:
            config_path = self.config_path
        
        try:
            # Convertir a diccionario
            data = {}
            for key in self.__dataclass_fields__.keys():
                value = getattr(self, key)
                # Convertir objetos Path a string
                if isinstance(value, Path):
                    value = str(value)
                data[key] = value
            
            # Asegurar que el directorio existe
            Path(config_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar en archivo
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuración guardada en {config_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
            return False
    
    # En la clase Settings de config/settings.py, añade:
    def get_color(self, color_name: str, variant: str = 'full'):
        """
        Obtiene un color específico
        
        Args:
            color_name: Nombre del color (hp, mp, etc.)
            variant: Variante del color (full, medium, low, critical)
        
        Returns:
            Tupla BGR o None si no se encuentra
        """
        if color_name in self.colors:
            color_dict = self.colors[color_name]
            if isinstance(color_dict, dict) and variant in color_dict:
                return color_dict[variant]
            elif isinstance(color_dict, tuple):
                return color_dict
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la configuración a diccionario"""
        return {k: getattr(self, k) for k in self.__dataclass_fields__.keys()}
    
    def print_summary(self):
        """Imprime un resumen de la configuración"""
        print("\n" + "="*50)
        print("⚙️  CONFIGURACIÓN DEL BOT")
        print("="*50)
        
        print(f"\n📁 Archivo: {self.config_path}")
        print(f"📊 Log level: {self.log_level}")
        print(f"🖥️  Monitor: {self.monitor_index}")
        print(f"🎯 Confianza detección: {self.detection_confidence}")
        print(f"⏱️  Intervalo: {self.detection_interval}s")
        
        print(f"\n❤️  HP emergencia: {self.emergency_hp_threshold}%")
        print(f"💙 MP emergencia: {self.emergency_mp_threshold}%")
        print(f"🩹 Auto-curación: {'✅' if self.auto_heal_enabled else '❌'}")
        print(f"🔵 Auto-maná: {'✅' if self.auto_mana_enabled else '❌'}")
        
        print("="*50)