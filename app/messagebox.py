import tkinter as tk
from tkinter import messagebox
import os
from app.config import ICON_PATH, MESSAGEBOX_WIDTH, MESSAGEBOX_HEIGHT, COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT, FONT_FAMILY, FONT_SIZE_NORMAL, BUTTON_STYLE_PARAMS, BUTTON_IMAGE_PATH, BUTTON_IMG_WIDTH, BUTTON_IMG_HEIGHT # Import image paths and dimensions
from app.utils import centrar_ventana, get_dpi_scale_factor
from app.ui import _load_and_scale_image # Import the helper from app.ui

def show_custom_messagebox(parent, title, message, file_path=None):

    custom_messagebox = tk.Toplevel(parent) # Use parent instead of root
    custom_messagebox.title(title)
    custom_messagebox.config(bg=COLOR_PRIMARY)
    custom_messagebox.resizable(False, False)
    
    # Set the window to be modal
    custom_messagebox.grab_set()
    
    centrar_ventana(custom_messagebox, MESSAGEBOX_WIDTH, MESSAGEBOX_HEIGHT)

    # Get DPI scale factor specific to the messagebox
    msgbox_scale_factor = get_dpi_scale_factor(custom_messagebox)

    msg_label = tk.Label(
        custom_messagebox,
        text=message,
        bg=COLOR_PRIMARY,
        fg=COLOR_TEXT,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        wraplength=350
    )
    msg_label.pack(pady=20)

    buttons_frame = tk.Frame(
        custom_messagebox,
        bg=COLOR_PRIMARY
    )
    buttons_frame.pack(fill="x", pady=20)
    
    button_image_loaded = _load_and_scale_image(BUTTON_IMAGE_PATH, BUTTON_IMG_WIDTH, BUTTON_IMG_HEIGHT, msgbox_scale_factor)

    def cerrar_seguro():
        ok_button.config(state="disabled")
        custom_messagebox.destroy()

    ok_button = tk.Button(
        buttons_frame,
        text="OK",
        command=cerrar_seguro,
        **BUTTON_STYLE_PARAMS
    )
    if button_image_loaded: # Use the image if provided
        ok_button.config(image=button_image_loaded)
        ok_button.image = button_image_loaded # Anchor image to widget
    ok_button.bind(
        "<Enter>",
        lambda e: ok_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT)
    )
    ok_button.bind(
        "<Leave>",
        lambda e: ok_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT)
    )

    if not file_path:
        ok_button.pack()
    else:
        ok_button.pack(side="left", padx=40)

        def abrir_carpeta():
            try:
                carpeta = os.path.dirname(file_path)
                if os.path.exists(carpeta):
                    os.startfile(carpeta)
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo abrir la carpeta:\n{str(e)}"
                )

        open_button = tk.Button(
            buttons_frame,
            text="Abrir carpeta",
            command=abrir_carpeta,
            **BUTTON_STYLE_PARAMS
        )
        if button_image_loaded: # Use the image if provided
            open_button.config(image=button_image_loaded)
            open_button.image = button_image_loaded # Anchor image to widget
        open_button.pack(side="right", padx=40)

        open_button.bind(
            "<Enter>",
            lambda e: open_button.config(
                bg=COLOR_PRIMARY,
                fg=COLOR_ACCENT
            )
        )
        open_button.bind(
            "<Leave>",
            lambda e: open_button.config(
                bg=COLOR_PRIMARY,
                fg=COLOR_TEXT
            )
        )

    custom_messagebox.iconbitmap(ICON_PATH)

    if file_path:
        custom_messagebox.update_idletasks()

        base_height = MESSAGEBOX_HEIGHT
        extra_needed = msg_label.winfo_reqheight() - 80

        if extra_needed > 0:
            centrar_ventana(
                custom_messagebox,
                MESSAGEBOX_WIDTH,
                base_height + extra_needed
            )
    
    parent.wait_window(custom_messagebox)