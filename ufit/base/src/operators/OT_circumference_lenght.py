import bpy
from .core.OT_base import OTBase
from .utils import general
from math import ceil, floor

# Функция для создания временной окружности


def add_circumference(context, z=0.0):
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return
    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_circle_add(radius=0.2, enter_editmode=False, align='WORLD', location=(0, 0, z),
                                      scale=(1, 1, 1))
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode='OBJECT')

    circum_obj = bpy.context.active_object
    circum_obj.name = "Temp_circumference"
    circum_obj.lock_location[0] = True
    circum_obj.lock_location[1] = True

    boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'INTERSECT'
    boolean_mod.solver = 'FAST'
    boolean_mod.object = measure_obj
    # Add limit location constraint (only for Z-axis)
    limit_loc = circum_obj.constraints.new(type='LIMIT_LOCATION')
    limit_loc.use_transform_limit = True
    step = 0.001  # Adding offset
    min_z, max_z = general.get_min_max(measure_obj, 'z')
    limit_loc.use_min_z = limit_loc.use_max_z = True
    limit_loc.min_z = ceil(min_z / step) * step + step
    limit_loc.max_z = floor(max_z / step) * step - step
    limit_loc.use_min_x = limit_loc.use_max_x = False
    limit_loc.use_min_y = limit_loc.use_max_y = False

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    bpy.ops.wm.tool_set_by_id(name="builtin.move")


# Функция для удаления временной окружности
def delete_circumference(context):
    if "Temp_circumference" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Temp_circumference"], do_unlink=True)
        print("Temp_circumference has been deleted.")


# Функция для вычисления длины окружности
def calc_circumference(context, z=0.0):
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return
    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    original_active_obj = context.view_layer.objects.active
    selected_objects = context.selected_objects

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.mesh.primitive_circle_add(radius=0.2, enter_editmode=False, align='WORLD', location=(0, 0, z),
                                          scale=(1, 1, 1))

        circum_obj = bpy.context.active_object
        context.view_layer.objects.active = circum_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode='OBJECT')

        circum_obj.lock_location[0] = True
        circum_obj.lock_location[1] = True

        boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
        boolean_mod.operation = 'INTERSECT'
        boolean_mod.solver = 'FAST'
        boolean_mod.object = measure_obj

        override = {"object": circum_obj, "active_object": circum_obj}
        bpy.ops.object.modifier_apply(override, modifier="Boolean")

        bpy.ops.object.mode_set(mode='EDIT')
        circumference = general.get_mesh_circumference(circum_obj)
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.data.objects.remove(circum_obj, do_unlink=True)

        print(f"Circumference at Z={z}: {circumference}")
        return circumference
    finally:
        context.view_layer.objects.active = original_active_obj
        for obj in selected_objects:
            obj.select_set(True)


# Оператор для создания окружности
class OTAddCircumference(OTBase):
    bl_idname = "ufit_operators.add_circumference"
    bl_label = "Add Circumference"

    @classmethod
    def poll(cls, context):
        return "Temp_circumference" not in bpy.data.objects  # Кнопка доступна только если Temp_circumference не существует

    def main_func(self, context):
        add_circumference(context)

    def execute(self, context):
        return self.execute_base(context, operator_name="add_circumference")


# Оператор для удаления окружности
class OTDeleteCircumference(OTBase):
    bl_idname = "ufit_operators.delete_circumference"
    bl_label = "Delete Circumference"

    @classmethod
    def poll(cls, context):
        return "Temp_circumference" in bpy.data.objects  # Кнопка доступна только если Temp_circumference существует

    def main_func(self, context):
        delete_circumference(context)

    def execute(self, context):
        return self.execute_base(context, operator_name="delete_circumference")


# Оператор для вычисления длины окружности
class OTCircumferenceLenght(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.circumference_lenght"
    bl_label = "Calculate Circumference"
    # bl_options = {"REGISTER", "UNDO"}

    def main_func(self, context):
        if 'Temp_circumference' in bpy.data.objects:
            z_position = bpy.data.objects['Temp_circumference'].location.z
        else:
            z_position = 0.0

        circumference = calc_circumference(context, z=z_position)
        context.scene.ufit_circumference_result = circumference * 100.0 if circumference else 0.0

    def execute(self, context):
        return self.execute_base(context, operator_name="circumference_lenght")
