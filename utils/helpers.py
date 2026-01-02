"""
Helpers - Funciones de utilidad general para el bot
"""
import sys
import os
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
import colorama
from colorama import Fore, Style

# Inicializar colorama para colores en consola
colorama.init()

def display_banner():
    """Muestra el banner del bot"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🤖 {Fore.YELLOW}DEEP BOT - TIBIA AUTOMATION SYSTEM{Fore.CYAN} 🤖           ║
║                                                              ║
║    {Fore.WHITE}Detección de UI • Monitoreo • Acciones Automatizadas{Fore.CYAN}    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

def validate_environment() -> bool:
    """
    Valida el entorno de ejecución
    
    Returns:
        True si el entorno es válido
    """
    print(f"{Fore.CYAN}🔍 Validando entorno de ejecución...{Style.RESET_ALL}")
    
    checks = []
    
    # 1. Verificar versión de Python
    python_version = sys.version_info
    python_ok = python_version >= (3, 8)
    checks.append(("Python 3.8+", python_ok, f"{python_version.major}.{python_version.minor}.{python_version.micro}"))
    
    # 2. Verificar sistema operativo (Windows recomendado para Tibia)
    import platform
    os_name = platform.system()
    os_ok = os_name in ["Windows", "Linux", "Darwin"]
    checks.append(("Sistema operativo compatible", os_ok, os_name))
    
    # 3. Verificar estructura de directorios
    required_dirs = ['core', 'config', 'detectors', 'processors', 'utils']
    dirs_ok = all(Path(dir_name).exists() for dir_name in required_dirs)
    checks.append(("Estructura de directorios", dirs_ok, f"{len(required_dirs)} directorios"))
    
    # 4. Verificar archivos esenciales
    essential_files = [
        'main.py',
        'core/tibia_bot.py',
        'config/settings.py',
        'utils/logger.py'
    ]
    files_ok = all(Path(file_path).exists() for file_path in essential_files)
    checks.append(("Archivos esenciales", files_ok, f"{len(essential_files)} archivos"))
    
    # Mostrar resultados
    print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📋 RESULTADOS DE VALIDACIÓN:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    
    all_passed = True
    
    for check_name, passed, details in checks:
        status = f"{Fore.GREEN}✅ PASÓ" if passed else f"{Fore.RED}❌ FALLÓ"
        print(f"  {check_name:30} {status:20} {Fore.WHITE}{details}{Style.RESET_ALL}")
        
        if not passed:
            all_passed = False
    
    print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    
    if all_passed:
        print(f"{Fore.GREEN}🎉 ¡Entorno validado correctamente!{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.YELLOW}⚠️  Hay problemas en el entorno que deben resolverse.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Recomendaciones:{Style.RESET_ALL}")
        
        if not python_ok:
            print(f"  • Actualiza a Python 3.8 o superior")
        
        if not dirs_ok:
            print(f"  • Verifica la estructura de carpetas del proyecto")
        
        if not files_ok:
            print(f"  • Asegúrate de tener todos los archivos del proyecto")
        
        return False

def get_project_root() -> Path:
    """
    Obtiene la raíz del proyecto
    
    Returns:
        Path de la raíz del proyecto
    """
    return Path(__file__).parent.parent

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Asegura que un directorio exista
    
    Args:
        path: Ruta del directorio
        
    Returns:
        Path del directorio creado/verificado
    """
    path_obj = Path(path) if isinstance(path, str) else path
    
    # Si es relativo, hacerlo absoluto desde la raíz del proyecto
    if not path_obj.is_absolute():
        path_obj = get_project_root() / path_obj
    
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj

def save_json(data: Dict[str, Any], file_path: Union[str, Path], 
              indent: int = 2, ensure_ascii: bool = False) -> bool:
    """
    Guarda datos en un archivo JSON
    
    Args:
        data: Datos a guardar
        file_path: Ruta del archivo
        indent: Indentación del JSON
        ensure_ascii: Si True, convierte caracteres no ASCII
        
    Returns:
        True si se guardó exitosamente
    """
    try:
        file_path_obj = Path(file_path) if isinstance(file_path, str) else file_path
        
        # Si es relativo, hacerlo absoluto desde la raíz del proyecto
        if not file_path_obj.is_absolute():
            file_path_obj = get_project_root() / file_path_obj
        
        # Asegurar directorio
        file_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path_obj, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
        
        print(f"{Fore.GREEN}💾 JSON guardado en: {file_path_obj}{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error guardando JSON {file_path}: {e}{Style.RESET_ALL}")
        return False

