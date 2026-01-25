import json
import os
import locale
from app.config import LANG_FOLDER, DEFAULT_LANG, AVAILABLE_LANGS, resource_path

class LocalizationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.translations = {}
        self.current_lang = DEFAULT_LANG
        self.load_translations()
        self.set_language(self.detect_system_language())

    def load_translations(self):
        """Carga todos los archivos de traducción disponibles."""
        for lang_code in AVAILABLE_LANGS:
            lang_file_path = resource_path(os.path.join(LANG_FOLDER, f"{lang_code}.json"))
            try:
                with open(lang_file_path, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except FileNotFoundError:
                print(f"Advertencia: Archivo de traducción no encontrado para '{lang_code}'. Esperado en: {lang_file_path}")
            except json.JSONDecodeError:
                print(f"Error: Archivo de traducción '{lang_code}.json' está mal formado.")

    def set_language(self, lang_code):
        """Establece el idioma actual si está disponible."""
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        elif lang_code.split('_')[0] in self.translations: # Try base language (e.g., 'es' for 'es_ES')
            self.current_lang = lang_code.split('_')[0]
            return True
        else:
            print(f"Advertencia: Idioma '{lang_code}' no disponible. Usando el idioma por defecto '{DEFAULT_LANG}'.")
            self.current_lang = DEFAULT_LANG # Fallback to default
            return False

    def detect_system_language(self):
        """Detecta el idioma del sistema operativo."""
        try:
            # Obtener el código de idioma del sistema (ej. 'es_ES', 'en_US')
            system_lang = locale.getdefaultlocale()[0]
            if system_lang:
                # Comprobar si el idioma completo está disponible
                if system_lang in AVAILABLE_LANGS:
                    return system_lang
                # Comprobar si el idioma base está disponible
                elif system_lang.split('_')[0] in AVAILABLE_LANGS:
                    return system_lang.split('_')[0]
            return DEFAULT_LANG # Fallback si no se detecta o no está en la lista
        except Exception as e:
            print(f"Error al detectar idioma del sistema: {e}. Usando el idioma por defecto '{DEFAULT_LANG}'.")
            return DEFAULT_LANG

    def get_string(self, key):
        """Obtiene la cadena traducida para una clave dada."""
        # Intenta en el idioma actual
        if self.current_lang in self.translations and key in self.translations[self.current_lang]:
            return self.translations[self.current_lang][key]
        # Intenta en el idioma por defecto si no se encuentra en el actual
        elif DEFAULT_LANG in self.translations and key in self.translations[DEFAULT_LANG]:
            # print(f"Advertencia: Clave '{key}' no encontrada en '{self.current_lang}'. Usando idioma por defecto.")
            return self.translations[DEFAULT_LANG][key]
        # Si no se encuentra en ningún lugar, devuelve la clave como está
        else:
            print(f"Advertencia: Clave '{key}' no encontrada en ningún idioma disponible.")
            return key

# Instancia global para fácil acceso
_ = LocalizationManager().get_string
set_language = LocalizationManager().set_language
get_current_language = lambda: LocalizationManager().current_lang
get_available_languages = lambda: AVAILABLE_LANGS
