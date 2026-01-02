# create_default_config.py
import json
import os

def create_default_config():
    """Crea un archivo de configuración por defecto"""
    
    config = {
        "config_path": "configs/default_settings.json",
        "log_level": "INFO",
        "log_file": "logs/tibia_bot.log",
        "log_to_console": True,
        "monitor_index": 1,
        "capture_fps": 5,
        "capture_quality": 80,
        "detection_confidence": 0.7,
        "detection_interval": 0.5,
        "colors": {
            "hp": {
                "full": [50, 50, 200],
                "medium": [40, 40, 150],
                "low": [30, 30, 100],
                "critical": [20, 20, 80]
            },
            "mp": {
                "full": [200, 50, 50],
                "medium": [150, 40, 40],
                "low": [100, 30, 30],
                "critical": [80, 20, 20]
            }
        },
        "emergency_hp_threshold": 30,
        "emergency_mp_threshold": 20,
        "auto_heal_enabled": True,
        "auto_mana_enabled": True
    }
    
    # Asegurar que el directorio existe
    os.makedirs("configs", exist_ok=True)
    
    # Guardar configuración
    config_path = "configs/default_settings.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Archivo de configuración creado: {config_path}")
    print("📋 Contenido:")
    print(json.dumps(config, indent=2))
    
    # También crear directorio de logs
    os.makedirs("logs", exist_ok=True)
    print("✅ Directorio de logs creado")

if __name__ == "__main__":
    create_default_config()