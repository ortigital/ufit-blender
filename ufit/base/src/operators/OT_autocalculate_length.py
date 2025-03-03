import bpy
from .core.OT_base import OTBase
from ..properties.callbacks import draw_callback_px


# Оператор для отслеживания позиции мыши
class OTTrackMousePosition(OTBase):
    bl_idname = "wm.track_mouse_position"
    bl_label = "Track Mouse Position"

    mouse_position = (0, 0)
    handler = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        # Обновляем позицию мыши
        if event.type == 'MOUSEMOVE':
            self.mouse_position = (event.mouse_x, event.mouse_y)

        # Выход из режима, если галочка отключена
        if not context.scene.display_mouse_position:
            print("removed")
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        args = (self, context)
        self.handler = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        print("added")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
