"""
Clase PerformanceMonitor - Monitoreo de rendimiento del bot
"""
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import statistics

@dataclass
class PerformanceMetrics:
    """Métricas de rendimiento para una operación"""
    operation_name: str
    call_count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    last_time: float = 0.0
    timestamps: List[float] = field(default_factory=list)
    
    @property
    def average_time(self) -> float:
        """Tiempo promedio en milisegundos"""
        if self.call_count == 0:
            return 0.0
        return (self.total_time / self.call_count) * 1000  # Convertir a ms
    
    @property
    def calls_per_second(self) -> float:
        """Llamadas por segundo"""
        if self.total_time == 0:
            return 0.0
        return self.call_count / self.total_time
    
    @property
    def fps(self) -> float:
        """Frames por segundo (si aplica)"""
        avg_time = self.average_time / 1000  # Convertir a segundos
        if avg_time == 0:
            return 0.0
        return 1.0 / avg_time
    
    def add_measurement(self, duration: float):
        """Agrega una nueva medición"""
        self.call_count += 1
        self.total_time += duration
        self.min_time = min(self.min_time, duration)
        self.max_time = max(self.max_time, duration)
        self.last_time = duration
        self.timestamps.append(time.time())
        
        # Mantener solo las últimas 1000 mediciones
        if len(self.timestamps) > 1000:
            self.timestamps = self.timestamps[-1000:]

