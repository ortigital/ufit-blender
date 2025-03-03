import bpy
from .UI_logo import UIUFitLogo
from .UI_platform_login import UIPlatformLogin
from .UI_steps_checkpoints import UIAssistance, UICheckpoints, UIProgress
from .UI_view import UIUFitGizmo, UIUFitView
from .UI_errors import UIReportProblem, UIErrorMessage
from .UI_device_type import UIDeviceType
from .UI_autocalculate_length import MousePositionPanel


def register():
    bpy.utils.register_class(UIUFitLogo)
    bpy.utils.register_class(UIReportProblem)
    bpy.utils.register_class(UIUFitView)
    bpy.utils.register_class(UIPlatformLogin)
    bpy.utils.register_class(UIUFitGizmo)
    bpy.utils.register_class(UICheckpoints)
    bpy.utils.register_class(UIAssistance)
    bpy.utils.register_class(UIProgress)
    bpy.utils.register_class(UIErrorMessage)
    bpy.utils.register_class(UIDeviceType)
    bpy.utils.register_class(MousePositionPanel)


def unregister():
    bpy.utils.unregister_class(UIUFitLogo)
    bpy.utils.unregister_class(UIReportProblem)
    bpy.utils.unregister_class(UIUFitView)
    bpy.utils.unregister_class(UIPlatformLogin)
    bpy.utils.unregister_class(UIUFitGizmo)
    bpy.utils.unregister_class(UICheckpoints)
    bpy.utils.unregister_class(UIAssistance)
    bpy.utils.unregister_class(UIProgress)
    bpy.utils.unregister_class(UIErrorMessage)
    bpy.utils.unregister_class(UIDeviceType)
    bpy.utils.unregister_class(MousePositionPanel)
