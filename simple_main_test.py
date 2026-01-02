# simple_main_test.py
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
