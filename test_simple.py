# test_simple.py
import sys
import os

# Añadir directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple():
    """Prueba simple del sistema"""
    
    print("🧪 Prueba simple del sistema...")
    print("="*50)
    
    try:
        # 1. Test importaciones básicas
        print("\n1. Probando importaciones...")
        import cv2
        import mss
        import numpy as np
        print("✅ OpenCV, MSS, NumPy importados")
        
        # 2. Test ScreenCapturer
        print("\n2. Probando ScreenCapturer...")
        from core.screen_capturer import ScreenCapturer
        capturer = ScreenCapturer(monitor_index=1)
        print("✅ ScreenCapturer creado")
        
        # 3. Test UIDetector
        print("\n3. Probando UIDetector...")
        from core.ui_detector import UIDetector
        from config.settings import Settings
        from config.ui_config import UIConfig
        
        settings = Settings()
        ui_config = UIConfig()
        detector = UIDetector(settings, ui_config)
        print("✅ UIDetector creado")
        
        # 4. Test TibiaBot
        print("\n4. Probando TibiaBot...")
        from core.tibia_bot import TibiaBot
        
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        print("✅ TibiaBot creado")
        
        # 5. Test auto_detect_ui
        print("\n5. Probando auto_detect_ui...")
        try:
            success = bot.auto_detect_ui()
            print(f"✅ auto_detect_ui ejecutado: {'Éxito' if success else 'Falló'}")
        except AttributeError as e:
            print(f"❌ Error de atributo: {e}")
            print("💡 Faltan métodos en UIDetector")
        except Exception as e:
            print(f"⚠️  Otro error: {e}")
        
        print("\n" + "="*50)
        print("🎉 ¡Prueba completada!")
        
        if success:
            print("\n🚀 ¡Sistema listo! Ejecuta: python main.py")
        else:
            print("\n💡 Sistema básico funciona, pero la detección necesita ajustes")
            print("   Ejecuta: python calibrate_ui.py para calibración manual")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}")
        print("\n💡 Instala las dependencias faltantes:")
        print("   pip install opencv-python mss numpy")
        return False
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple()
    
    if not success:
        print("\n🔧 Algunos problemas encontrados.")
        print("💡 Revisa los mensajes de error arriba.")