def load_json(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """
    Carga datos desde un archivo JSON
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        Datos cargados o None si hay error
    """
    try:
        file_path_obj = Path(file_path) if isinstance(file_path, str) else file_path
        
        # Si es relativo, hacerlo absoluto desde la raíz del proyecto
        if not file_path_obj.is_absolute():
            file_path_obj = get_project_root() / file_path_obj
        
        if not file_path_obj.exists():
            print(f"{Fore.YELLOW}⚠️  Archivo no existe: {file_path_obj}{Style.RESET_ALL}")
            return None
        
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"{Fore.GREEN}📂 JSON cargado desde: {file_path_obj}{Style.RESET_ALL}")
        return data
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error cargando JSON {file_path}: {e}{Style.RESET_ALL}")
        return None

def print_progress(iteration: int, total: int, prefix: str = '', suffix: str = '', 
                   length: int = 50, fill: str = '█'):
    """
    Imprime una barra de progreso
    
    Args:
        iteration: Iteración actual
        total: Total de iteraciones
        prefix: Texto prefijo
        suffix: Texto sufijo
        length: Longitud de la barra
        fill: Carácter de relleno
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    # Colores según el porcentaje
    if percent == "100.0":
        color = Fore.GREEN
    elif float(percent) > 50:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    print(f'\r{prefix} |{color}{bar}{Style.RESET_ALL}| {percent}% {suffix}', end='\r')
    
    # Nueva línea cuando se complete
    if iteration == total:
        print()

def format_time(seconds: float) -> str:
    """
    Formatea segundos en un string legible
    
    Args:
        seconds: Segundos a formatear
        
    Returns:
        String formateado
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"

def format_size(size_bytes: int) -> str:
    """
    Formatea bytes en un string legible
    
    Args:
        size_bytes: Bytes a formatear
        
    Returns:
        String formateado
    """
    if size_bytes == 0:
        return "0B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {units[i]}"

def calculate_hash(data: Union[str, bytes], algorithm: str = "md5") -> str:
    """
    Calcula el hash de datos
    
    Args:
        data: Datos a hashear
        algorithm: Algoritmo de hash
        
    Returns:
        Hash calculado
    """
    hash_func = hashlib.new(algorithm)
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    hash_func.update(data)
    return hash_func.hexdigest()

