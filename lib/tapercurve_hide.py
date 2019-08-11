import bpy
from . import _common


class ahs_tapercurve_hide(bpy.types.Operator):
    bl_idname = 'object.ahs_tapercurve_hide'
    bl_label = "Hide"
    bl_description = "Hide/Show All Tapers/Bevels"
    bl_options = {'REGISTER', 'UNDO'}

    items = [
        ('TAPER', "Taper", "", 'CURVE_NCURVE', 1),
        ('BEVEL', "Bevel", "", 'SURFACE_NCIRCLE', 2),
        ('BOTH', "Both", "", 'ARROW_LEFTRIGHT', 3),
    ]
    mode = bpy.props.EnumProperty(items=items, name="Both", default='BOTH')

    is_hide = bpy.props.BoolProperty(name="Hide")

    @classmethod
    def poll(cls, context):
        try:
            taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
            if not len(taper_and_bevel_objects):
                return False
        except:
            return False
        return True

    def execute(self, context):
        if self.mode == 'TAPER':
            taper_or_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object]
        elif self.mode == 'BEVEL':
            taper_or_bevel_objects = [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
        else:
            taper_or_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]

        for ob in taper_or_bevel_objects:
            _common.set_hide(ob, self.is_hide)
        return {'FINISHED'}
