import bpy
from .ST_0_start.UI_start_modeling import UIStartModelingFS
from .ST_10_import_scan.UI_import_scan import UIImportScanFS
from .ST_20_indicate.UI_indicate_patella import UIMoveScanFS
from .ST_30_clean_up.UI_clean_up import UICleanUpScanFS
from .ST_40_verify_clean_up.UI_verify_clean_up import UIVerifyCleanUpFS
from .ST_50_rotate.UI_rotate_scan import UIRotateFS
from .ST_70_push_pull_smooth.UI_push_pull_smooth import UIPushPullRegionsFS
from .ST_80_scale.UI_liner_scaling import UIScaleScanFS
from .ST_90_verify_scaling.UI_verify_scaling import UIVerifyScalingFS
from .ST_95_border_choice.UI_border_choice import UIBorderChoiceFS
from .ST_100_cutout_prep.UI_cutout_prep import UICutoutPrepFS
from .ST_110_cutout.UI_cutout import UICutoutFS
from .ST_115_cutout_selection.UI_cutout_selection import UICutoutSelectionFS
from .ST_120_new_cutout.UI_new_cutout import UINewCutoutFS
from .ST_125_draw.UI_draw import UIDrawFS
from .ST_180_export.UI_export_socket import UIExportSocketFS
from .ST_190_finish.UI_finish import UIFinishedFS


def register():
    bpy.utils.register_class(UIStartModelingFS)
    bpy.utils.register_class(UIImportScanFS)
    bpy.utils.register_class(UIMoveScanFS)
    bpy.utils.register_class(UICleanUpScanFS)
    bpy.utils.register_class(UIVerifyCleanUpFS)
    bpy.utils.register_class(UIRotateFS)
    bpy.utils.register_class(UIPushPullRegionsFS)
    bpy.utils.register_class(UIScaleScanFS)
    bpy.utils.register_class(UIVerifyScalingFS)
    bpy.utils.register_class(UIBorderChoiceFS)
    bpy.utils.register_class(UICutoutPrepFS)
    bpy.utils.register_class(UICutoutFS)
    bpy.utils.register_class(UICutoutSelectionFS)
    bpy.utils.register_class(UINewCutoutFS)
    bpy.utils.register_class(UIDrawFS)
    bpy.utils.register_class(UIExportSocketFS)
    bpy.utils.register_class(UIFinishedFS)


def unregister():
    bpy.utils.unregister_class(UIStartModelingFS)
    bpy.utils.unregister_class(UIImportScanFS)
    bpy.utils.unregister_class(UIMoveScanFS)
    bpy.utils.unregister_class(UICleanUpScanFS)
    bpy.utils.unregister_class(UIVerifyCleanUpFS)
    bpy.utils.unregister_class(UIRotateFS)
    bpy.utils.unregister_class(UIPushPullRegionsFS)
    bpy.utils.unregister_class(UIScaleScanFS)
    bpy.utils.unregister_class(UIVerifyScalingFS)
    bpy.utils.unregister_class(UIBorderChoiceFS)
    bpy.utils.unregister_class(UICutoutPrepFS)
    bpy.utils.unregister_class(UICutoutFS)
    bpy.utils.unregister_class(UICutoutSelectionFS)
    bpy.utils.unregister_class(UINewCutoutFS)
    bpy.utils.unregister_class(UIDrawFS)
    bpy.utils.unregister_class(UIExportSocketFS)
    bpy.utils.unregister_class(UIFinishedFS)
