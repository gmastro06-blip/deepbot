"""
Configuración de posiciones de elementos de UI
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class UIElement:
    """Representa un elemento de la interfaz de usuario"""
    name: str
    x: int
    y: int
    width: int
    height: int
    confidence: float = 0.0
    detection_method: str = "unknown"
    last_detected: datetime = field(default_factory=datetime.now)
    
    @property
    def area(self) -> int:
        """Área del elemento en píxeles"""
        return self.width * self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        """Centro del elemento"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def bottom_right(self) -> Tuple[int, int]:
        """Esquina inferior derecha"""
        return (self.x + self.width, self.y + self.height)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'confidence': self.confidence,
            'detection_method': self.detection_method,
            'last_detected': self.last_detected.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UIElement':
        """Crea desde diccionario"""
        # Parsear fecha
        if 'last_detected' in data and isinstance(data['last_detected'], str):
            last_detected = datetime.fromisoformat(data['last_detected'])
        else:
            last_detected = datetime.now()
        
        return cls(
            name=data.get('name', ''),
            x=data.get('x', 0),
            y=data.get('y', 0),
            width=data.get('width', 0),
            height=data.get('height', 0),
            confidence=data.get('confidence', 0.0),
            detection_method=data.get('detection_method', 'unknown'),
            last_detected=last_detected
        )
    
    def contains_point(self, point_x: int, point_y: int) -> bool:
        """
        Verifica si un punto está dentro del elemento
        
        Args:
            point_x: Coordenada X del punto
            point_y: Coordenada Y del punto
        
        Returns:
            True si el punto está dentro
        """
        return (self.x <= point_x <= self.x + self.width and
                self.y <= point_y <= self.y + self.height)

