# create_real_templates.py
import cv2
import numpy as np
import os

def create_hp_template():
    """Crea una plantilla realista de barra de HP"""
    height = 24
    width = 200
    
    # Crear gradiente de rojo (HP lleno a vacío)
    template = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Parte llena (rojo brillante)
    for i in range(width):
        # Gradiente: más brillante a la izquierda, más oscuro a la derecha
        intensity = int(200 * (1 - i/width))
        template[:, i] = [0, 0, intensity]  # BGR: azul=0, verde=0, rojo=intensity
    
    # Añadir bordes oscuros
    template[0, :] = [0, 0, 50]  # Borde superior
    template[-1, :] = [0, 0, 50]  # Borde inferior
    template[:, 0] = [0, 0, 50]  # Borde izquierdo
    template[:, -1] = [0, 0, 50]  # Borde derecho
    
    cv2.imwrite("templates/hp_bar_segment.png", template)
    print("✅ Plantilla HP creada: templates/hp_bar_segment.png")
    
    # También crear versión pequeña para matching
    small_hp = template[:, :50]  # Primeros 50 píxeles
    cv2.imwrite("templates/hp_bar_corner.png", small_hp)
    print("✅ Plantilla HP pequeña creada: templates/hp_bar_corner.png")

def create_mp_template():
    """Crea una plantilla realista de barra de MP"""
    height = 24
    width = 200
    
    # Crear gradiente de azul (MP lleno a vacío)
    template = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Parte llena (azul brillante)
    for i in range(width):
        # Gradiente: más brillante a la izquierda, más oscuro a la derecha
        intensity = int(200 * (1 - i/width))
        template[:, i] = [intensity, 0, 0]  # BGR: azul=intensity, verde=0, rojo=0
    
    # Añadir bordes oscuros
    template[0, :] = [50, 0, 0]  # Borde superior
    template[-1, :] = [50, 0, 0]  # Borde inferior
    template[:, 0] = [50, 0, 0]  # Borde izquierdo
    template[:, -1] = [50, 0, 0]  # Borde derecho
    
    cv2.imwrite("templates/mp_bar_segment.png", template)
    print("✅ Plantilla MP creada: templates/mp_bar_segment.png")

def create_inventory_template():
    """Crea una plantilla de esquina de inventario"""
    size = 50
    
    # Esquina gris con borde más oscuro
    template = np.ones((size, size, 3), dtype=np.uint8) * 100
    
    # Añadir borde
    template[0, :] = [50, 50, 50]  # Borde superior
    template[-1, :] = [50, 50, 50]  # Borde inferior
    template[:, 0] = [50, 50, 50]  # Borde izquierdo
    template[:, -1] = [50, 50, 50]  # Borde derecho
    
    # Añadir patrón de cuadrícula ligero
    for i in range(1, 4):
        pos = int(size * i / 4)
        template[:, pos] = [70, 70, 70]
        template[pos, :] = [70, 70, 70]
    
    cv2.imwrite("templates/inventory_corner.png", template)
    print("✅ Plantilla inventario creada: templates/inventory_corner.png")

def create_minimap_template():
    """Crea una plantilla de minimapa circular"""
    size = 100
    
    # Crear círculo verde (minimapa)
    template = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Dibujar círculo
    center = (size // 2, size // 2)
    radius = size // 2 - 5
    cv2.circle(template, center, radius, (0, 150, 0), -1)  # Verde medio
    
    # Añadir borde
    cv2.circle(template, center, radius, (0, 100, 0), 2)
    
    # Añadir cruz central (jugador)
    cv2.line(template, (center[0]-5, center[1]), (center[0]+5, center[1]), (0, 0, 255), 2)
    cv2.line(template, (center[0], center[1]-5), (center[0], center[1]+5), (0, 0, 255), 2)
    
    cv2.imwrite("templates/minimap_circle.png", template)
    print("✅ Plantilla minimapa creada: templates/minimap_circle.png")

def main():
    print("🎨 Creando plantillas realistas...")
    
    # Asegurar que existe el directorio
    os.makedirs("templates", exist_ok=True)
    
    create_hp_template()
    create_mp_template()
    create_inventory_template()
    create_minimap_template()
    
    print("\n✅ Todas las plantillas creadas!")
    print("📁 Plantillas disponibles:")
    for file in os.listdir("templates"):
        print(f"   • {file}")

if __name__ == "__main__":
    main()