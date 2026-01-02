# fix_errors.py
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_and_fix():
    """Verifica y corrige errores comunes"""
    
    # 1. Verificar que existan los directorios necesarios
    directories = ['templates', 'configs', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Directorio creado: {directory}")
    
    # 2. Verificar archivos de plantilla mínimos
    templates_needed = ['hp_bar_segment.png', 'mp_bar_segment.png']
    for template in templates_needed:
        template_path = os.path.join('templates', template)
        if not os.path.exists(template_path):
            # Crear plantilla dummy (rectángulo rojo/azul)
            import cv2
            import numpy as np
            
            if 'hp' in template:
                color = (0, 0, 255)  # Rojo en BGR
            else:
                color = (255, 0, 0)  # Azul en BGR
            
            dummy_template = np.ones((20, 100, 3), dtype=np.uint8) * color
            cv2.imwrite(template_path, dummy_template)
            print(f"⚠️ Plantilla dummy creada: {template_path}")
    
    # 3. Verificar archivo de configuración UI
    ui_config_path = 'configs/ui_positions.json'
    if not os.path.exists(ui_config_path):
        import json
        default_config = {
            "screen": {
                "width": 1920,
                "height": 1080
            },
            "elements": []
        }
        with open(ui_config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"✅ Configuración UI creada: {ui_config_path}")
    
    print("\n✅ Verificación completada. Ejecuta main.py para probar.")

if __name__ == "__main__":
    check_and_fix()