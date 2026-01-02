# create_tibia_bot_structure.py
import os
from pathlib import Path

def create_file(rel_path: str, content: str = "", create_init: bool = False):
    """
    Crea un archivo en la ruta relativa dentro del proyecto.
    Si content es vacío y create_init=True, crea un __init__.py vacío.
    """
    base_dir = Path("DEEPBOT")
    full_path = base_dir / rel_path

    # Crear directorios padres si no existen
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Si es un __init__.py y no se pasó contenido, dejar vacío
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    marker = "📄" if full_path.suffix else "📁"
    print(f"{marker} Creado: {full_path}")

def create_structure():
    """Crea la estructura completa del proyecto DEEPBOT para un bot de Tibia"""
    
    base_dir = Path("DEEPBOT")
    
    # === Carpetas principales ===
    directories = [
        "templates",
        "debug",
        "configs",
        "logs",
        "tests",
        "modules",
        "modules/cavebot",
        "modules/healing",
        "modules/targeting",
        "modules/utils",
        "data",
        "data/maps",
        "data/items",
        "utils"
    ]
    
    for dir_path in directories:
        full_dir = base_dir / dir_path
        full_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Carpeta creada: {full_dir}")

    # === Archivos básicos ===
    
    # __init__.py en módulos para que sea paquete Python
    init_modules = [
        "modules/__init__.py",
        "modules/cavebot/__init__.py",
        "modules/healing/__init__.py",
        "modules/targeting/__init__.py",
        "modules/utils/__init__.py",
        "utils/__init__.py",
    ]
    
    for init_path in init_modules:
        create_file(init_path, "# Paquete Python\n")

    # Archivo de configuración ejemplo
    config_content = """{
    "game": {
        "client_path": "C:/Tibia/tibia.exe",
        "window_title": "Tibia",
        "process_name": "tibia.exe"
    },
    "bot": {
        "enabled": true,
        "debug_mode": false,
        "log_level": "INFO"
    },
    "healing": {
        "hp_threshold": 70,
        "mana_threshold": 50,
        "potions": {
            "strong_health": {"hotkey": "F1", "min_hp": 60},
            "ultimate_health": {"hotkey": "F2", "min_hp": 30}
        }
    },
    "cavebot": {
        "enabled": false,
        "waypoints_file": "data/waypoints.json"
    }
}"""
    create_file("configs/config.json", config_content)

    # Archivo principal del bot
    main_content = '''"""DEEPBOT - Bot avanzado para Tibia"""

from utils.logger import setup_logger
from modules.cavebot import CavebotModule
from modules.healing import HealingModule

def main():
    logger = setup_logger()
    logger.info("Iniciando DEEPBOT...")
    
    # Aquí se inicializarán los módulos
    healing = HealingModule()
    cavebot = CavebotModule()
    
    logger.info("Bot iniciado correctamente.")

if __name__ == "__main__":
    main()
'''
    create_file("main.py", main_content)

    # Logger básico
    logger_content = '''import logging
import os
from pathlib import Path

def setup_logger(name: str = "DEEPBOT", log_file: str = "logs/bot.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicados
    if logger.handlers:
        return logger
    
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    
    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    
    # File
    fh = logging.FileHandler(log_dir / log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger
'''
    create_file("utils/logger.py", logger_content)
