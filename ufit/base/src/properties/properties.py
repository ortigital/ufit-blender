import bpy
from ..operators.utils import general
from math import ceil, floor
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    StringProperty,
)
from . import callbacks


ufit_scene_properties = [
    # settings
    'ufit_full_screen',
    'ufit_quad_view',
    'ufit_orthographic_view',
    'ufit_device_type',

    # progress
    'ufit_progress',

    # files
    'ufit_scan_filename',
    'ufit_folder_modeling',
    'ufit_folder_checkpoints',

    # steps
    'ufit_active_step',
    'ufit_substep',

    # checkpoints
    'ufit_checkpoints',
    'ufit_checkpoint_collection',

    # assistance
    'ufit_assistance_previews_dir',
    'ufit_assistance_previews',
    'ufit_help_text',

    # error message
    'ufit_error_message',

    # import scan
    'ufit_file_type',
    'ufit_scan_scale_size',
    'ufit_colored_scan',

    # clean up
    'ufit_non_manifold_highlighted',

    # circumferences
    'ufit_circum_z_ixs',
    'ufit_init_circumferences',
    'ufit_sculpt_circumferences',
    'ufit_circumferences',
    'ufit_circums_highlighted',
    'ufit_circums_distance',

    'ufit_show_original',
    'ufit_enable_colors',

    # sculpt
    'ufit_sculpt_mode',
    'ufit_sculpt_tool',
    'ufit_vertex_color_all',
    'ufit_smooth_factor',
    'ufit_push_pull_circular',
    'ufit_extrude_amount',
    'ufit_sculpt_brush',

    # cutout
    'ufit_cutout_style',
    'ufit_plane_operation',
    'ufit_number_of_cutouts',
    'ufit_mean_tilt',
    'cutout_selection',

    # scaling
    'ufit_scaling_unit',
    'ufit_liner_scaling',
    'ufit_show_prescale',

    # draw
    'ufit_draw_type',
    'ufit_free_draw_thickness',
    'ufit_solidify_thickness',
    'ufit_voronoi_type',
    'ufit_voronoi_one_thickness',
    'ufit_voronoi_two_thickness',
    'ufit_voronoi_size',

    # socket or milling
    'ufit_socket_or_milling',
    'ufit_milling_flare',
    'ufit_milling_margin',

    # thickness
    'ufit_print_thickness',

    # flare
    'ufit_flare_tool',
    'ufit_flare_height',
    'ufit_flare_percentage',
    'ufit_show_connector',

    # alignment
    'ufit_x_ray',
    'ufit_anchor_point',
    'ufit_alignment_object',
    'ufit_alignment_tool',
    'ufit_connector_loc',

    # transition
    'ufit_try_perfect_print',
    'ufit_total_contact_socket',

    # export
    'ufit_smooth_borders',
    'ufit_show_inner_part',
]


# property group that stores the step and file_path of a checkpoint
class CheckpointPG(bpy.types.PropertyGroup):
    step: StringProperty()
    step_nr: IntProperty()
    sub_step_nr: IntProperty()
    name: StringProperty()
    technical_name: StringProperty()
    file_path: StringProperty()


#################################
# Properties
#################################
is_updating = False
circumference_handler = None
saved_mode = None


