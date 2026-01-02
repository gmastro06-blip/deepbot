# calibrate_manual.py
import sys
import os
import cv2
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def calibrate_manual():
    """Calibración manual de posiciones de UI"""
    
    print("🎯 CALIBRACIÓN MANUAL")
    print("=" * 50)
    
    try:
        from core.screen_capturer import ScreenCapturer
        
        # Capturar pantalla
        capturer = ScreenCapturer(monitor_index=1)
        screenshot = capturer.capture_full_screen()
        
        # Mostrar la captura
        cv2.imshow("Pantalla completa - Presiona 'q' para continuar", screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print("\n📝 Elementos a calibrar:")
        print("   1. Barra de HP (Salud)")
        print("   2. Barra de MP (Maná)")
        print("   3. Inventario")
        print("   4. Minimapa")
        print("   5. Equipo")
        print("   6. Habilidades")
        
        calibrations = {}
        
        for element in ['hp_bar', 'mp_bar', 'inventory', 'minimap', 'equipment', 'skills']:
            print(f"\n🎯 Calibrando: {element}")
            print("   Haz clic y arrastra para seleccionar el área, presiona 'Enter' para confirmar")
            
            # Usar OpenCV para seleccionar región
            clone = screenshot.copy()
            roi = cv2.selectROI(f"Selecciona {element}", clone)
            cv2.destroyAllWindows()
            
            if roi[2] > 0 and roi[3] > 0:  # Ancho y alto > 0
                x, y, w, h = roi
                calibrations[element] = {
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'confidence': 1.0,
                    'method': 'manual_calibration'
                }
                
                # Mostrar selección
                cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("Selección actual", screenshot)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
                
                print(f"   ✅ {element}: ({x}, {y}, {w}, {h})")
            else:
                print(f"   ⚠️  {element}: No seleccionado")
        
        # Guardar calibración
        if calibrations:
            config_path = "configs/ui_positions_calibrated.json"
            
            config = {
                'screen': {
                    'width': screenshot.shape[1],
                    'height': screenshot.shape[0]
                },
                'elements': calibrations
            }
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Calibración guardada en: {config_path}")
            print("\n📋 Para usar esta calibración:")
            print(f'   Cambia en tibia_bot.py: config_path="{config_path}"')
        else:
            print("\n⚠️  No se guardó ninguna calibración")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    calibrate_manual()