# calibrate_ui.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def calibrate_ui():
    """Herramienta simple de calibración"""
    
    print("🎯 Herramienta de calibración de UI")
    print("="*50)
    
    try:
        from core.screen_capturer import ScreenCapturer
        from config.ui_config import UIConfig
        
        # Inicializar
        capturer = ScreenCapturer(monitor_index=1)
        ui_config = UIConfig()
        
        # Capturar pantalla
        print("\n📸 Capturando pantalla...")
        screenshot = capturer.capture_full_screen()
        
        height, width = screenshot.shape[:2]
        print(f"✅ Resolución: {width}x{height}")
        
        # Elementos comunes con posiciones por defecto
        elements = {
            'hp_bar': {
                'name': 'Barra de Salud (HP)',
                'description': 'La barra roja de vida',
                'default': (width // 2 - 200, 50, 400, 20)
            },
            'mp_bar': {
                'name': 'Barra de Maná (MP)', 
                'description': 'La barra azul de maná',
                'default': (width // 2 - 200, 75, 400, 20)
            },
            'inventory': {
                'name': 'Inventario',
                'description': 'Ventana del inventario',
                'default': (width - 300, height - 400, 280, 380)
            },
            'minimap': {
                'name': 'Minimapa',
                'description': 'El mapa pequeño',
                'default': (width - 200, 50, 150, 150)
            }
        }
        
        print("\n📋 Elementos a calibrar:")
        for key, info in elements.items():
            print(f"   • {info['name']} - {info['description']}")
        
        response = input("\n¿Usar posiciones por defecto? (s/n): ").strip().lower()
        
        if response == 's':
            # Usar posiciones por defecto
            for key, info in elements.items():
                x, y, w, h = info['default']
                ui_config.add_element(
                    name=key,
                    x=x, y=y, width=w, height=h,
                    confidence=0.7,
                    method="default_position"
                )
                print(f"✅ {info['name']}: ({x}, {y}) {w}x{h}")
        else:
            # Calibrar manualmente
            print("\n🔧 Calibración manual seleccionada")
            print("💡 Necesitarías una interfaz gráfica para esto")
            print("   Por ahora usaremos posiciones por defecto")
            
            for key, info in elements.items():
                x, y, w, h = info['default']
                ui_config.add_element(
                    name=key,
                    x=x, y=y, width=w, height=h,
                    confidence=0.5,
                    method="manual_estimation"
                )
        
        # Guardar configuración
        ui_config.save_to_file()
        
        # Mostrar resumen
        print("\n📋 Resumen de calibración:")
        ui_config.print_summary()
        
        print("\n🎉 Calibración completada!")
        print("💡 Ahora ejecuta: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    calibrate_ui()