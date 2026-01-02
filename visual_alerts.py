# visual_alerts.py
"""
Alertas visuales simples sin OBS
"""
import tkinter as tk
from tkinter import messagebox
import threading

class VisualAlert:
    """Muestra alertas visuales"""
    
    def __init__(self):
        self.root = None
        self.alert_thread = None
    
    def show_alert(self, title="Alerta", message="¡Cuidado!", alert_type="info"):
        """Muestra una alerta"""
        
        def _show():
            self.root = tk.Tk()
            self.root.withdraw()  # Ocultar ventana principal
            
            if alert_type == "error":
                messagebox.showerror(title, message)
            elif alert_type == "warning":
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
            
            self.root.destroy()
        
        # Ejecutar en un hilo separado
        self.alert_thread = threading.Thread(target=_show)
        self.alert_thread.daemon = True
        self.alert_thread.start()
    
    def show_hp_alert(self, hp_percent):
        """Alerta de HP bajo"""
        self.show_alert(
            "⚠️  HP BAJO",
            f"¡HP crítico: {hp_percent}%!\n¡Cúrate o huye!",
            "warning"
        )

# Uso:
# alert = VisualAlert()
# alert.show_hp_alert(25)