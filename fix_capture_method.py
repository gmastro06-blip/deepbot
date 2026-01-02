#!/usr/bin/env python3
"""
Script para corregir el nombre del método capture_full a capture_full_screen
"""
import os
import re

def fix_tibia_bot():
    """Corrige el método en tibia_bot.py"""
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    print(f"🔧 Corrigiendo {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar
    old_pattern = r'capture_full\(\)'
    new_pattern = 'capture_full_screen()'
    
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_pattern, content)
        print(f"✅ Reemplazado 'capture_full()' por 'capture_full_screen()'")
    else:
        print(f"⚠️  No se encontró 'capture_full()' en el archivo")
    
    # También verificar otros posibles errores
    corrections = [
        (r'capture_full\b', 'capture_full_screen'),
    ]
    
    for old, new in corrections:
        if re.search(old, content):
            content = re.sub(old, new, content)
            print(f"✅ Reemplazado '{old}' por '{new}'")
    
    # Guardar archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corregido exitosamente")
    return True

def check_screen_capturer():
    """Verifica que ScreenCapturer tenga el método correcto"""
    file_path = "core/screen_capturer.py"
    
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return False
    
    print(f"🔍 Verificando {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar que exista el método capture_full_screen
    if 'def capture_full_screen' in content:
        print("✅ Método 'capture_full_screen' encontrado en ScreenCapturer")
        return True
    else:
        print("❌ Método 'capture_full_screen' NO encontrado en ScreenCapturer")
        
        # Verificar qué métodos tiene
        methods = re.findall(r'def (\w+)', content)
        print(f"📋 Métodos disponibles: {', '.join(methods)}")
        
        return False

def main():
    """Función principal"""
    print("🔧 CORRIGIENDO MÉTODO DE CAPTURA")
    print("=" * 50)
    
    # Paso 1: Verificar ScreenCapturer
    check_screen_capturer()
    
    # Paso 2: Corregir tibia_bot.py
    fix_tibia_bot()
    
    print("\n" + "=" * 50)
    print("🎉 ¡Corrección completada!")
    print("\n💡 Ahora puedes ejecutar:")
    print("   python main.py --auto-detect")
    print("=" * 50)

if __name__ == "__main__":
    main()