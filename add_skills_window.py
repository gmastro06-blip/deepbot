# add_skills_window.py
import os

def add_skills_window_method():
    """Añade el método detect_skills_window a ui_detector.py"""
    
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya tiene el método
        if 'def detect_skills_window' in content:
            print("✅ detect_skills_window ya existe")
            return
        
        # Buscar donde insertar (después de detect_equipment_window)
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            new_lines.append(line)
            
            # Insertar después de detect_equipment_window
            if 'def detect_equipment_window' in line:
                # Método detect_skills_window
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
        
        # Guardar archivo actualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ Método detect_skills_window añadido a {file_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_skills_window_method()