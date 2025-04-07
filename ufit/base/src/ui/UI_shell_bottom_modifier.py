import bpy
import math
from  ..base_constants import base_ui_consts
from ..utils.general import UFitPanel

offsetval = 0;

def update_vertices_to_sphere(verts, offsetval):
    for i, v in enumerate(verts):
        angle = (i / len(verts)) * 3.14
        v.co.z = offsetval * sin(angle)
        v.co.x = offsetval * cos(angle) * sin(angle)
        v.co.y = offsetval * cos(angle) * cos(angle)

def update_vertices_to_squircle(verts, offsetval):
    for v in verts:
        v.co.x = offsetval * (v.co.x ** 4) / (offsetval ** 4)
        v.co.y = offsetval * (v.co.y ** 4) / (offsetval ** 4)


#APL - класс применения изменений
class APL_Squircle(bpy.types.operator):
    bl_idname = "apl.sqrcl"
    bl_label = "Apply new squircle-like position"

    def execute(self, context):
        obj = context.active_object
        update_vertices_to_squircle(obj.data.vertices,1)
        return {'FINISHED'}


class APL_Halfsphere(bpy.types.operator):
    bl_idname = "apl.hlsphr"
    bl_label = "Apply new half-sphere position"

    def execute(self, context):
        obj = context.active_object
        update_vertices_to_sphere(obj.data.vertices,1)
        return {'FINISHED'}

class OffsetOperator(bpy.types.operator):
    bl_idname = "op.offset"
    bl_label = "Offset Vertexes"

    offset: bpy.props.FloatProperty(name = "Offset", default = .0, min = -10, max = 10)
    def execute(self, context):
        context.window_manager.modal_handler_add(self)

#Главный класс изменения дна гильзы
class BottomVertexEditor(UFitPanel, bpy.types.Panel):
    bl_label = base_ui_consts['view']['ui_name']['gunshell']
    bl_idname = "VIEW3D_PT_Shell_Editor"

    #Метод отрисовки как нового меню
    def draw(self, context):
        layout = self.layout
        self.draw_base(context, "apl.sqrcl", "apl.hlsphr","op.offset")
        layout.operator("apl.sqrcl", text = "Squircle")
        layout.operator("apl.hlsphr", text = "Half-Sphere")
        layout.operator("op.offset", text = "Offset")

