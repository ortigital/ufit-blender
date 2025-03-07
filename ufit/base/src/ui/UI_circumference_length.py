import bpy
from ..base_constants import base_ui_consts
from .utils.general import UFitPanel


class UICircumferenceLength(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_circumference_length"
    bl_label = base_ui_consts['persistent']['circumference_length']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (
                context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'indicate', 'verify_clean_up', 'clean_up', 'rotate', 'import_scan']
                and not context.scene.ufit_circums_highlighted
        )

    def draw(self, context):
        layout = self.layout

        # Галочка для включения/выключения вычислений
        row1 = layout.row()
        row1.prop(context.scene, "ufit_circumference_toggle", text="Calculate Circumference")

        # Поле для вывода результата
        if hasattr(context.scene, 'ufit_circumference_result'):
            row2 = layout.row()
            row2.label(text="Circumference Result:")
            row2.prop(context.scene, "ufit_circumference_result", text="")
        