import bpy
from bpy_extras.view3d_utils import location_3d_to_region_2d
from ufit.utils import ensure_mode, throttle
from ..operators.utils import general
from math import ceil, floor
from typing import Optional
import traceback
from .core.OT_base import OTBase
import blf

# Глобальные переменные
is_updating = False
circumference_handler = None
saved_mode = None
saved_active = None
saved_selected = None
global_prev_z = 0.0
draw_handler = None  # Для хранения ссылки на обработчик отрисовки
mouse_position = (0, 0)  # Текущая позиция мыши


# Функция для создания временной окружности
def add_circumference(context, z=0.0):
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return
    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']

    # Устанавливаем uFit как активный и выделенный
    context.view_layer.objects.active = measure_obj
    measure_obj.select_set(True)

    # Создаем коллекцию "Circumferences", если она не существует
    collection_name = "Circumferences"
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(new_collection)
    else:
        new_collection = bpy.data.collections[collection_name]

    # Создаем временную окружность
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_circle_add(
        radius=0.2,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, z),
        scale=(1, 1, 1)
    )
    circum_obj = context.active_object

    # Добавляем объект в коллекцию "Circumferences" и удаляем из других коллекций
    for coll in circum_obj.users_collection:
        coll.objects.unlink(circum_obj)
    new_collection.objects.link(circum_obj)

    # Заполняем круг гранью
    context.view_layer.objects.active = circum_obj
    circum_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Настройка свойств окружности
    circum_obj.name = "TempObject"
    circum_obj.lock_location[0] = True
    circum_obj.lock_location[1] = True

    # Добавляем модификатор Boolean
    boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
    boolean_mod.operation = 'INTERSECT'
    boolean_mod.solver = 'FAST'
    boolean_mod.object = measure_obj

    # Добавляем ограничение по оси Z
    limit_loc = circum_obj.constraints.new(type='LIMIT_LOCATION')
    limit_loc.use_transform_limit = True
    step = 0.001
    min_z, max_z = general.get_min_max(measure_obj, 'z')
    limit_loc.use_min_z = limit_loc.use_max_z = True
    limit_loc.min_z = ceil(min_z / step) * step + step
    limit_loc.max_z = floor(max_z / step) * step - step
    limit_loc.use_min_x = limit_loc.use_max_x = False
    limit_loc.use_min_y = limit_loc.use_max_y = False

    # Настройка центра масс и инструмента перемещения
    context.view_layer.objects.active = circum_obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    bpy.ops.wm.tool_set_by_id(name="builtin.move")

    global global_prev_z
    global_prev_z = circum_obj.location.z


# Функция для удаления временной окружности
def delete_circumference(context):
    temp_obj = bpy.data.objects.get("TempObject")
    if temp_obj:
        bpy.data.objects.remove(temp_obj, do_unlink=True)
        print("TempObject has been deleted.")


