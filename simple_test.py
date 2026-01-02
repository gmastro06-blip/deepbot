# simple_test.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Prueba simple del sistema...")

try:
    # Test 1: ScreenCapturer
    print("\n1. Probando ScreenCapturer...")
    from core.screen_capturer import ScreenCapturer
    capturer = ScreenCapturer(monitor_index=1)
    screenshot = capturer.capture_full_screen()
    print(f"✅ Captura: {screenshot.shape}")
    
    # Test 2: UIDetector
    print("\n2. Probando UIDetector...")
    from core.ui_detector import UIDetector
    
    # Crear settings dummy
    class DummySettings:
        def get_color(self, name, variant='full'):
            if name == 'hp':
                return (0, 0, 255)  # Rojo
            elif name == 'mp':
                return (255, 0, 0)  # Azul
            return (0, 0, 0)
    
    class DummyUIConfig:
        def get_position(self, name):
            return None
    
    settings = DummySettings()
    ui_config = DummyUIConfig()
    
    detector = UIDetector(settings, ui_config)
    print("✅ UIDetector creado")
    
    # Test 3: Métodos básicos
    print("\n3. Probando métodos básicos...")
    hp_region = detector.detect_health_bar(screenshot)
    print(f"   HP: {hp_region}")
    
    mp_region = detector.detect_mana_bar(screenshot)
    print(f"   MP: {mp_region}")
    
    # Test 4: TibiaBot
    print("\n4. Probando TibiaBot...")
    from core.tibia_bot import TibiaBot
    
    bot = TibiaBot(
        config_path="configs/default_settings.json",
        debug_mode=True,
        logger=None
    )
    print("✅ Bot creado")
    
    # Test 5: auto_detect_ui
    print("\n5. Probando auto_detect_ui...")
    success = bot.auto_detect_ui()
    print(f"   Resultado: {'Éxito' if success else 'Falló'}")
    
    print("\n🎉 ¡Prueba completada!")
    print("\n💡 Ahora puedes:")
    print("   1. Ejecutar: python main.py")
    print("   2. O calibrar: python calibrate_ui.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()