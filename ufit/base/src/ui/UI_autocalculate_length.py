import bpy
from ..base_constants import base_ui_consts
from .utils.general import UFitPanel


# Панель для управления отображением позиции мыши
class MousePositionPanel(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_mouse_position"
    bl_label = base_ui_consts['persistent']['autocalculate_length']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (
            context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'indicate', 'verify_clean_up', 'clean_up', 'rotate', 'import_scan']
            and not context.scene.ufit_circums_highlighted
        )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "display_mouse_position")
