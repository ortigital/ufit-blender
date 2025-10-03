import inspect
import time
from functools import wraps

import bpy
import mathutils

# from typing import List


# Vector3DType = tuple[float, float, float]


# def divide_tuples(tuple1, tuple2) -> Vector3DType:
#     return tuple(a / b for a, b in zip(tuple1, tuple2))


# def sum_tuples(tuple1, tuple2) -> Vector3DType:
#     return tuple(a + b for a, b in zip(tuple1, tuple2))


# # def average_arifm(coords: List[mathutils.Vector]) -> mathutils.Vector:
# def average_arifm(coords: List[Vector3DType]) -> Vector3DType:
#     # Initialize a zero vector
#     # sum_vector = mathutils.Vector((0.0, 0.0, 0.0))
#     sum_vector = tuple((0.0, 0.0, 0.0))

#     # Sum all vectors in the list
#     for coord in coords:
#         # sum_vector += coord
#         sum_vector = sum_tuples(sum_vector, coord)

#     # Divide by the number of vectors to get the average
#     if len(coords) > 0:  # Check if coords is not empty to avoid division by zero
#         n_coords = float(len(coords))
#         return divide_tuples(sum_vector, tuple((n_coords, n_coords, n_coords)))
#     else:
#         return sum_vector

def vertex_extremum_find(verts):
    coords = [(v[0], v[1], v[2]) for v in verts]
    x, y, z = zip(*coords)
    return [min(x), max(x), min(y), max(y), min(z), max(z)]


def find_center_coordinates(verts):
    extremum = vertex_extremum_find(verts)
    return mathutils.Vector((extremum[0] + ((extremum[1] - extremum[0]) / 2),
                             extremum[2] + ((extremum[3] - extremum[2]) / 2),
                             extremum[4] + ((extremum[5] - extremum[4]) / 2)))

# def create_center(verts):
#     # Одна координата
#     coord = verts

#     # Создание меша и объекта
#     mesh = bpy.data.meshes.new("CenterMesh")
#     obj = bpy.data.objects.new("CenterObject", mesh)

#     # Добавление объекта в сцену
#     bpy.context.collection.objects.link(obj)

#     # Установка объекта как активного и выделенного
#     bpy.context.view_layer.objects.active = obj
#     obj.select_set(True)

#     # Создание одной вершины
#     verts = [coord.to_tuple()]
#     edges = []
#     faces = []

#     # Загрузка данных в меш
#     mesh.from_pydata(verts, edges, faces)
#     mesh.update()

# def create_centervert(verts):
#     # Создание меша и объекта
#     mesh = bpy.data.meshes.new("CenterVMesh")
#     obj = bpy.data.objects.new("CenterVObj", mesh)

#     # Добавление объекта в сцену
#     bpy.context.collection.objects.link(obj)

#     # Установка объекта активным и выделенным
#     bpy.context.view_layer.objects.active = obj
#     obj.select_set(True)

#     # Создание вершины
#     verts = [verts['co'].to_tuple()]
#     edges = []
#     faces = []

#     # Загрузка данных в меш
#     mesh.from_pydata(verts, edges, faces)
#     mesh.update()

# def create_furthestrvert(verts):
#     # Создание меша и объекта
#     mesh = bpy.data.meshes.new("FMesh")
#     obj = bpy.data.objects.new("FObj", mesh)

#     # Добавление объекта в сцену
#     bpy.context.collection.objects.link(obj)

#     # Установка объекта активным и выделенным
#     bpy.context.view_layer.objects.active = obj
#     obj.select_set(True)

#     # Создание вершины
#     verts = [verts['co'].to_tuple()]
#     edges = []
#     faces = []

#     # Загрузка данных в меш
#     mesh.from_pydata(verts, edges, faces)
#     mesh.update()

# def create_object_selectedverts(verts):
#     #Шаг 1: Преобразуем все координаты в mathutils.Vector
#     vertices = [mathutils.Vector(point['co']) for point in verts]

#     # Шаг 3: Создание объекта в Blender
#     mesh_data = bpy.data.meshes.new(name="CustomObject")
#     mesh_object = bpy.data.objects.new("CustomObject", mesh_data)

#     # Добавляем объект в сцену
#     bpy.context.collection.objects.link(mesh_object)

#     # Шаг 4: Создание вершин и граней в mesh_data
#     mesh_data.from_pydata(vertices, [], [])

#     # Обновляем данные mesh
#     mesh_data.update()

#     # Перевод объекта в активный
#     bpy.context.view_layer.objects.active = mesh_object
#     mesh_object.select_set(True)

def ensure_mode(mode: bpy.ops._ModuleType) -> bool:
    """
    Ensure that the current mode is the given mode.
    If the current mode is not the given mode, switch to the given mode.

    :param mode: The mode to ensure.
    :return: True if the mode was changed, False otherwise.
    """
    if bpy.context.mode != mode:
        bpy.ops.object.mode_set(mode=mode)
        return True
    return False


class ThrottleDecorator:
    """
    Decorator that limits how often a function can be called.
    Only executes the function if enough time has passed since the last call.
    """

    def __init__(self, func, interval: float):
        self.func = func
        self.interval = interval
        self.last_run = 0

        # Get function signature information
        self.signature = inspect.signature(func)
        self.params = list(self.signature.parameters.keys())

    def _prepare_args(self, args, kwargs):
        """Prepare arguments according to function signature"""
        try:
            bound_args = self.signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return bound_args.args, bound_args.kwargs
        except TypeError as e:
            if len(args) > len(self.params):
                args = args[:len(self.params)]
                return self._prepare_args(args, kwargs)
            raise e

    def __call__(self, *args, **kwargs):
        now = time.time()
        delta = now - self.last_run

        # Prepare current arguments
        args, kwargs = self._prepare_args(args, kwargs)

        # If enough time has passed, execute immediately
        if delta >= self.interval:
            self.last_run = now
            return self.func(*args, **kwargs)


def throttle(interval: float):
    def apply_decorator(func):
        decorator = ThrottleDecorator(func=func, interval=interval)
        return wraps(func)(decorator)
    return apply_decorator