# Вычисление окружности
# @throttle(0.66)
def calc_circumference(context, z=0.0) -> Optional[float]:
    print('CALL calc_circumference z = ', z)
    if not hasattr(context, 'view_layer') or not hasattr(context, 'selected_objects') or not hasattr(context, 'active_object'):
        print("Error: Invalid context.")
        return None
    if 'uFit' not in bpy.data.objects:
        print("Error: Object 'uFit' not found.")
        return None
    measure_obj = bpy.data.objects['uFit']
    if 'uFit_Measure' in bpy.data.objects:
        measure_obj = bpy.data.objects['uFit_Measure']
    original_active_obj = context.view_layer.objects.active
    selected_objects = context.selected_objects
    try:
        ensure_mode('OBJECT')
        collection_name = "Circumferences"
        if collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(collection_name)
            context.scene.collection.children.link(new_collection)
        else:
            new_collection = bpy.data.collections[collection_name]

        # Создаем временную окружность
        bpy.ops.mesh.primitive_circle_add(radius=0.2, enter_editmode=False, align='WORLD', location=(0, 0, z), scale=(1, 1, 1))
        circum_obj = bpy.context.active_object

        # Добавляем объект в коллекцию "Circumferences"
        for coll in circum_obj.users_collection:
            coll.objects.unlink(circum_obj)
        new_collection.objects.link(circum_obj)

        # Заполняем круг гранью
        context.view_layer.objects.active = circum_obj
        circum_obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode='OBJECT')

        # Добавляем модификатор Boolean
        boolean_mod = circum_obj.modifiers.new(name="Boolean", type="BOOLEAN")
        boolean_mod.operation = 'INTERSECT'
        boolean_mod.solver = 'FAST'
        boolean_mod.object = measure_obj

        override = {"object": circum_obj, "active_object": circum_obj}
        bpy.ops.object.modifier_apply(override, modifier="Boolean")

        # Вычисляем окружность
        bpy.ops.object.mode_set(mode='EDIT')
        circumference = general.get_mesh_circumference(circum_obj)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Удаляем временный объект
        bpy.data.objects.remove(circum_obj, do_unlink=True)
        return circumference
    except BaseException as e:
        print('ERROR BaseException calc_circumference', e)
        print(traceback.format_exc())
        return None
    finally:
        # Возвращаемся к исходному состоянию
        print('FINALLY calc_circumference')
        context.view_layer.objects.active = original_active_obj
        if selected_objects is not None:
            for obj in selected_objects:
                obj.select_set(True)


# Постоянные вычисления окружности
@throttle(0.66)
def continuous_calc_circumference(scene):
    print('CALL continuous_calc_circumference')
    try:
        if "TempObject" not in bpy.data.objects:
            return
        circum_obj = bpy.data.objects["TempObject"]
        current_z = circum_obj.location.z
        circumference = calc_circumference(bpy.context, z=current_z)
        if circumference is not None:
            scene.ufit_circumference_result = circumference * 100.0
            draw_circumference_text(current_z, circumference)  # Отрисовываем текст на экране
        else:
            print("Warning: circumference calculation returned None")
    except ValueError as e:
        print('ERROR ValueError continuous_calc_circumference', e)
    except BaseException as e:
        print('ERROR continuous_calc_circumference', e)


been_moved = False


def move_finished_handler(scene):
    if "TempObject" in bpy.data.objects:
        circum_obj = bpy.data.objects["TempObject"]
        global global_prev_z, been_moved
        current_z = circum_obj.location.z

        # Проверяем, изменилось ли положение по Z
        if global_prev_z == current_z and been_moved == True:
            print("Move tool released, updating circumference...")
            global_prev_z = current_z  # Обновляем предыдущее положение
            circumference = calc_circumference(bpy.context, z=current_z)
            scene.ufit_circumference_result = circumference * 100.0
            draw_circumference_text(current_z, circumference)  # Отрисовываем текст на экране
            been_moved = False
        if global_prev_z != current_z:
            been_moved = True


