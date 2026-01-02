# setup_and_test.py
import os
import cv2
import numpy as np

def create_dummy_templates():
    """Crea plantillas dummy para evitar errores"""
    
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    templates = {
        "hp_bar_segment.png": (20, 100, (0, 0, 255)),     # Rojo (BGR)
        "mp_bar_segment.png": (20, 100, (255, 0, 0)),     # Azul (BGR)
        "inventory_corner.png": (50, 50, (100, 100, 100)), # Gris (BGR)
        "minimap_circle.png": (100, 100, (0, 255, 0)),    # Verde (BGR)
    }
    
    for filename, (height, width, color) in templates.items():
        path = os.path.join(templates_dir, filename)
        
        if not os.path.exists(path):
            img = np.ones((height, width, 3), dtype=np.uint8) * color
            cv2.imwrite(path, img)
            print(f"✅ Plantilla dummy creada: {path}")
        else:
            print(f"✅ Plantilla ya existe: {path}")

def test_basic_system():
    """Prueba básica del sistema"""
    
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    print("\n🧪 Probando sistema básico...")
    
    try:
        # 1. ScreenCapturer
        print("\n1. Probando ScreenCapturer...")
        from core.screen_capturer import ScreenCapturer
        capturer = ScreenCapturer(monitor_index=1)
        screenshot = capturer.capture_full_screen()
        print(f"✅ Captura de pantalla: {screenshot.shape}")
        
        # 2. Configuración dummy para UIDetector
        print("\n2. Creando configuración dummy...")
        
        class DummySettings:
            def get_color(self, name, variant='full'):
                if name == 'hp':
                    return (0, 0, 255)  # Rojo en BGR
                elif name == 'mp':
                    return (255, 0, 0)  # Azul en BGR
                return (0, 0, 0)
            
            # Añadir otros atributos que podrían ser necesarios
            colors = {
                'hp': {'full': (0, 0, 255)},
                'mp': {'full': (255, 0, 0)}
            }
            color_tolerance = 30
            min_region_area = 100
        
        class DummyUIConfig:
            def get_position(self, name):
                return None
        
        settings = DummySettings()
        ui_config = DummyUIConfig()
        
        # 3. UIDetector
        print("\n3. Probando UIDetector...")
        from core.ui_detector import UIDetector
        detector = UIDetector(settings, ui_config)
        
        # Probar detecciones
        print("   Probando detección de HP...")
        hp_region = detector.detect_health_bar(screenshot)
        print(f"   Región HP: {hp_region}")
        
        print("   Probando detección de MP...")
        mp_region = detector.detect_mana_bar(screenshot)
        print(f"   Región MP: {mp_region}")
        
        # 4. TibiaBot
        print("\n4. Probando TibiaBot...")
        from core.tibia_bot import TibiaBot
        
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        print("✅ Bot creado")
        
        # 5. auto_detect_ui
        print("\n5. Probando auto_detect_ui...")
        success = bot.auto_detect_ui()
        print(f"✅ auto_detect_ui: {'Éxito' if success else 'Falló'}")
        
        if success:
            print("\n🎉 ¡El sistema básico funciona!")
            print("📋 Ahora puedes:")
            print("   1. Ejecutar el bot: python main.py")
            print("   2. Calibrar manualmente: python calibrate_ui.py")
        else:
            print("\n⚠️  Algunas funcionalidades podrían no estar completamente implementadas.")
            print("   Pero al menos el sistema se ejecuta sin errores críticos.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Configurando plantillas dummy...")
    create_dummy_templates()
    
    print("\n" + "="*50)
    test_basic_system()