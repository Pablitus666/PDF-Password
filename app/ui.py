import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

from app.config import (
    ICON_PATH, LOGO_PATH, BUTTON_IMAGE_PATH, ROBOT_IMAGE_PATH,
    BUTTON_IMG_WIDTH, BUTTON_IMG_HEIGHT, LOGO_IMG_WIDTH, LOGO_IMG_HEIGHT, ROBOT_IMG_WIDTH, ROBOT_IMG_HEIGHT,
    BUTTON_STYLE_PARAMS, COLOR_PRIMARY, COLOR_ACCENT, COLOR_TEXT,
    FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_BUTTON, FONT_SIZE_INFO,
    INFO_WINDOW_WIDTH, INFO_WINDOW_HEIGHT
)
from app.utils import centrar_ventana, on_drop, clear_text_fields, salir, get_dpi_scale_factor, _load_and_scale_image # Import _load_and_scale_image from utils
from app.events import open_file_dialog, process_file_encrypt, process_file_decrypt, process_file_encrypt_edit
from app.localization_manager import _ # Import global translation function


def load_main_window_images(window):
    """
    Carga y escala las imágenes principales (logo, botón) según el DPI de la ventana principal.
    """
    scale_factor = get_dpi_scale_factor(window)
    
    images = {}
    images['button'] = _load_and_scale_image(BUTTON_IMAGE_PATH, BUTTON_IMG_WIDTH, BUTTON_IMG_HEIGHT, scale_factor)
    images['logo'] = _load_and_scale_image(LOGO_PATH, LOGO_IMG_WIDTH, LOGO_IMG_HEIGHT, scale_factor)
    
    return images


def show_info(root_window, main_window_images):
    if not hasattr(root_window, 'info_window') or not root_window.info_window.winfo_exists():
        info_window = tk.Toplevel(root_window)
        info_window.withdraw()
        info_window.title(_("info_window_title"))
        info_window.config(bg=COLOR_PRIMARY)
        info_window.resizable(0, 0)

        if os.path.exists(ICON_PATH):
            info_window.iconbitmap(ICON_PATH)

        frame_info = tk.Frame(info_window, bg=COLOR_PRIMARY)
        frame_info.pack(pady=20, padx=20)

        # Get DPI scale factor specific to the info window
        info_scale_factor = get_dpi_scale_factor(info_window)

        robot_photo = _load_and_scale_image(ROBOT_IMAGE_PATH, ROBOT_IMG_WIDTH, ROBOT_IMG_HEIGHT, info_scale_factor)
        if robot_photo:
            img_label = tk.Label(frame_info, image=robot_photo, bg=COLOR_PRIMARY)
            img_label.image = robot_photo # Anchor image
            img_label.grid(row=0, column=0, rowspan=2, padx=(0, 20), pady=(10, 10))

        message = tk.Label(
            frame_info,
            text=_(f"info_window_text"),
            justify="center",
            bg=COLOR_PRIMARY,
            fg=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE_INFO, "bold"),
            anchor="center"
        )
        message.grid(row=0, column=1, padx=8, pady=(10, 0), sticky="n")

        # Load button image specific to info window DPI
        close_button_image = _load_and_scale_image(BUTTON_IMAGE_PATH, BUTTON_IMG_WIDTH, BUTTON_IMG_HEIGHT, info_scale_factor)
        close_button = tk.Button(
            frame_info,
            text=_("close_button"),
            command=info_window.destroy,
            image=close_button_image,
            **BUTTON_STYLE_PARAMS
        )
        close_button.image = close_button_image # Anchor image
        close_button.grid(row=1, column=1, pady=(10, 10))
        close_button.bind("<Enter>", lambda e: close_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
        close_button.bind("<Leave>", lambda e: close_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))
        close_button.config(borderwidth=0, highlightthickness=0, relief="flat")

        centrar_ventana(info_window, INFO_WINDOW_WIDTH, INFO_WINDOW_HEIGHT)
        info_window.deiconify()
        root_window.info_window = info_window


