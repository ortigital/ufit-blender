import bpy
from ..base_constants import base_ui_consts
from .utils.general import UFitPanel


class UICircumferenceLenght(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_circumference_lenght"
    bl_label = base_ui_consts['persistent']['circumference_lenght']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.row().column()

        # row = layout.row(align=True)
        # row.prop(context.scene, "circumference_lenght", text="")

        row1 = layout.row()
        row1.operator("ufit_operators.circumference_lenght", text="Next")

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'import_scan'] \
            and not context.scene.ufit_circums_highlighted
