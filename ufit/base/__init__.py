from .src.preferences import preferences
from .src.properties import properties
from .src.operators import operators
from .src.ui import ui
import bpy


def register():
    global user_use_translate_new_dataname
    user_use_translate_new_dataname = bpy.context.preferences.view.use_translate_new_dataname
    bpy.context.preferences.view.use_translate_new_dataname = False
    preferences.register()
    properties.register()
    operators.register()
    ui.register()


def unregister():
    global user_use_translate_new_dataname
    bpy.context.preferences.view.use_translate_new_dataname = user_use_translate_new_dataname
    preferences.unregister()
    properties.unregister()
    operators.unregister()
    ui.unregister()
