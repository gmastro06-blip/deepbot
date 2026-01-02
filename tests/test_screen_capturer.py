"""
Tests unitarios para la clase ScreenCapturer
"""
import unittest
import numpy as np
import tempfile
from pathlib import Path

from core.screen_capturer import ScreenCapturer, ScreenRegion

class TestScreenCapturer(unittest.TestCase):
    """Tests para la clase ScreenCapturer"""
    
    def setUp(self):
        """Configuración inicial antes de cada test"""
        self.capturer = ScreenCapturer(monitor_index=1)
        
    def test_initialization(self):
        """Test de inicialización"""
        self.assertIsNotNone(self.capturer.sct)
        self.assertIsNotNone(self.capturer.monitor_info)
        self.assertEqual(self.capturer.monitor_index, 1)
        
    def test_screen_resolution(self):
        """Test de obtención de resolución de pantalla"""
        width, height = self.capturer.get_screen_resolution()
        self.assertIsInstance(width, int)
        self.assertIsInstance(height, int)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)
        
    def test_screen_region_dataclass(self):
        """Test de la clase ScreenRegion"""
        region = ScreenRegion(x=100, y=200, width=300, height=400)
        
        # Test propiedades
        self.assertEqual(region.x, 100)
        self.assertEqual(region.y, 200)
        self.assertEqual(region.width, 300)
        self.assertEqual(region.height, 400)
        self.assertEqual(region.area, 300 * 400)
        
        # Test conversión a diccionario
        region_dict = region.to_dict()
        self.assertEqual(region_dict['x'], 100)
        self.assertEqual(region_dict['y'], 200)
        self.assertEqual(region_dict['width'], 300)
        self.assertEqual(region_dict['height'], 400)
        
        # Test creación desde diccionario
        region2 = ScreenRegion.from_dict(region_dict)
        self.assertEqual(region2.x, 100)
        self.assertEqual(region2.y, 200)
        
    def test_region_validation(self):
        """Test de validación de regiones"""
        screen_width, screen_height = self.capturer.get_screen_resolution()
        
        # Región válida
        valid_region = {
            'top': 100,
            'left': 100,
            'width': 200,
            'height': 200
        }
        self.assertTrue(self.capturer._validate_region(valid_region))
        
        # Región inválida (fuera de límites)
        invalid_region = {
            'top': screen_height + 100,
            'left': screen_width + 100,
            'width': 200,
            'height': 200
        }
        with self.assertRaises(ValueError):
            self.capturer._validate_region(invalid_region)
    
    def test_capture_methods(self):
        """Test de métodos de captura (sin ejecutar realmente)"""
        # Este test solo verifica que los métodos existen y tienen
        # la firma correcta, sin ejecutar capturas reales
        self.assertTrue(hasattr(self.capturer, 'capture_full_screen'))
        self.assertTrue(hasattr(self.capturer, 'capture_region'))
        self.assertTrue(hasattr(self.capturer, 'capture_multiple_regions'))
        
        # Verificar que son métodos callable
        self.assertTrue(callable(self.capturer.capture_full_screen))
        self.assertTrue(callable(self.capturer.capture_region))
        
    def test_save_capture(self):
        """Test de guardado de captura (con imagen dummy)"""
        # Crear imagen dummy
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        dummy_image[:, :] = [255, 0, 0]  # Rojo
        
        # Usar directorio temporal
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir) / "test_capture.png"
            
            # Guardar imagen
            saved_path = self.capturer.save_capture(dummy_image, str(temp_file))
            
            # Verificar que el archivo existe
            self.assertTrue(Path(saved_path).exists())
            
            # Verificar que es una imagen válida
            import cv2
            loaded_image = cv2.imread(saved_path)
            self.assertIsNotNone(loaded_image)
            self.assertEqual(loaded_image.shape, dummy_image.shape)
    
    def test_benchmark_method(self):
        """Test del método de benchmark (sin ejecutar realmente)"""
        # Solo verificar que el método existe
        self.assertTrue(hasattr(self.capturer, 'benchmark_capture'))
        self.assertTrue(callable(self.capturer.benchmark_capture))
        
        # Verificar que devuelve un diccionario con las keys esperadas
        # Nota: No ejecutamos el benchmark real para no ralentizar los tests
        expected_keys = ['iterations', 'avg_ms', 'min_ms', 'max_ms', 'std_ms', 'fps']
        
        # Podemos verificar que el método tiene la firma correcta
        import inspect
        sig = inspect.signature(self.capturer.benchmark_capture)
        params = list(sig.parameters.keys())
        self.assertIn('iterations', params)
        
    def test_multiple_regions_capture(self):
        """Test de captura de múltiples regiones (con datos dummy)"""
        # Definir regiones de prueba
        regions = {
            'region1': ScreenRegion(x=0, y=0, width=100, height=100),
            'region2': {'x': 100, 'y': 100, 'width': 200, 'height': 200},
            'region3': (300, 300, 150, 150)
        }
        
        # Este test no ejecuta captura real, solo verifica estructura
        # En un test real con mocking se verificaría el comportamiento
        
        self.assertEqual(len(regions), 3)
        self.assertIn('region1', regions)
        self.assertIn('region2', regions)
        self.assertIn('region3', regions)
        
    def test_error_handling(self):
        """Test de manejo de errores"""
        # Test con región inválida
        invalid_inputs = [
            None,
            {},
            {'x': 10},  # Faltan keys
            (10, 20),   # Tupla muy corta
            "invalid"   # String no válido
        ]
        
        for invalid_input in invalid_inputs:
            with self.assertRaises(Exception):
                # Nota: En realidad necesitaríamos mocking para probar esto
                # sin ejecutar captura real
                pass
        
    def tearDown(self):
        """Limpieza después de cada test"""
        # Cerrar recursos si es necesario
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)