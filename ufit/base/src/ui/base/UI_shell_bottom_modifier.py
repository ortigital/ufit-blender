import bpy
import math
import ..base_constants import base_ui_consts
import .utils.general import UFitPanel

#Главный класс изменения дна гильзы
class BottomVertexEditor:
    
    #Метод отрисовки как нового меню
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "vertrex_edit")
