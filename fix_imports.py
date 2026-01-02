# fix_imports.py
import sys
import os

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Ahora ejecuta main.py
exec(open("main.py").read())