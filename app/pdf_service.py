import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
import os
import shutil
import tempfile
from app.localization_manager import _ # Import global translation function


def is_valid_pdf(file_path):
    """
    Verifica si el archivo:
    - Existe
    - Tiene extensión .pdf
    - Es un PDF real (no corrupto)
    """
    if not file_path.lower().endswith(".pdf"):
        return False, _("file_selected_not_pdf")

    try:
        # Intenta abrir con PyPDF2.PdfReader primero
        with open(file_path, "rb") as f:
            PdfReader(f)
        return True, None
    except Exception as pypdf2_e:
        # Si PyPDF2 falla, intenta con fitz.open() como respaldo
        try:
            doc = fitz.open(file_path)
            doc.close()
            return True, None # fitz pudo abrirlo, entonces es un PDF válido
        except Exception as fitz_e:
            # Si ambos fallan, entonces el archivo no es un PDF válido o está dañado.
            return False, _("file_not_valid_or_damaged")


# ==================================================
# DETECCIÓN GENERAL
# ==================================================

def is_pdf_encrypted(file_path):
    try:
        reader = PdfReader(file_path)
        return reader.is_encrypted
    except Exception:
        return False


def get_pdf_security_type(file_path):
    """
    Retorna:
    - "visual"  -> requiere contraseña para abrir
    - "edit"    -> solo protegido contra edición
    - "none"    -> sin protección
    - "unknown" -> error o PDF inválido
    """
    try:
        doc = fitz.open(file_path)

        # 🔐 CASO 1: REQUIERE CONTRASEÑA PARA ABRIR (visual)
        if doc.needs_pass:
            doc.close()
            return "visual"

        # Define la bandera de permiso para "modificar contenidos"
        # Esto corresponde al bit 3 (0x0008) en la documentación de PyMuPDF
        PERM_MODIFY_CONTENTS = 0x0008 

        # Si no requiere contraseña para abrirse, y el permiso de modificar contenidos está ACTIVO
        if (not doc.needs_pass) and (doc.permissions & PERM_MODIFY_CONTENTS):
            doc.close()
            return "none"
        # Si no requiere contraseña para abrirse, pero el permiso de modificar contenidos NO está ACTIVO,
        # significa que tiene protección contra edición.
        elif not doc.needs_pass:
            doc.close()
            return "edit"

        doc.close()
        return "unknown" # Fallback, should ideally not be reached if logic is exhaustive

    except Exception as e:
        print(f"Error en get_pdf_security_type: {e}")
        return "unknown"


# ==================================================
# CIFRADO VISUAL (CONTRASEÑA PARA ABRIR)
# ==================================================

def encrypt_pdf(input_file, output_file, password):
    valid, error_msg = is_valid_pdf(input_file)
    if not valid:
        raise ValueError(error_msg)

    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(user_password=password)

    with open(output_file, "wb") as f:
        writer.write(f)


# ==================================================
# DESCIFRADO INTELIGENTE
# ==================================================

def smart_decrypt_pdf(input_file, output_file, password=None):
    valid, error_msg = is_valid_pdf(input_file)
    if not valid:
        raise ValueError(error_msg)

    security_type = get_pdf_security_type(input_file)

    # 🔐 CASO 1: CIFRADO DE VISUALIZACIÓN
    if security_type == "visual":
        if not password:
            raise ValueError(_("pdf_requires_password"))

        reader = PdfReader(input_file)

        if not reader.decrypt(password):
            raise ValueError(_("incorrect_password"))

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_file, "wb") as f:
            writer.write(f)

        return True, _("pdf_decrypted_visual_success")

    # ✏️ CASO 2: SOLO PROTECCIÓN DE EDICIÓN
    elif security_type == "edit":
        doc = fitz.open(input_file)

        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".pdf",
            dir=os.path.dirname(input_file)
        )
        os.close(temp_fd)

        # Guardar sin cifrado ni permisos
        doc.save(temp_path)
        doc.close()

        shutil.move(temp_path, output_file)
        return True, _("edit_protection_removed_success")

    # 🟢 CASO 3: SIN PROTECCIÓN
    elif security_type == "none":
        # Do not copy the file if it has no protection
        return False, _("file_no_protection_message")

    # ⚠️ CASO 4: ERROR
    else:
        raise ValueError(_("cannot_determine_protection"))


# ==================================================
# CIFRADO SOLO PARA EDICIÓN (VISUALIZABLE)
# ==================================================

def encrypt_edit_pdf(input_file, output_file, password):
    valid, error_msg = is_valid_pdf(input_file)
    if not valid:
        raise ValueError(error_msg)

    try:
        doc = fitz.open(input_file)

        permissions = fitz.PDF_PERM_PRINT  # permite imprimir, bloquea edición

        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".pdf",
            dir=os.path.dirname(input_file)
        )
        os.close(temp_fd)

        doc.save(
            temp_path,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            owner_pw=password,
            # SIN user_pw → se abre sin contraseña
            permissions=permissions
        )
        doc.close()

        shutil.move(temp_path, output_file)
        return True, _("file_encrypted_edit_success_message"), output_file

    except Exception as e:
        raise e