class PerformanceMonitor:
    """Monitor de rendimiento para el bot"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.start_time = time.time()
        self.measurement_stack: List[Tuple[str, float]] = []
        
        # Estadísticas generales
        self.stats = {
            'total_operations': 0,
            'total_time': 0.0,
            'peak_memory_usage': 0.0,
            'errors_count': 0,
            'warnings_count': 0
        }
        
        print("📊 PerformanceMonitor inicializado")
    
    def start_measurement(self, operation_name: str) -> None:
        """
        Inicia la medición de una operación
        
        Args:
            operation_name: Nombre de la operación a medir
        """
        if not self.enabled:
            return
        
        # Agregar al stack para mediciones anidadas
        self.measurement_stack.append((operation_name, time.time()))
    
    def end_measurement(self, operation_name: str) -> float:
        """
        Finaliza la medición de una operación
        
        Args:
            operation_name: Nombre de la operación
            
        Returns:
            Duración en segundos
        """
        if not self.enabled:
            return 0.0
        
        # Buscar en el stack (para manejar mediciones anidadas)
        for i in range(len(self.measurement_stack) - 1, -1, -1):
            name, start_time = self.measurement_stack[i]
            if name == operation_name:
                duration = time.time() - start_time
                
                # Actualizar métricas
                if operation_name not in self.metrics:
                    self.metrics[operation_name] = PerformanceMetrics(operation_name)
                
                self.metrics[operation_name].add_measurement(duration)
                self.stats['total_operations'] += 1
                self.stats['total_time'] += duration
                
                # Eliminar del stack
                self.measurement_stack.pop(i)
                
                return duration
        
        # Si no se encontró en el stack, crear nueva medición
        print(f"⚠️  Medición no iniciada para: {operation_name}")
        return 0.0
    
    def measure(self, operation_name: str):
        """
        Decorador para medir el tiempo de ejecución de una función
        
        Args:
            operation_name: Nombre de la operación
            
        Returns:
            Decorador
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                self.start_measurement(operation_name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    self.end_measurement(operation_name)
            return wrapper
        return decorator
    
    def get_metrics(self, operation_name: str) -> Optional[PerformanceMetrics]:
        """
        Obtiene las métricas para una operación
        
        Args:
            operation_name: Nombre de la operación
            
        Returns:
            Métricas o None si no existe
        """
        return self.metrics.get(operation_name)
    
    def get_average_time(self, operation_name: str) -> float:
        """
        Obtiene el tiempo promedio para una operación
        
        Args:
            operation_name: Nombre de la operación
            
        Returns:
            Tiempo promedio en milisegundos
        """
        metrics = self.get_metrics(operation_name)
        if metrics:
            return metrics.average_time
        return 0.0
    
    def get_all_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Obtiene todas las métricas"""
        return self.metrics.copy()
    
    def get_slowest_operations(self, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Obtiene las operaciones más lentas
        
        Args:
            limit: Número máximo de operaciones a devolver
            
        Returns:
            Lista de (nombre, tiempo_promedio_ms)
        """
        operations = []
        for name, metrics in self.metrics.items():
            if metrics.call_count > 0:
                operations.append((name, metrics.average_time))
        
        # Ordenar por tiempo promedio (de mayor a menor)
        operations.sort(key=lambda x: x[1], reverse=True)
        
        return operations[:limit]
    
    def get_most_called_operations(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Obtiene las operaciones más llamadas
        
        Args:
            limit: Número máximo de operaciones a devolver
            
        Returns:
            Lista de (nombre, conteo)
        """
        operations = []
        for name, metrics in self.metrics.items():
            operations.append((name, metrics.call_count))
        
        # Ordenar por conteo (de mayor a menor)
        operations.sort(key=lambda x: x[1], reverse=True)
        
        return operations[:limit]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del rendimiento
        
        Returns:
            Diccionario con resumen de rendimiento
        """
        total_uptime = time.time() - self.start_time
        
        # Calcular operaciones por segundo
        ops_per_second = 0.0
        if total_uptime > 0:
            ops_per_second = self.stats['total_operations'] / total_uptime
        
        # Obtener operaciones más lentas
        slowest_ops = self.get_slowest_operations(5)
        
        # Obtener operaciones más llamadas
        most_called_ops = self.get_most_called_operations(5)
        
        return {
            'uptime_seconds': total_uptime,
            'uptime_human': self._format_time(total_uptime),
            'total_operations': self.stats['total_operations'],
            'total_measured_time': self.stats['total_time'],
            'operations_per_second': ops_per_second,
            'unique_operations': len(self.metrics),
            'slowest_operations': slowest_ops,
            'most_called_operations': most_called_ops,
            'errors_count': self.stats['errors_count'],
            'warnings_count': self.stats['warnings_count']
        }
    
    def _format_time(self, seconds: float) -> str:
        """Formatea tiempo en formato legible"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def reset(self):
        """Reinicia todas las métricas"""
        self.metrics.clear()
        self.measurement_stack.clear()
        self.start_time = time.time()
        
        self.stats = {
            'total_operations': 0,
            'total_time': 0.0,
            'peak_memory_usage': 0.0,
            'errors_count': 0,
            'warnings_count': 0
        }
        
        print("🔄 PerformanceMonitor reiniciado")
    
    def print_summary(self, detailed: bool = False):
        """
        Imprime un resumen del rendimiento
        
        Args:
            detailed: Si True, muestra detalles por operación
        """
        if not self.enabled:
            print("📊 PerformanceMonitor desactivado")
            return
        
        summary = self.get_performance_summary()
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE RENDIMIENTO")
        print("="*60)
        
        print(f"\n⏱️  Tiempo activo: {summary['uptime_human']}")
        print(f"🔢 Operaciones totales: {summary['total_operations']:,}")
        print(f"⚡ Ops/segundo: {summary['operations_per_second']:.2f}")
        print(f"🎯 Operaciones únicas: {summary['unique_operations']}")
        
        if summary['slowest_operations']:
            print(f"\n🐌 Operaciones más lentas:")
            for name, avg_time in summary['slowest_operations']:
                print(f"  • {name}: {avg_time:.2f}ms")
        
        if summary['most_called_operations']:
            print(f"\n📞 Operaciones más llamadas:")
            for name, count in summary['most_called_operations']:
                print(f"  • {name}: {count:,} veces")
        
        if detailed and self.metrics:
            print(f"\n📈 Métricas detalladas:")
            print("-"*40)
            
            # Ordenar alfabéticamente
            sorted_metrics = sorted(self.metrics.items(), key=lambda x: x[0])
            
            for name, metrics in sorted_metrics:
                if metrics.call_count > 0:
                    print(f"\n{name}:")
                    print(f"  Llamadas: {metrics.call_count:,}")
                    print(f"  Tiempo total: {metrics.total_time:.3f}s")
                    print(f"  Promedio: {metrics.average_time:.2f}ms")
                    print(f"  Mínimo: {metrics.min_time*1000:.2f}ms")
                    print(f"  Máximo: {metrics.max_time*1000:.2f}ms")
                    print(f"  Último: {metrics.last_time*1000:.2f}ms")
                    print(f"  Llamadas/s: {metrics.calls_per_second:.2f}")
        
        print("\n" + "="*60)
    
    def enable(self):
        """Habilita el monitoreo"""
        self.enabled = True
        print("✅ PerformanceMonitor habilitado")
    
    def disable(self):
        """Deshabilita el monitoreo"""
        self.enabled = False
        print("✅ PerformanceMonitor deshabilitado")
    
    def log_error(self):
        """Registra un error"""
        self.stats['errors_count'] += 1
    
    def log_warning(self):
        """Registra una advertencia"""
        self.stats['warnings_count'] += 1
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Obtiene el uso de memoria actual
        
        Returns:
            Diccionario con información de memoria
        """
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            memory_data = {
                'rss_mb': memory_info.rss / (1024 * 1024),  # Resident Set Size
                'vms_mb': memory_info.vms / (1024 * 1024),  # Virtual Memory Size
                'percent': process.memory_percent()
            }
            
            # Actualizar peak memory
            self.stats['peak_memory_usage'] = max(
                self.stats['peak_memory_usage'],
                memory_data['rss_mb']
            )
            
            return memory_data
            
        except ImportError:
            return {
                'rss_mb': 0.0,
                'vms_mb': 0.0,
                'percent': 0.0,
                'error': 'psutil no instalado'
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtiene información del sistema
        
        Returns:
            Diccionario con información del sistema
        """
        try:
            import psutil
            import platform
            
            system_info = {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_total_gb': psutil.virtual_memory().total / (1024**3),
                'memory_available_gb': psutil.virtual_memory().available / (1024**3),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage_percent': psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else 0
            }
            
            return system_info
            
        except ImportError:
            return {
                'platform': platform.platform() if 'platform' in locals() else 'Desconocido',
                'python_version': platform.python_version() if 'platform' in locals() else 'Desconocido',
                'error': 'psutil no instalado'
            }