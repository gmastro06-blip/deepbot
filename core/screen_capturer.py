"""
Clase ScreenCapturer - Manejo eficiente de capturas de pantalla
"""
import mss
import numpy as np
import cv2
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ScreenRegion:
    """Representa una región de la pantalla"""
    x: int
    y: int
    width: int
    height: int
    
    @property
    def area(self) -> int:
        """Calcula el área de la región"""
        return self.width * self.height
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return {
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ScreenRegion':
        """Crea desde diccionario"""
        return cls(
            x=data.get('x', 0),
            y=data.get('y', 0),
            width=data.get('width', 0),
            height=data.get('height', 0)
        )

class ScreenCapturer:
    """Maneja la captura de pantalla de manera eficiente"""
    
    def __init__(self, monitor_index: int = 1):
        """
        Inicializa el capturador de pantalla
        
        Args:
            monitor_index: Índice del monitor a capturar (1 = principal)
        """
        self.sct = mss.mss()
        self.monitor_index = monitor_index
        self.monitor_info = self._get_monitor_info()
        self.last_capture = None
        self.capture_count = 0
        
        print(f"✅ ScreenCapturer inicializado para monitor {monitor_index}")
        print(f"   Resolución: {self.monitor_info['width']}x{self.monitor_info['height']}")
    
    def _get_monitor_info(self) -> Dict:
        """Obtiene información del monitor"""
        if self.monitor_index < len(self.sct.monitors):
            return self.sct.monitors[self.monitor_index]
        return self.sct.monitors[1]  # Monitor principal por defecto
    
    def capture_full_screen(self) -> np.ndarray:
        """
        Captura toda la pantalla
        
        Returns:
            Imagen en formato numpy array (BGR)
        """
        try:
            # Capturar pantalla
            screenshot = self.sct.grab(self.monitor_info)
            
            # Convertir a numpy array
            img_array = np.array(screenshot)
            
            # Convertir de BGRA a BGR si es necesario
            if img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            self.last_capture = img_array
            self.capture_count += 1
            
            return img_array
            
        except Exception as e:
            raise RuntimeError(f"Error capturando pantalla completa: {e}")
    
    def capture_region(self, region: Union[Dict, ScreenRegion, Tuple]) -> np.ndarray:
        """
        Captura una región específica de la pantalla
        
        Args:
            region: Puede ser:
                   - Dict con keys: x, y, width, height
                   - Instancia de ScreenRegion
                   - Tuple: (x, y, width, height)
        
        Returns:
            Imagen de la región (BGR)
        """
        try:
            # Normalizar región a diccionario
            if isinstance(region, ScreenRegion):
                region_dict = region.to_dict()
            elif isinstance(region, tuple) and len(region) == 4:
                region_dict = {'x': region[0], 'y': region[1], 
                              'width': region[2], 'height': region[3]}
            else:
                region_dict = region
            
            # Crear monitor config para MSS
            monitor = {
                "top": region_dict['y'],
                "left": region_dict['x'],
                "width": region_dict['width'],
                "height": region_dict['height']
            }
            
            # Verificar que la región esté dentro de los límites
            self._validate_region(monitor)
            
            # Capturar región
            screenshot = self.sct.grab(monitor)
            img_array = np.array(screenshot)
            
            # Convertir color si es necesario
            if img_array.shape[2] == 4:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
            
            self.capture_count += 1
            
            return img_array
            
        except Exception as e:
            raise RuntimeError(f"Error capturando región {region}: {e}")
    
    def capture_multiple_regions(self, regions: Dict[str, Union[Dict, ScreenRegion]]) -> Dict[str, np.ndarray]:
        """
        Captura múltiples regiones eficientemente
        
        Args:
            regions: Diccionario con nombres y regiones
        
        Returns:
            Diccionario con imágenes capturadas
        """
        results = {}
        
        for name, region in regions.items():
            try:
                results[name] = self.capture_region(region)
            except Exception as e:
                print(f"⚠️ Error capturando región '{name}': {e}")
                results[name] = None
        
        return results
    
    def _validate_region(self, region: Dict) -> bool:
        """
        Valida que una región esté dentro de los límites de la pantalla
        
        Args:
            region: Región a validar
        
        Returns:
            True si la región es válida
        """
        screen_width = self.monitor_info['width']
        screen_height = self.monitor_info['height']
        
        if (region['left'] < 0 or region['top'] < 0 or
            region['left'] + region['width'] > screen_width or
            region['top'] + region['height'] > screen_height):
            raise ValueError(
                f"Región fuera de límites: {region}. "
                f"Pantalla: {screen_width}x{screen_height}"
            )
        return True
    
    def get_screen_resolution(self) -> Tuple[int, int]:
        """Obtiene la resolución de la pantalla"""
        return (self.monitor_info['width'], self.monitor_info['height'])
    
    def save_capture(self, image: np.ndarray, filename: str = None) -> str:
        """
        Guarda una captura en disco
        
        Args:
            image: Imagen a guardar
            filename: Nombre del archivo (opcional)
        
        Returns:
            Ruta del archivo guardado
        """
        if filename is None:
            filename = f"capture_{self.capture_count:06d}.png"
        
        output_dir = Path("debug/captures")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        try:
            cv2.imwrite(str(filepath), image)
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"Error guardando captura: {e}")
    
    def benchmark_capture(self, iterations: int = 100) -> Dict:
        """
        Realiza un benchmark de la captura de pantalla
        
        Args:
            iterations: Número de iteraciones
        
        Returns:
            Diccionario con resultados del benchmark
        """
        import time
        
        print(f"⏱️  Ejecutando benchmark ({iterations} iteraciones)...")
        
        times = []
        
        for i in range(iterations):
            start_time = time.perf_counter()
            self.capture_full_screen()
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # Convertir a ms
        
        # Calcular estadísticas
        avg_time = np.mean(times)
        min_time = np.min(times)
        max_time = np.max(times)
        std_time = np.std(times)
        
        results = {
            'iterations': iterations,
            'avg_ms': avg_time,
            'min_ms': min_time,
            'max_ms': max_time,
            'std_ms': std_time,
            'fps': 1000 / avg_time if avg_time > 0 else 0
        }
        
        print(f"✅ Benchmark completado:")
        print(f"   Tiempo promedio: {avg_time:.2f}ms ({results['fps']:.1f} FPS)")
        print(f"   Mejor tiempo: {min_time:.2f}ms")
        print(f"   Peor tiempo: {max_time:.2f}ms")
        
        return results