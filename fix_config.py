#!/usr/bin/env python3
"""
Script para arreglar problemas de configuración
"""
import os
import json
from pathlib import Path

def fix_settings_file():
    """Arregla el archivo settings.py"""
    settings_path = Path("config/settings.py")
    
    if not settings_path.exists():
        print("❌ Archivo config/settings.py no encontrado")
        return False
    
    print("🔧 Arreglando config/settings.py...")
    
    # Leer contenido actual
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar la definición de LogLevel
    if "class LogLevel(Enum):" in content:
        content = content.replace("class LogLevel(Enum):", "class LogLevel(str, Enum):")
        print("✅ LogLevel ahora hereda de str")
    
    # Asegurar que Settings tenga atributo colors inicializado
    if "colors: ColorSettings = field(default_factory=ColorSettings)" not in content:
        # Buscar la definición de la clase Settings
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "class Settings:" in line:
                # Insertar después de la clase
                insert_index = i + 2
                # Buscar donde empiezan los atributos
                for j in range(i, len(lines)):
                    if "log_level:" in lines[j]:
                        # Insertar después de los atributos principales
                        for k in range(j, len(lines)):
                            if lines[k].strip() == "" or "def __init__" in lines[k]:
                                insert_index = k
                                break
                        break
                
                # Insertar atributo colors si no existe
                if "colors:" not in content:
                    lines.insert(insert_index, "    colors: ColorSettings = field(default_factory=ColorSettings)")
                    print("✅ Añadido atributo 'colors' a Settings")
                
                break
        
        content = '\n'.join(lines)
    
    # Escribir archivo corregido
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ config/settings.py arreglado")
    return True

def fix_logger_file():
    """Arregla el archivo logger.py"""
    logger_path = Path("utils/logger.py")
    
    if not logger_path.exists():
        print("❌ Archivo utils/logger.py no encontrado")
        return False
    
    print("🔧 Arreglando utils/logger.py...")
    
    with open(logger_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar método set_level
    if "def set_level(self, level: str):" in content:
        # Reemplazar con versión que maneja LogLevel
        old_method = '''    def set_level(self, level: str):
        """Establece el nivel de logging"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))
        for handler in self.logger.handlers:
            handler.setLevel(level_map.get(level.upper(), logging.INFO))'''
        
        new_method = '''    def set_level(self, level):
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
            handler.setLevel(logging_level)'''
        
        content = content.replace(old_method, new_method)
        print("✅ Método set_level arreglado para manejar LogLevel")
    
    with open(logger_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ utils/logger.py arreglado")
    return True

def create_default_configs():
    """Crea archivos de configuración por defecto"""
    print("📝 Creando archivos de configuración por defecto...")
    
    # Crear directorio configs si no existe
    configs_dir = Path("configs")
    configs_dir.mkdir(exist_ok=True)
    
    # default_settings.json
    default_settings = {
        "log_level": "INFO",
        "debug_mode": False,
        "config_version": "1.0.0",
        "colors": {
            "hp_colors": [[50, 50, 200], [40, 40, 150], [30, 30, 100], [20, 20, 80]],
            "mp_colors": [[200, 100, 50], [150, 80, 40], [100, 60, 30], [80, 40, 20]],
            "color_tolerance": 40,
            "similarity_threshold": 0.7
        },
        "detection": {
            "preferred_method": "hybrid",
            "min_confidence": 0.6,
            "good_confidence": 0.8
        },
        "monitoring": {
            "monitoring_interval": 0.5,
            "low_hp_threshold": 50.0,
            "critical_hp_threshold": 30.0,
            "low_mana_threshold": 40.0
        },
        "actions": {
            "action_keys": {
                "heal": "F1",
                "mana_potion": "F2",
                "attack": "F3",
                "inventory": "F7"
            },
            "enable_auto_heal": True,
            "enable_auto_mana": True
        }
    }
    
    with open(configs_dir / "default_settings.json", 'w', encoding='utf-8') as f:
        json.dump(default_settings, f, indent=2)
    print("✅ configs/default_settings.json creado")
    
    # ui_positions.json (vacío)
    with open(configs_dir / "ui_positions.json", 'w', encoding='utf-8') as f:
        json.dump({}, f, indent=2)
    print("✅ configs/ui_positions.json creado")
    
    return True

def main():
    """Función principal"""
    print("🔧 ARREGLANDO CONFIGURACIÓN DEL BOT")
    print("=" * 50)
    
    # Paso 1: Arreglar settings.py
    fix_settings_file()
    
    # Paso 2: Arreglar logger.py
    fix_logger_file()
    
    # Paso 3: Crear archivos de configuración
    create_default_configs()
    
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración arreglada!")
    print("\n💡 Ahora puedes ejecutar:")
    print("   python main.py --auto-detect")
    print("=" * 50)

if __name__ == "__main__":
    main()