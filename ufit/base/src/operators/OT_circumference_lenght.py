from .core.OT_base import OTBase


class OTCircumferenceLenght(OTBase):
    """Tooltip"""
    bl_idname = "ufit_operators.circumference_lenght"
    bl_label = "Device Type"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return self.execute_base(context,
                                 'circumference_lenght')

    def main_func(self, context):
        print("Text message")