def register():
    # platform
    bpy.types.Scene.ufit_platform = EnumProperty(name="Platform", default=1,
                                                 items=[
                                                     ("https://ufit.ugani.org", "uFit", "", 1),
                                                 ])
    # bpy.types.Scene.ufit_platform = EnumProperty(name="Platform", default=1,
    #                                              items=[
    #                                                  ("http://localhost:8069", "uFit", "", 1),
    #                                              ])
    bpy.types.Scene.ufit_user = StringProperty(name="User")
    bpy.types.Scene.ufit_password = StringProperty(name="Password", subtype='PASSWORD')

    # device type
    bpy.types.Scene.ufit_device_type = EnumProperty(name="Device Type", default=1,
                                                    items=[
                                                        ("transtibial", "Transtibial", "", 1),
                                                        ("transfemoral", "Transfemoral", "", 2),
                                                        ("free_sculpting", "Free Sculpting", "", 3),
                                                    ])

    # settings
    bpy.types.Scene.ufit_full_screen = BoolProperty(name="Full Screen", default=False,
                                                    update=callbacks.full_screen)
    bpy.types.Scene.ufit_quad_view = BoolProperty(name="Quad View", default=False,
                                                  update=callbacks.quad_view)
    bpy.types.Scene.ufit_orthographic_view = BoolProperty(name="Ortho. View", default=False,
                                                          update=callbacks.orthographic_view)

    # progress
    bpy.types.Scene.ufit_progress = FloatProperty(name="Progress", subtype="PERCENTAGE", soft_min=0, soft_max=100,
                                                  precision=0)

    # files
    bpy.types.Scene.ufit_scan_filename = StringProperty(name="Scan File Name")
    bpy.types.Scene.ufit_folder_modeling = StringProperty(name="Folder Modeling")
    bpy.types.Scene.ufit_folder_checkpoints = StringProperty(name="Folder Checkpoints")

    # steps (overview)
    bpy.types.Scene.ufit_active_step = StringProperty(name="Active Step", default='platform_login')
    bpy.types.Scene.ufit_substep = IntProperty(name="Active Substep", default=0)

    # checkpoints
    bpy.utils.register_class(CheckpointPG)
    bpy.types.Scene.ufit_checkpoints = EnumProperty(items=callbacks.checkpoint_items)  # gets checkpoints dynamically
    bpy.types.Scene.ufit_checkpoint_collection = CollectionProperty(type=CheckpointPG)  # a collection of CheckpointPG items

    # assistance
    bpy.types.Scene.ufit_assistance_previews_dir = StringProperty(name="Assistance Folder Path")
    bpy.types.Scene.ufit_assistance_previews = EnumProperty(items=callbacks.enum_previews_for_assistance)
    bpy.types.Scene.ufit_help_text = StringProperty(name="Help Text")

    # error message
    bpy.types.Scene.ufit_error_message = StringProperty(name="Error Message")

    # import scan
    bpy.types.Scene.ufit_file_type = EnumProperty(name="File Type", default=2,
                                                  items=[
                                                      ("zip", ".zip", "", 1),
                                                      ("obj", ".obj", "", 2),
                                                      ("stl", ".stl", "", 3),
                                                  ])
    bpy.types.Scene.ufit_scan_scale_size = FloatProperty(name="Scale Scan", min=0.001, max=1.000, step=1, precision=3,
                                                         default=0.001)
    bpy.types.Scene.ufit_colored_scan = BoolProperty(name='Colored Scan', default=True)

    # clean up
    bpy.types.Scene.ufit_non_manifold_highlighted = StringProperty(name="Non Manifold Highlighted")

    # circumferences

    def add_circumference(context, z=0.0):
        if 'uFit' not in bpy.data.objects:
            print("Error: Object 'uFit' not found.")
            return
        measure_obj = bpy.data.objects['uFit']
        if 'uFit_Measure' in bpy.data.objects:
            measure_obj = bpy.data.objects['uFit_Measure']

        # Сохраняем текущий активный объект
        original_active_obj = context.view_layer.objects.active

        try:
            # Создаём временную окружность
            bpy.ops.object.mode_set(mode='OBJECT')  # Убедимся, что мы в OBJECT mode
            bpy.ops.mesh.primitive_circle_add(radius=0.2, enter_editmode=False, align='WORLD', location=(0, 0, z),
                                              scale=(1, 1, 1))

            # Заполняем круг гранью
            circum_obj = bpy.context.active_object
            context.view_layer.objects.active = circum_obj  # Устанавливаем новый объект как активный
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.object.mode_set(mode='OBJECT')

            # Настройка свойств окружности
            circum_obj.name = "Temp_circumference"
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
            step = 0.001  # Оффсет
            min_z, max_z = general.get_min_max(measure_obj, 'z')
            limit_loc.use_min_z = limit_loc.use_max_z = True
            limit_loc.min_z = ceil(min_z / step) * step + step
            limit_loc.max_z = floor(max_z / step) * step - step
            limit_loc.use_min_x = limit_loc.use_max_x = False
            limit_loc.use_min_y = limit_loc.use_max_y = False

            # Настройка центра масс и инструмента перемещения
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.wm.tool_set_by_id(name="builtin.move")

        finally:
            # Восстанавливаем оригинальный активный объект
            context.view_layer.objects.active = original_active_obj

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

    # Функция для постоянных вычислений

    def continuous_calc_circumference(scene):
        global is_updating
        if is_updating:
            return
        is_updating = True

        try:
            # Проверяем, что временная окружность существует
            if "Temp_circumference" in bpy.data.objects:
                circum_obj = bpy.data.objects["Temp_circumference"]
                z_position = circum_obj.location.z

                # Выполняем вычисления
                circumference = calc_circumference(bpy.context, z=z_position)

                # Сохраняем результат в свойство сцены
                bpy.context.scene.ufit_circumference_result = circumference
        finally:
            is_updating = False

    # Обработчик изменения состояния галочки
    # Список допустимых режимов для bpy.ops.object.mode_set
    VALID_MODES = {'OBJECT', 'EDIT', 'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT'}

    def toggle_circumference(self, context):
        global circumference_handler, saved_mode

        if context.scene.ufit_circumference_toggle:
            # Если галочка включена:
            # 1. Сохраняем текущий режим
            saved_mode = bpy.context.object.mode

            # 2. Создаём окружность и регистрируем обработчик
            if "Temp_circumference" not in bpy.data.objects:  # Проверяем, существует ли уже окружность
                add_circumference(context)

            # Регистрируем обработчик, если он ещё не зарегистрирован
            if circumference_handler is None or circumference_handler not in bpy.app.handlers.depsgraph_update_post:
                circumference_handler = continuous_calc_circumference
                bpy.app.handlers.depsgraph_update_post.append(circumference_handler)

            # Устанавливаем режим OBJECT (требуется для работы с окружностью)
            bpy.ops.object.mode_set(mode='OBJECT')

        else:
            # Если галочка выключена:
            # 1. Удаляем окружность и обработчик
            if "Temp_circumference" in bpy.data.objects:
                delete_circumference(context)

            # 2. Удаляем обработчик, если он был зарегистрирован
            if circumference_handler is not None and circumference_handler in bpy.app.handlers.depsgraph_update_post:
                bpy.app.handlers.depsgraph_update_post.remove(circumference_handler)
                circumference_handler = None  # Сбрасываем ссылку на обработчик

            # 3. Возвращаемся к сохранённому режиму (если он допустим)
            if saved_mode and saved_mode in VALID_MODES:
                try:
                    bpy.ops.object.mode_set(mode=saved_mode)
                except RuntimeError:
                    # Если невозможно вернуться к предыдущему режиму,
                    # устанавливаем OBJECT mode по умолчанию
                    bpy.ops.object.mode_set(mode='OBJECT')
            else:
                # Если сохранённый режим недопустим, устанавливаем OBJECT mode
                bpy.ops.object.mode_set(mode='OBJECT')

            # Очищаем результат вычислений
            context.scene.ufit_circumference_result = 0.0

    max_num_circumferences = 15
    bpy.types.Scene.ufit_circum_z_ixs = FloatVectorProperty(name='Circumferences Heights', size=max_num_circumferences)
    bpy.types.Scene.ufit_init_circumferences = FloatVectorProperty(name='Init. Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_sculpt_circumferences = FloatVectorProperty(name='Sculpt. Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_circumferences = FloatVectorProperty(name='Circumferences', size=max_num_circumferences)
    bpy.types.Scene.ufit_circums_highlighted = BoolProperty(name='Circumferences Highlighted', default=False)
    bpy.types.Scene.ufit_circums_distance = FloatProperty(name="Distance", min=0.001, max=float("inf"), step=0.01,
                                                          default=0.05, subtype="DISTANCE", unit="LENGTH")
    bpy.types.Scene.ufit_circumference_result = FloatProperty(name="Circumference Result",
                                                              description="Result of the circumference calculation",
                                                              min=0.0, max=float("inf"), step=0.01, default=0.01,
                                                              precision=4)
    bpy.types.Scene.ufit_circumference_toggle = bpy.props.BoolProperty(
        name="Calculate Circumference",
        description="Toggle to calculate circumference dynamically",
        default=False,
        update=toggle_circumference  # Обработчик изменения
    )

    # sculpt
    bpy.types.Scene.ufit_sculpt_mode = EnumProperty(name="Mode", default=1,
                                                    items=[
                                                        ("guided", "Guided", "", 1),
                                                        ("free", "Free", "", 2),
                                                    ],
                                                    update=callbacks.sculpt_mode_update)
    bpy.types.Scene.ufit_sculpt_tool = EnumProperty(name="Sculpting Tool", default=1,
                                                    items=[
                                                        ("push_pull", "Push/Pull", "", 1),
                                                        ("smooth", "Smooth", "", 2),
                                                    ])
    bpy.types.Scene.ufit_enable_colors = BoolProperty(name="Enable Colors", default=True,
                                                      update=callbacks.update_colors_enable)
    bpy.types.Scene.ufit_vertex_color_all = BoolProperty(name="Highlight Whole Object", default=False,
                                                         update=callbacks.update_vertex_color_all)
    bpy.types.Scene.ufit_smooth_factor = IntProperty(name="Factor", min=0, max=50, step=1, default=15)
    bpy.types.Scene.ufit_push_pull_circular = BoolProperty(name="Circular Push/Pull", default=True)
    bpy.types.Scene.ufit_extrude_amount = FloatProperty(name="Amount", min=0, max=100.0, step=50, default=3.5)
    bpy.types.Scene.ufit_sculpt_brush = EnumProperty(name="Sculpting Tool", default=1,
                                                     items=[
                                                         ("push_brush", "Push", "", 1),
                                                         ("pull_brush", "Pull", "", 2),
                                                         ("smooth_brush", "Smooth", "", 3),
                                                         ("flatten_brush", "Flatten", "", 4),
                                                     ],
                                                     update=callbacks.sculpt_brush_update)

    # border
    bpy.types.Scene.ufit_border_choice = EnumProperty(name="Border Choice", default=1,
                                                      items=[
                                                          ("border", "Yes", "", 1),
                                                          ("no_border", "No", "", 2),
                                                      ])

    # cutout
    bpy.types.Scene.ufit_cutout_style = EnumProperty(name="Cutout Style", default=1,
                                                     items=[
                                                         ("free", "Free", "", 1),
                                                         ("straight", "Straight", "", 2),
                                                     ],
                                                     update=callbacks.cutout_style_update)
    bpy.types.Scene.ufit_plane_operation = EnumProperty(name="Plane Operation", default=1,
                                                        items=[
                                                            ("move", "Move", "", 1),
                                                            ("rotate", "Rotate", "", 2),
                                                            ("scale", "Scale", "", 3),
                                                        ],
                                                        update=callbacks.plane_operation_update)

    bpy.types.Scene.ufit_number_of_cutouts = IntProperty(name="Number of Cutouts", default=0)
    bpy.types.Scene.ufit_mean_tilt = EnumProperty(name="Tilt", default=3,
                                                  items=[
                                                      ("0", "0°", "", 1),
                                                      ("45", "45°", "", 2),
                                                      ("90", "90°", "", 3),
                                                      ("135", "135°", "", 4),
                                                  ],
                                                  update=callbacks.mean_tilt_update)

    # cutout selection
    bpy.types.Scene.cutout_selection = EnumProperty(name="The part you would like to keep?", default=1,
                                                    items=[
                                                        ("ufit_part1", "Part 1", "", 1),
                                                        ("ufit_part2", "Part 2", "", 2),
                                                    ],
                                                    update=callbacks.cutout_selection_update)

    # scaling
    bpy.types.Scene.ufit_scaling_unit = EnumProperty(name="Scaling Unit", default=1,
                                                     items=[
                                                         ("millimeter", "mm", "", 1),
                                                         ("percentage", "%", "", 2)
                                                     ])
    bpy.types.Scene.ufit_liner_scaling = FloatProperty(name="Scaling", min=-50.0, max=50.0, step=50, default=0)
    bpy.types.Scene.ufit_show_prescale = BoolProperty(name="Show Pre-scaling", default=True,
                                                      update=callbacks.show_prescale_update)
    bpy.types.Scene.ufit_show_original = BoolProperty(name="Show Original", default=True,
                                                      update=callbacks.show_original_update)

    # draw
    bpy.types.Scene.ufit_draw_type = EnumProperty(name="Draw Type", default=1,
                                                  items=[
                                                      ("free", "Free", "", 1),
                                                      ("solid", "Solid", "", 2),
                                                      ("voronoi", "Voronoi", "", 3),
                                                  ],
                                                  update=callbacks.draw_type_update)
    bpy.types.Scene.ufit_free_draw_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10, default=2.1,
                                                             update=callbacks.draw_thickness_update)
    bpy.types.Scene.ufit_voronoi_type = EnumProperty(name="Voronoi Type", default=1,
                                                     items=[
                                                         ("voronoi_one", "Voronoi 1", "", 1),
                                                         ("voronoi_two", "Voronoi 2", "", 2),
                                                     ],
                                                     update=callbacks.voronoi_type_update)
    bpy.types.Scene.ufit_solidify_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10, default=2.1,
                                                            update=callbacks.solidify_thickness_update)

    bpy.types.Scene.ufit_voronoi_one_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10, default=2.1,
                                                               update=callbacks.voronoi_one_thickness_update)
    bpy.types.Scene.ufit_voronoi_two_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10, default=2.1,
                                                               update=callbacks.voronoi_two_thickness_update)
    bpy.types.Scene.ufit_voronoi_size = EnumProperty(name="Size", default=3,
                                                     items=[
                                                         ("very_small", "Very Small", "", 1),
                                                         ("small", "Small", "", 2),
                                                         ("medium", "Medium", "", 3),
                                                         ("big", "Big", "", 4),
                                                         ("very_big", "Very Big", "", 5),
                                                         ("empty", "Empty Space", "", 6),
                                                     ],
                                                     update=callbacks.voronoi_size_update)

    # socket or milling
    bpy.types.Scene.ufit_socket_or_milling = EnumProperty(name="3D Printing or CNC Milling?", default=1,
                                                          items=[
                                                              ("socket", "3D Printing", "", 1),
                                                              ("milling", "CNC Milling", "", 2),
                                                          ])
    bpy.types.Scene.ufit_milling_flare = BoolProperty(name="Milling Flare", default=True)
    bpy.types.Scene.ufit_milling_margin = FloatProperty(name="Milling Margin", min=1.0, max=10.0, step=10,
                                                        default=3.0)

    # thickness
    bpy.types.Scene.ufit_print_thickness = FloatProperty(name="Thickness", min=0.0, max=10.0, step=10, default=4.2)

    # flare
    bpy.types.Scene.ufit_flare_tool = EnumProperty(name="Mode", default=2,
                                                   items=[
                                                       ("builtin.scale", "interactive", "", 1),
                                                       ("builtin.select_box", "input", "", 2),
                                                   ],
                                                   update=callbacks.flare_tool_update)
    bpy.types.Scene.ufit_flare_height = bpy.props.FloatProperty(name="Flare Height", step=10,
                                                                get=callbacks.get_flare_height,
                                                                set=callbacks.set_flare_height)
    bpy.types.Scene.ufit_flare_percentage = FloatProperty(name='Flare Perc.', subtype="PERCENTAGE",
                                                          min=0, max=50.0, default=3, precision=1)

    # alignment
    bpy.types.Scene.ufit_x_ray = BoolProperty(name="X-Ray", default=False,
                                              update=callbacks.xray_update)
    bpy.types.Scene.ufit_anchor_point = FloatVectorProperty(name='Anchor Point')

    bpy.types.Scene.ufit_show_connector = BoolProperty(name="Show Connector", default=False,
                                                       update=callbacks.show_connector_update)

    bpy.types.Scene.ufit_alignment_object = EnumProperty(name="Object", default=1,
                                                         items=[
                                                             ("uFit", "socket", "", 1),
                                                             ("Connector", "connector", "", 2),
                                                         ],
                                                         update=callbacks.alignment_object_update)

    bpy.types.Scene.ufit_alignment_tool = EnumProperty(name="Tool", default=1,
                                                       items=[
                                                           ("builtin.rotate", "rotate", "", 1),
                                                           ("builtin.move", "translate", "", 2),
                                                       ],
                                                       update=callbacks.alignment_tool_update)
    bpy.types.Scene.ufit_connector_loc = FloatVectorProperty(name='Connector Location')

    # transition
    bpy.types.Scene.ufit_try_perfect_print = BoolProperty(name="Try Perfect Print", default=False)
    bpy.types.Scene.ufit_total_contact_socket = BoolProperty(name="Total Contact Socket", default=False)

    # export
    bpy.types.Scene.ufit_smooth_borders = BoolProperty(name="Smooth Borders", default=True,
                                                       update=callbacks.smooth_borders_update)
    bpy.types.Scene.ufit_show_inner_part = BoolProperty(name="Show Inner Part", default=False,
                                                        update=callbacks.show_inner_part_update)


