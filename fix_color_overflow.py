# fix_color_overflow.py
import numpy as np

def fix_color_detector_overflow():
    """Arregla el warning de overflow en color_detector.py"""
    
    file_path = "processors/color_detector.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar las líneas problemáticas
    old_code = '''        # Crear rango
        lower = np.array([
            max(0, hsv_color[0] - tolerance),
            max(0, hsv_color[1] - tolerance),
            max(0, hsv_color[2] - tolerance)
        ])
        
        upper = np.array([
            min(179, hsv_color[0] + tolerance),
            min(255, hsv_color[1] + tolerance),
            min(255, hsv_color[2] + tolerance)
        ])'''
    
    new_code = '''        # Crear rango (usar int para evitar overflow)
        lower = np.array([
            max(0, int(hsv_color[0]) - tolerance),
            max(0, int(hsv_color[1]) - tolerance),
            max(0, int(hsv_color[2]) - tolerance)
        ], dtype=np.int32)
        
        upper = np.array([
            min(179, int(hsv_color[0]) + tolerance),
            min(255, int(hsv_color[1]) + tolerance),
            min(255, int(hsv_color[2]) + tolerance)
        ], dtype=np.int32)'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ color_detector.py arreglado (overflow corregido)")
    else:
        print("⚠️  No se encontró el código a reemplazar")

if __name__ == "__main__":
    fix_color_detector_overflow()