from .src.preferences import preferences
from .src.properties import properties
from .src.operators import operators
from .src.ui import ui
import bpy
from .storage import Storage

def register():
    Storage.user_use_translate_new_dataname = bpy.context.preferences.view.use_translate_new_dataname
    bpy.context.preferences.view.use_translate_new_dataname = False
    preferences.register()
    properties.register()
    operators.register()
    ui.register()


def unregister():
    bpy.context.preferences.view.use_translate_new_dataname = Storage.user_use_translate_new_dataname
    preferences.unregister()
    properties.unregister()
    operators.unregister()
    ui.unregister()
