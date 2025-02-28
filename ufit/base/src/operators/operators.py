import bpy
from .OT_platform_login import OTPlatformLogin
from .OT_steps_checkpoints import OTPreviousStep, OTCheckpointRollback
from .OT_gizmo import OTuFitGizmo
from .OT_errors import OTReportProblem
from .OT_device_type import OTDeviceType
from .OT_restart import OTRestart
from .OT_circumference_lenght import OTCircumferenceLenght, OTAddCircumference, OTDeleteCircumference


def register():
    bpy.utils.register_class(OTPlatformLogin)
    bpy.utils.register_class(OTCheckpointRollback)
    bpy.utils.register_class(OTPreviousStep)
    bpy.utils.register_class(OTuFitGizmo)
    bpy.utils.register_class(OTReportProblem)
    bpy.utils.register_class(OTDeviceType)
    bpy.utils.register_class(OTRestart)
    bpy.utils.register_class(OTCircumferenceLenght)
    bpy.utils.register_class(OTAddCircumference)
    bpy.utils.register_class(OTDeleteCircumference)


def unregister():
    bpy.utils.unregister_class(OTPlatformLogin)
    bpy.utils.unregister_class(OTCheckpointRollback)
    bpy.utils.unregister_class(OTPreviousStep)
    bpy.utils.unregister_class(OTuFitGizmo)
    bpy.utils.unregister_class(OTReportProblem)
    bpy.utils.unregister_class(OTDeviceType)
    bpy.utils.unregister_class(OTRestart)
    bpy.utils.unregister_class(OTCircumferenceLenght)
    bpy.utils.unregister_class(OTAddCircumference)
    bpy.utils.unregister_class(OTDeleteCircumference)
