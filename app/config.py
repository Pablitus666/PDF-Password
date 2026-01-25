import ctypes
import os
import sys

# ============================
# WINDOWS APP ID
# ============================

def set_app_id(app_id):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

APP_ID = "PDFPassword.GestorPDF"

# ============================
# RUTAS
# ============================

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



ICON_PATH = resource_path(os.path.join('images', 'icon.ico'))
LOGO_PATH = resource_path(os.path.join('images', 'logo.png'))
BUTTON_IMAGE_PATH = resource_path(os.path.join('images', 'boton.png'))
ROBOT_IMAGE_PATH = resource_path(os.path.join('images', 'robot.png'))

# Configuración de Internacionalización (i18n)
LANG_FOLDER = resource_path('app/lang')
DEFAULT_LANG = 'es' # Idioma por defecto
AVAILABLE_LANGS = ['es', 'en', 'pt', 'fr', 'de', 'ja', 'ru', 'zh-Hans'] # Idiomas disponibles

# ... (rest of the file)

# ============================
# COLORES
# ============================

COLOR_PRIMARY = '#023047'
COLOR_ACCENT = '#ffdd57'
COLOR_BUTTON_BG = '#033077'
COLOR_TEXT = 'white'

# ============================
# FUENTES
# ============================

FONT_FAMILY = "Comic Sans MS"
FONT_SIZE_TITLE = 14
FONT_SIZE_NORMAL = 12
FONT_SIZE_BUTTON = 10
FONT_SIZE_INFO = 14

# ============================
# TAMAÑOS
# ============================

WINDOW_WIDTH = 544
WINDOW_HEIGHT = 400
MESSAGEBOX_WIDTH = 400
MESSAGEBOX_HEIGHT = 200
INFO_WINDOW_WIDTH = 375
INFO_WINDOW_HEIGHT = 225
BUTTON_IMG_WIDTH = 100
BUTTON_IMG_HEIGHT = 40
LOGO_IMG_WIDTH = 100
LOGO_IMG_HEIGHT = 100
ROBOT_IMG_WIDTH = 120
ROBOT_IMG_HEIGHT = 150

# ============================
# ESTILO BOTONES (se carga la imagen en ui.py)
# ============================
BUTTON_STYLE_PARAMS = {
    'compound': 'center',
    'fg': COLOR_TEXT,
    'font': (FONT_FAMILY, FONT_SIZE_BUTTON, "bold"),
    'bd': 0,
    'bg': COLOR_BUTTON_BG,
    'highlightthickness': 0,
    'relief': 'flat',
    'activebackground': COLOR_PRIMARY,
    'activeforeground': COLOR_ACCENT
}
