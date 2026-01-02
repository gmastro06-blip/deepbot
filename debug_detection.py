# debug_detection.py
import sys
import os
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_detection_components():
    print("🔍 Probando componentes de detección...")
    
    try:
        # 1. Test ScreenCapturer
        print("\n1. Probando ScreenCapturer:")
        from core.screen_capturer import ScreenCapturer
        capturer = ScreenCapturer(monitor_index=1)
        screenshot = capturer.capture_full_screen()
        print(f"   ✅ Captura exitosa: {screenshot.shape}")
        
        # 2. Test ColorDetector
        print("\n2. Probando ColorDetector:")
        from config.settings import Settings
        from processors.color_detector import ColorDetector
        settings = Settings()
        color_detector = ColorDetector(settings)
        print(f"   ✅ ColorDetector creado")
        print(f"   color_tolerance: {color_detector.color_tolerance}")
        print(f"   predefined_ranges keys: {list(color_detector.predefined_ranges.keys())[:3]}...")
        
        # 3. Test TemplateMatcher
        print("\n3. Probando TemplateMatcher:")
        from processors.template_matcher import TemplateMatcher
        template_matcher = TemplateMatcher()
        
        # Test match_template
        test_template = "templates/hp_bar_segment.png"
        if os.path.exists(test_template):
            result = template_matcher.match_template(screenshot, test_template, threshold=0.5)
            print(f"   ✅ match_template ejecutado: {result.get('found', False)}")
        else:
            print(f"   ⚠️  Plantilla no encontrada: {test_template}")
        
        # 4. Test UIDetector
        print("\n4. Probando UIDetector:")
        from config.ui_config import UIConfig
        from core.ui_detector import UIDetector
        
        ui_config = UIConfig()
        detector = UIDetector(settings, ui_config)
        
        # Verificar métodos
        methods = ['detect_health_bar', 'detect_mana_bar', 'detect_inventory', 
                  'detect_minimap', 'detect_equipment_window']
        
        for method in methods:
            if hasattr(detector, method):
                print(f"   ✅ {method} disponible")
            else:
                print(f"   ❌ {method} NO disponible")
        
        # 5. Test HealthDetector
        print("\n5. Probando HealthDetector:")
        from detectors.health_detector import HealthDetector
        health_detector = HealthDetector(settings)
        result = health_detector.detect(screenshot)
        print(f"   ✅ HealthDetector.detect(): conf={result.confidence}, region={result.region}")
        
        print("\n🎉 Todas las pruebas completadas!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detection_components()