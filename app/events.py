import tkinter as tk
from tkinter import filedialog
import os
import PyPDF2

from app.messagebox import show_custom_messagebox
from app.pdf_service import encrypt_pdf, smart_decrypt_pdf, encrypt_edit_pdf, is_pdf_encrypted
from app.localization_manager import _ # Import global translation function


def open_file_dialog(file_entry):
    file_path = filedialog.askopenfilename(
        filetypes=[(_("file_dialog_pdf_files"), "*.pdf")]
    )
    if file_path:
        file_path = file_path.strip('{}') # Clean the path
        file_entry.config(state='normal')
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_entry.config(state='readonly')


def _validate_inputs_for_encryption(root, file_entry, password_entry):
    """Helper to validate common inputs for encryption functions."""
    file_path = file_entry.get().strip('{}')
    password = password_entry.get()

    if not file_path.strip() or not password.strip():
        show_custom_messagebox(
            root,
            _("input_error_title"),
            _("input_error_provide_path_password"),
            None
        )
        return None, None

    # Check if the PDF is already encrypted
    if is_pdf_encrypted(file_path):
        show_custom_messagebox(
            root,
            _("file_already_encrypted_title"),
            _("file_already_encrypted_message"),
            None
        )
        return None, None

    return file_path, password


def process_file_encrypt(root, file_entry, password_entry):
    file_path, password = _validate_inputs_for_encryption(root, file_entry, password_entry)
    if not file_path:
        return

    new_file_path = (
        os.path.splitext(file_path)[0] + "_protected.pdf"
    )

    try:
        encrypt_pdf(file_path, new_file_path, password)
        show_custom_messagebox(
            root,
            _("success_title"),
            _(f"file_encrypted_view_success_message") + \
                f"{_('saved_as_message_suffix')}{os.path.basename(new_file_path)}",
            new_file_path
        )
    except ValueError as e:
        show_custom_messagebox(
            root,
            _("file_error_title"),
            str(e),
            None
        )


def process_file_decrypt(root, file_entry, password_entry):
    file_path = file_entry.get().strip('{}')
    if not file_path:
        show_custom_messagebox(
            root,
            _("input_error_title"),
            _("input_error_select_pdf"),
            None
        )
        return

    new_file_path = os.path.splitext(file_path)[0] + "_decrypted.pdf"
    password = password_entry.get().strip() or None

    try:
        success, msg = smart_decrypt_pdf(
            input_file=file_path,
            output_file=new_file_path,
            password=password
        )
        
        if not success and msg == _("file_no_protection_message"): # Check success boolean
            show_custom_messagebox(
                root,
                _("no_protection_title"),
                _("no_protection_message"),
                None
            )
        else:
            show_custom_messagebox(
                root,
                _("success_title"),
                f"{msg}{_('saved_as_message_suffix')}{os.path.basename(new_file_path)}",
                new_file_path
            )
    except ValueError as e:
        show_custom_messagebox(
            root,
            _("file_error_title"),
            str(e),
            None
        )


def process_file_encrypt_edit(root, file_entry, password_entry):
    file_path, password = _validate_inputs_for_encryption(root, file_entry, password_entry)
    if not file_path:
        return

    new_file_path = (
        os.path.splitext(file_path)[0] + "_edit_protected.pdf"
    )
    try:
        encrypt_edit_pdf(file_path, new_file_path, password)
        show_custom_messagebox(
            root,
            _("success_title"),
            _(f"file_encrypted_edit_success_message") + \
                f"{_('saved_as_message_suffix')}{os.path.basename(new_file_path)}",
            new_file_path
        )
    except ValueError as e:
        show_custom_messagebox(
            root,
            _("file_error_title"),
            str(e),
            None
        )