def create_widgets(root_window, main_window_images):
    file_label = tk.Label(
        root_window,
        text=_("file_label"),
        bg=COLOR_PRIMARY,
        fg=COLOR_TEXT,
        font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold")
    )
    file_label.grid(row=0, column=0, columnspan=2, pady=10)

    file_entry = tk.Entry(
        root_window,
        width=50,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        relief='flat',
        state='readonly'
    )
    file_entry.grid(row=1, column=0, columnspan=2, ipady=5, padx=20)

    button_image_loaded = main_window_images.get('button')

    file_button = tk.Button(
        root_window,
        text=_("search_button"),
        command=lambda: open_file_dialog(file_entry),
        image=button_image_loaded,
        **BUTTON_STYLE_PARAMS
    )
    file_button.image = button_image_loaded
    file_button.grid(row=2, column=0, columnspan=2, pady=10)
    file_button.bind("<Enter>", lambda e: file_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
    file_button.bind("<Leave>", lambda e: file_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))

    password_label = tk.Label(
        root_window,
        text=_("password_label"),
        bg=COLOR_PRIMARY,
        fg=COLOR_TEXT,
        font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold")
    )
    password_label.grid(row=3, column=0, columnspan=2, pady=10)

    password_entry = tk.Entry(
        root_window,
        show='*',
        width=50,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        relief='flat'
    )
    password_entry.grid(row=4, column=0, columnspan=2, ipady=5, padx=20)

    encrypt_button = tk.Button(
        root_window,
        text=_("encrypt_pdf_button"),
        command=lambda: process_file_encrypt(root_window, file_entry, password_entry),
        image=button_image_loaded,
        **BUTTON_STYLE_PARAMS
    )
    encrypt_button.image = button_image_loaded
    encrypt_button.grid(row=5, column=0, padx=10, pady=15)
    encrypt_button.bind("<Enter>", lambda e: encrypt_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
    encrypt_button.bind("<Leave>", lambda e: encrypt_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))

    decrypt_button = tk.Button(
        root_window,
        text=_("decrypt_pdf_button"),
        command=lambda: process_file_decrypt(root_window, file_entry, password_entry),
        image=button_image_loaded,
        **BUTTON_STYLE_PARAMS
    )
    decrypt_button.image = button_image_loaded
    decrypt_button.grid(row=5, column=1, pady=10)
    decrypt_button.bind("<Enter>", lambda e: decrypt_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
    decrypt_button.bind("<Leave>", lambda e: decrypt_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))

    encrypt_edit_button = tk.Button(
        root_window,
        text=_("encrypt_edit_button"),
        command=lambda: process_file_encrypt_edit(root_window, file_entry, password_entry),
        image=button_image_loaded,
        **BUTTON_STYLE_PARAMS
    )
    encrypt_edit_button.image = button_image_loaded
    encrypt_edit_button.grid(row=6, column=0, padx=10, pady=10)
    encrypt_edit_button.bind("<Enter>", lambda e: encrypt_edit_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
    encrypt_edit_button.bind("<Leave>", lambda e: encrypt_edit_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))

    exit_button = tk.Button(
        root_window,
        text=_("exit_button"),
        command=lambda: salir(root_window),
        image=button_image_loaded,
        **BUTTON_STYLE_PARAMS
    )
    exit_button.image = button_image_loaded
    exit_button.grid(row=6, column=1, padx=10, pady=10)
    exit_button.bind("<Enter>", lambda e: exit_button.config(bg=COLOR_PRIMARY, fg=COLOR_ACCENT))
    exit_button.bind("<Leave>", lambda e: exit_button.config(bg=COLOR_PRIMARY, fg=COLOR_TEXT))

    logo_image_loaded = main_window_images.get('logo')
    logo_label = tk.Label(root_window, image=logo_image_loaded, bg=COLOR_PRIMARY)
    logo_label.image = logo_image_loaded
    logo_label.place(x=220, y=260) 
    logo_label.bind("<Button-1>", lambda event: show_info(root_window, main_window_images))

    root_window.bind("<Delete>", lambda event: clear_text_fields(file_entry, password_entry))
    
    return file_entry, password_entry
