"""
Clase BotActions - Manejo de acciones automatizadas del bot
"""
import pyautogui
import time
import random
import threading
from typing import Optional, Dict, Tuple, List, Any
from dataclasses import dataclass
import keyboard
from pynput import mouse

from core.screen_capturer import ScreenCapturer
from config.settings import Settings
from utils.logger import AppLogger

@dataclass
class ActionResult:
    """Resultado de una acción"""
    success: bool
    message: str
    duration: float
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'success': self.success,
            'message': self.message,
            'duration': self.duration,
            'timestamp': self.timestamp
        }

class BotActions:
    """Clase para manejar todas las acciones automatizadas del bot"""
    
    def __init__(self, capturer: ScreenCapturer, settings: Settings, logger: AppLogger = None):
        """
        Inicializa el manejador de acciones
        
        Args:
            capturer: Instancia de ScreenCapturer
            settings: Configuración del bot
            logger: Logger para registro
        """
        self.capturer = capturer
        self.settings = settings
        self.logger = logger or AppLogger()
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Estado de las acciones
        self.is_acting = False
        self.action_queue = []
        self.action_history = []
        self.max_history_size = 100
        
        # Control de ratón y teclado
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Bloqueo para operaciones concurrentes
        self.action_lock = threading.Lock()
        
        self.logger.info("🤖 BotActions inicializado")
    
    def heal_character(self, heal_key: Optional[str] = None) -> ActionResult:
        """
        Cura al personaje
        
        Args:
            heal_key: Tecla para curar (None = usar configuración)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = heal_key or self.settings.get_action_key('heal')
            if not key:
                return ActionResult(False, "No hay tecla de cura configurada", 0, start_time)
            
            self.logger.debug(f"Curando con tecla: {key}")
            
            # Presionar tecla de cura
            pyautogui.press(key)
            
            # Pequeña pausa aleatoria para parecer humano
            self._human_delay(0.1, 0.3)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Personaje curado con {key}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error curando: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en heal_character: {e}")
            return result
    
    def use_mana_potion(self, mana_key: Optional[str] = None) -> ActionResult:
        """
        Usa una poción de maná
        
        Args:
            mana_key: Tecla para maná (None = usar configuración)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = mana_key or self.settings.get_action_key('mana_potion')
            if not key:
                return ActionResult(False, "No hay tecla de maná configurada", 0, start_time)
            
            self.logger.debug(f"Usando poción de maná con tecla: {key}")
            
            # Presionar tecla de maná
            pyautogui.press(key)
            
            self._human_delay(0.1, 0.3)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Poción de maná usada con {key}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error usando maná: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en use_mana_potion: {e}")
            return result
    
    def attack_target(self, attack_key: Optional[str] = None) -> ActionResult:
        """
        Ataca al objetivo actual
        
        Args:
            attack_key: Tecla de ataque (None = usar configuración)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = attack_key or self.settings.get_action_key('attack')
            if not key:
                return ActionResult(False, "No hay tecla de ataque configurada", 0, start_time)
            
            self.logger.debug(f"Atacando con tecla: {key}")
            
            # Presionar tecla de ataque
            pyautogui.press(key)
            
            self._human_delay(0.2, 0.5)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Ataque ejecutado con {key}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error atacando: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en attack_target: {e}")
            return result
    
    def loot_corpse(self, position: Optional[Tuple[int, int]] = None) -> ActionResult:
        """
        Lootea un cuerpo/cadáver
        
        Args:
            position: Posición donde hacer click (None = posición actual del ratón)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            self.logger.debug("Intentando lootear...")
            
            # Guardar posición actual del ratón
            original_pos = pyautogui.position()
            
            # Mover a la posición del cuerpo si se especifica
            if position:
                x, y = position
                pyautogui.moveTo(x, y, duration=0.2)
                self._human_delay(0.1, 0.2)
            
            # Ctrl + Click derecho (común para loot en Tibia)
            pyautogui.keyDown('ctrl')
            self._human_delay(0.1, 0.2)
            pyautogui.rightClick()
            self._human_delay(0.1, 0.2)
            pyautogui.keyUp('ctrl')
            
            # Volver a posición original
            if position:
                pyautogui.moveTo(original_pos, duration=0.2)
            
            self._human_delay(0.3, 0.5)
            
            duration = time.time() - start_time
            result = ActionResult(True, "Loot completado", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error looting: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en loot_corpse: {e}")
            return result
    
    def open_inventory(self, inventory_key: Optional[str] = None) -> ActionResult:
        """
        Abre o cierra el inventario
        
        Args:
            inventory_key: Tecla del inventario (None = usar configuración)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = inventory_key or self.settings.get_action_key('inventory')
            if not key:
                return ActionResult(False, "No hay tecla de inventario configurada", 0, start_time)
            
            self.logger.debug(f"Abriendo/cerrando inventario con tecla: {key}")
            
            # Presionar tecla del inventario
            pyautogui.press(key)
            
            # Esperar a que se abra/cierre
            self._human_delay(0.3, 0.5)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Inventario accionado con {key}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error con inventario: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en open_inventory: {e}")
            return result
    
    def move_to_position(self, screen_x: int, screen_y: int) -> ActionResult:
        """
        Mueve el personaje a una posición en pantalla
        
        Args:
            screen_x: Coordenada X en pantalla
            screen_y: Coordenada Y en pantalla
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            self.logger.debug(f"Moviendo a posición: ({screen_x}, {screen_y})")
            
            # Guardar posición actual
            original_x, original_y = pyautogui.position()
            
            # Mover ratón a la posición objetivo
            pyautogui.moveTo(screen_x, screen_y, duration=0.3)
            self._human_delay(0.1, 0.2)
            
            # Click izquierdo para mover
            pyautogui.click()
            
            # Pequeña pausa después del movimiento
            self._human_delay(0.5, 1.0)
            
            # Volver a posición original (opcional)
            # pyautogui.moveTo(original_x, original_y, duration=0.3)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Movido a ({screen_x}, {screen_y})", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error moviendo: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en move_to_position: {e}")
            return result
    
    def cast_spell(self, spell_key: str, target_pos: Optional[Tuple[int, int]] = None) -> ActionResult:
        """
        Lanza un hechizo
        
        Args:
            spell_key: Tecla del hechizo
            target_pos: Posición objetivo (None = objetivo actual)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            self.logger.debug(f"Lanzando hechizo con tecla: {spell_key}")
            
            # Presionar tecla del hechizo
            pyautogui.press(spell_key)
            self._human_delay(0.2, 0.3)
            
            # Si hay posición objetivo, hacer click
            if target_pos:
                x, y = target_pos
                pyautogui.click(x=x, y=y)
                self._human_delay(0.1, 0.2)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Hechizo {spell_key} lanzado", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error lanzando hechizo: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en cast_spell: {e}")
            return result
    
    def eat_food(self, food_key: Optional[str] = None) -> ActionResult:
        """
        Come comida
        
        Args:
            food_key: Tecla de comida (None = usar configuración)
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = food_key or self.settings.get_action_key('food')
            if not key:
                return ActionResult(False, "No hay tecla de comida configurada", 0, start_time)
            
            self.logger.debug(f"Comiendo con tecla: {key}")
            
            # Presionar tecla de comida
            pyautogui.press(key)
            
            # Comer toma tiempo
            self._human_delay(0.5, 1.0)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Comida consumida con {key}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error comiendo: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en eat_food: {e}")
            return result
    
    def use_hotkey(self, hotkey_name: str) -> ActionResult:
        """
        Usa un hotkey genérico
        
        Args:
            hotkey_name: Nombre del hotkey en la configuración
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            key = self.settings.get_action_key(hotkey_name)
            if not key:
                return ActionResult(False, f"No hay tecla configurada para {hotkey_name}", 0, start_time)
            
            self.logger.debug(f"Usando hotkey {hotkey_name} con tecla: {key}")
            
            # Presionar tecla
            pyautogui.press(key)
            
            self._human_delay(0.1, 0.3)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Hotkey {hotkey_name} ejecutado", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error usando hotkey: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en use_hotkey: {e}")
            return result
    
    def send_chat_message(self, message: str, channel: str = "local") -> ActionResult:
        """
        Envía un mensaje al chat
        
        Args:
            message: Mensaje a enviar
            channel: Canal ("local", "party", "guild", "trade")
        
        Returns:
            Resultado de la acción
        """
        start_time = time.time()
        
        try:
            self.logger.debug(f"Enviando mensaje al chat {channel}: {message[:50]}...")
            
            # Presionar Enter para abrir chat
            pyautogui.press('enter')
            self._human_delay(0.1, 0.2)
            
            # Escribir canal si es necesario
            if channel != "local":
                channel_prefix = {
                    "party": "!",
                    "guild": "@",
                    "trade": "#"
                }.get(channel, "")
                
                if channel_prefix:
                    pyautogui.write(channel_prefix)
                    self._human_delay(0.1, 0.2)
            
            # Escribir mensaje
            pyautogui.write(message)
            self._human_delay(0.1, 0.2)
            
            # Presionar Enter para enviar
            pyautogui.press('enter')
            
            self._human_delay(0.2, 0.4)
            
            duration = time.time() - start_time
            result = ActionResult(True, f"Mensaje enviado a {channel}", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error enviando mensaje: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en send_chat_message: {e}")
            return result
    
    def _human_delay(self, min_delay: float = 0.1, max_delay: float = 0.3):
        """
        Espera un tiempo aleatorio (para parecer más humano)
        
        Args:
            min_delay: Mínimo delay en segundos
            max_delay: Máximo delay en segundos
        """
        if self.settings.actions.human_like_variation > 0:
            variation = self.settings.actions.human_like_variation
            base_delay = random.uniform(min_delay, max_delay)
            random_factor = random.uniform(1 - variation, 1 + variation)
            delay = base_delay * random_factor
            time.sleep(max(0.01, delay))
        else:
            time.sleep(random.uniform(min_delay, max_delay))
    
    def _add_to_history(self, result: ActionResult):
        """Agrega un resultado al historial"""
        self.action_history.append(result)
        
        # Mantener tamaño máximo del historial
        if len(self.action_history) > self.max_history_size:
            self.action_history = self.action_history[-self.max_history_size:]
    
    def get_action_history(self, limit: int = 10) -> List[ActionResult]:
        """
        Obtiene el historial de acciones
        
        Args:
            limit: Número máximo de acciones a devolver
        
        Returns:
            Lista de acciones recientes
        """
        return self.action_history[-limit:] if self.action_history else []
    
    def clear_action_history(self):
        """Limpia el historial de acciones"""
        self.action_history.clear()
        self.logger.info("Historial de acciones limpiado")
    
    def start_emergency_listeners(self):
        """Inicia listeners de emergencia para detener el bot"""
        def on_mouse_click(x, y, button, pressed):
            if pressed and button == mouse.Button.middle:
                self.logger.warning("🚨 Click medio detectado - Parada de emergencia")
                self.emergency_stop()
                return False
        
        def on_key_press(key):
            try:
                if hasattr(key, 'char') and key.char == '`':
                    self.logger.warning("🚨 Tecla ` detectada - Parada de emergencia")
                    self.emergency_stop()
                    return False
            except:
                pass
        
        # Iniciar listeners
        self.mouse_listener = mouse.Listener(on_click=on_mouse_click)
        self.keyboard_listener = keyboard.on_press(on_key_press)
        
        self.mouse_listener.start()
        self.logger.info("Listeners de emergencia iniciados")
    
    def stop_emergency_listeners(self):
        """Detiene los listeners de emergencia"""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            keyboard.unhook_all()
        self.logger.info("Listeners de emergencia detenidos")
    
    def emergency_stop(self):
        """
        Detención de emergencia - detiene todas las acciones
        
        Returns:
            Resultado de la parada de emergencia
        """
        start_time = time.time()
        
        try:
            self.logger.warning("🚨 EJECUTANDO PARADA DE EMERGENCIA")
            
            # Detener cualquier acción en curso
            self.is_acting = False
            self.action_queue.clear()
            
            # Mover ratón a esquina (activar failsafe de pyautogui)
            screen_width, screen_height = self.capturer.get_screen_resolution()
            pyautogui.moveTo(10, 10, duration=0.1)
            
            # Presionar Escape para cancelar acciones
            pyautogui.press('esc')
            
            # Detener listeners
            self.stop_emergency_listeners()
            
            duration = time.time() - start_time
            result = ActionResult(True, "Parada de emergencia ejecutada", duration, start_time)
            self._add_to_history(result)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            result = ActionResult(False, f"Error en parada de emergencia: {e}", duration, start_time)
            self._add_to_history(result)
            self.logger.error(f"Error en emergency_stop: {e}")
            return result
    
    def execute_action_sequence(self, actions: List[Dict[str, Any]]) -> List[ActionResult]:
        """
        Ejecuta una secuencia de acciones
        
        Args:
            actions: Lista de diccionarios con acciones a ejecutar
        
        Returns:
            Lista de resultados
        """
        results = []
        
        for action in actions:
            action_type = action.get('type')
            params = action.get('params', {})
            
            if not action_type:
                continue
            
            # Ejecutar acción según tipo
            if action_type == 'heal':
                result = self.heal_character(**params)
            elif action_type == 'mana':
                result = self.use_mana_potion(**params)
            elif action_type == 'attack':
                result = self.attack_target(**params)
            elif action_type == 'loot':
                result = self.loot_corpse(**params)
            elif action_type == 'inventory':
                result = self.open_inventory(**params)
            elif action_type == 'move':
                result = self.move_to_position(**params)
            elif action_type == 'spell':
                result = self.cast_spell(**params)
            elif action_type == 'food':
                result = self.eat_food(**params)
            elif action_type == 'hotkey':
                result = self.use_hotkey(**params)
            elif action_type == 'chat':
                result = self.send_chat_message(**params)
            elif action_type == 'delay':
                delay = params.get('seconds', 1.0)
                time.sleep(delay)
                result = ActionResult(True, f"Delay de {delay}s completado", delay, time.time())
            else:
                result = ActionResult(False, f"Tipo de acción desconocido: {action_type}", 0, time.time())
            
            results.append(result)
            
            # Si una acción falla, podemos decidir continuar o parar
            if not result.success and action.get('stop_on_failure', False):
                break
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del manejador de acciones
        
        Returns:
            Diccionario con estado
        """
        return {
            'is_acting': self.is_acting,
            'queue_size': len(self.action_queue),
            'history_size': len(self.action_history),
            'emergency_listeners_active': self.mouse_listener is not None and self.mouse_listener.is_alive()
        }
    
    def print_status(self):
        """Imprime el estado actual del manejador de acciones"""
        status = self.get_status()
        
        print("\n" + "="*50)
        print("🎮 ESTADO DE ACCIONES DEL BOT")
        print("="*50)
        
        print(f"📊 Ejecutando acción: {'✅ SÍ' if status['is_acting'] else '❌ NO'}")
        print(f"📋 Cola de acciones: {status['queue_size']}")
        print(f"📜 Historial: {status['history_size']} acciones")
        print(f"🚨 Listeners emergencia: {'✅ ACTIVOS' if status['emergency_listeners_active'] else '❌ INACTIVOS'}")
        
        # Mostrar últimas 5 acciones
        recent_actions = self.get_action_history(5)
        if recent_actions:
            print(f"\n🕒 Últimas acciones:")
            for action in recent_actions:
                success_icon = "✅" if action.success else "❌"
                print(f"  {success_icon} {action.message} ({action.duration:.2f}s)")
        
        print("="*50)