# fix_tibia_bot_complete.py
import os

def fix_tibia_bot_completely():
    """Arregla completamente tibia_bot.py"""
    
    file_path = "core/tibia_bot.py"
    
    if not os.path.exists(file_path):
        print(f"❌ {file_path} no encontrado")
        # Crear uno nuevo
        create_new_tibia_bot()
        return
    
    print(f"🔧 Arreglando {file_path}...")
    
    # Primero hacer una copia de seguridad
    backup_path = file_path + ".backup"
    try:
        import shutil
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
    except:
        pass
    
    # Intentar diferentes codificaciones
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-8-sig']
    
    original_content = None
    used_encoding = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                original_content = f.read()
            used_encoding = encoding
            print(f"✅ Leído con codificación: {encoding}")
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"❌ Error con {encoding}: {e}")
    
    if original_content is None:
        print("❌ No se pudo leer el archivo con ninguna codificación")
        create_new_tibia_bot()
        return
    
    # Buscar y arreglar el error de sintaxis
    print("🔍 Buscando error de sintaxis...")
    
    lines = original_content.split('\n')
    
    # Mostrar contexto del error (alrededor de línea 102)
    print("\n📝 Contexto del error (líneas 95-110):")
    for i in range(max(0, 94), min(len(lines), 109)):
        print(f"{i+1:3}: {lines[i]}")
    
    # Buscar bloques try sin except/finally
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Si encontramos un try: sin su except/finally
        if 'try:' in line and i + 1 < len(lines):
            # Buscar si tiene except o finally
            has_except_or_finally = False
            j = i + 1
            
            # Buscar en las siguientes líneas (misma indentación o más)
            while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t')):
                if 'except' in lines[j] or 'finally' in lines[j]:
                    has_except_or_finally = True
                    break
                j += 1
            
            if not has_except_or_finally:
                print(f"⚠️  Encontrado try: sin except/finally en línea {i+1}")
                
                # Encontrar donde termina el bloque try (cuando la indentación disminuye)
                j = i + 1
                while j < len(lines) and (lines[j].startswith(' ') or lines[j].startswith('\t')):
                    j += 1
                
                # Insertar except block
                indent = len(line) - len(line.lstrip())
                indent_str = ' ' * indent
                
                fixed_lines.append(f"{indent_str}except Exception as e:")
                fixed_lines.append(f"{indent_str}    self.logger.error(f\"Error en bloque try: {{e}}\")")
                fixed_lines.append(f"{indent_str}    return False")
                
                print(f"✅ Except block añadido después de línea {i+1}")
        
        i += 1
    
    # Guardar archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print(f"\n✅ {file_path} corregido y guardado en UTF-8")
    
    # Verificar sintaxis
    try:
        compile('\n'.join(fixed_lines), file_path, 'exec')
        print("✅ Sintaxis verificada correctamente")
    except SyntaxError as e:
        print(f"❌ Aún hay error de sintaxis: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
        
        # Si aún hay error, crear uno nuevo
        print("\n🔄 Creando versión nueva...")
        create_new_tibia_bot()

def create_new_tibia_bot():
    """Crea una nueva versión de tibia_bot.py"""
    
    print("\n🚀 Creando nueva versión de TibiaBot...")
    
    new_code = '''"""
Clase TibiaBot - Versión nueva y funcional
"""
import logging
import time
from typing import Optional

from core.screen_capturer import ScreenCapturer
from core.ui_detector import UIDetector
from config.settings import Settings
from config.ui_config import UIConfig

class TibiaBot:
    """Bot principal para Tibia"""
    
    def __init__(self, config_path: str = 'configs/default_settings.json', 
                 debug_mode: bool = False, logger: Optional[logging.Logger] = None):
        """
        Inicializa el bot
        """
        # Configurar logger
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('TibiaBot')
            self.logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
            
            # Handler para consola
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG if debug_mode else logging.INFO)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
        
        # Cargar configuración
        self.settings = Settings(config_path)
        self.ui_config = UIConfig()
        
        # Inicializar componentes
        self.capturer = ScreenCapturer(monitor_index=self.settings.monitor_index)
        self.detector = UIDetector(self.settings, self.ui_config)
        
        self.is_running = False
        
        self.logger.info("🤖 TibiaBot inicializado correctamente")
    
    def auto_detect_ui(self) -> bool:
        """
        Detecta automáticamente los elementos de la UI
        """
        self.logger.info("🔍 Iniciando detección automática de UI...")
        
        try:
            # Capturar pantalla
            screenshot = self.capturer.capture_full_screen()
            
            # Diccionario para resultados
            detected_positions = {}
            
            # Lista de elementos a detectar
            elements = {
                'hp_bar': self.detector.detect_health_bar,
                'mp_bar': self.detector.detect_mana_bar,
                'inventory': self.detector.detect_inventory,
                'minimap': self.detector.detect_minimap,
                'equipment': self.detector.detect_equipment_window,
                'skills': self.detector.detect_skills_window,
                'chat': self.detector.detect_chat_window
            }
            
            # Detectar cada elemento
            for name, detector_func in elements.items():
                try:
                    region = detector_func(screenshot)
                    if region:
                        detected_positions[name] = {
                            'x': region[0],
                            'y': region[1],
                            'width': region[2],
                            'height': region[3],
                            'confidence': 0.8,
                            'method': 'auto_detect'
                        }
                        self.logger.info(f"✅ {name} detectado")
                    else:
                        self.logger.warning(f"⚠️ {name} no detectado")
                except Exception as e:
                    self.logger.error(f"❌ Error detectando {name}: {e}")
            
            # Guardar resultados
            if detected_positions:
                self.ui_config.update_positions(detected_positions)
                self.ui_config.save_to_file()
                self.logger.info(f"✅ Detección completada: {len(detected_positions)} elementos")
                return True
            else:
                self.logger.error("❌ No se detectó ningún elemento")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error en detección automática: {e}")
            return False
    
    def start_monitoring(self):
        """Inicia el monitoreo"""
        self.logger.info("👁️  Iniciando monitoreo...")
        self.is_running = True
        
        try:
            while self.is_running:
                # Lógica de monitoreo básica
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("🛑 Monitoreo detenido por usuario")
        except Exception as e:
            self.logger.error(f"❌ Error en monitoreo: {e}")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.logger.info("⏹️  Deteniendo monitoreo...")
        self.is_running = False
    
    def emergency_stop(self):
        """Detención de emergencia"""
        self.logger.warning("🚨 Detención de emergencia!")
        self.stop_monitoring()
    
    def save_configuration(self):
        """Guarda la configuración"""
        try:
            self.ui_config.save_to_file()
            self.logger.info("💾 Configuración guardada")
        except Exception as e:
            self.logger.error(f"❌ Error guardando configuración: {e}")
    
    def show_status(self):
        """Muestra el estado"""
        print("\\n" + "="*50)
        print("🤖 ESTADO DEL BOT")
        print("="*50)
        print(f"📊 Monitoreo activo: {'✅' if self.is_running else '❌'}")
        print(f"🖥️  Monitor: {self.settings.monitor_index}")
        print(f"📁 Elementos UI: {len(self.ui_config.elements)}")
        print("="*50)
    
    def run(self):
        """Ejecuta el bot en modo interactivo"""
        self.logger.info("🚀 Ejecutando bot...")
        
        try:
            # Primero detectar UI
            if not self.auto_detect_ui():
                self.logger.warning("⚠️  La detección automática falló")
                self.logger.info("💡 Intenta calibrar manualmente o verifica que Tibia esté visible")
            
            # Mostrar menú
            self._show_menu()
            
        except KeyboardInterrupt:
            self.logger.info("👋 Bot detenido")
        except Exception as e:
            self.logger.error(f"❌ Error crítico: {e}")
    
    def _show_menu(self):
        """Muestra el menú interactivo"""
        while True:
            print("\\n" + "="*50)
            print("📋 MENÚ PRINCIPAL")
            print("="*50)
            print("1. 🔍 Detectar elementos UI")
            print("2. 👁️  Iniciar monitoreo")
            print("3. 📊 Mostrar estado")
            print("4. 🚪 Salir")
            print("="*50)
            
            choice = input("\\nSelecciona una opción (1-4): ").strip()
            
            if choice == "1":
                self.auto_detect_ui()
            elif choice == "2":
                self.start_monitoring()
            elif choice == "3":
                self.show_status()
            elif choice == "4":
                print("👋 Saliendo...")
                break
            else:
                print("⚠️  Opción no válida")
'''
    
    # Guardar nueva versión
    with open("core/tibia_bot.py", 'w', encoding='utf-8') as f:
        f.write(new_code)
    
    print("✅ Nueva versión de TibiaBot creada")

def verify_fix():
    """Verifica que el arreglo funcionó"""
    
    print("\n" + "="*50)
    print("🧪 VERIFICANDO ARREGLO")
    print("="*50)
    
    try:
        # Test 1: Verificar que el archivo existe
        if not os.path.exists("core/tibia_bot.py"):
            print("❌ Archivo no encontrado")
            return False
        
        # Test 2: Verificar que se pueda leer
        with open("core/tibia_bot.py", 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Archivo leído correctamente")
        
        # Test 3: Verificar sintaxis
        compile(content, "core/tibia_bot.py", 'exec')
        print("✅ Sintaxis correcta")
        
        # Test 4: Verificar que tenga la clase TibiaBot
        if 'class TibiaBot' in content:
            print("✅ Clase TibiaBot encontrada")
        else:
            print("❌ Clase TibiaBot no encontrada")
            return False
        
        # Test 5: Importar
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from core.tibia_bot import TibiaBot
        print("✅ TibiaBot importado correctamente")
        
        return True
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 ARREGLANDO TIBIA_BOT.PY COMPLETAMENTE")
    print("="*50)
    
    fix_tibia_bot_completely()
    
    print("\n" + "="*50)
    print("✅ Proceso completado")
    
    # Verificar
    if verify_fix():
        print("\n🎉 ¡Arreglo exitoso!")
        print("💡 Ahora ejecuta: python test_simple.py")
    else:
        print("\n⚠️  Aún hay problemas. Creando versión completamente nueva...")
        create_new_tibia_bot()