def unregister():
    # platform
    del bpy.types.Scene.ufit_platform
    del bpy.types.Scene.ufit_user
    del bpy.types.Scene.ufit_password

    # device type
    del bpy.types.Scene.ufit_device_type

    # settings
    del bpy.types.Scene.ufit_full_screen
    del bpy.types.Scene.ufit_quad_view
    del bpy.types.Scene.ufit_orthographic_view

    # progress
    del bpy.types.Scene.ufit_progress

    # files
    del bpy.types.Scene.ufit_scan_filename
    del bpy.types.Scene.ufit_folder_modeling
    del bpy.types.Scene.ufit_folder_checkpoints

    # steps (overview)
    del bpy.types.Scene.ufit_active_step
    del bpy.types.Scene.ufit_substep

    # checkpoints
    bpy.utils.unregister_class(CheckpointPG)
    del bpy.types.Scene.ufit_checkpoints
    del bpy.types.Scene.ufit_checkpoint_collection

    # assistance
    del bpy.types.Scene.ufit_assistance_previews_dir
    del bpy.types.Scene.ufit_assistance_previews
    del bpy.types.Scene.ufit_help_text

    # error message
    del bpy.types.Scene.ufit_error_message

    # import scan
    del bpy.types.Scene.ufit_file_type
    del bpy.types.Scene.ufit_scan_scale_size
    del bpy.types.Scene.ufit_colored_scan

    # clean up
    del bpy.types.Scene.ufit_non_manifold_highlighted

    # circumferences
    del bpy.types.Scene.ufit_circum_z_ixs
    del bpy.types.Scene.ufit_init_circumferences
    del bpy.types.Scene.ufit_sculpt_circumferences
    del bpy.types.Scene.ufit_circumferences
    del bpy.types.Scene.ufit_circums_highlighted
    del bpy.types.Scene.ufit_circums_distance
    del bpy.types.Scene.ufit_circumference_result
    del bpy.types.Scene.ufit_circumference_toggle

    # extrude/smooth regions
    del bpy.types.Scene.ufit_sculpt_mode
    del bpy.types.Scene.ufit_sculpt_tool
    del bpy.types.Scene.ufit_vertex_color_all
    del bpy.types.Scene.ufit_smooth_factor
    del bpy.types.Scene.ufit_enable_colors
    del bpy.types.Scene.ufit_push_pull_circular
    del bpy.types.Scene.ufit_extrude_amount
    del bpy.types.Scene.ufit_sculpt_brush

    # cutout
    del bpy.types.Scene.ufit_cutout_style
    del bpy.types.Scene.ufit_plane_operation
    del bpy.types.Scene.ufit_number_of_cutouts
    del bpy.types.Scene.ufit_mean_tilt
    del bpy.types.Scene.cutout_selection

    # Scaling
    del bpy.types.Scene.ufit_scaling_unit
    del bpy.types.Scene.ufit_liner_scaling
    del bpy.types.Scene.ufit_show_prescale
    del bpy.types.Scene.ufit_show_original

    # draw
    del bpy.types.Scene.ufit_draw_type
    del bpy.types.Scene.ufit_free_draw_thickness
    del bpy.types.Scene.ufit_solidify_thickness
    del bpy.types.Scene.ufit_voronoi_type
    del bpy.types.Scene.ufit_voronoi_one_thickness
    del bpy.types.Scene.ufit_voronoi_two_thickness
    del bpy.types.Scene.ufit_voronoi_size

    # socket or milling
    del bpy.types.Scene.ufit_socket_or_milling
    del bpy.types.Scene.ufit_milling_flare
    del bpy.types.Scene.ufit_milling_margin

    # thickness
    del bpy.types.Scene.ufit_print_thickness

    # Flare
    del bpy.types.Scene.ufit_flare_tool
    del bpy.types.Scene.ufit_flare_height
    del bpy.types.Scene.ufit_flare_percentage

    # alignment
    del bpy.types.Scene.ufit_x_ray
    del bpy.types.Scene.ufit_show_connector
    del bpy.types.Scene.ufit_anchor_point
    del bpy.types.Scene.ufit_alignment_object
    del bpy.types.Scene.ufit_alignment_tool
    del bpy.types.Scene.ufit_connector_loc

    # transition
    del bpy.types.Scene.ufit_try_perfect_print
    del bpy.types.Scene.ufit_total_contact_socket

    # export
    del bpy.types.Scene.ufit_smooth_borders
    del bpy.types.Scene.ufit_show_inner_part
