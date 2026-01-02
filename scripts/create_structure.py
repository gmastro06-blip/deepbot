#!/usr/bin/env python3
"""
Script para crear automáticamente toda la estructura del proyecto Tibia Bot
"""
import os
import sys
from pathlib import Path

class ProjectCreator:
    """Crea la estructura completa del proyecto"""
    
    def __init__(self, project_name="tibia_bot"):
        self.project_name = project_name
        self.base_dir = Path(project_name)
        
    def create_structure(self):
        """Crea toda la estructura de carpetas y archivos"""
        print(f"🚀 Creando proyecto: {self.project_name}")
        print("=" * 50)
        
        # Crear directorio base
        self.base_dir.mkdir(exist_ok=True)
        
        # Crear todas las carpetas
        folders = [
            "core",
            "config",
            "detectors",
            "processors",
            "utils",
            "tests",
            "templates",
            "configs",
            "scripts",
            "logs",
            "debug",
            "data"
        ]
        
        for folder in folders:
            folder_path = self.base_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 {folder_path}")
        
        # Crear archivos principales
        self.create_main_files()
        
        print("\n" + "=" * 50)
        print("✅ Estructura creada exitosamente!")
        print(f"📦 Ubicación: {self.base_dir.absolute()}")
        print("\n🎯 Siguientes pasos:")
        print("1. cd " + self.project_name)
        print("2. pip install -r requirements.txt")
        print("3. python main.py --help")
        print("=" * 50)
    
    def create_main_files(self):
        """Crea los archivos principales del proyecto"""
        files = {
            "requirements.txt": self.get_requirements_content(),
            "README.md": self.get_readme_content(),
            ".gitignore": self.get_gitignore_content(),
            "main.py": self.get_main_content(),
            
            # Core
            "core/__init__.py": "# Core modules\n",
            "core/tibia_bot.py": self.get_tibia_bot_content(),
            "core/screen_capturer.py": self.get_screen_capturer_content(),
            "core/ui_detector.py": self.get_ui_detector_content(),
            "core/bot_actions.py": self.get_bot_actions_content(),
            "core/bot_state.py": self.get_bot_state_content(),
            
            # Config
            "config/__init__.py": "# Configuration modules\n",
            "config/settings.py": self.get_settings_content(),
            "config/ui_config.py": self.get_ui_config_content(),
            
            # Detectors
            "detectors/__init__.py": "# Element detectors\n",
            "detectors/health_detector.py": self.get_health_detector_content(),
            "detectors/mana_detector.py": self.get_mana_detector_content(),
            "detectors/inventory_detector.py": self.get_inventory_detector_content(),
            "detectors/minimap_detector.py": self.get_minimap_detector_content(),
            
            # Processors
            "processors/__init__.py": "# Image processors\n",
            "processors/image_processor.py": self.get_image_processor_content(),
            "processors/color_detector.py": self.get_color_detector_content(),
            "processors/template_matcher.py": self.get_template_matcher_content(),
            
            # Utils
            "utils/__init__.py": "# Utility modules\n",
            "utils/logger.py": self.get_logger_content(),
            "utils/helpers.py": self.get_helpers_content(),
            "utils/file_manager.py": self.get_file_manager_content(),
            "utils/performance_monitor.py": self.get_performance_monitor_content(),
            
            # Tests
            "tests/__init__.py": "# Unit tests\n",
            "tests/test_screen_capturer.py": self.get_test_screen_capturer_content(),
            "tests/test_health_detector.py": self.get_test_health_detector_content(),
            "tests/test_ui_detector.py": "# Tests for UI Detector\n",
            "tests/test_bot_actions.py": "# Tests for Bot Actions\n",
            
            # Scripts
            "scripts/__init__.py": "# Utility scripts\n",
            "scripts/create_structure.py": "# This file!\n",
            "scripts/calibrate_colors.py": "# Color calibration script\n",
            "scripts/generate_templates.py": "# Template generation script\n",
            
            # Configs
            "configs/default_settings.json": self.get_default_settings_json(),
            "configs/ui_positions.json": "{}",
        }
        
        for filepath, content in files.items():
            full_path = self.base_dir / filepath
            
            # Crear directorios padres si no existen
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📄 {full_path}")
    
 
