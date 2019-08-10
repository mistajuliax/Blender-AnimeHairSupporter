import bpy
from . import _common


class ahs_tapercurve_activate(bpy.types.Operator):
    bl_idname = 'object.ahs_tapercurve_activate'
    bl_label = "Add Taper/Bevel"
    bl_description = "Add Taper/Bevel to Curve"
    bl_options = {'REGISTER', 'UNDO'}

    items = [
        ('TAPER', "Taper", "", 'CURVE_NCURVE', 1),
        ('BEVEL', "Bevel", "", 'SURFACE_NCIRCLE', 2),
    ]
    mode = bpy.props.EnumProperty(items=items, name="モード")

    @classmethod
    def poll(cls, context):
        try:
            curve = _common.get_active_object().data
            if curve.taper_object and curve.bevel_object:
                return True

            taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
            if _common.get_active_object() in taper_and_bevel_objects:
                return True
        except:
            return False
        return True

    def execute(self, context):
        ob = _common.get_active_object()
        curve = ob.data

        if curve.taper_object and curve.bevel_object:
            if self.mode == 'TAPER':
                target_ob = curve.taper_object
            elif self.mode == 'BEVEL':
                target_ob = curve.bevel_object

            if not target_ob:
                return {'CANCELLED'}

            for o in context.blend_data.objects:
                o.select = False
            _common.select(target_ob, True)
            _common.set_hide(target_ob, False)
            _common.set_active_object(target_ob)
        else:
            target_ob = None
            for o in context.blend_data.objects:
                if o.type != 'CURVE':
                    continue
                if o.data.taper_object == ob and self.mode == 'BEVEL':
                    target_ob = o.data.bevel_object
                    break
                if o.data.bevel_object == ob and self.mode == 'TAPER':
                    target_ob = o.data.taper_object
                    break
            if not target_ob:
                return {'CANCELLED'}

            for o in context.blend_data.objects:
                _common.select(o, False)
            _common.select(target_ob, True)
            _common.set_active_object(target_ob)

        return {'FINISHED'}
