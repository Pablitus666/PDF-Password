import tkinter as tk
from app.config import set_app_id, APP_ID, ICON_PATH, COLOR_PRIMARY, WINDOW_WIDTH, WINDOW_HEIGHT
from app.ui import load_main_window_images, create_widgets
from app.utils import centrar_ventana
import sys # Added for sys.frozen check
from app.localization_manager import _ # Import global translation function

# 🔴 DEBE IR ANTES DE CREAR ROOT
set_app_id(APP_ID)

# ============================
# ROOT
# ============================

root = tk.Tk()
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
# Drag & Drop (SOLO EN DESARROLLO)
# ============================

IS_EXE = getattr(sys, 'frozen', False)

if not IS_EXE:
    try:
        from app.ui_dnd import enable_drag_and_drop
        enable_drag_and_drop(file_entry)
    except ImportError:
        pass

# ============================
# START
# ============================

centrar_ventana(root, WINDOW_WIDTH, WINDOW_HEIGHT)
root.deiconify()
root.mainloop()