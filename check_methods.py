# check_methods.py
import re

with open('core/tibia_bot.py', 'r') as f:
    content = f.read()

# Buscar todas las llamadas a métodos de detector
pattern = r'self\.detector\.(\w+)'
methods = re.findall(pattern, content)

# Filtrar solo los que empiezan con 'detect_'
detect_methods = [m for m in methods if m.startswith('detect_')]
unique_methods = sorted(set(detect_methods))

print("Métodos detect_* requeridos por tibia_bot.py:")
for method in unique_methods:
    print(f"  - {method}")