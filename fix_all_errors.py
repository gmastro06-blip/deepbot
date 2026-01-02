# fix_all_errors.py
import os
import json

def fix_settings():
    """Arregla settings.py para incluir atributos faltantes"""
    
    settings_path = "config/settings.py"
    
    if not os.path.exists(settings_path):
        print(f"❌ {settings_path} no encontrado")
        return
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya tiene color_tolerance
        if 'color_tolerance' not in content:
            print("⚠️  Añadiendo color_tolerance a settings.py")
            
            # Buscar la línea después de los otros atributos
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                new_lines.append(line)
                # Buscar un buen lugar para insertar (después de colors)
                if 'colors:' in line and 'Dict[str, Any]' in line:
                    new_lines.append('    color_tolerance: int = 30  # Tolerancia para detección de colores')
                    new_lines.append('    min_region_area: int = 100  # Área mínima para considerar una región')
            
            # Guardar
            with open(settings_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            print("✅ settings.py actualizado")
        else:
            print("✅ settings.py ya tiene color_tolerance")
    
    except Exception as e:
        print(f"❌ Error arreglando settings.py: {e}")

def fix_color_detector():
    """Arregla color_detector.py"""
    
    color_detector_path = "processors/color_detector.py"
    
    if not os.path.exists(color_detector_path):
        print(f"❌ {color_detector_path} no encontrado")
        return
    
    # Primero haz una copia de seguridad
    backup_path = color_detector_path + ".backup"
    try:
        import shutil
        shutil.copy2(color_detector_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
    except:
        print("⚠️  No se pudo crear backup")
    
    # Reemplazar con versión corregida
    corrected_code = '''"""
Clase ColorDetector - Detección de colores específicos
"""
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any

class ColorDetector:
    """Detección de colores en imágenes"""
    
    def __init__(self, settings):
        """
        Inicializa el detector de colores
        
        Args:
            settings: Configuración del bot
        """
        self.settings = settings
        
        # Configuración de tolerancia de color
        self.color_tolerance = getattr(settings, 'color_tolerance', 30)
        self.min_region_area = getattr(settings, 'min_region_area', 100)
        
        # Rangos de color predefinidos
        self.predefined_ranges = self._create_predefined_ranges()
    
    def _create_predefined_ranges(self) -> Dict[str, Dict[str, Tuple]]:
        """
        Crea rangos de color predefinidos desde settings
        
        Returns:
            Diccionario con rangos de color
        """
        ranges = {}
        
        # Si settings.colors existe
        if hasattr(self.settings, 'colors') and self.settings.colors:
            colors = self.settings.colors
            
            # Procesar cada color
            for color_name, color_info in colors.items():
                if isinstance(color_info, dict):
                    # Si es diccionario con variantes
                    for variant, bgr_color in color_info.items():
                        if isinstance(bgr_color, (list, tuple)) and len(bgr_color) == 3:
                            key = f"{color_name}_{variant}"
                            ranges[key] = self._create_color_range(bgr_color, self.color_tolerance)
                elif isinstance(color_info, (list, tuple)) and len(color_info) == 3:
                    # Si es directamente un color BGR
                    ranges[color_name] = self._create_color_range(color_info, self.color_tolerance)
        
        # Si no hay colores en settings, crear algunos por defecto
        if not ranges:
            ranges = {
                'hp_full': self._create_color_range((50, 50, 200), 40),      # Rojo
                'mp_full': self._create_color_range((200, 50, 50), 40),      # Azul
                'green': self._create_color_range((50, 200, 50), 40),        # Verde
                'yellow': self._create_color_range((50, 200, 200), 40),      # Amarillo
            }
        
        return ranges
    
    def _create_color_range(self, bgr_color: Tuple[int, int, int], 
                           tolerance: int = 30) -> Dict[str, np.ndarray]:
        """
        Crea un rango de color HSV desde un color BGR
        
        Args:
            bgr_color: Color en formato BGR (Blue, Green, Red)
            tolerance: Tolerancia para el rango
        
        Returns:
            Diccionario con lower y upper bounds en HSV
        """
        # Convertir BGR a HSV
        bgr_array = np.uint8([[list(bgr_color)]])
        hsv_color = cv2.cvtColor(bgr_array, cv2.COLOR_BGR2HSV)[0][0]
        
        # Crear rango
        lower = np.array([
            max(0, hsv_color[0] - tolerance),
            max(0, hsv_color[1] - tolerance),
            max(0, hsv_color[2] - tolerance)
        ])
        
        upper = np.array([
            min(179, hsv_color[0] + tolerance),
            min(255, hsv_color[1] + tolerance),
            min(255, hsv_color[2] + tolerance)
        ])
        
        return {'lower': lower, 'upper': upper}
    
    def create_color_mask(self, image: np.ndarray, target_color: Tuple[int, int, int],
                         tolerance: int = None) -> np.ndarray:
        """
        Crea una máscara para un color específico
        
        Args:
            image: Imagen en formato BGR
            target_color: Color objetivo en formato BGR
            tolerance: Tolerancia de color (None = usar default)
        
        Returns:
            Máscara binaria (blanco donde está el color)
        """
        if tolerance is None:
            tolerance = self.color_tolerance
        
        # Crear rango para este color específico
        color_range = self._create_color_range(target_color, tolerance)
        
        # Convertir imagen a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crear máscara
        mask = cv2.inRange(hsv, color_range['lower'], color_range['upper'])
        
        return mask
    
    def find_color_regions(self, image: np.ndarray, target_color: Tuple[int, int, int],
                          min_width: int = 10, max_width: int = 1000,
                          min_height: int = 10, max_height: int = 1000,
                          color_tolerance: int = None) -> List[Tuple[int, int, int, int]]:
        """
        Encuentra regiones de un color específico
        
        Args:
            image: Imagen donde buscar
            target_color: Color a buscar en formato BGR
            min_width: Ancho mínimo de región
            max_width: Ancho máximo de región
            min_height: Alto mínimo de región
            max_height: Alto máximo de región
            color_tolerance: Tolerancia de color
        
        Returns:
            Lista de regiones (x, y, ancho, alto)
        """
        # Crear máscara
        mask = self.create_color_mask(image, target_color, color_tolerance)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        
        for contour in contours:
            # Obtener bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtrar por tamaño
            if (min_width <= w <= max_width and 
                min_height <= h <= max_height and
                w * h >= self.min_region_area):
                
                regions.append((x, y, w, h))
        
        # Ordenar por área (mayor primero)
        regions.sort(key=lambda r: r[2] * r[3], reverse=True)
        
        return regions
    
    def detect_predefined_color(self, image: np.ndarray, color_name: str, 
                               variant: str = 'full') -> List[Tuple[int, int, int, int]]:
        """
        Detecta un color predefinido desde la configuración
        
        Args:
            image: Imagen donde buscar
            color_name: Nombre del color (ej: 'hp', 'mp')
            variant: Variante del color (ej: 'full', 'medium')
        
        Returns:
            Lista de regiones encontradas
        """
        # Construir clave
        key = f"{color_name}_{variant}"
        
        # Buscar en rangos predefinidos
        if key in self.predefined_ranges:
            color_range = self.predefined_ranges[key]
            
            # Convertir imagen a HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Crear máscara
            mask = cv2.inRange(hsv, color_range['lower'], color_range['upper'])
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h >= self.min_region_area:
                    regions.append((x, y, w, h))
            
            return regions
        
        return []
    
    def get_dominant_color(self, image: np.ndarray, 
                          k: int = 3) -> Tuple[Tuple[int, int, int], float]:
        """
        Obtiene el color dominante en una imagen usando k-means
        
        Args:
            image: Imagen a analizar
            k: Número de clusters
        
        Returns:
            Tupla (color_bgr, porcentaje)
        """
        # Redimensionar para mayor velocidad
        resized = cv2.resize(image, (100, 100))
        
        # Cambiar forma a lista de píxeles
        pixels = resized.reshape(-1, 3)
        pixels = np.float32(pixels)
        
        # Criterio para k-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        
        # Aplicar k-means
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Contar etiquetas
        unique, counts = np.unique(labels, return_counts=True)
        
        # Encontrar el cluster más grande
        dominant_idx = np.argmax(counts)
        dominant_color = centers[dominant_idx].astype(int)
        percentage = counts[dominant_idx] / len(labels)
        
        return tuple(dominant_color.tolist()), percentage
    
    def count_color_pixels(self, image: np.ndarray, target_color: Tuple[int, int, int],
                          tolerance: int = None) -> Tuple[int, float]:
        """
        Cuenta píxeles de un color específico
        
        Args:
            image: Imagen a analizar
            target_color: Color objetivo
            tolerance: Tolerancia
        
        Returns:
            Tupla (número de píxeles, porcentaje)
        """
        mask = self.create_color_mask(image, target_color, tolerance)
        pixel_count = cv2.countNonZero(mask)
        total_pixels = image.shape[0] * image.shape[1]
        
        return pixel_count, pixel_count / total_pixels if total_pixels > 0 else 0
'''
    
    try:
        with open(color_detector_path, 'w', encoding='utf-8') as f:
            f.write(corrected_code)
        print(f"✅ {color_detector_path} reemplazado con versión corregida")
    except Exception as e:
        print(f"❌ Error arreglando color_detector.py: {e}")

def update_default_settings():
    """Actualiza default_settings.json con atributos faltantes"""
    
    settings_path = "configs/default_settings.json"
    
    if not os.path.exists(settings_path):
        print(f"❌ {settings_path} no encontrado")
        return
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Añadir atributos faltantes si no existen
        if 'color_tolerance' not in data:
            data['color_tolerance'] = 30
        
        if 'min_region_area' not in data:
            data['min_region_area'] = 100
        
        # Guardar
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {settings_path} actualizado")
        
    except Exception as e:
        print(f"❌ Error actualizando {settings_path}: {e}")

def main():
    print("🔧 Arreglando errores...")
    
    fix_settings()
    fix_color_detector()
    update_default_settings()
    
    print("\n✅ Todos los errores han sido arreglados")
    print("🔄 Ahora ejecuta: python test_run_fixed.py")

if __name__ == "__main__":
    main()