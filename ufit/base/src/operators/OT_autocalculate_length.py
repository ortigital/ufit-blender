import bpy
from bpy_extras.view3d_utils import region_2d_to_origin_3d, region_2d_to_vector_3d
from .core.OT_base import OTBase
from mathutils import Vector
from math import atan2
# from .utils.general import get_mesh_circumference
import bmesh
import blf


# Глобальная переменная для хранения временной плоскости
temp_plane = None


# Функция для получения Z-координаты через raycast
def get_z_position_from_raycast(context, mouse_x, mouse_y):
    region = context.region
    rv3d = context.space_data.region_3d

    if not region or not rv3d:
        return None

    try:
        # Получаем направление и начало raycast'а
        origin = region_2d_to_origin_3d(region, rv3d, (mouse_x, mouse_y))
        direction = region_2d_to_vector_3d(region, rv3d, (mouse_x, mouse_y)).normalized()

        # Raycast по всем объектам в сцене
        depsgraph = context.evaluated_depsgraph_get()
        result, location, normal, index, object, matrix = context.scene.ray_cast(
            depsgraph=depsgraph,
            origin=origin,
            direction=direction,
            distance=1000.0
        )

        if result:  # Если найдена точка соприкосновения
            return location.z
        else:  # Если нет соприкосновения
            target_point = origin + direction * 1.0
            return target_point.z

    except Exception as e:
        print(f"Error during raycast: {e}")
        return None


# Функция для вычисления периметра с использованием кэшированной плоскости
def calculate_perimeter_at_z(context, z_position):
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return "N/A"

    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    # Создаём временную геометрию для пересечения
    bm = bmesh.new()
    bm.from_mesh(measure_obj.data)
    bm.transform(measure_obj.matrix_world)

    # Фильтруем вершины по оси Z
    vertices = [v for v in bm.verts if abs(v.co.z - z_position) < 0.0001]

    if not vertices:
        bm.free()
        return 0.0

    # Сортируем вершины по углу для правильного подсчёта периметра
    center = sum((v.co for v in vertices), Vector()) / len(vertices)
    vertices.sort(key=lambda v: atan2(v.co.y - center.y, v.co.x - center.x))

    perimeter = 0.0
    num_verts = len(vertices)
    for i in range(num_verts):
        v1 = vertices[i].co
        v2 = vertices[(i + 1) % num_verts].co
        perimeter += (v2 - v1).length

    bm.free()
    return perimeter


# Обработчик отрисовки текста
def draw_text(self, context):
    if not context.scene.display_mouse_position:
        return

    # Получаем текущую позицию мыши
    mouse_x, mouse_y = self.mouse_position

    # Получаем Z-координату через raycast
    z_position = get_z_position_from_raycast(context, mouse_x, mouse_y)

    if z_position is None:
        text = "Z: N/A, Perimeter: N/A"
    else:
        # Вычисляем периметр на уровне Z
        perimeter = calculate_perimeter_at_z(context, z_position)
        text = f"Z: {z_position * 100.0:.2f} cm, Perimeter: {perimeter*100.0:.2f} cm"

    # Создаем шейдер для отрисовки текста
    font_id = 0
    blf.size(font_id, 20, 72)  # Размер шрифта

    # Определяем позицию текста (немного выше курсора)
    text_x = mouse_x + 15
    text_y = mouse_y + 15

    # Рисуем текст
    blf.position(font_id, text_x, text_y, 0)
    blf.color(font_id, 1, 1, 1, 1)  # Цвет текста (белый)
    blf.draw(font_id, text)


def toggle_display(self, context):
    if context.scene.display_mouse_position:
        bpy.ops.wm.track_mouse_position('INVOKE_DEFAULT')


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
            if self.handler:
                bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
                self.handler = None
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        args = (self, context)
        self.handler = bpy.types.SpaceView3D.draw_handler_add(draw_text, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
