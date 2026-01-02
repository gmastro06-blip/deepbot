"""
Clase BotState - Manejo del estado del bot y del personaje
"""
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

@dataclass
class CharacterStatus:
    """Estado actual del personaje"""
    timestamp: float
    hp_percentage: Optional[float] = None
    mp_percentage: Optional[float] = None
    inventory_open: Optional[bool] = None
    position: Optional[Dict[str, int]] = None
    target_exists: bool = False
    in_combat: bool = False
    in_safe_zone: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'timestamp': self.timestamp,
            'hp_percentage': self.hp_percentage,
            'mp_percentage': self.mp_percentage,
            'inventory_open': self.inventory_open,
            'position': self.position,
            'target_exists': self.target_exists,
            'in_combat': self.in_combat,
            'in_safe_zone': self.in_safe_zone,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat()
        }

@dataclass
class BotStatus:
    """Estado interno del bot"""
    is_running: bool = False
    is_monitoring: bool = False
    is_acting: bool = False
    last_update: float = field(default_factory=time.time)
    cycle_count: int = 0
    error_count: int = 0
    ui_elements_detected: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'is_running': self.is_running,
            'is_monitoring': self.is_monitoring,
            'is_acting': self.is_acting,
            'last_update': self.last_update,
            'cycle_count': self.cycle_count,
            'error_count': self.error_count,
            'ui_elements_detected': self.ui_elements_detected,
            'uptime': time.time() - self.last_update if self.is_running else 0
        }

