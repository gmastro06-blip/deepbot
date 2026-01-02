"""
Clase ImageProcessor - Procesamiento básico de imágenes
"""
import cv2
import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from pathlib import Path

class ImageProcessor:
    """Procesador de imágenes con utilidades básicas"""
    
    @staticmethod
    def resize_image(image: np.ndarray, width: int = None, height: int = None,
                    keep_aspect_ratio: bool = True) -> np.ndarray:
        """
        Redimensiona una imagen
        
        Args:
            image: Imagen a redimensionar
            width: Ancho deseado
            height: Alto deseado
            keep_aspect_ratio: Mantener relación de aspecto
        
        Returns:
            Imagen redimensionada
        """
        if width is None and height is None:
            return image
        
        h, w = image.shape[:2]
        
        if keep_aspect_ratio:
            if width is not None and height is None:
                # Calcular altura manteniendo aspecto
                ratio = width / w
                height = int(h * ratio)
            elif height is not None and width is None:
                # Calcular ancho manteniendo aspecto
                ratio = height / h
                width = int(w * ratio)
            else:
                # Ambos especificados, usar el factor de escala más pequeño
                ratio_w = width / w
                ratio_h = height / h
                ratio = min(ratio_w, ratio_h)
                width = int(w * ratio)
                height = int(h * ratio)
        
        return cv2.resize(image, (width, height))
    
    @staticmethod
    def crop_image(image: np.ndarray, x: int, y: int, 
                  width: int, height: int) -> np.ndarray:
        """
        Recorta una región de una imagen
        
        Args:
            image: Imagen original
            x, y: Esquina superior izquierda
            width, height: Tamaño del recorte
        
        Returns:
            Imagen recortada
        """
        h, w = image.shape[:2]
        
        # Asegurar que no se sale de los límites
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(w, x + width)
        y2 = min(h, y + height)
        
        return image[y1:y2, x1:x2]
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float, 
                    center: Tuple[int, int] = None) -> np.ndarray:
        """
        Rota una imagen
        
        Args:
            image: Imagen a rotar
            angle: Ángulo en grados
            center: Centro de rotación (None = centro de imagen)
        
        Returns:
            Imagen rotada
        """
        h, w = image.shape[:2]
        
        if center is None:
            center = (w // 2, h // 2)
        
        # Obtener matriz de rotación
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calcular nuevo tamaño
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # Ajustar matriz de transformación
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # Aplicar rotación
        rotated = cv2.warpAffine(image, M, (new_w, new_h))
        
        return rotated
    
    @staticmethod
    def adjust_brightness_contrast(image: np.ndarray, 
                                  brightness: float = 0.0,
                                  contrast: float = 1.0) -> np.ndarray:
        """
        Ajusta brillo y contraste
        
        Args:
            image: Imagen original
            brightness: Ajuste de brillo (-255 a 255)
            contrast: Factor de contraste
        
        Returns:
            Imagen ajustada
        """
        # Convertir a float para operaciones
        img_float = image.astype(np.float32)
        
        # Aplicar brillo y contraste
        img_float = img_float * contrast + brightness
        
        # Recortar a rango válido
        img_float = np.clip(img_float, 0, 255)
        
        return img_float.astype(np.uint8)
    
    @staticmethod
    def apply_gaussian_blur(image: np.ndarray, 
                           kernel_size: Tuple[int, int] = (5, 5),
                           sigma: float = 0) -> np.ndarray:
        """
        Aplica desenfoque gaussiano
        
        Args:
            image: Imagen original
            kernel_size: Tamaño del kernel (ancho, alto)
            sigma: Desviación estándar (0 = calcular automáticamente)
        
        Returns:
            Imagen desenfocada
        """
        return cv2.GaussianBlur(image, kernel_size, sigma)
    
    @staticmethod
    def detect_edges(image: np.ndarray, 
                     low_threshold: int = 50,
                     high_threshold: int = 150) -> np.ndarray:
        """
        Detecta bordes usando algoritmo Canny
        
        Args:
            image: Imagen original
            low_threshold: Umbral bajo
            high_threshold: Umbral alto
        
        Returns:
            Imagen con bordes detectados
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        return cv2.Canny(gray, low_threshold, high_threshold)
    
    @staticmethod
    def find_contours(image: np.ndarray, 
                      mode: int = cv2.RETR_EXTERNAL,
                      method: int = cv2.CHAIN_APPROX_SIMPLE) -> List[np.ndarray]:
        """
        Encuentra contornos en una imagen
        
        Args:
            image: Imagen binaria
            mode: Modo de recuperación de contornos
            method: Método de aproximación
        
        Returns:
            Lista de contornos
        """
        contours, _ = cv2.findContours(image, mode, method)
        return contours
    
    @staticmethod
    def draw_contours(image: np.ndarray, contours: List[np.ndarray],
                      color: Tuple[int, int, int] = (0, 255, 0),
                      thickness: int = 2) -> np.ndarray:
        """
        Dibuja contornos en una imagen
        
        Args:
            image: Imagen donde dibujar
            contours: Contornos a dibujar
            color: Color en BGR
            thickness: Grosor de línea
        
        Returns:
            Imagen con contornos dibujados
        """
        result = image.copy()
        cv2.drawContours(result, contours, -1, color, thickness)
        return result
    
    @staticmethod
    def find_largest_contour(contours: List[np.ndarray]) -> Optional[np.ndarray]:
        """
        Encuentra el contorno más grande
        
        Args:
            contours: Lista de contornos
        
        Returns:
            Contorno más grande o None
        """
        if not contours:
            return None
        
        return max(contours, key=cv2.contourArea)
    
    @staticmethod
    def get_contour_bounds(contour: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Obtiene límites de un contorno
        
        Args:
            contour: Contorno
        
        Returns:
            (x, y, width, height)
        """
        return cv2.boundingRect(contour)
    
    @staticmethod
    def calculate_contour_area(contour: np.ndarray) -> float:
        """
        Calcula el área de un contorno
        
        Args:
            contour: Contorno
        
        Returns:
            Área
        """
        return cv2.contourArea(contour)
    
    @staticmethod
    def calculate_contour_perimeter(contour: np.ndarray) -> float:
        """
        Calcula el perímetro de un contorno
        
        Args:
            contour: Contorno
        
        Returns:
            Perímetro
        """
        return cv2.arcLength(contour, True)
    
    @staticmethod
    def get_image_statistics(image: np.ndarray) -> Dict[str, Any]:
        """
        Calcula estadísticas de una imagen
        
        Args:
            image: Imagen a analizar
        
        Returns:
            Diccionario con estadísticas
        """
        stats = {}
        
        # Dimensiones
        stats['height'], stats['width'] = image.shape[:2]
        stats['channels'] = 1 if len(image.shape) == 2 else image.shape[2]
        
        # Valores de píxel
        if len(image.shape) == 2:
            # Imagen en escala de grises
            stats['min'] = float(np.min(image))
            stats['max'] = float(np.max(image))
            stats['mean'] = float(np.mean(image))
            stats['std'] = float(np.std(image))
            stats['median'] = float(np.median(image))
        else:
            # Imagen a color
            for i, channel in enumerate(['b', 'g', 'r']):
                channel_data = image[:, :, i]
                stats[f'{channel}_min'] = float(np.min(channel_data))
                stats[f'{channel}_max'] = float(np.max(channel_data))
                stats[f'{channel}_mean'] = float(np.mean(channel_data))
                stats[f'{channel}_std'] = float(np.std(channel_data))
                stats[f'{channel}_median'] = float(np.median(channel_data))
        
        return stats
    
    @staticmethod
    def save_image(image: np.ndarray, filename: str, 
                  create_dir: bool = True) -> bool:
        """
        Guarda una imagen en disco
        
        Args:
            image: Imagen a guardar
            filename: Ruta del archivo
            create_dir: Crear directorio si no existe
        
        Returns:
            True si se guardó exitosamente
        """
        try:
            if create_dir:
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            cv2.imwrite(filename, image)
            return True
            
        except Exception as e:
            print(f"Error guardando imagen {filename}: {e}")
            return False
    
    @staticmethod
    def load_image(filename: str) -> Optional[np.ndarray]:
        """
        Carga una imagen desde disco
        
        Args:
            filename: Ruta del archivo
        
        Returns:
            Imagen cargada o None si hay error
        """
        try:
            image = cv2.imread(filename)
            if image is None:
                print(f"Error: No se pudo cargar imagen {filename}")
                return None
            return image
        except Exception as e:
            print(f"Error cargando imagen {filename}: {e}")
            return None
    
    @staticmethod
    def show_image(image: np.ndarray, window_name: str = "Image",
                  wait_key: bool = True, destroy: bool = True):
        """
        Muestra una imagen en una ventana
        
        Args:
            image: Imagen a mostrar
            window_name: Nombre de la ventana
            wait_key: Esperar tecla antes de continuar
            destroy: Cerrar ventana después
        """
        cv2.imshow(window_name, image)
        
        if wait_key:
            cv2.waitKey(0)
        
        if destroy:
            cv2.destroyWindow(window_name)
    
    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Convierte imagen a escala de grises
        
        Args:
            image: Imagen original
        
        Returns:
            Imagen en escala de grises
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    @staticmethod
    def convert_to_hsv(image: np.ndarray) -> np.ndarray:
        """
        Convierte imagen a espacio de color HSV
        
        Args:
            image: Imagen original en BGR
        
        Returns:
            Imagen en HSV
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    @staticmethod
    def apply_threshold(image: np.ndarray, 
                       threshold_value: int = 127,
                       max_value: int = 255,
                       threshold_type: int = cv2.THRESH_BINARY) -> np.ndarray:
        """
        Aplica umbral a una imagen
        
        Args:
            image: Imagen en escala de grises
            threshold_value: Valor de umbral
            max_value: Valor máximo
            threshold_type: Tipo de umbral
        
        Returns:
            Imagen binarizada
        """
        _, thresholded = cv2.threshold(image, threshold_value, max_value, threshold_type)
        return thresholded
    
    @staticmethod
    def apply_adaptive_threshold(image: np.ndarray,
                                max_value: int = 255,
                                adaptive_method: int = cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                threshold_type: int = cv2.THRESH_BINARY,
                                block_size: int = 11,
                                C: int = 2) -> np.ndarray:
        """
        Aplica umbral adaptativo
        
        Args:
            image: Imagen en escala de grises
            max_value: Valor máximo
            adaptive_method: Método adaptativo
            threshold_type: Tipo de umbral
            block_size: Tamaño del bloque
            C: Constante a restar
        
        Returns:
            Imagen binarizada
        """
        return cv2.adaptiveThreshold(image, max_value, adaptive_method, 
                                    threshold_type, block_size, C)
    
    @staticmethod
    def find_circles(image: np.ndarray,
                    min_radius: int = 10,
                    max_radius: int = 100,
                    dp: float = 1.0,
                    min_dist: float = 20.0,
                    param1: int = 50,
                    param2: int = 30) -> Optional[np.ndarray]:
        """
        Encuentra círculos en una imagen
        
        Args:
            image: Imagen en escala de grises
            min_radius: Radio mínimo
            max_radius: Radio máximo
            dp: Ratio de resolución inversa
            min_dist: Distancia mínima entre centros
            param1: Umbral alto para detector de bordes
            param2: Umbral para detección de centro
        
        Returns:
            Array de círculos [x, y, radius] o None
        """
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, min_dist,
                                  param1=param1, param2=param2,
                                  minRadius=min_radius, maxRadius=max_radius)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            return circles[0]
        
        return None
    
    @staticmethod
    def find_lines(image: np.ndarray,
                  rho: float = 1.0,
                  theta: float = np.pi / 180,
                  threshold: int = 50,
                  min_line_length: int = 30,
                  max_line_gap: int = 10) -> Optional[np.ndarray]:
        """
        Encuentra líneas en una imagen
        
        Args:
            image: Imagen con bordes
            rho: Resolución de rho en píxeles
            theta: Resolución de theta en radianes
            threshold: Umbral mínimo de votos
            min_line_length: Longitud mínima de línea
            max_line_gap: Máximo hueco permitido
        
        Returns:
            Array de líneas [x1, y1, x2, y2] o None
        """
        lines = cv2.HoughLinesP(image, rho, theta, threshold,
                               minLineLength=min_line_length,
                               maxLineGap=max_line_gap)
        return lines
    
    @staticmethod
    def match_template(image: np.ndarray, template: np.ndarray,
                      method: int = cv2.TM_CCOEFF_NORMED) -> np.ndarray:
        """
        Busca una plantilla en una imagen
        
        Args:
            image: Imagen donde buscar
            template: Plantilla a buscar
            method: Método de comparación
        
        Returns:
            Mapa de coincidencia
        """
        return cv2.matchTemplate(image, template, method)
    
    @staticmethod
    def find_template_location(result: np.ndarray,
                              threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Encuentra la mejor ubicación de plantilla
        
        Args:
            result: Resultado de matchTemplate
            threshold: Umbral de confianza
        
        Returns:
            (x, y) de mejor coincidencia o None
        """
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            return max_loc
        
        return None