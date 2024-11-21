from .core.OT_base import OTBase
import ufit.base.src.operators.core.platform as platform


class OTPlatformLogin(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.platform_login"
    bl_label = "Login"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.scene.ufit_user \
                and context.scene.ufit_password:
            return True

    def execute(self, context):
        return self.execute_base(context,
                                 'platform_login')

    def main_func(self, context):
        platform.platform_login(context)