class BotState:
    """Maneja el estado del bot y del personaje"""
    
    def __init__(self):
        self.character_status = CharacterStatus(timestamp=time.time())
        self.bot_status = BotStatus()
        self.status_history: List[CharacterStatus] = []
        self.max_history_size = 1000
        
        # Estadísticas
        self.stats = {
            'hp_low_count': 0,
            'mp_low_count': 0,
            'heals_performed': 0,
            'mana_potions_used': 0,
            'attacks_performed': 0,
            'errors_detected': 0,
            'start_time': time.time()
        }
        
        # Configuración de umbrales
        self.thresholds = {
            'low_hp': 50.0,
            'critical_hp': 30.0,
            'low_mp': 40.0,
            'hp_change_alert': 10.0,  # Cambio significativo en HP
            'mp_change_alert': 15.0   # Cambio significativo en MP
        }
        
        # Estado anterior para detección de cambios
        self.previous_status: Optional[CharacterStatus] = None
        
        print("🤖 BotState inicializado")
    
    def update_character_status(self, **kwargs):
        """
        Actualiza el estado del personaje
        
        Args:
            **kwargs: Campos a actualizar
        """
        # Guardar estado anterior
        self.previous_status = CharacterStatus(
            timestamp=self.character_status.timestamp,
            hp_percentage=self.character_status.hp_percentage,
            mp_percentage=self.character_status.mp_percentage,
            inventory_open=self.character_status.inventory_open,
            position=self.character_status.position.copy() if self.character_status.position else None,
            target_exists=self.character_status.target_exists,
            in_combat=self.character_status.in_combat,
            in_safe_zone=self.character_status.in_safe_zone
        )
        
        # Actualizar campos
        for key, value in kwargs.items():
            if hasattr(self.character_status, key):
                setattr(self.character_status, key, value)
        
        # Actualizar timestamp
        self.character_status.timestamp = time.time()
        
        # Agregar al historial
        self._add_to_history()
        
        # Actualizar estadísticas
        self._update_stats()
        
        # Detectar cambios significativos
        self._detect_significant_changes()
    
    def update_bot_status(self, **kwargs):
        """
        Actualiza el estado del bot
        
        Args:
            **kwargs: Campos a actualizar
        """
        for key, value in kwargs.items():
            if hasattr(self.bot_status, key):
                setattr(self.bot_status, key, value)
        
        self.bot_status.last_update = time.time()
    
    def _add_to_history(self):
        """Agrega el estado actual al historial"""
        # Crear una copia del estado actual
        status_copy = CharacterStatus(
            timestamp=self.character_status.timestamp,
            hp_percentage=self.character_status.hp_percentage,
            mp_percentage=self.character_status.mp_percentage,
            inventory_open=self.character_status.inventory_open,
            position=self.character_status.position.copy() if self.character_status.position else None,
            target_exists=self.character_status.target_exists,
            in_combat=self.character_status.in_combat,
            in_safe_zone=self.character_status.in_safe_zone
        )
        
        self.status_history.append(status_copy)
        
        # Mantener tamaño máximo
        if len(self.status_history) > self.max_history_size:
            self.status_history = self.status_history[-self.max_history_size:]
    
    def _update_stats(self):
        """Actualiza estadísticas basadas en el estado actual"""
        # Contar HP bajo
        if self.character_status.hp_percentage is not None:
            if self.character_status.hp_percentage < self.thresholds['low_hp']:
                self.stats['hp_low_count'] += 1
        
        # Contar MP bajo
        if self.character_status.mp_percentage is not None:
            if self.character_status.mp_percentage < self.thresholds['low_mp']:
                self.stats['mp_low_count'] += 1
    
    def _detect_significant_changes(self):
        """Detecta cambios significativos en el estado"""
        if self.previous_status is None:
            return
        
        changes = []
        
        # Detectar cambio significativo en HP
        if (self.character_status.hp_percentage is not None and 
            self.previous_status.hp_percentage is not None):
            hp_change = abs(self.character_status.hp_percentage - self.previous_status.hp_percentage)
            if hp_change >= self.thresholds['hp_change_alert']:
                changes.append(f"HP cambió {hp_change:.1f}%")
        
        # Detectar cambio significativo en MP
        if (self.character_status.mp_percentage is not None and 
            self.previous_status.mp_percentage is not None):
            mp_change = abs(self.character_status.mp_percentage - self.previous_status.mp_percentage)
            if mp_change >= self.thresholds['mp_change_alert']:
                changes.append(f"MP cambió {mp_change:.1f}%")
        
        # Detectar cambio en posición
        if (self.character_status.position and self.previous_status.position):
            pos1 = self.character_status.position
            pos2 = self.previous_status.position
            if pos1.get('x') != pos2.get('x') or pos1.get('y') != pos2.get('y'):
                changes.append(f"Posición cambió a ({pos1.get('x')}, {pos1.get('y')})")
        
        # Detectar cambio en inventario
        if (self.character_status.inventory_open is not None and 
            self.previous_status.inventory_open is not None and
            self.character_status.inventory_open != self.previous_status.inventory_open):
            state = "ABIERTO" if self.character_status.inventory_open else "CERRADO"
            changes.append(f"Inventario {state}")
        
        # Si hay cambios, imprimirlos
        if changes:
            print(f"📈 Cambios detectados: {', '.join(changes)}")
    
    def get_character_status(self) -> CharacterStatus:
        """Obtiene el estado actual del personaje"""
        return self.character_status
    
    def get_bot_status(self) -> BotStatus:
        """Obtiene el estado actual del bot"""
        return self.bot_status
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene las estadísticas acumuladas"""
        current_time = time.time()
        uptime = current_time - self.stats['start_time']
        
        stats_copy = self.stats.copy()
        stats_copy['uptime_seconds'] = uptime
        stats_copy['uptime_human'] = str(timedelta(seconds=int(uptime)))
        stats_copy['average_cycle_time'] = (
            uptime / self.bot_status.cycle_count if self.bot_status.cycle_count > 0 else 0
        )
        
        return stats_copy
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen completo del estado"""
        return {
            'character': self.character_status.to_dict(),
            'bot': self.bot_status.to_dict(),
            'stats': self.get_stats(),
            'history_size': len(self.status_history),
            'thresholds': self.thresholds
        }
    
    def is_hp_low(self) -> bool:
        """Verifica si el HP está bajo"""
        if self.character_status.hp_percentage is None:
            return False
        return self.character_status.hp_percentage < self.thresholds['low_hp']
    
    def is_hp_critical(self) -> bool:
        """Verifica si el HP es crítico"""
        if self.character_status.hp_percentage is None:
            return False
        return self.character_status.hp_percentage < self.thresholds['critical_hp']
    
    def is_mp_low(self) -> bool:
        """Verifica si el MP está bajo"""
        if self.character_status.mp_percentage is None:
            return False
        return self.character_status.mp_percentage < self.thresholds['low_mp']
    
    def should_heal(self) -> bool:
        """Determina si se debe curar"""
        return self.is_hp_low()
    
    def should_use_mana_potion(self) -> bool:
        """Determina si se debe usar poción de maná"""
        return self.is_mp_low()
    
    def get_status_history(self, limit: int = 100) -> List[CharacterStatus]:
        """
        Obtiene el historial de estados
        
        Args:
            limit: Número máximo de estados a devolver
        
        Returns:
            Lista de estados históricos
        """
        return self.status_history[-limit:] if self.status_history else []
    
    def save_state_to_file(self, filename: str = None):
        """
        Guarda el estado actual en un archivo
        
        Args:
            filename: Nombre del archivo (None = auto-generado)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/bot_state_{timestamp}.json"
        
        try:
            data = {
                'character_status': self.character_status.to_dict(),
                'bot_status': self.bot_status.to_dict(),
                'stats': self.stats,
                'thresholds': self.thresholds,
                'save_timestamp': time.time(),
                'save_datetime': datetime.now().isoformat()
            }
            
            # Asegurar que el directorio existe
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Estado guardado en {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando estado: {e}")
            return False
    
    def load_state_from_file(self, filename: str) -> bool:
        """
        Carga el estado desde un archivo
        
        Args:
            filename: Nombre del archivo
        
        Returns:
            True si se cargó exitosamente
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar estado del personaje
            char_data = data.get('character_status', {})
            self.character_status = CharacterStatus(
                timestamp=char_data.get('timestamp', time.time()),
                hp_percentage=char_data.get('hp_percentage'),
                mp_percentage=char_data.get('mp_percentage'),
                inventory_open=char_data.get('inventory_open'),
                position=char_data.get('position'),
                target_exists=char_data.get('target_exists', False),
                in_combat=char_data.get('in_combat', False),
                in_safe_zone=char_data.get('in_safe_zone', False)
            )
            
            # Cargar estado del bot
            bot_data = data.get('bot_status', {})
            self.bot_status = BotStatus(
                is_running=bot_data.get('is_running', False),
                is_monitoring=bot_data.get('is_monitoring', False),
                is_acting=bot_data.get('is_acting', False),
                last_update=bot_data.get('last_update', time.time()),
                cycle_count=bot_data.get('cycle_count', 0),
                error_count=bot_data.get('error_count', 0),
                ui_elements_detected=bot_data.get('ui_elements_detected', 0)
            )
            
            # Cargar estadísticas
            self.stats = data.get('stats', self.stats.copy())
            
            # Cargar umbrales
            self.thresholds = data.get('thresholds', self.thresholds.copy())
            
            print(f"📂 Estado cargado desde {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando estado: {e}")
            return False
    
    def print_status_summary(self):
        """Imprime un resumen del estado actual"""
        char = self.character_status
        bot = self.bot_status
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("🤖 RESUMEN DE ESTADO DEL BOT")
        print("="*60)
        
        # Estado del personaje
        print(f"\n🎮 PERSONAJE:")
        hp_str = f"{char.hp_percentage:.1f}%" if char.hp_percentage is not None else "?"
        mp_str = f"{char.mp_percentage:.1f}%" if char.mp_percentage is not None else "?"
        
        hp_icon = "❤️"
        mp_icon = "💙"
        
        if self.is_hp_critical():
            hp_icon = "💔"
        elif self.is_hp_low():
            hp_icon = "🩸"
        
        if self.is_mp_low():
            mp_icon = "💧"
        
        print(f"  {hp_icon} HP: {hp_str}")
        print(f"  {mp_icon} MP: {mp_str}")
        
        if char.position:
            print(f"  📍 Posición: ({char.position.get('x', '?')}, {char.position.get('y', '?')})")
        
        print(f"  📦 Inventario: {'ABIERTO' if char.inventory_open else 'CERRADO'}")
        print(f"  ⚔️  Combate: {'✅ SÍ' if char.in_combat else '❌ NO'}")
        print(f"  🛡️  Zona segura: {'✅ SÍ' if char.in_safe_zone else '❌ NO'}")
        
        # Estado del bot
        print(f"\n🤖 BOT:")
        print(f"  🏃 Ejecutándose: {'✅ SÍ' if bot.is_running else '❌ NO'}")
        print(f"  👁️  Monitoreando: {'✅ SÍ' if bot.is_monitoring else '❌ NO'}")
        print(f"  🎯 Actuando: {'✅ SÍ' if bot.is_acting else '❌ NO'}")
        print(f"  🔄 Ciclos: {bot.cycle_count}")
        print(f"  ⚠️  Errores: {bot.error_count}")
        print(f"  🔍 Elementos UI: {bot.ui_elements_detected}")
        
        # Estadísticas
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"  ⏱️  Tiempo activo: {stats['uptime_human']}")
        print(f"  🩸 HP bajo: {stats['hp_low_count']} veces")
        print(f"  💧 MP bajo: {stats['mp_low_count']} veces")
        print(f"  💊 Curas: {stats['heals_performed']}")
        print(f"  🧪 Poción maná: {stats['mana_potions_used']}")
        print(f"  ⚔️  Ataques: {stats['attacks_performed']}")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        if self.should_heal():
            print(f"  ⚠️  ¡HP bajo! Considera curar.")
        if self.should_use_mana_potion():
            print(f"  ⚠️  ¡MP bajo! Considera usar poción de maná.")
        if not self.should_heal() and not self.should_use_mana_potion():
            print(f"  ✅ Estado estable. Continuar monitoreo.")
        
        print("="*60)
    
    def reset(self):
        """Reinicia el estado del bot"""
        self.__init__()  # Reinicializar
        print("🔄 Estado del bot reiniciado")


# Exportar la clase principal
__all__ = ['BotState', 'CharacterStatus', 'BotStatus']