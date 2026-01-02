# final_test.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 Prueba final del sistema...")

try:
    # 1. Test imports básicos
    print("\n1. Probando imports...")
    import cv2
    import mss
    import numpy as np
    print("✅ OpenCV, MSS y NumPy importados")
    
    # 2. Test ScreenCapturer
    print("\n2. Probando ScreenCapturer...")
    from core.screen_capturer import ScreenCapturer
    capturer = ScreenCapturer(monitor_index=1)
    screenshot = capturer.capture_full_screen()
    print(f"✅ Captura exitosa: {screenshot.shape}")
    
    # 3. Test UIDetector
    print("\n3. Probando UIDetector...")
    from config.settings import Settings
    from config.ui_config import UIConfig
    from core.ui_detector import UIDetector
    
    settings = Settings()
    ui_config = UIConfig()
    detector = UIDetector(settings, ui_config)
    
    # Verificar métodos
    methods_to_check = [
        'detect_health_bar',
        'detect_mana_bar',
        'detect_inventory',
        'detect_minimap',
        'detect_equipment_window',
        'detect_skills_window'
    ]
    
    all_ok = True
    for method in methods_to_check:
        if hasattr(detector, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} - FALTANTE")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Faltan métodos en UIDetector")
        print("   Ejecuta: python fix_missing_methods.py")
        sys.exit(1)
    
    # 4. Test detección básica
    print("\n4. Probando detección básica...")
    try:
        hp_region = detector.detect_health_bar(screenshot)
        print(f"   HP detectado: {'Sí' if hp_region else 'No'}")
        
        mp_region = detector.detect_mana_bar(screenshot)
        print(f"   MP detectado: {'Sí' if mp_region else 'No'}")
    except Exception as e:
        print(f"   ⚠️  Error en detección: {e}")
    
    # 5. Test TibiaBot
    print("\n5. Probando TibiaBot...")
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(
        config_path="configs/default_settings.json",
        debug_mode=True,
        logger=None
    )
    
    print("✅ Bot creado exitosamente")
    
    # 6. Test auto_detect_ui
    print("\n6. Probando auto_detect_ui...")
    try:
        success = bot.auto_detect_ui()
        print(f"   Resultado: {'Éxito' if success else 'Falló'}")
    except Exception as e:
        print(f"   ❌ Error en auto_detect_ui: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 ¡Prueba completada!")
    print("\n📋 Resumen:")
    print("   - Dependencias: ✅")
    print("   - ScreenCapturer: ✅")
    print("   - UIDetector: ✅")
    print("   - TibiaBot: ✅")
    print("   - Auto-detección: " + ("✅" if success else "⚠️"))
    
    if success:
        print("\n🚀 ¡El bot está listo! Ejecuta: python main.py")
    else:
        print("\n🔧 Algunas funcionalidades necesitan ajustes.")
        print("   Ejecuta: python calibrate_ui.py (si existe)")
        
except ImportError as e:
    print(f"\n❌ Error de importación: {e}")
    print("\n💡 Instala las dependencias faltantes:")
    print("   pip install opencv-python mss numpy")
    
except Exception as e:
    print(f"\n❌ Error general: {e}")
    import traceback
    traceback.print_exc()
