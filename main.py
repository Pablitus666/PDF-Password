import sys
import os
import tkinter as tk
import ctypes # Import ctypes here

# ============================
# DPI AWARENESS CONFIGURATION
# ============================
try:
    # Intenta el método más moderno para configurar el reconocimiento de DPI (Windows 10 v1607+)
    DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
    if hasattr(ctypes.windll.shcore, 'SetProcessDpiAwarenessContext'):
        ctypes.windll.shcore.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    elif hasattr(ctypes.windll.shcore, 'SetProcessDpiAwareness'):
        ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
    elif hasattr(ctypes.windll.user32, 'SetProcessDPIAware'):
        ctypes.windll.user32.SetProcessDPIAware()
    else:
        print("Advertencia: No se encontró ninguna función para establecer el reconocimiento de DPI.")
except Exception as e:
    print(f"Error al configurar el reconocimiento de DPI: {e}")

# ============================
# ROOT & TCL PATH CONFIGURATION
# ============================

from app.config import set_app_id, APP_ID, ICON_PATH, COLOR_PRIMARY, WINDOW_WIDTH, WINDOW_HEIGHT
from app.ui import load_main_window_images, create_widgets
from app.utils import centrar_ventana
from app.localization_manager import _ # Import global translation function

set_app_id(APP_ID)

root = tk.Tk()

# Immediately after creating the root, configure the Tcl path if frozen.
# This is the most reliable way to ensure the interpreter is correctly configured.
if getattr(sys, 'frozen', False):
    try:
        # This path is where our --add-data command places the tkdnd library
        tcl_lib_path = os.path.join(sys._MEIPASS, 'tkdnd', 'win64')
        root.tk.call('lappend', 'auto_path', tcl_lib_path)
    except Exception as e:
        # If this fails, drag-and-drop will not work.
        print(f"CRITICAL: Failed to set Tcl auto_path for tkdnd: {e}")

root.withdraw()


root.title(_("app_title"))
root.config(bg=COLOR_PRIMARY)
root.iconbitmap(ICON_PATH)
root.resizable(False, False)

# ============================
# DPI-AWARE IMAGE LOADING & WIDGET CREATION
# ============================

# Load all images, scaled for the current monitor's DPI
images = load_main_window_images(root)

# Create the widgets, passing the pre-scaled images
file_entry, password_entry = create_widgets(root, images)

# ============================
# Drag & Drop
# ============================

try:
    from app.ui_dnd import enable_drag_and_drop
    enable_drag_and_drop(file_entry)
except ImportError as e:
    # Log or handle the error if needed, but don't prevent the app from running
    print(f"Could not enable Drag & Drop: {e}")
    pass

# ============================
# START
# ============================

centrar_ventana(root, WINDOW_WIDTH, WINDOW_HEIGHT)
root.deiconify()
root.mainloop()