def get_timestamp() -> str:
    """
    Obtiene un timestamp formateado
    
    Returns:
        Timestamp en formato YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_datetime_string() -> str:
    """
    Obtiene fecha y hora formateadas
    
    Returns:
        String con fecha y hora
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def human_readable_time(seconds: float) -> str:
    """
    Convierte segundos a tiempo legible
    
    Args:
        seconds: Segundos a convertir
        
    Returns:
        String legible
    """
    time_obj = timedelta(seconds=seconds)
    
    days = time_obj.days
    hours, remainder = divmod(time_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    División segura (evita división por cero)
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor por defecto si denominador es cero
        
    Returns:
        Resultado de la división o valor por defecto
    """
    if denominator == 0:
        return default
    return numerator / denominator

def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Limita un valor entre un mínimo y un máximo
    
    Args:
        value: Valor a limitar
        min_val: Valor mínimo
        max_val: Valor máximo
        
    Returns:
        Valor limitado
    """
    return max(min_val, min(max_val, value))

def print_colored(text: str, color: str = Fore.WHITE, style: str = Style.NORMAL) -> None:
    """
    Imprime texto con color y estilo
    
    Args:
        text: Texto a imprimir
        color: Color (de colorama.Fore)
        style: Estilo (de colorama.Style)
    """
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def print_success(message: str) -> None:
    """Imprime un mensaje de éxito"""
    print_colored(f"✅ {message}", Fore.GREEN)

def print_error(message: str) -> None:
    """Imprime un mensaje de error"""
    print_colored(f"❌ {message}", Fore.RED)

def print_warning(message: str) -> None:
    """Imprime un mensaje de advertencia"""
    print_colored(f"⚠️  {message}", Fore.YELLOW)

def print_info(message: str) -> None:
    """Imprime un mensaje informativo"""
    print_colored(f"ℹ️  {message}", Fore.CYAN)

def print_debug(message: str) -> None:
    """Imprime un mensaje de debug"""
    print_colored(f"🐛 {message}", Fore.MAGENTA)

def ask_yes_no(question: str, default: bool = True) -> bool:
    """
    Pregunta sí/no al usuario
    
    Args:
        question: Pregunta a hacer
        default: Respuesta por defecto
        
    Returns:
        True si sí, False si no
    """
    choices = "Y/n" if default else "y/N"
    
    while True:
        response = input(f"{Fore.CYAN}{question} [{choices}]: {Style.RESET_ALL}").strip().lower()
        
        if response == "":
            return default
        elif response in ["y", "yes", "sí", "si"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print(f"{Fore.YELLOW}Por favor responde 'y' (sí) o 'n' (no){Style.RESET_ALL}")

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(seconds: int, message: str = "Iniciando en"):
    """
    Muestra una cuenta regresiva
    
    Args:
        seconds: Segundos para contar
        message: Mensaje a mostrar
    """
    for i in range(seconds, 0, -1):
        print(f"\r{Fore.CYAN}{message} {i}...{Style.RESET_ALL}", end="")
        time.sleep(1)
    print(f"\r{Fore.GREEN}{message.replace('en', '')} ¡Ahora!{' ' * 20}{Style.RESET_ALL}")

def get_memory_usage() -> Dict[str, float]:
    """
    Obtiene información de uso de memoria
    
    Returns:
        Diccionario con información de memoria
    """
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / (1024 * 1024),  # Resident Set Size
            'vms_mb': memory_info.vms / (1024 * 1024),  # Virtual Memory Size
            'percent': process.memory_percent()
        }
        
    except ImportError:
        return {
            'rss_mb': 0.0,
            'vms_mb': 0.0,
            'percent': 0.0,
            'error': 'psutil no instalado'
        }

def get_system_info() -> Dict[str, Any]:
    """
    Obtiene información del sistema
    
    Returns:
        Diccionario con información del sistema
    """
    import platform
    
    info = {
        'platform': platform.platform(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation(),
    }
    
    # Intentar obtener info de CPU y memoria si psutil está disponible
    try:
        import psutil
        info.update({
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'memory_available_gb': psutil.virtual_memory().available / (1024**3),
            'memory_percent': psutil.virtual_memory().percent,
        })
    except ImportError:
        info['psutil_error'] = 'psutil no instalado'
    
    return info

def print_system_info():
    """Imprime información del sistema"""
    info = get_system_info()
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💻 INFORMACIÓN DEL SISTEMA:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}Sistema operativo:{Style.RESET_ALL} {info['platform']}")
    print(f"{Fore.WHITE}Arquitectura:{Style.RESET_ALL} {info['machine']}")
    print(f"{Fore.WHITE}Procesador:{Style.RESET_ALL} {info['processor']}")
    
    if 'cpu_count' in info:
        print(f"{Fore.WHITE}Núcleos CPU:{Style.RESET_ALL} {info['cpu_count']}")
        print(f"{Fore.WHITE}Uso CPU:{Style.RESET_ALL} {info['cpu_percent']:.1f}%")
    
    if 'memory_total_gb' in info:
        print(f"{Fore.WHITE}Memoria total:{Style.RESET_ALL} {info['memory_total_gb']:.1f} GB")
        print(f"{Fore.WHITE}Memoria disponible:{Style.RESET_ALL} {info['memory_available_gb']:.1f} GB")
        print(f"{Fore.WHITE}Uso memoria:{Style.RESET_ALL} {info['memory_percent']:.1f}%")
    
    print(f"{Fore.WHITE}Python:{Style.RESET_ALL} {info['python_version']} ({info['python_implementation']})")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def check_dependencies() -> List[Tuple[str, bool, str]]:
    """
    Verifica dependencias instaladas
    
    Returns:
        Lista de (dependencia, instalada, versión)
    """
    dependencies = [
        ('opencv-python', 'cv2'),
        ('numpy', 'numpy'),
        ('mss', 'mss'),
        ('pyautogui', 'pyautogui'),
        ('colorama', 'colorama'),
        ('Pillow', 'PIL'),
    ]
    
    results = []
    
    for pip_name, import_name in dependencies:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'Desconocida')
            results.append((pip_name, True, version))
        except ImportError:
            results.append((pip_name, False, 'No instalado'))
    
    return results

def print_dependencies():
    """Imprime estado de las dependencias"""
    deps = check_dependencies()
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📦 DEPENDENCIAS:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    for dep_name, installed, version in deps:
        status = f"{Fore.GREEN}✅" if installed else f"{Fore.RED}❌"
        print(f"  {dep_name:20} {status:5} {Fore.WHITE}{version}{Style.RESET_ALL}")
    
    all_installed = all(installed for _, installed, _ in deps)
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if all_installed:
        print(f"{Fore.GREEN}🎉 ¡Todas las dependencias están instaladas!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  Faltan algunas dependencias.{Style.RESET_ALL}")
        missing = [dep for dep, installed, _ in deps if not installed]
        print(f"{Fore.CYAN}💡 Instala con: pip install {' '.join(missing)}{Style.RESET_ALL}")
    
    return all_installed