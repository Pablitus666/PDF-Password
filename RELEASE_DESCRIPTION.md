## 🚀 PDF Password v1.1.0 – Con Drag & Drop y Gestión Avanzada de Protección

Nos complace anunciar el lanzamiento de **PDF Password v1.1.0**, una actualización significativa de nuestra aplicación de escritorio para **proteger y gestionar archivos PDF mediante contraseña**, diseñada con un enfoque en **estabilidad, simplicidad y experiencia de usuario en Windows**.

Esta versión introduce **mejoras clave en la funcionalidad de Drag & Drop y en la gestión inteligente de la protección de PDFs**, consolidándose como una herramienta aún más robusta y amigable para el usuario final.

---

### ✨ Características destacadas

* ✨ **Funcionalidad Drag & Drop** para añadir archivos PDF fácilmente.
* 🔐 **Protección de visualización y edición** de PDFs con contraseña.
* 🔍 **Detección inteligente** del tipo de protección del PDF (visual/edición).
* 🔓 **Descifrado inteligente** de PDFs (elimina protección de edición sin contraseña, visual con contraseña).
* 🚫 **Previene el cifrado** de PDFs ya protegidos.
* 📂 Selección de archivos mediante botón **Buscar PDF**
* 🖼️ Interfaz gráfica limpia y moderna desarrollada con **Tkinter**
* 🖥️ Compatibilidad completa con monitores **HiDPI / 4K**
* 🎨 Uso de imágenes HD escalables (logo, botones y gráficos)
* 💬 **Cuadros de mensaje (pop-ups) modales** con altura dinámica y botones personalizados.
* 🌐 Soporte de **Internacionalización (i18n)**
* 🧠 Arquitectura clara y mantenible (UI / Config / Utils)
* 📦 Ejecutable **.exe empaquetado con PyInstaller**
* 🔏 **Ejecutable firmado digitalmente** para mayor confianza en Windows
* 🚫 Eliminación de dependencias inestables en producción

---

### 🛡️ Estabilidad y seguridad

* ✔️ Sin dependencias experimentales en el ejecutable final
* ✔️ **Drag & Drop robusto y habilitado en producción**, gracias a la inclusión y configuración de `tkinterdnd2`.
* ✔️ **Carga inteligente de imágenes** que se adaptan automáticamente al factor de escala del monitor, garantizando nitidez en cualquier pantalla.
* ✔️ DPI Awareness activado para evitar escalado borroso
* ✔️ Comportamiento consistente en Windows 10 y Windows 11

---

### 📦 Contenido del Release

* `PDF Password.exe` – Ejecutable principal firmado
* Recursos gráficos embebidos
* No requiere instalación de Python ni dependencias externas

---

### 🚀 Cómo usar

1. Descarga el archivo desde esta sección **Releases**
2. Ejecuta `PDF Password.exe`
3. **Arrastra y suelta un archivo PDF en la aplicación o selecciona uno con el botón "Buscar PDF".**
4. Ingresa la contraseña (si es necesario para descifrar)
5. Protege o gestiona tu PDF en segundos

---

### ⚠️ Nota legal

Este software está destinado únicamente al uso legítimo sobre archivos PDF de los cuales el usuario tenga autorización.
El autor no se responsabiliza por el uso indebido de la herramienta.

---

### 📄 Licencia

Distribuido bajo licencia **MIT**.

---

💬 **Feedback, reportes de errores y sugerencias son bienvenidos**
Este proyecto seguirá evolucionando con foco en estabilidad y buenas prácticas.
