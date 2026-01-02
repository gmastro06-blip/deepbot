# test_run_fixed.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bot():
    print("🧪 Probando bot...")
    
    try:
        # Importar DENTRO de la función
        from core.tibia_bot import TibiaBot
        
        print("✅ TibiaBot importado exitosamente")
        
        # Crear instancia CON LOS PARÁMETROS CORRECTOS
        bot = TibiaBot(
            config_path="configs/default_settings.json",
            debug_mode=True,
            logger=None
        )
        
        print("✅ Instancia de TibiaBot creada correctamente")
        
        # Intentar detección automática
        print("🔍 Intentando detección automática...")
        success = bot.auto_detect_ui()
        
        if success:
            print("✅ Detección automática exitosa")
        else:
            print("⚠️  Detección automática falló")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bot()
    if success:
        print("\n🎉 ¡Prueba exitosa! Ahora ejecuta python main.py")
    else:
        print("\n💥 Prueba fallida. Revisa los errores.")