# Переключение окружности
def toggle_circumference(self, context):
    global circumference_handler, saved_mode, saved_active, saved_selected, draw_handler
    print('CALL toggle_circumference')
    if context.scene.ufit_circumference_toggle:
        # Сохраняем текущее состояние
        active_obj = bpy.data.objects["uFit"] if "uFit" in bpy.data.objects else None
        if active_obj:
            saved_mode = active_obj.mode
        else:
            saved_mode = 'OBJECT'

        # Сохраняем активный объект и выделенные объекты
        saved_active = context.view_layer.objects.active
        saved_selected = context.selected_objects.copy()

        if "TempObject" not in bpy.data.objects:
            add_circumference(context)

        if circumference_handler not in bpy.app.handlers.depsgraph_update_post:
            circumference_handler = continuous_calc_circumference
            bpy.app.handlers.depsgraph_update_post.append(circumference_handler)
        if move_finished_handler not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(move_finished_handler)

        try:
            ensure_mode('OBJECT')
        except RuntimeError:
            pass

        # Регистрируем обработчик отрисовки
        if draw_handler is None:
            args = (context,)
            draw_handler = bpy.types.SpaceView3D.draw_handler_add(draw_text, args, 'WINDOW', 'POST_PIXEL')
    else:
        if circumference_handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(circumference_handler)
            circumference_handler = None

        if move_finished_handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(move_finished_handler)

        if "TempObject" in bpy.data.objects:
            delete_circumference(context)

        # Восстанавливаем сохраненное состояние
        if saved_active:
            context.view_layer.objects.active = saved_active
        if saved_selected:
            for obj in saved_selected:
                obj.select_set(True)
            for obj in context.selected_objects:
                if obj not in saved_selected:
                    obj.select_set(False)
        if saved_mode:
            try:
                if context.active_object:
                    bpy.ops.object.mode_set(mode=saved_mode)
                else:
                    bpy.ops.object.mode_set(mode='OBJECT')
            except RuntimeError:
                bpy.ops.object.mode_set(mode='OBJECT')

        # Удаляем обработчик отрисовки
        if draw_handler:
            bpy.types.SpaceView3D.draw_handler_remove(draw_handler, 'WINDOW')
            draw_handler = None

        context.scene.ufit_circumference_result = 0.0
        saved_mode = None
        saved_active = None
        saved_selected = None


# Отрисовка текста с окружностью
def draw_circumference_text(z, circumference):
    global mouse_position
    font_id = 0
    blf.size(font_id, 20, 72)  # Размер шрифта
    text = f"Z: {z * 100:.2f} cm, Circumference: {circumference * 100:.2f} cm"

    # Определяем позицию текста (немного выше курсора)
    text_x = mouse_position[0] + 15
    text_y = mouse_position[1] + 15

    # Рисуем текст
    blf.position(font_id, text_x, text_y, 0)
    blf.color(font_id, 1, 1, 1, 1)  # Цвет текста (белый)
    blf.draw(font_id, text)


# Отрисовка текста на экране
def draw_text(context):
    global mouse_position
    if not context.scene.ufit_circumference_toggle:
        return

    # Получаем текущий объект TempObject
    temp_obj = bpy.data.objects.get("TempObject")
    if not temp_obj:
        return

    # Преобразуем центр объекта из 3D в 2D
    region = context.region
    rv3d = context.space_data.region_3d
    center_3d = temp_obj.location  # Центр объекта в 3D-пространстве
    center_2d = location_3d_to_region_2d(region, rv3d, center_3d)

    if not center_2d:  # Если объект вне видимости камеры
        return

    # Определяем позицию текста (немного выше центра объекта)
    text_x = center_2d.x - 50  # Смещение по X для центрирования
    text_y = center_2d.y + 15   # Смещение по Y для размещения над объектом

    # Если результат вычислений доступен, отображаем его
    if hasattr(context.scene, 'ufit_circumference_result'):
        circumference = context.scene.ufit_circumference_result / 100.0
        z_position = temp_obj.location.z

        # Создаем шейдер для отрисовки текста
        font_id = 0
        blf.size(font_id, 20, 72)  # Размер шрифта

        # Формируем текст
        text = f"Z: {z_position * 100:.2f} cm, Circumference: {circumference * 100:.2f} cm"

        # Рисуем текст
        blf.position(font_id, text_x, text_y, 0)
        blf.color(font_id, 1, 1, 1, 1)  # Цвет текста (белый)
        blf.draw(font_id, text)


# Оператор для отслеживания позиции мыши
class OTCircumferenceLength(bpy.types.Operator):
    bl_idname = "ufit_operators.circumference_length"
    bl_label = "show data"

    mouse_position = (0, 0)
    handler = None

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        # Обновляем позицию мыши
        if event.type == 'MOUSEMOVE':
            self.mouse_position = (event.mouse_x, event.mouse_y)

        # Выход из режима, если галочка отключена
        if not context.scene.ufit_circumference_toggle:
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
