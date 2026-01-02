# fix_missing_methods.py
import os

def add_missing_methods():
    file_path = "core/ui_detector.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Lista de métodos que deben estar presentes
    required_methods = [
        'detect_health_bar',
        'detect_mana_bar',
        'detect_inventory',
        'detect_minimap',
        'detect_equipment_window',
        'detect_skills_window',
        'detect_chat_window'
    ]
    
    # Verificar qué métodos ya están presentes
    existing_methods = []
    for method in required_methods:
        if f'def {method}' in content:
            existing_methods.append(method)
    
    # Si todos los métodos ya existen, no hay nada que hacer
    if set(required_methods) == set(existing_methods):
        print("✅ Todos los métodos requeridos ya existen en UIDetector.")
        return
    
    # Agregar los métodos faltantes
    lines = content.split('\n')
    new_lines = []
    
    # Encontrar la posición para insertar (después del último método existente o después de __init__)
    insert_index = 0
    for i, line in enumerate(lines):
        if 'def ' in line and any(method in line for method in required_methods):
            insert_index = i + 1
        # También queremos insertar después de __init__ si no hay métodos después
        if '__init__' in line:
            init_index = i
    
    # Si no encontramos un método existente, insertaremos después de __init__
    if insert_index == 0:
        insert_index = init_index + 1
    
    # Construir los métodos faltantes
    missing_methods = [m for m in required_methods if m not in existing_methods]
    
    # Crear una lista con los nuevos métodos
    new_methods_code = []
    for method in missing_methods:
        if method == 'detect_chat_window':
            code = '''    def detect_chat_window(self, screenshot):
        """
        Detecta la ventana de chat.
        """
        try:
            # Por ahora, retorna None ya que no está implementado
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ Detección de chat no implementada")
            return None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error detectando chat: {e}")
            return None'''
        else:
            # Para otros métodos, creamos un placeholder similar
            code = f'''    def {method}(self, screenshot):
        """
        Método {method} (placeholder).
        """
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("⚠️ {method} no implementado")
            return None
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {method}: {{e}}")
            return None'''
        
        new_methods_code.append(code)
    
    # Insertar los nuevos métodos
    lines.insert(insert_index, '\n\n'.join(new_methods_code))
    
    # Escribir el archivo de nuevo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Métodos agregados: {missing_methods}")

if __name__ == "__main__":
    add_missing_methods()