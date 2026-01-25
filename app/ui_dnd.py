from tkinterdnd2 import DND_FILES
from tkinterdnd2.TkinterDnD import _require # Import _require
from app.utils import on_drop

def enable_drag_and_drop(entry_widget):
    # Ensure tkdnd is loaded for the root window
    _require(entry_widget._root()) 
    entry_widget.drop_target_register(DND_FILES)
    entry_widget.dnd_bind("<<Drop>>", lambda e: on_drop(e, entry_widget))