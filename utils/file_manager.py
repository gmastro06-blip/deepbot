"""
Clase FileManager - Manejo de archivos y directorios
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import hashlib

class FileManager:
    """Manejador de archivos para el bot"""
    
    def __init__(self, base_dir: str = "."):
        """
        Inicializa el manejador de archivos
        
        Args:
            base_dir: Directorio base para operaciones
        """
        self.base_dir = Path(base_dir)
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        """Asegura que el directorio base exista"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def ensure_directory(self, directory_path: Union[str, Path]) -> Path:
        """
        Asegura que un directorio exista
        
        Args:
            directory_path: Ruta del directorio
            
        Returns:
            Path del directorio creado/verificado
        """
        if isinstance(directory_path, str):
            directory_path = Path(directory_path)
        
        # Si es relativo, hacerlo relativo al base_dir
        if not directory_path.is_absolute():
            directory_path = self.base_dir / directory_path
        
        directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path
    
    def ensure_file_directory(self, file_path: Union[str, Path]) -> Path:
        """
        Asegura que el directorio de un archivo exista
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Path del directorio creado
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        # Si es relativo, hacerlo relativo al base_dir
        if not file_path.is_absolute():
            file_path = self.base_dir / file_path
        
        # Crear directorio padre si no existe
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path.parent
    
    def save_json(self, data: Dict[str, Any], file_path: Union[str, Path], 
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
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            # Asegurar directorio
            self.ensure_file_directory(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
            
            print(f"💾 JSON guardado en: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando JSON {file_path}: {e}")
            return False
    
    def load_json(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Carga datos desde un archivo JSON
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Datos cargados o None si hay error
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            if not file_path.exists():
                print(f"⚠️  Archivo no existe: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📂 JSON cargado desde: {file_path}")
            return data
            
        except Exception as e:
            print(f"❌ Error cargando JSON {file_path}: {e}")
            return None
    
    def save_text(self, text: str, file_path: Union[str, Path]) -> bool:
        """
        Guarda texto en un archivo
        
        Args:
            text: Texto a guardar
            file_path: Ruta del archivo
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            # Asegurar directorio
            self.ensure_file_directory(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"💾 Texto guardado en: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando texto {file_path}: {e}")
            return False
    
    def load_text(self, file_path: Union[str, Path]) -> Optional[str]:
        """
        Carga texto desde un archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Texto cargado o None si hay error
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            if not file_path.exists():
                print(f"⚠️  Archivo no existe: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            print(f"📂 Texto cargado desde: {file_path}")
            return text
            
        except Exception as e:
            print(f"❌ Error cargando texto {file_path}: {e}")
            return None
    
    def list_files(self, directory: Union[str, Path], pattern: str = "*", 
                   recursive: bool = False) -> List[Path]:
        """
        Lista archivos en un directorio
        
        Args:
            directory: Directorio a listar
            pattern: Patrón de búsqueda (ej: "*.json")
            recursive: Si True, busca recursivamente
            
        Returns:
            Lista de archivos encontrados
        """
        try:
            if isinstance(directory, str):
                directory = Path(directory)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not directory.is_absolute():
                directory = self.base_dir / directory
            
            if not directory.exists():
                return []
            
            if recursive:
                files = list(directory.rglob(pattern))
            else:
                files = list(directory.glob(pattern))
            
            return files
            
        except Exception as e:
            print(f"❌ Error listando archivos en {directory}: {e}")
            return []
    
    def get_file_info(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de un archivo
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Información del archivo o None si hay error
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            if not file_path.exists():
                return None
            
            stats = file_path.stat()
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'size_bytes': stats.st_size,
                'size_human': self._format_size(stats.st_size),
                'created': datetime.fromtimestamp(stats.st_ctime),
                'modified': datetime.fromtimestamp(stats.st_mtime),
                'accessed': datetime.fromtimestamp(stats.st_atime),
                'is_file': file_path.is_file(),
                'is_dir': file_path.is_dir(),
                'extension': file_path.suffix.lower(),
                'parent': str(file_path.parent)
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo info de {file_path}: {e}")
            return None
    
    def _format_size(self, size_bytes: int) -> str:
        """Formatea tamaño en bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def calculate_hash(self, file_path: Union[str, Path], algorithm: str = "md5") -> Optional[str]:
        """
        Calcula el hash de un archivo
        
        Args:
            file_path: Ruta del archivo
            algorithm: Algoritmo de hash ("md5", "sha1", "sha256")
            
        Returns:
            Hash del archivo o None si hay error
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            if not file_path.exists() or not file_path.is_file():
                return None
            
            hash_func = getattr(hashlib, algorithm, None)
            if hash_func is None:
                raise ValueError(f"Algoritmo no soportado: {algorithm}")
            
            hash_obj = hash_func()
            
            with open(file_path, 'rb') as f:
                # Leer en chunks para manejar archivos grandes
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            print(f"❌ Error calculando hash de {file_path}: {e}")
            return None
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path], 
                  overwrite: bool = False) -> bool:
        """
        Copia un archivo
        
        Args:
            source: Archivo origen
            destination: Archivo destino
            overwrite: Si True, sobrescribe si existe
            
        Returns:
            True si se copió exitosamente
        """
        try:
            if isinstance(source, str):
                source = Path(source)
            if isinstance(destination, str):
                destination = Path(destination)
            
            # Si son relativos, hacerlos relativos al base_dir
            if not source.is_absolute():
                source = self.base_dir / source
            if not destination.is_absolute():
                destination = self.base_dir / destination
            
            if not source.exists():
                print(f"⚠️  Archivo origen no existe: {source}")
                return False
            
            if destination.exists() and not overwrite:
                print(f"⚠️  Archivo destino ya existe: {destination}")
                return False
            
            # Asegurar directorio destino
            self.ensure_file_directory(destination)
            
            shutil.copy2(source, destination)
            print(f"📋 Copiado {source} → {destination}")
            return True
            
        except Exception as e:
            print(f"❌ Error copiando archivo {source} → {destination}: {e}")
            return False
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path], 
                  overwrite: bool = False) -> bool:
        """
        Mueve un archivo
        
        Args:
            source: Archivo origen
            destination: Archivo destino
            overwrite: Si True, sobrescribe si existe
            
        Returns:
            True si se movió exitosamente
        """
        try:
            if isinstance(source, str):
                source = Path(source)
            if isinstance(destination, str):
                destination = Path(destination)
            
            # Si son relativos, hacerlos relativos al base_dir
            if not source.is_absolute():
                source = self.base_dir / source
            if not destination.is_absolute():
                destination = self.base_dir / destination
            
            if not source.exists():
                print(f"⚠️  Archivo origen no existe: {source}")
                return False
            
            if destination.exists() and not overwrite:
                print(f"⚠️  Archivo destino ya existe: {destination}")
                return False
            
            # Asegurar directorio destino
            self.ensure_file_directory(destination)
            
            shutil.move(source, destination)
            print(f"🚚 Movido {source} → {destination}")
            return True
            
        except Exception as e:
            print(f"❌ Error moviendo archivo {source} → {destination}: {e}")
            return False
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """
        Elimina un archivo
        
        Args:
            file_path: Ruta del archivo a eliminar
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            
            # Si es relativo, hacerlo relativo al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            if not file_path.exists():
                print(f"⚠️  Archivo no existe: {file_path}")
                return False
            
            if file_path.is_file():
                file_path.unlink()
                print(f"🗑️  Eliminado archivo: {file_path}")
                return True
            elif file_path.is_dir():
                shutil.rmtree(file_path)
                print(f"🗑️  Eliminado directorio: {file_path}")
                return True
            else:
                return False
            
        except Exception as e:
            print(f"❌ Error eliminando {file_path}: {e}")
            return False
    
    def create_backup(self, file_path: Union[str, Path], backup_dir: Union[str, Path] = "backups") -> Optional[Path]:
        """
        Crea un backup de un archivo
        
        Args:
            file_path: Archivo a respaldar
            backup_dir: Directorio de backups
            
        Returns:
            Ruta del backup creado o None si hay error
        """
        try:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            if isinstance(backup_dir, str):
                backup_dir = Path(backup_dir)
            
            # Si son relativos, hacerlos relativos al base_dir
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            if not backup_dir.is_absolute():
                backup_dir = self.base_dir / backup_dir
            
            if not file_path.exists():
                print(f"⚠️  Archivo a respaldar no existe: {file_path}")
                return None
            
            # Crear nombre de backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            
            # Asegurar directorio de backups
            self.ensure_directory(backup_dir)
            
            # Copiar archivo
            if self.copy_file(file_path, backup_path, overwrite=False):
                print(f"💾 Backup creado: {backup_path}")
                return backup_path
            
            return None
            
        except Exception as e:
            print(f"❌ Error creando backup de {file_path}: {e}")
            return None
    
    def cleanup_old_files(self, directory: Union[str, Path], pattern: str = "*", 
                          max_age_days: int = 30, max_files: int = 100) -> int:
        """
        Limpia archivos antiguos
        
        Args:
            directory: Directorio a limpiar
            pattern: Patrón de archivos a considerar
            max_age_days: Edad máxima en días
            max_files: Número máximo de archivos a mantener
            
        Returns:
            Número de archivos eliminados
        """
        try:
            files = self.list_files(directory, pattern, recursive=False)
            
            if not files:
                return 0
            
            # Obtener información de cada archivo
            file_infos = []
            for file_path in files:
                info = self.get_file_info(file_path)
                if info:
                    file_infos.append((file_path, info))
            
            # Ordenar por fecha de modificación (más antiguos primero)
            file_infos.sort(key=lambda x: x[1]['modified'])
            
            deleted_count = 0
            current_time = datetime.now()
            
            for file_path, info in file_infos:
                # Verificar por antigüedad
                age_days = (current_time - info['modified']).days
                
                # Verificar por cantidad
                file_index = file_infos.index((file_path, info))
                
                should_delete = False
                
                # Eliminar si es demasiado viejo
                if max_age_days > 0 and age_days > max_age_days:
                    should_delete = True
                    reason = f"demasiado viejo ({age_days} días)"
                
                # Eliminar si excede el límite de cantidad
                elif max_files > 0 and file_index < len(file_infos) - max_files:
                    should_delete = True
                    reason = f"excede límite de {max_files} archivos"
                
                if should_delete:
                    if self.delete_file(file_path):
                        deleted_count += 1
                        print(f"🧹 Eliminado {file_path.name} ({reason})")
            
            if deleted_count > 0:
                print(f"🧹 Total eliminados: {deleted_count}")
            
            return deleted_count
            
        except Exception as e:
            print(f"❌ Error limpiando archivos en {directory}: {e}")
            return 0