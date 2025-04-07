import math
import bmesh
import bpy
import mathutils
import .....utils
from .base_constants import base_ui_consts
from .general import UFitPanel


def find_center_coordinates(verts):
    """
    function is used to find center, where should start a half-sphere
    from bottom of shell
    """
    extremum = utils.vertex_extremum_find(verts)
    return mathutils.Vector((extremum[0] + ((extremum[1] - extremum[0]) / 2),
                             extremum[2] + ((extremum[3] - extremum[2]) / 2),
                             extremum[5]))


def find_radius(verts):
    """
    function is used to search radius length from center
    """
    extremum = utils.vertex_extremum_find(verts)
    center = find_center_coordinates(verts)
    return (abs(extremum[1] - center[0]) + abs(extremum[3] - center[1])) / 2


def update_vertices_to_sphere(obj, offset, center, radius):
    """
    function is used to update vertices position to make half-sphere shape
    """
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    # Мировая матрица и её обратная
    matrix_world = obj.matrix_world
    matrix_world_inv = matrix_world.inverted()
    for v in bm.verts:
        if v.select:
            # Мировые координаты вершины
            world_co = matrix_world @ v.co
            # Вектор от центра сферы к вершине
            direction = world_co - center
            length = direction.length
            # Коэффициент преобразования вектора
            # (Изменение его длинны под радиусу)
            k = radius / length
            direction = direction * k
            # Подменяем старый вектор на новый вектор новой длины
            v.co = direction + center
            # Обновляем координаты вершины (в локальных координатах объекта)
            v.co = matrix_world_inv @ (center)
    # Применить изменения
    bmesh.update_edit_mesh(obj.data)
    obj.data.update()


def update_vertices_to_squircle(verts, ofs):
    for v in verts:
        v.co.x = ofs * (v.co.x ** 4) / (ofs ** 4)
        v.co.y = ofs * (v.co.y ** 4) / (ofs ** 4)


# APL - класс применения изменений
class apl_squircle(bpy.types.Operator):
    bl_idname = "apl.sqrcl"
    bl_label = "Apply new squircle-like position"

    def execute(self, context):
        obj = context.active_object
        OFS = context.scene.slider.floatvalue
        update_vertices_to_squircle(bmesh.from_edit_mesh(obj.data).verts, OFS)
        return {'FINISHED'}


class apl_halfsphere(bpy.types.Operator):
    """
    blender requier registration class in UI. apl_halfsphere - one of requiered
    """
    bl_idname = "apl.hlsphr"
    bl_label = "Apply new half-sphere position"

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        verts = [(obj.matrix_world @ v.co).to_tuple()
                 for v in bm.verts if v.select]
        OFS = context.scene.slider.floatvalue
        update_vertices_to_sphere(
            obj, OFS, find_center_coordinates(verts), find_radius(verts))
        return {'FINISHED'}


class OffsetOperator(bpy.types.PropertyGroup):
    floatvalue: bpy.props.FloatProperty(
        name="Offset", description="FUCK", default=0, min=-10.0, max=10.0, step=0.1)

    # Главный класс изменения дна гильзы


class BottomVertexEditor(UFitPanel, bpy.types.Panel):
    bl_label = "Edit verts"
    bl_idname = "VIEW3D_PT_Shell_Editor"
    bl_space_type = "VIEW_3D"
    bl_category = "Presets"

    # Метод отрисовки элементов панели
    def draw(self, context):
        layout = self.layout
        # self.draw_base(context, "apl.sqrcl", "apl.hlsphr","op.ofs")
        layout.operator(APL_Squircle.bl_idname, text="Squircle")
        layout.operator(APL_Halfsphere.bl_idname, text="Half-Sphere")
        Sc = context.scene.slider
        layout.prop(Sc, "floatvalue", text="Offset")
