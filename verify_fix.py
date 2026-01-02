    # verify_fix.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verificando que todos los errores estén resueltos...")

try:
    # 1. Importar UIDetector
    from core.ui_detector import UIDetector
    
    # Mock objects
    class MockSettings:
        def get_color(self, name, variant='full'):
            return (0, 0, 255)
    
    class MockUIConfig:
        def get_position(self, name):
            return None
    
    # Crear detector
    detector = UIDetector(MockSettings(), MockUIConfig())
    
    # 2. Verificar métodos CRÍTICOS (los que causaban errores)
    critical_methods = [
        'detect_chat_window',
        'detect_skills_window', 
        'detect_equipment_window',
        'detect_health_bar',
        'detect_mana_bar',
        'detect_inventory',
        'detect_minimap'
    ]
    
    print("\n✅ Métodos críticos disponibles:")
    for method in critical_methods:
        if hasattr(detector, method):
            print(f"   ✓ {method}")
        else:
            print(f"   ✗ {method} - ¡ERROR CRÍTICO!")
    
    # 3. Test tibia_bot
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(
        config_path="configs/default_settings.json",
        debug_mode=False,
        logger=None
    )
    
    print("\n✅ TibiaBot creado exitosamente")
    
    # 4. Test auto_detect_ui
    print("\n🧪 Probando auto_detect_ui...")
    try:
        success = bot.auto_detect_ui()
        print(f"✅ auto_detect_ui ejecutado: {'Éxito' if success else 'Falló'}")
        
        if not success:
            print("💡 Esto es normal en la primera ejecución sin calibración")
    except AttributeError as e:
        print(f"❌ Error de atributo: {e}")
        print("\n💡 Probablemente aún falta algún método")
    except Exception as e:
        print(f"⚠️  Otro error: {e}")
    
    print("\n🎉 Verificación completada!")
    
except Exception as e:
    print(f"\n❌ Error durante la verificación: {e}")
    import traceback
    traceback.print_exc()