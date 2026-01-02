"""
Tests unitarios para HealthDetector
"""
import unittest
import numpy as np
import cv2
from pathlib import Path

from detectors.health_detector import HealthDetector
from config.settings import Settings

class TestHealthDetector(unittest.TestCase):
    """Tests para la clase HealthDetector"""
    
    def setUp(self):
        """Configuración inicial"""
        self.settings = Settings("configs/default_settings.json")
        self.detector = HealthDetector(self.settings)
        
        # Crear imágenes de prueba
        self.create_test_images()
    
    def create_test_images(self):
        """Crea imágenes de prueba para los tests"""
        # Imagen de barra de HP llena (roja)
        self.full_hp_bar = np.zeros((20, 200, 3), dtype=np.uint8)
        self.full_hp_bar[:, :, 2] = 200  # Rojo en BGR
        self.full_hp_bar[:, :, 0] = 50
        self.full_hp_bar[:, :, 1] = 50
        
        # Imagen de barra de HP a mitad
        self.half_hp_bar = np.zeros((20, 200, 3), dtype=np.uint8)
        self.half_hp_bar[:, :100, 2] = 200  # Mitad roja
        self.half_hp_bar[:, :100, 0] = 50
        self.half_hp_bar[:, :100, 1] = 50
        # La otra mitad oscura (HP vacío)
        self.half_hp_bar[:, 100:, :] = 30
        
        # Imagen de barra de HP vacía
        self.empty_hp_bar = np.zeros((20, 200, 3), dtype=np.uint8)
        self.empty_hp_bar[:, :, :] = 30  # Todo oscuro
        
        # Imagen de pantalla completa con barra de HP
        self.full_screenshot = np.zeros((1080, 1920, 3), dtype=np.uint8)
        # Agregar barra de HP en posición típica
        self.full_screenshot[50:70, 100:300, :] = self.full_hp_bar
    
    def test_initialization(self):
        """Test de inicialización"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector.settings)
        self.assertIsNotNone(self.detector.color_detector)
        self.assertIsNotNone(self.detector.image_processor)
        
        # Verificar colores de HP configurados
        self.assertIn('full', self.detector.hp_colors)
        self.assertIn('low', self.detector.hp_colors)
        
    def test_analyze_full_hp(self):
        """Test de análisis de barra de HP llena"""
        percentage = self.detector.analyze(self.full_hp_bar)
        
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 90.0)
        self.assertLessEqual(percentage, 100.0)
        
    def test_analyze_half_hp(self):
        """Test de análisis de barra de HP a mitad"""
        percentage = self.detector.analyze(self.half_hp_bar)
        
        self.assertIsInstance(percentage, float)
        # Debería estar alrededor del 50%
        self.assertGreaterEqual(percentage, 40.0)
        self.assertLessEqual(percentage, 60.0)
        
    def test_analyze_empty_hp(self):
        """Test de análisis de barra de HP vacía"""
        percentage = self.detector.analyze(self.empty_hp_bar)
        
        self.assertIsInstance(percentage, float)
        self.assertLess(percentage, 10.0)
        
    def test_detect_in_screenshot(self):
        """Test de detección en pantalla completa"""
        result = self.detector.detect(self.full_screenshot)
        
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.confidence)
        self.assertIsInstance(result.confidence, float)
        
        # Si detectó la barra, debería tener región
        if result.confidence > 0.5:
            self.assertIsNotNone(result.region)
            x, y, w, h = result.region
            self.assertGreater(w, 0)
            self.assertGreater(h, 0)
            
            # Verificar que la región está en la posición esperada
            self.assertGreaterEqual(y, 50)
            self.assertLessEqual(y, 70)
    
    def test_analyze_by_color(self):
        """Test del método _analyze_by_color"""
        percentage = self.detector._analyze_by_color(self.full_hp_bar)
        
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 0.0)
        self.assertLessEqual(percentage, 100.0)
        
    def test_analyze_by_edge(self):
        """Test del método _analyze_by_edge"""
        percentage = self.detector._analyze_by_edge(self.half_hp_bar)
        
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 0.0)
        self.assertLessEqual(percentage, 100.0)
        
        # Para la barra a mitad, debería estar alrededor del 50%
        self.assertGreater(percentage, 40.0)
        self.assertLess(percentage, 60.0)
    
    def test_analyze_by_brightness(self):
        """Test del método _analyze_by_brightness"""
        percentage = self.detector._analyze_by_brightness(self.full_hp_bar)
        
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 0.0)
        self.assertLessEqual(percentage, 100.0)
        
    def test_select_best_hp_region(self):
        """Test de selección de mejor región de HP"""
        # Crear regiones de prueba
        regions = [
            (100, 50, 200, 20),   # Buena: larga y delgada
            (100, 100, 50, 50),   # Mala: cuadrada
            (100, 150, 300, 5),   # Muy delgada
        ]
        
        best_region = self.detector._select_best_hp_region(regions)
        
        self.assertIsInstance(best_region, tuple)
        self.assertEqual(len(best_region), 4)
        
        # Debería seleccionar la primera (mejor aspect ratio)
        self.assertEqual(best_region, regions[0])
    
    def test_estimate_hp_from_region(self):
        """Test de estimación de HP desde región"""
        # Usar la pantalla completa con barra de HP
        region = (100, 50, 200, 20)
        percentage = self.detector._estimate_hp_from_region(
            self.full_screenshot, region
        )
        
        self.assertIsInstance(percentage, float)
        self.assertGreaterEqual(percentage, 0.0)
        self.assertLessEqual(percentage, 100.0)
        
    def test_error_handling(self):
        """Test de manejo de errores"""
        # Imagen inválida
        invalid_images = [
            None,
            np.array([]),
            np.zeros((0, 0, 3)),
            np.zeros((10, 10))  # 2D en lugar de 3D
        ]
        
        for img in invalid_images:
            percentage = self.detector.analyze(img)
            self.assertEqual(percentage, 0.0)
            
    def test_detection_methods(self):
        """Test de los diferentes métodos de detección"""
        # Estos métodos normalmente necesitarían mocking
        # Solo verificamos que existen
        methods = [
            '_detect_by_color',
            '_detect_by_template',
            '_detect_by_pattern'
        ]
        
        for method_name in methods:
            self.assertTrue(hasattr(self.detector, method_name))
            method = getattr(self.detector, method_name)
            self.assertTrue(callable(method))
    
    def tearDown(self):
        """Limpieza"""
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)