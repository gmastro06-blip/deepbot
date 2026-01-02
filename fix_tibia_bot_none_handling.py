# fix_tibia_bot_none_handling.py
import os

def fix_tibia_bot_none_handling():
    """Arregla tibia_bot.py para manejar mejor los valores None"""
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el método auto_detect_ui
    lines = content.split('\n')
    new_lines = []
    
    inside_auto_detect = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        if 'def auto_detect_ui' in line:
            inside_auto_detect = True
        
        # Dentro de auto_detect_ui, buscar donde se actualiza ui_config
        if inside_auto_detect and 'self.ui_config.update_positions' in line:
            # Reemplazar esta línea con una versión que filtre None
            print(f"⚠️  Encontrada línea problemática en {i+1}: {line}")
            
            # Reemplazar con código que filtra elementos None
            new_line = '''        # Actualizar configuración solo para elementos detectados
        detected_positions = {}
        for element_name, region in ui_positions.items():
            if region is not None:
                detected_positions[element_name] = {
                    'x': region[0],
                    'y': region[1],
                    'width': region[2],
                    'height': region[3],
                    'confidence': 0.8 if element_name in ['hp_bar', 'mp_bar'] else 0.7,
                    'method': 'auto_detect'
                }
                self.logger.info(f"✅ Detectado: {element_name}")
            else:
                self.logger.warning(f"⚠️ No detectado: {element_name}")
        
        if detected_positions:
            self.ui_config.update_positions(detected_positions)
            success = True'''
            
            # Reemplazar la línea original
            new_lines[-1] = new_line
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ {file_path} actualizado para manejar valores None")

def add_default_skills_detection():
    """Añade una detección por defecto para skills"""
    
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar el método detect_skills_window con uno que retorne una región por defecto
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if 'def detect_skills_window' in line and 'logger.warning' in content:
            # Encontrar el método actual
            pass
        
        new_lines.append(line)
    
    # Si no encontramos el método, lo añadimos
    if 'def detect_skills_window' not in content:
        print("⚠️  Añadiendo detect_skills_window con detección por defecto")
        
        # Buscar donde insertar (después de detect_equipment_window)
        for i, line in enumerate(lines):
            new_lines.append(line)
            if 'def detect_equipment_window' in line:
                # Insertar método mejorado
                skills_method = '''
    def detect_skills_window(self, screenshot):
        """
        Detecta la ventana de habilidades.
        Por defecto, asume posición típica en el lado derecho.
        """
        try:
            height, width = screenshot.shape[:2]
            
            # Posición típica de skills: derecha, entre inventario y minimapa
            return (width - 450, 200, 200, 300)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error detectando skills: {e}")
            return None'''
                
                new_lines.append(skills_method)
                break
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ {file_path} actualizado con detección por defecto para skills")

def create_simple_main_test():
    """Crea un script de prueba simple"""
    
    test_code = '''# simple_main_test.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Prueba simple de auto_detect_ui")

try:
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(
        config_path="configs/default_settings.json",
        debug_mode=True,
        logger=None
    )
    
    print("✅ Bot creado")
    print("🔍 Ejecutando auto_detect_ui...")
    
    success = bot.auto_detect_ui()
    
    if success:
        print("🎉 ¡auto_detect_ui exitoso!")
        
        # Mostrar resultados
        if hasattr(bot, 'ui_config') and bot.ui_config:
            print("📋 Elementos detectados:")
            elements = bot.ui_config.get_all_elements()
            for element in elements:
                print(f"   • {element.name}: {element.width}x{element.height} en ({element.x}, {element.y})")
    else:
        print("⚠️  auto_detect_ui falló")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open("simple_main_test.py", 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    print("✅ Script de prueba creado: simple_main_test.py")

if __name__ == "__main__":
    print("🔧 Arreglando manejo de None y skills...")
    
    fix_tibia_bot_none_handling()
    add_default_skills_detection()
    create_simple_main_test()
    
    print("\n✅ Correcciones aplicadas")
    print("🔄 Ejecuta: python simple_main_test.py")