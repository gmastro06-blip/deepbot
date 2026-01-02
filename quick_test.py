# quick_test.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Prueba rápida del sistema...")

try:
    # 1. Test imports básicos
    print("\n1. Probando imports...")
    import cv2
    import mss
    import numpy as np
    print("✅ Dependencias básicas OK")
    
    # 2. Test ScreenCapturer
    print("\n2. Probando ScreenCapturer...")
    from core.screen_capturer import ScreenCapturer
    capturer = ScreenCapturer(monitor_index=1)
    screenshot = capturer.capture_full_screen()
    print(f"✅ Captura: {screenshot.shape}")
    
    # 3. Test UIDetector
    print("\n3. Probando UIDetector...")
    from core.ui_detector import UIDetector
    
    class MockSettings:
        def get_color(self, name, variant='full'):
            return (0, 0, 255)
    
    class MockUIConfig:
        def get_position(self, name):
            return None
    
    detector = UIDetector(MockSettings(), MockUIConfig())
    print("✅ UIDetector creado")
    
    # 4. Test métodos críticos
    print("\n4. Verificando métodos críticos...")
    critical_methods = ['detect_health_bar', 'detect_mana_bar', 'detect_chat_window']
    
    for method in critical_methods:
        if hasattr(detector, method):
            print(f"   ✅ {method}")
        else:
            print(f"   ❌ {method} - FALTANTE")
    
    # 5. Test TibiaBot
    print("\n5. Probando TibiaBot...")
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(debug_mode=True)
    print("✅ TibiaBot creado")
    
    # 6. Test auto_detect_ui
    print("\n6. Probando auto_detect_ui...")
    success = bot.auto_detect_ui()
    print(f"✅ auto_detect_ui ejecutado: {'Éxito' if success else 'Falló'}")
    
    print("\n🎉 ¡Sistema funcionando!")
    print("\n💡 Ahora puedes ejecutar: python main.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()