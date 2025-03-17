import bpy
from bpy_extras.view3d_utils import region_2d_to_origin_3d, region_2d_to_vector_3d
import bmesh
import blf


# Глобальные переменные
z_position = 0.0
perimeter = 0.0
circumference_handler = None
is_updating = False


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


# Создание круга программно
def create_circle(radius, location, name="Circle"):
    mesh = bpy.data.meshes.new(name=f"{name}_Mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=radius, segments=32)
    bm.to_mesh(mesh)
    bm.free()

    obj.location = location
    obj.scale = (1, 1, 1)

    return obj


# Вычисление периметра
def calculate_perimeter_at_z(context, z_position):
    global perimeter
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return "N/A"

    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    # Создание круга программно
    circum_obj = create_circle(radius=0.2, location=(0, 0, z_position), name="Circum")
    print("circle added")

    # Убедимся, что контекст настроен правильно
    override = {
        "object": circum_obj,
        "active_object": circum_obj,
        "selected_objects": [circum_obj],
        "selected_editable_objects": [circum_obj]
    }

    # Заполнение круга гранью
    bpy.ops.object.mode_set(override, mode='EDIT')
    bpy.ops.mesh.edge_face_add(override)
    bpy.ops.object.mode_set(override, mode='OBJECT')
    print("circle edited")

    # Добавление модификатора Boolean
    boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'INTERSECT'
    boolean_mod.solver = 'FAST'
    boolean_mod.object = measure_obj

    # Применение модификатора Boolean
    bpy.ops.object.mode_set(mode='OBJECT')
    print(bpy.context.object.mode)
    override_apply = {"object": circum_obj, "active_object": circum_obj}
    bpy.ops.object.modifier_apply(override_apply, modifier="Boolean")

    # Вычисление периметра
    circumference = get_mesh_circumference(circum_obj)
    # print("Perimeter calculated:", circumference)

    # Удаление временного объекта
    bpy.data.objects.remove(circum_obj, do_unlink=True)
    return circumference


# Вычисление периметра с помощью bmesh
def get_mesh_circumference(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)  # Учитываем трансформации объекта

    circumference = 0.0
    for edge in bm.edges:
        if len(edge.link_faces) < 2:  # Только внешние рёбра
            circumference += edge.calc_length()

    bm.free()  # Освобождаем bmesh
    return circumference


# Обработчик отрисовки текста
def draw_text(self, context):
    global z_position, perimeter
    if not context.scene.display_mouse_position:
        return

    # Получаем текущую позицию мыши
    mouse_x, mouse_y = self.mouse_position

    # Получаем Z-координату через raycast
    z_position = get_z_position_from_raycast(context, mouse_x, mouse_y)
    print(z_position, "-", perimeter)
    if z_position is None or perimeter is None:
        text = "Z: N/A, Perimeter: N/A"
    else:
        text = f"Z: {z_position * 100.0:.2f} cm, Perimeter: {perimeter * 100.0:.2f} cm"

    # Отрисовка текста
    font_id = 0
    blf.size(font_id, 20, 72)  # Размер шрифта
    text_x = mouse_x + 15
    text_y = mouse_y + 15

    blf.position(font_id, text_x, text_y, 0)
    blf.color(font_id, 1, 1, 1, 1)  # Цвет текста (белый)
    blf.draw(font_id, text)


# Функция для постоянных вычислений
def continuous_calc_circumference(scene):
    global is_updating, perimeter, z_position
    if is_updating:
        return
    is_updating = True

    try:
        # Выполняем вычисления
        perimeter = calculate_perimeter_at_z(bpy.context, z_position)
    finally:
        is_updating = False


# Переключение обработчика
def toggle_display(self, context):
    global circumference_handler
    if context.scene.display_mouse_position:
        bpy.ops.wm.track_mouse_position('INVOKE_DEFAULT')

        if circumference_handler is None or circumference_handler not in bpy.app.handlers.depsgraph_update_post:
            circumference_handler = continuous_calc_circumference
            bpy.app.handlers.depsgraph_update_post.append(circumference_handler)
    else:
        if circumference_handler is not None and circumference_handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(circumference_handler)
            circumference_handler = None


# Оператор для отслеживания позиции мыши
class OTTrackMousePosition(bpy.types.Operator):
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
