# final_check.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def final_check():
    print("🔍 Verificación final del sistema...")
    
    # 1. Verificar que todos los métodos existan
    print("\n1. Verificando métodos de UIDetector:")
    try:
        from core.ui_detector import UIDetector
        from config.settings import Settings
        from config.ui_config import UIConfig
        
        settings = Settings()
        ui_config = UIConfig()
        detector = UIDetector(settings, ui_config)
        
        required_methods = [
            'detect_health_bar',
            'detect_mana_bar', 
            'detect_inventory',
            'detect_minimap',
            'detect_equipment_window',
            'detect_skills_window'
        ]
        
        for method in required_methods:
            if hasattr(detector, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} - FALTANTE")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Verificar plantillas
    print("\n2. Verificando plantillas:")
    templates = [
        "templates/hp_bar_segment.png",
        "templates/mp_bar_segment.png", 
        "templates/inventory_corner.png",
        "templates/minimap_circle.png"
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} - NO EXISTE")
    
    # 3. Verificar TemplateMatcher
    print("\n3. Verificando TemplateMatcher:")
    try:
        from processors.template_matcher import TemplateMatcher
        matcher = TemplateMatcher()
        
        if hasattr(matcher, 'match_template'):
            print("   ✅ match_template disponible")
        else:
            print("   ❌ match_template NO disponible")
        
        if hasattr(matcher, 'match'):
            print("   ✅ match disponible")
        else:
            print("   ❌ match NO disponible")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Verificar ejecución del bot
    print("\n4. Probando creación del bot:")
    try:
        from core.tibia_bot import TibiaBot
        
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        print("   ✅ Bot creado exitosamente")
        
        if hasattr(bot, 'auto_detect_ui'):
            print("   ✅ auto_detect_ui disponible")
        else:
            print("   ❌ auto_detect_ui NO disponible")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Verificación completada!")

if __name__ == "__main__":
    final_check()