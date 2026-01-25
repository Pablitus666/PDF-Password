## 🤝 Contribuir a Programa Apagado

¡Gracias por tu interés en contribuir a Programa Apagado! A continuación, encontrarás las guías para compilar el proyecto desde el código fuente y entender el flujo de trabajo de automatización.

## 📦 Instalación y Compilación

Si deseas compilar el proyecto desde el código fuente, necesitarás:

*   **Python 3.10** o superior.
*   **`pip`** (gestor de paquetes de Python).

Para compilar tu propio ejecutable (requiere Windows):

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Pablitus666/Apagado.git
    cd Apagado
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    pip install pyinstaller auto-py-to-exe
    ```
3.  **Ejecuta `auto-py-to-exe`:**
    ```bash
    auto-py-to-exe
    ```
4.  En la interfaz de `auto-py-to-exe`:
    *   **Script Location:** Selecciona `Apagado.py`.
    *   **Onefile:** Marca esta opción.
    *   **Windowed (no console):** Marca esta opción.
    *   **Add Data:** Añade la carpeta `images` (destino: `images`) y el archivo `requireAdministrator.manifest` (destino: `requireAdministrator.manifest`).
    *   **Icon:** Selecciona `images/icon.png`.
    *   Haz clic en "Convert .py to .exe".

El ejecutable se generará en la carpeta `output/`.

## 🚀 Automatización con GitHub Actions

Este repositorio incluye un flujo de trabajo de GitHub Actions para automatizar la compilación del ejecutable cada vez que se realizan cambios en la rama `main`.

El archivo `.github/workflows/build.yml` contiene la configuración:

```yaml
name: Build EXE

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller pillow

    - name: Build executable
      run: |
        pyinstaller --noconfirm --onefile --windowed --add-data "images;images" Apagado.py

    - name: Upload EXE
      uses: actions/upload-artifact@v4
      with:
        name: ApagadoApp
        path: dist/*.exe
```