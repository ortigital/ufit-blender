import bpy

from datetime import datetime
import ufit.base.src.operators.utils.authenticate as authenticate


def platform_login(context):
    ufit_prefs = context.preferences.addons['ufit'].preferences
    ufit_prefs.username = context.scene.ufit_user
    ufit_prefs.password = context.scene.ufit_password

    authenticate.platform_authenticate(context)

    if authenticate.is_authenticated():
        ufit_prefs.last_authentication = datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        ufit_prefs.username = ""
        ufit_prefs.password = ""
        ufit_prefs.last_authentication = ""
        raise Exception(f'Authentication failed. Make sure you have internet connection and provided the correct credentials.')

    # save the userpref
    bpy.ops.wm.save_userpref()
