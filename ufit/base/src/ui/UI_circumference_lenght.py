import bpy
from ..base_constants import base_ui_consts
from .utils.general import UFitPanel


class UICircumferenceLenght(UFitPanel, bpy.types.Panel):
    bl_idname = "VIEW3D_PT_circumference_lenght"
    bl_label = base_ui_consts['persistent']['circumference_lenght']['ui_name']
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.scene.ufit_active_step not in ['platform_login', 'device_type', 'start', 'verify_clean_up', 'clean_up', 'rotate', 'import_scan'] \
            and not context.scene.ufit_circums_highlighted

    def draw(self, context):
        layout = self.layout
        col = layout.row().column()

        # Кнопка для создания окружности
        row1 = layout.row()
        if "Temp_circumference" not in bpy.data.objects:
            row1.operator("ufit_operators.add_circumference", text="Create Circumference")
        else:
            row1.label(text="Create Circumference (Already Exists)", icon='ERROR')

        # Кнопка для удаления окружности
        row2 = layout.row()
        if "Temp_circumference" in bpy.data.objects:
            row2.operator("ufit_operators.delete_circumference", text="Delete Circumference")
        else:
            row2.label(text="Temp Circumference (Does Not Exist)", icon='ERROR')

        # Кнопка для вычисления длины окружности
        row3 = layout.row()
        if "Temp_circumference" in bpy.data.objects:
            row3.operator("ufit_operators.circumference_lenght", text="Calculate Circumference")
        else:
            row2.label(text="Temp Circumference (Does Not Exist)", icon='ERROR')

        # Поле для вывода результата
        if hasattr(context.scene, 'ufit_circumference_result'):
            row4 = layout.row()
            row4.label(text="Circumference Result:")
            row4.prop(context.scene, "ufit_circumference_result", text="")
