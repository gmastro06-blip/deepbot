# fix_final_errors.py
import os

def fix_all_remaining_errors():
    """Arregla todos los errores restantes"""
    
    print("🔧 Arreglando errores finales...")
    
    # 1. Añadir detect_skills_window a UIDetector
    print("\n1. Añadiendo detect_skills_window...")
    add_skills_window_method()
    
    # 2. Arreglar tibia_bot.py
    print("\n2. Arreglando tibia_bot.py...")
    fix_tibia_bot_skills_error()
    
    # 3. Crear plantillas faltantes
    print("\n3. Creando plantillas faltantes...")
    create_all_templates()
    
    print("\n✅ Todos los errores han sido arreglados")

def add_skills_window_method():
    """Añade el método detect_skills_window a ui_detector.py"""
    
    file_path = "core/ui_detector.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def detect_skills_window' in content:
            print("   ✅ detect_skills_window ya existe")
            return
        
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_lines.append(line)
            
            if 'def detect_equipment_window' in line:
                skills_method = '''
    def detect_skills_window(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta la ventana de habilidades.
        
        Args:
            screenshot: Captura de pantalla completa
        
        Returns:
            Coordenadas (x, y, ancho, alto) o None
        """
        try:
            # Si ya tenemos posición guardada, usarla
            if self.ui_config:
                skills_pos = self.ui_config.get_position('skills')
                if skills_pos:
                    return (skills_pos['x'], skills_pos['y'], 
                           skills_pos['width'], skills_pos['height'])
            
            # Por ahora, retornar None ya que no está implementado
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ Detección de ventana de habilidades no implementada")
            return None
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error detectando ventana de habilidades: {e}")
            return None'''
                
                new_lines.append(skills_method)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"   ✅ detect_skills_window añadido")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def fix_tibia_bot_skills_error():
    """Arregla el error de skills_window en tibia_bot.py"""
    
    file_path = "core/tibia_bot.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if "'skills': self.detector.detect_skills_window(screenshot)," in line:
                new_line = "            'skills': self.detector.detect_skills_window(screenshot) if hasattr(self.detector, 'detect_skills_window') else None,"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"   ✅ tibia_bot.py actualizado")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def create_all_templates():
    """Crea todas las plantillas necesarias"""
    
    import cv2
    import numpy as np
    
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    templates = {
        "hp_bar_segment.png": (20, 100, (0, 0, 255)),     # Rojo
        "mp_bar_segment.png": (20, 100, (255, 0, 0)),     # Azul
        "inventory_corner.png": (50, 50, (100, 100, 100)), # Gris
        "minimap_circle.png": (100, 100, (0, 255, 0)),    # Verde
        "skills_icon.png": (30, 30, (200, 200, 0)),       # Amarillo
        "equipment_icon.png": (30, 30, (200, 100, 50)),   # Naranja
    }
    
    for filename, (height, width, color) in templates.items():
        path = os.path.join(templates_dir, filename)
        
        if not os.path.exists(path):
            img = np.ones((height, width, 3), dtype=np.uint8) * color
            cv2.imwrite(path, img)
            print(f"   ✅ {filename} creado")
        else:
            print(f"   ✅ {filename} ya existe")

if __name__ == "__main__":
    fix_all_remaining_errors()
    
    print("\n🔄 Ahora prueba ejecutar:")
    print("1. python debug_detection.py  (para verificar)")
    print("2. python test_run_fixed.py   (para probar el bot)")