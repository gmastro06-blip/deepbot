# fix_tibia_bot.py
import os

def fix_tibia_bot_imports():
    """Arregla imports problemáticos en tibia_bot.py"""
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si hay imports problemáticos
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Mantener todos los imports excepto potencialmente problemáticos
            if line.strip().startswith('from config.ui_config import') or \
               line.strip().startswith('from .ui_config import'):
                print(f"⚠️  Modificando línea potencialmente problemática: {line.strip()}")
                # Cambiar a import absoluto
                fixed_lines.append("from config.ui_config import UIConfig")
            else:
                fixed_lines.append(line)
        
        # Guardar el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        
        print(f"✅ Archivo {file_path} procesado")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_tibia_bot_imports()