class UIConfig:
    """Maneja la configuración de posiciones de UI"""
    
    def __init__(self, config_file: str = None):
        """
        Inicializa configuración de UI
        
        Args:
            config_file: Ruta al archivo de configuración
        """
        self.elements: Dict[str, UIElement] = {}
        self.config_file = config_file or "configs/ui_positions.json"
        self.screen_width: int = 1920
        self.screen_height: int = 1080
        self.loaded = False
        
        # Cargar si el archivo existe
        if Path(self.config_file).exists():
            self.load_from_file(self.config_file)
    
    def load_from_file(self, config_file: str = None) -> bool:
        """
        Carga configuración desde archivo JSON
        
        Args:
            config_file: Ruta al archivo (None = usar config por defecto)
        
        Returns:
            True si se cargó exitosamente
        """
        if config_file is None:
            config_file = self.config_file
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar elementos
            self.elements.clear()
            for element_data in data.get('elements', []):
                element = UIElement.from_dict(element_data)
                self.elements[element.name] = element
            
            # Cargar resolución de pantalla
            screen_info = data.get('screen', {})
            self.screen_width = screen_info.get('width', 1920)
            self.screen_height = screen_info.get('height', 1080)
            
            self.loaded = True
            print(f"✅ Configuración de UI cargada desde {config_file}")
            print(f"   Elementos: {len(self.elements)}")
            print(f"   Resolución: {self.screen_width}x{self.screen_height}")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error cargando configuración de UI: {e}")
            return False
    
    def save_to_file(self, config_file: str = None) -> bool:
        """
        Guarda configuración en archivo JSON
        
        Args:
            config_file: Ruta donde guardar (None = usar config por defecto)
        
        Returns:
            True si se guardó exitosamente
        """
        if config_file is None:
            config_file = self.config_file
        
        try:
            # Preparar datos
            data = {
                'screen': {
                    'width': self.screen_width,
                    'height': self.screen_height,
                    'timestamp': datetime.now().isoformat()
                },
                'elements': [element.to_dict() for element in self.elements.values()]
            }
            
            # Asegurar que el directorio existe
            Path(config_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar en archivo
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuración de UI guardada en {config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando configuración de UI: {e}")
            return False
    
    def add_element(self, name: str, x: int, y: int, width: int, height: int,
                   confidence: float = 1.0, method: str = "manual") -> UIElement:
        """
        Agrega o actualiza un elemento
        
        Args:
            name: Nombre del elemento
            x, y: Posición superior izquierda
            width, height: Tamaño
            confidence: Confianza de detección (0.0-1.0)
            method: Método de detección
        
        Returns:
            El elemento creado/actualizado
        """
        element = UIElement(
            name=name,
            x=x,
            y=y,
            width=width,
            height=height,
            confidence=confidence,
            detection_method=method,
            last_detected=datetime.now()
        )
        
        self.elements[name] = element
        return element
    
    def get_element(self, name: str) -> Optional[UIElement]:
        """
        Obtiene un elemento por nombre
        
        Args:
            name: Nombre del elemento
        
        Returns:
            UIElement o None si no existe
        """
        return self.elements.get(name)
    
    def get_position(self, name: str) -> Optional[Dict[str, int]]:
        """
        Obtiene la posición de un elemento
        
        Args:
            name: Nombre del elemento
        
        Returns:
            Diccionario con x, y, width, height o None
        """
        element = self.get_element(name)
        if element:
            return {
                'x': element.x,
                'y': element.y,
                'width': element.width,
                'height': element.height
            }
        return None
    
    def remove_element(self, name: str) -> bool:
        """
        Elimina un elemento
        
        Args:
            name: Nombre del elemento a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        if name in self.elements:
            del self.elements[name]
            return True
        return False
    
    def clear(self):
        """Elimina todos los elementos"""
        self.elements.clear()
        print("🧹 Configuración de UI limpiada")
    
    def update_positions(self, positions: Dict[str, Dict]):
        """
        Actualiza múltiples posiciones a la vez
        
        Args:
            positions: Diccionario con nombre -> posición
        """
        for name, pos_data in positions.items():
            if all(k in pos_data for k in ['x', 'y', 'width', 'height']):
                self.add_element(
                    name=name,
                    x=pos_data['x'],
                    y=pos_data['y'],
                    width=pos_data['width'],
                    height=pos_data['height'],
                    confidence=pos_data.get('confidence', 0.8),
                    method=pos_data.get('method', 'auto_detect')
                )
    
    def get_all_elements(self) -> List[UIElement]:
        """Obtiene todos los elementos"""
        return list(self.elements.values())
    
    def get_element_names(self) -> List[str]:
        """Obtiene nombres de todos los elementos"""
        return list(self.elements.keys())
    
    def has_element(self, name: str) -> bool:
        """Verifica si existe un elemento"""
        return name in self.elements
    
    def validate_positions(self, screen_width: int, screen_height: int) -> List[str]:
        """
        Valida que todas las posiciones estén dentro de la pantalla
        
        Args:
            screen_width: Ancho de pantalla actual
            screen_height: Alto de pantalla actual
        
        Returns:
            Lista de mensajes de error
        """
        errors = []
        
        for name, element in self.elements.items():
            # Verificar que esté dentro de los límites
            if element.x < 0:
                errors.append(f"{name}: x ({element.x}) no puede ser negativo")
            if element.y < 0:
                errors.append(f"{name}: y ({element.y}) no puede ser negativo")
            if element.x + element.width > screen_width:
                errors.append(f"{name}: ancho excede pantalla ({element.x + element.width} > {screen_width})")
            if element.y + element.height > screen_height:
                errors.append(f"{name}: alto excede pantalla ({element.y + element.height} > {screen_height})")
            
            # Verificar dimensiones razonables
            if element.width <= 0:
                errors.append(f"{name}: width debe ser mayor que 0")
            if element.height <= 0:
                errors.append(f"{name}: height debe ser mayor que 0")
        
        return errors
    
    def print_summary(self):
        """Imprime un resumen de la configuración"""
        if not self.elements:
            print("📭 No hay elementos configurados")
            return
        
        print("\n" + "="*50)
        print("🗺️  ELEMENTOS DE UI CONFIGURADOS")
        print("="*50)
        
        for name, element in self.elements.items():
            print(f"\n📌 {name}:")
            print(f"  Posición: ({element.x}, {element.y})")
            print(f"  Tamaño: {element.width}x{element.height}")
            print(f"  Confianza: {element.confidence:.1%}")
            print(f"  Método: {element.detection_method}")
            print(f"  Detectado: {element.last_detected.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("="*50)
    
    def find_element_at(self, x: int, y: int) -> Optional[str]:
        """
        Encuentra qué elemento contiene un punto
        
        Args:
            x, y: Coordenadas del punto
        
        Returns:
            Nombre del elemento o None
        """
        for name, element in self.elements.items():
            if element.contains_point(x, y):
                return name
        return None
    
    def calibrate_from_points(self, points: Dict[str, Tuple[int, int, int, int]]):
        """
        Calibra posiciones desde puntos seleccionados manualmente
        
        Args:
            points: Diccionario con nombre -> (x1, y1, x2, y2)
                   donde (x1, y1) es esquina superior izquierda
                   y (x2, y2) es esquina inferior derecha
        """
        for name, (x1, y1, x2, y2) in points.items():
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            x = min(x1, x2)
            y = min(y1, y2)
            
            self.add_element(
                name=name,
                x=x,
                y=y,
                width=width,
                height=height,
                confidence=1.0,
                method="manual_calibration"
            )
        
        print(f"✅ Calibración manual completada: {len(points)} elementos")

# Singleton global
_ui_config_instance: Optional[UIConfig] = None

def get_ui_config(config_file: str = None) -> UIConfig:
    """
    Obtiene la instancia singleton de UIConfig
    
    Args:
        config_file: Ruta al archivo de configuración
    
    Returns:
        Instancia de UIConfig
    """
    global _ui_config_instance
    
    if _ui_config_instance is None:
        _ui_config_instance = UIConfig(config_file)
    
    return _ui_config_instance