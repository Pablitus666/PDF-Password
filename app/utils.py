import tkinter as tk
import os
import ctypes
from PIL import Image, ImageTk # Import PIL and ImageTk

# Para interactuar con las entradas globales del UI (file_entry, password_entry)
# estas serán pasadas como argumentos o se usará una estructura para encapsularlas.
# Por ahora, se asume que las referencias a root, file_entry, password_entry
# serán resueltas a través del módulo main o de un objeto UI central.

def get_dpi_scale_factor(window):
    """
    Obtiene el factor de escala de DPI para una ventana dada en Windows.
    Intenta usar métodos modernos y recurre a los más antiguos por compatibilidad.
    Retorna 1.0 si no se puede determinar.
    """
    scale_factor = 1.0 # Default fallback
    
    try:
        # Intenta el método más moderno para configurar el reconocimiento de DPI (Windows 10 v1607+)
        # PROCESS_PER_MONITOR_DPI_AWARE = 2
        # ctypes.windll.shcore.SetProcessDpiAwareness(2) is deprecated, use SetProcessDpiAwarenessContext
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
        if hasattr(ctypes.windll.shcore, 'SetProcessDpiAwarenessContext'):
            ctypes.windll.shcore.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
        elif hasattr(ctypes.windll.shcore, 'SetProcessDpiAwareness'):
            ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
        elif hasattr(ctypes.windll.user32, 'SetProcessDPIAware'):
            ctypes.windll.user32.SetProcessDPIAware()
        else:
            print("Advertencia: No se encontró ninguna función para establecer el reconocimiento de DPI.")
            
        # Obtener el handle de la ventana
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())

        # Intentar GetDpiForWindow (Windows 10 v1607+)
        if hasattr(ctypes.windll.user32, 'GetDpiForWindow'):
            dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
            scale_factor = dpi / 96.0
        else:
            # Recurrir a GetDeviceCaps si GetDpiForWindow no está disponible
            dc = ctypes.windll.user32.GetDC(0)
            # 90 es LOGPIXELSY (píxeles lógicos por pulgada vertical)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 90)
            ctypes.windll.user32.ReleaseDC(0, dc)
            scale_factor = dpi / 96.0

    except Exception as e:
        print(f"No se pudo obtener el factor de escala DPI: {e}")
        scale_factor = 1.0 # Fallback seguro

    return scale_factor


# Helper to load and scale an image based on DPI factor
def _load_and_scale_image(path, base_width, base_height, scale_factor):
    try:
        img = Image.open(path)
        new_width = int(base_width * scale_factor)
        new_height = int(base_height * scale_factor)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo de imagen: {path}")
        return None

def on_drop(event, file_entry):
    # tkinterdnd2 can return paths enclosed in {}
    file_path = event.data.strip('{}')
    file_entry.config(state='normal')
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)
    file_entry.config(state='readonly')


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.update_idletasks()


def salir(root):
    root.quit()


def clear_text_fields(file_entry, password_entry):
    file_entry.config(state='normal')
    file_entry.delete(0, tk.END)
    file_entry.config(state='readonly')
    password_entry.delete(0, tk.END)
