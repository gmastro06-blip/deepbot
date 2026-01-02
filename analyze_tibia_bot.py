# analyze_tibia_bot.py
import sys
import os
import inspect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def analyze_tibia_bot():
    """Analiza la clase TibiaBot"""
    
    print("🔍 Analizando TibiaBot...")
    
    try:
        from core.tibia_bot import TibiaBot
        
        print(f"✅ Clase: {TibiaBot}")
        print(f"📁 Módulo: {TibiaBot.__module__}")
        
        # Información del constructor
        print("\n🧱 CONSTRUCTOR __init__:")
        sig = inspect.signature(TibiaBot.__init__)
        print(f"   Firma: {sig}")
        
        print("\n   Parámetros:")
        for name, param in sig.parameters.items():
            if name != 'self':
                print(f"   - {name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'sin tipo'}")
                if param.default != inspect.Parameter.empty:
                    print(f"     Valor por defecto: {param.default}")
        
        # Métodos disponibles
        print("\n🔧 MÉTODOS DISPONIBLES:")
        methods = [m for m in dir(TibiaBot) if not m.startswith('_')]
        for method in methods:
            print(f"   • {method}")
        
        # Atributos
        print("\n📦 ATRIBUTOS (si hay instancia):")
        try:
            # Intentar crear instancia
            try:
                bot = TibiaBot()
            except TypeError:
                # Si falla, probar con parámetros comunes
                try:
                    from config.settings import Settings
                    bot = TibiaBot(settings=Settings())
                except:
                    bot = None
            
            if bot:
                attrs = [a for a in dir(bot) if not a.startswith('_') and not callable(getattr(bot, a))]
                for attr in attrs[:10]:  # Primeros 10 atributos
                    print(f"   • {attr}")
                if len(attrs) > 10:
                    print(f"   • ... y {len(attrs)-10} más")
        
        except Exception as e:
            print(f"   ❌ Error creando instancia: {e}")
        
    except ImportError as e:
        print(f"❌ Error importando TibiaBot: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_tibia_bot()