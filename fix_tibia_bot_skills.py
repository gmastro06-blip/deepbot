# fix_tibia_bot_skills.py
import os

def fix_tibia_bot_skills_error():
    """Arregla el error de skills_window en tibia_bot.py"""
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la línea con 'skills' en auto_detect_ui
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Reemplazar la línea problemática con manejo seguro
            if "'skills': self.detector.detect_skills_window(screenshot)," in line:
                new_line = "            'skills': self.detector.detect_skills_window(screenshot) if hasattr(self.detector, 'detect_skills_window') else None,"
                new_lines.append(new_line)
                print(f"✅ Línea corregida: {line.strip()} -> {new_line.strip()}")
            else:
                new_lines.append(line)
        
        # Guardar archivo actualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ {file_path} actualizado")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_tibia_bot_skills_error()